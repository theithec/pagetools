'''
Created on 14.12.2013

@author: lotek
'''
from collections import defaultdict

from django import template
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core import urlresolvers
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_delete
from django.db.utils import IntegrityError
from django.template.context import Context
from django.utils.functional import lazy
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.managers import TreeManager
from mptt.models import MPTTModel


from pagetools.models import LangManager, LangModel
from pagetools.utils import get_classname

from .settings import MENU_TEMPLATE


class MenuManager(TreeManager):
    def create(self, *args, **kwargs):
        raise AttributeError(
            _("Use 'add_child' or 'add_root' instead of 'create'"))

    def add_child(self, parent, content_object, **kwargs):
        if not getattr(content_object, 'get_absolute_url', None):
            raise ValidationError(
                _('MenuEntry.content_object requires get_absolute_url'))
        kwargs['title'] = kwargs.get('title', u'%s' % content_object)
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
        menu, created = TreeManager.get_or_create(self,
                    title=title,
                    parent=None
        )
        if not created:
            raise ValidationError(
                _('Menu %(name)s already exists'),
                params={'name': title}
            )
        return menu


class MenuEntry(MPTTModel, LangModel):
    title = models.CharField(u'Title', max_length=128)
    parent = TreeForeignKey('self',
            null=True, blank=True,
            related_name='children'
    )
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    enabled = models.BooleanField(default=False)
    objects = LangManager()
    tree = MenuManager()

    def get_entry_classname(self):
        return get_classname(self.content_object.__class__)

    def __unicode__(self):
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


class Menu(MenuEntry):
    def add_child(self, obj, title=''):
        self.tree.add_child(self, obj, title)

    def children_list(self, clist=None, children=None, for_admin=False):
        filterkwargs = {'parent': self}
        if not for_admin:
            filterkwargs['enabled'] = True
        if clist == None:
            clist = []
        if children == None:
            children = self.get_children().filter(**filterkwargs)
            # children = self.get_children().filter(filterkwargs)
        for order_id, c in enumerate(children):
            d = {
                'entry_title': c.title,
            }
            obj = c.content_object
            if for_admin:
                reverseurl = "admin:%s_%s_change" % (
                    obj.__class__.__module__[:-7].split('.')[-1],
                    obj.__class__.__name__.lower()
                )
                d.update({
                    'entry_order_id': order_id,
                    'entry_pk': c.pk,
                    'entry_del_url': urlresolvers.reverse('admin:menus_menuentry_delete', args=(c.pk,)),
                    'obj_admin_url': urlresolvers.reverse(reverseurl, args=(obj.id,)),
                    'obj_classname': get_classname(obj.__class__),
                    'obj_title': obj,
                    'obj_status': 'published' if getattr(obj, 'enabled', True) else 'draft',
                    'entry_enabled': "checked" if c.enabled else ""
                })
            else:
                if not getattr(obj, 'enabled', True):
                    continue
                url = c.get_absolute_url()
                slug = getattr(obj, 'slug', slugify(u'%s' % obj))
                d.update({
                    'entry_url': url,
                    'select_class_marker' : '%(sel_' + slug + ')s'
                })
            filterkwargs = {'parent': c}
            cc = c.get_children().filter(**filterkwargs)
            if cc:
                d['children'] = self.children_list(children=cc, for_admin=for_admin)
            clist.append(d)

        return clist

    def _render_no_sel(self):
        t = template.loader.get_template(MENU_TEMPLATE)
        children = self.children_list()
        return t.render(Context({'children': children, }))

    def render(self, selected):
        sel_entries = SelectedEntries()
        for s in selected:
            sel_entries['sel_' + s] = 'active'
        print "selentries", sel_entries
        use_cache = True
        t = None
        if use_cache:
            t = MenuCache.objects.get(menu=self).cache
        else:
            t = self._render_no_sel()
        print "t", t
        return t % sel_entries

    def update_entries(self, orderstr):
        '''orderstr = jquery.mjs.nestedSortable.js / serialize()'''
        entries_str = orderstr.split("&")
        parent = None
        for entry_str in entries_str:
            if not entry_str:
                break
            k, v = entry_str.split("=")
            b1, b2 = map(k.find, ("[", "]"))
            eid = int(entry_str[b1 + 1:b2])
            e = MenuEntry.objects.get(id=eid)
            if v == 'null':
                parent = e.get_root()
            else:
                parent = MenuEntry.objects.get(id=int(v))
            e.move_to(parent, 'last-child')
            e = MenuEntry.tree.get(pk=e.pk)
            parent = MenuEntry.tree.get(pk=parent.pk)
            # e.save()
            # parent.save()
        MenuEntry.tree.rebuild()
        self.save()

    def full_clean(self, *args, **kwargs):
        f = Menu.objects.filter(
            title=self.title, lang=''
        ).exclude(pk=self.pk)
        if f:
            raise ValidationError({'__all__': ('Language Error',)})
        return super(Menu, self).full_clean(*args, **kwargs)

    def __unicode__(self):
        return u'%s%s' % (self.title,
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
        verbose_name = 'Menu'
        proxy = True


class Link(models.Model):
    title = models.CharField(u'Title', max_length=128)
    url = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)

    def __unicode__(self):
        return self.url

    def get_absolute_url(self):
        return self.url

    class Meta:
        verbose_name = "Link"


class ViewLink(models.Model):
    title = models.CharField(u'Title', max_length=128)
#
    name = models.CharField(
            max_length=255,
           )

    def __init__(self, *args, **kwargs):
        super(ViewLink, self).__init__(*args, **kwargs)
        from pagetools.menus.utils import _entrieable_reverse_names
        self._meta.get_field_by_name('name')[0]._choices = [
            ('%s' % k, '%s' % k)
            for k in _entrieable_reverse_names
        ]
    enabled = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(self.name)

    class Meta:
        verbose_name = "ViewLink"
