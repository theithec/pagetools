'''
Created on 14.12.2013

@author: lotek
'''

from django import template
from django.core import urlresolvers
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_delete
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.template.context import Context

from concurrency.fields import IntegerVersionField
from collections import defaultdict

from mptt.fields import TreeForeignKey
from mptt.managers import TreeManager
from mptt.models import MPTTModel

from pagetools.core.models import LangManager, LangModel
from pagetools.core.utils import get_classname, get_adminedit_url

from .settings import MENU_TEMPLATE


class MenuManager(TreeManager, LangManager):
    def create(self, *args, **kwargs):
        raise AttributeError(
            _("Use 'add_child' or 'add_root' instead of 'create'"))

    def add_child(self, parent, content_object, **kwargs):
        if not getattr(content_object, 'get_absolute_url', None):
            raise ValidationError(
                _('MenuEntry.content_object requires get_absolute_url'))
        kwargs['title'] = kwargs.get('title', '%s' % content_object)
        kwargs['parent'] = parent
        kwargs['content_type'] = ContentType.objects.get_for_model(
            content_object)
        kwargs['object_id'] = content_object.pk
        try:
            created = False
            entry, created = TreeManager.get_or_create(self, **kwargs)
        except KeyError:
            pass
        if not created:
            raise ValidationError(
                _('Entry %(title)s already exists in %(parent)s'),
                params=kwargs)
        return entry

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
    slugs = models.CharField(
        _('slugs'), max_length=512,
        help_text=('Whitespace separated slugs of content'),
        default='', blank=True)
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    enabled = models.BooleanField(default=False)
    objects = MenuManager()
    #tree = MenuManager()
    version = IntegerVersionField()

    def get_entry_classname(self):
        return get_classname(self.content_object.__class__)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.content_object.get_absolute_url()

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
    #def add_child(self, obj, title=''):
    #    self.objects.add_child(self, obj, title)

    def children_list(self, mtree=None, children=None, for_admin=False, dict_parent=None):
        filterkwargs = {'parent': self}
        if not for_admin:
            filterkwargs['enabled'] = True
        if mtree is None:
            mtree = []
        if children is None:
            children = self.get_children().filter(**filterkwargs)

        for order_id, c in enumerate(children):
            d = {
                'entry_title': c.title,
            }
            d['dict_parent'] = dict_parent
            obj = c.content_object
            cc = c.get_children().filter(parent=c)
            if for_admin:
                reverseurl = get_adminedit_url(obj)
                d.update({
                    'entry_order_id': order_id,
                    'entry_pk': c.pk,
                    'entry_del_url': urlresolvers.reverse(
                        'admin:menus_menuentry_delete', args=(c.pk,)),
                    'obj_admin_url': reverseurl,
                    'obj_classname': get_classname(obj.__class__),
                    'obj_title': obj,
                    'obj_status': 'published' if getattr(obj, 'enabled', True) else 'draft',
                    'entry_enabled': "checked" if c.enabled else ""
                })
            else:
                if not getattr(obj, 'enabled', True):
                    continue
                url = c.get_absolute_url()
                d['entry_url'] = url
                cslugs = []
                node = c
                node_obj = obj

                cslugs += node.slugs.split(' ') if node.slugs else [
                    getattr(node_obj, 'slug', slugify('%s' % node_obj))
                ]
                dict_parent = d
                while dict_parent:
                    dict_parent['select_class_marker'] = ''.join(
                        '%(sel_' + s + ')s' for s in cslugs
                    )
                    try:
                        dict_parent = dict_parent['dict_parent']
                    except AttributeError:
                        break
            if cc:
                d['children'] = self.children_list(children=cc, for_admin=for_admin, dict_parent=d)
            mtree.append(d)
        return mtree

    def _render_no_sel(self):
        t = template.loader.get_template(MENU_TEMPLATE)
        children = self.children_list()
        return t.render(Context({'children': children, }))

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
        x = t % sel_entries
        return x

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
            parent = MenuEntry.objects.get(pk=parent.pk)
            # e.save()
            # parent.save()
        MenuEntry.objects.rebuild()
        self.save()

    def full_clean(self, *args, **kwargs):
        f = Menu.objects.filter(
            title=self.title, lang=''
        ).exclude(pk=self.pk)
        if f:
            raise ValidationError({'__all__': ('Language Error',)})
        return super(Menu, self).full_clean(*args, **kwargs)

    def __str__(self):
        return '%s%s' % (self.title,
                          (' (%s)' % self.lang) if self.lang else '')

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
        c.menu = self
        c.save()
        return s

    class Meta:
        verbose_name = _('Menu')
        proxy = True


class AbstractLink(models.Model):
    title = models.CharField(_('Title'), max_length=128)
    enabled = models.BooleanField(_('enabled'), default=True)

    class Meta:
        abstract = True


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
        super(ViewLink, self).__init__(*args, **kwargs)
        from pagetools.menus.utils import _entrieable_reverse_names
        self._meta.get_field_by_name('name')[0]._choices = [
            ('%s' % k, '%s' % k)
            for k in _entrieable_reverse_names
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(self.name)

    class Meta:
        verbose_name = _("ViewLink")
        verbose_name_plural = _("ViewLinks")
