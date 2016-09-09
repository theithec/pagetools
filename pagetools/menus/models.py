'''
Created on 14.12.2013

@author: Tim Heithecker
'''

from collections import defaultdict
import logging
import django
from django import template
from django.core import urlresolvers
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_delete
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from mptt.fields import TreeForeignKey
from mptt.managers import TreeManager
from mptt.models import MPTTModel

from pagetools.core.models import LangManager, LangModel
from pagetools.core.utils import get_classname, get_adminedit_url

import pagetools.menus.utils
from .settings import MENU_TEMPLATE

logger = logging.getLogger("pagetools")


class MenuEntryManager(TreeManager, LangManager):

    def add_child(self, content_object, **kwargs):
        if not getattr(content_object, 'get_absolute_url', None):
            raise ValidationError(
                _('MenuEntry.content_object requires get_absolute_url'))
        kwargs['title'] = kwargs.get('title', '%s' % content_object)
        # kwargs['parent'] = parent
        kwargs['content_type'] = ContentType.objects.get_for_model(
            content_object)
        kwargs['object_id'] = content_object.pk
        kwargs['slug'] = '%s' % getattr(
            content_object, 'slug',
            slugify(content_object))
        try:
            created = False
            entry, created = self.get_or_create(**kwargs)
        except KeyError:
            pass
        if not created:
            raise ValidationError(
                _('Entry %(title)s already exists in %(parent)s'),
                params=kwargs)
        return entry


class MenuManager(MenuEntryManager):

    def create(self, *args, **kwargs):
        raise AttributeError(
            _("Use 'add_child' or 'add_root' instead of 'create'"))

    def add_root(self, title, **kwargs):
        menu, created = TreeManager.get_or_create(
            self,
            title=title,
            parent=None,
            **kwargs
        )
        if not created:
            raise ValidationError(
                _('Menu %(name)s already exists'),
                params={'name': title}
            )
        return menu


class MenuEntry(MPTTModel, LangModel):
    title = models.CharField(_('Title'), max_length=128)
    slug = models.CharField(
        _('slug'), max_length=512,
        help_text=(_('Slug')),
        default='', blank=True)
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    enabled = models.BooleanField(default=False)
    objects = MenuEntryManager()

    def get_entry_classname(self):
        return get_classname(self.content_object.__class__)

    def __str__(self):
        return '%s%s' % (
            self.title, (' (%s)' % self.lang) if self.lang else '')

    def get_absolute_url(self):
        return self.content_object.get_absolute_url()

    def clean(self):
        try:
            e = MenuEntry.objects.get(title=self.title, lang=self.lang)
            if not (self.pk and e.pk == self.pk):
                raise ValidationError(
                    _('An entry with this title and language already exists'))
        except MenuEntry.DoesNotExist:
            pass

    class Meta:
        unique_together = ('title', 'lang')


def delete_content(sender, **kwargs):
    try:
        e = MenuEntry.objects.filter(
            content_type=ContentType.objects.get_for_model(sender),
            object_id=kwargs['instance'].pk
        )
        if e:
            e.delete()
    except:
        pass


pre_delete.connect(delete_content)


class SelectedEntries(defaultdict):
    def __missing__(self, key):
        return ''


class MenuCache(models.Model):
    menu = models.OneToOneField('Menu', blank=True, null=True)
    cache = models.TextField()

    def __str__(self):
        return 'Cache: %s' % self.menu

    def get_absolute_url(self):
        return ""


class Menu(MenuEntry):
    objects = MenuManager()

    def _render_no_sel(self):
        t = template.loader.get_template(MENU_TEMPLATE)
        children = self.children_list()
        return t.render({'children': children, })

    def render(self, selected):
        sel_entries = SelectedEntries()
        for s in selected:
            sel_entries['sel_' + s] = 'active'
        use_cache = self.enabled
        t = None
        if use_cache:
            t = MenuCache.objects.get(menu=self).cache
        else:
            t = self._render_no_sel()
        logger.debug(" TEMPLATE %s,  SELECTED: %s, KEYS: %s" % (
            t, selected,  ", ".join(sel_entries.keys())))
        rendered = t % sel_entries
        return rendered

    def update_entries(self, orderstr):
        '''orderstr = jquery.mjs.nestedSortable.js / serialize()'''
        entries_str = orderstr.split("&")
        parent = None
        for entry_str in entries_str:
            if not entry_str:
                break
            k, v = entry_str.split("=")
            b1, b2 = list(map(k.find, ("[", "]")))
            eid = int(entry_str[b1+1: b2])
            e = MenuEntry.objects.get(id=eid)
            if v == 'null':
                parent = e.get_root()
            else:
                parent = MenuEntry.objects.get(id=int(v))
            e.move_to(parent, 'last-child')
            e = MenuEntry.objects.get(pk=e.pk)
            # parent = MenuEntry.objects.get(pk=parent.pk)
        MenuEntry.objects.rebuild()
        self.save()

    def full_clean(self, *args, **kwargs):
        f = Menu.objects.filter(
            title=self.title, lang=''
        ).exclude(pk=self.pk)
        if f:
            raise ValidationError({'__all__': ('Language Error',)})
        return super(Menu, self).full_clean(*args, **kwargs)

    def update_cache(self):
        self.menucache.cache = self._render_no_sel()
        self.menucache.save()

    def save(self, *args, **kwargs):
        if self.is_child_node():
            return super(Menu, self).save(*args, **kwargs)
        try:
            c = self.menucache  # MenuCache.objects.get(menu=self)
        except MenuCache.DoesNotExist:
            c = MenuCache.objects.create()
            self.content_object = c
        s = super(Menu, self).save(*args, **kwargs)
        for child in self.get_children():
            slug = getattr(child.content_object, 'slug', None)
            if slug:
                if not slug == child.slug:
                    child.slug = slug
                    child.save()
        c.menu = self
        c.save()
        return s

    def _with_child(self, dict_, entry, entry_obj, dict_parent):
        if not getattr(entry_obj, 'is_published', True):
            return
        dict_['entry_url'] = entry.get_absolute_url()
        cslugs = []
        # cslugs += entry.slugs.split(' ') if entry.slugs else [
        cslugs += [
            getattr(
                entry_obj,
                'slug',
                getattr(entry_obj, 'menukey', slugify('%s' % entry_obj)))
        ]
        curr_dict = dict_
        while curr_dict:
            curr_dict['select_class_marker'] = curr_dict.get(
                'select_class_marker', '')
            curr_dict['select_class_marker'] += ''.join(
                '%(sel_' + s + ')s' for s in cslugs

            )
            curr_dict = curr_dict['dict_parent']

        return dict_

    def children_list(self, mtree=None, children=None, for_admin=False,
                      dict_parent=None):
        self.cnt = 0  # a non-recursive counter for a recursive fuction

        def _children_list(mtree=None, children=None, for_admin=False,
                           dict_parent=None):
            filterkwargs = {'parent': self}
            if not for_admin:
                filterkwargs['enabled'] = True

            if mtree is None:
                mtree = []

            if children is None:
                children = self.get_children().filter(**filterkwargs)

            for childentry in children:
                d = {
                    'entry_title': childentry.title,
                }

                d['dict_parent'] = dict_parent
                obj = childentry.content_object

                filterkwargs['parent'] = childentry
                cc = []
                if not for_admin and getattr(obj, 'auto_children', False):
                    d['auto_entry'] = True
                    cc = obj.get_children(parent=self)
                elif dict_parent and dict_parent.get('auto_entry', False):
                    cc = MenuEntry.objects.none()
                else:
                    cc = childentry.get_children().filter(**filterkwargs)
                if for_admin:
                    reverseurl = get_adminedit_url(obj)
                    d.update({
                        'entry_order_id': self.cnt,
                        'entry_pk': childentry.pk,
                        'entry_del_url': urlresolvers.reverse(
                            'admin:menus_menuentry_delete',
                            args=(childentry.pk, )),
                        'entry_change_url': urlresolvers.reverse(
                            'admin:menus_menuentry_change',
                            args=(childentry.pk,)),
                        'obj_admin_url': reverseurl,
                        'obj_classname': get_classname(obj.__class__),
                        'obj_title': obj,
                        'obj_status': 'published' if getattr(
                            obj, 'enabled', True) else 'draft',
                        'entry_enabled':
                            "checked" if childentry.enabled else ""
                    })
                else:
                    d = self._with_child(d, childentry, obj, dict_parent)

                self.cnt += 1
                if d and cc:
                    d['children'] = _children_list(
                        children=cc, for_admin=for_admin, dict_parent=d)

                if d:
                    mtree.append(d)

            return mtree
        return _children_list(for_admin=for_admin)

    class Meta:
        verbose_name = _('Menu')
        proxy = True


class AbstractLink(models.Model):
    title = models.CharField(_('Title'), max_length=128)
    enabled = models.BooleanField(_('enabled'), default=True)
    #  auto_children = False

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

    #  def get_children(self, parent=None):
    #    return super().get_children()


class Link(AbstractLink):
    url = models.CharField(_('URL'), max_length=255)

    def __str__(self):
        return self.url

    def get_absolute_url(self):
        return self.url

    class Meta:
        verbose_name = _("Link")
        verbose_name_plural = _("Links")


class ViewLink(AbstractLink):
    name = models.CharField(_('Name'), max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = tuple((
            ('%s' % k, '%s' % k)
            for k in pagetools.menus.utils._entrieable_reverse_names
        ))
        if django.VERSION < (1, 9):
            self._meta.get_field('name')._choices = choices
        else:
            self._meta.get_field('name').choices = choices

    def get_absolute_url(self):
        return reverse(self.name)

    @classmethod
    def show_in_menu_add(Clz):
        return len(pagetools.menus.utils._entrieable_reverse_names) > 0

    class Meta:
        verbose_name = _("View")
        verbose_name_plural = _("View")


class AutoPopulated(AbstractLink):
    '''
    Add entries from a function.

    '''
    auto_children = True
    name = models.CharField(_('Name'), max_length=255, choices=(("a", "1"),))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = tuple((
            ('%s' % k, '%s' % k)
            for k in pagetools.menus.utils._entrieable_auto_children
        ))
        if django.VERSION < (1, 9):
            self._meta.get_field('name')._choices = choices
        else:
            self._meta.get_field('name').choices = choices

    def get_children(self, parent):
        return pagetools.menus.utils._auto_children_funcs[self.name]()

    def get_absolute_url(self):
        return "."

    @classmethod
    def show_in_menu_add(Clz):
        return len(pagetools.menus.utils._entrieable_auto_children) > 0

    class Meta:
        verbose_name = _("Autopopulated Entry")
        verbose_name_plural = _("Autopopulated Entries")
