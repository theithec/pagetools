'''
Created on 14.12.2013

@author: Tim Heithecker
'''

import sys
from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from pagetools.core.admin import TinyMCEMixin
from pagetools.menus.models import (MenuEntry, Menu, Link, ViewLink, MenuCache,
                                    AutoPopulated)
from pagetools.menus.utils import entrieable_models
from pagetools.core.utils import get_adminadd_url, get_classname


class MenuChildrenWidget(forms.Widget):
    '''
    Drag and dropable menu entries
    '''

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super(MenuChildrenWidget, self).__init__(*args, **kwargs)

    def render(self, *args, **kwargs):
        m = Menu.objects.get(pk=self.instance.pk)
        return render_to_string(
            "menus/admin/menuentries.html",
            {'children': m.children_list(for_admin=True),
             'cls': 'class="sortable grp-grp-items sortable ui-sortable ' +
                    'mjs-nestedSortable-branch mjs-nestedSortable-expanded"',
             'original': m})


class MenuAddForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ('lang', 'title',)


class MenuChangeForm(forms.ModelForm):
    children = forms.Field()

    def __init__(self, *args, **kwargs):
        super(MenuChangeForm, self).__init__(*args, **kwargs)
        self.fields['children'] = forms.Field(
            required=False,
            widget=MenuChildrenWidget(instance=kwargs['instance']))

    def clean_children(self, *args, **kwargs):
        names = []
        cnt = 0
        while True:
            try:
                name = self.data['entry-text-%s' % cnt]
            except KeyError:
                break
            if name in names:
                raise ValidationError(_('Entry "%s" already exists' % name))
            names.append(name)
            cnt += 1

    class Meta:
        model = Menu
        fields = ('lang', 'title', 'children', )


class MenuAdmin(TinyMCEMixin, admin.ModelAdmin):
    save_as = True
    list_display = ("title", "lang")

    def get_form(self, request, obj=None, **kwargs):
        # Proper kwargs are form, fields, exclude, formfield_callback
        if obj:
            self.readonly_fields = ('addable_entries',)
            self.form = MenuChangeForm
        else:
            self.readonly_fields = ()
            self.form = MenuAddForm
        return super(MenuAdmin, self).get_form(request, obj, **kwargs)

    def addable_entries(self, obj, **kwargs):
        ems = entrieable_models()
        txt = "<ul>"
        for c in ems:
            txt += '<li><a href="%s?menu=%s">%s</a></li>' % (
                get_adminadd_url(c),
                obj.pk,
                get_classname(c),
            )
        return txt+"</ul>"
    addable_entries.short_description = _("Add")
    addable_entries.allow_tags = True

    def get_queryset(self, request):
        # import pdb; pdb.set_trace()
        return Menu.objects.root_nodes()

    def render_change_form(self, request, context, add=False,
                           change=False, form_url='', obj=None):
        if change:
            for c in entrieable_models():
                context['addable_entries'] = "".join([
                    '<li><a href="%s?menu=%s">%s</a></li>' % (
                        get_adminadd_url(c), context['object_id'],
                        get_classname(c)
                    ) for c in entrieable_models()
                ])
            menu_obj = Menu.objects.filter(pk=obj.pk)[0]
            context['menu_entries'] = menu_obj.children_list(for_admin=True)
        return admin.ModelAdmin.render_change_form(
            self, request, context, add=add, change=change,
            form_url=form_url, obj=obj)

    def save_related(self, request, form, formsets, change):
        obj = Menu.objects.get(pk=form.instance.pk)
        entry_order = form.data.get('entry-order')
        if entry_order:
            obj.update_entries(entry_order)
        '''if form.cleaned_data.get('addeentry'):
            import pdb; pdb.set_trace()
            modulename, classname, id = form.cleaned_data['addentry'].split("#")
            o = getattr(sys.modules[modulename], classname).objects.get(pk=id)
            MenuEntry.objects.create(
                content_type=ContentType.objects.get_for_model(o),
                object_id=o.pk,
                parent=form.instance,
                status='draft'
            )
        '''
        cnt = 0
        while True:
            try:
                eid = form.data['entry-order-id-%s' % cnt]
                name = form.data['entry-text-%s' % cnt]
                ispub = form.data.get('entry-published-%s' % cnt, 0)
            except KeyError:
                break
            entry = MenuEntry.objects.get(pk=eid)
            entry.title = name
            entry.enabled = ispub == "1"
            entry.save()
            cnt += 1
        if obj.enabled:
            obj.update_cache()

    class Meta:
        model = Menu

    class Media:
        js = (
            "js/jquery/dist/jquery.min.js",
            "js/jquery-ui/jquery-ui.min.js",
            "pagetools/admin/js/jquery.mjs.nestedSortable.js",
            'pagetools/admin/js/menuentries.js',
        )
        css = {'all': ('pagetools/admin/css/menuentries.css', )}


class EntrieableForm(forms.ModelForm):
    '''Adds a field: menus to the form. Preselect all menus which contain an
    entry for the obj
    '''

    menus = forms.Field()

    def __init__(self, *args, **kwargs):
        super(EntrieableForm, self).__init__(*args, **kwargs)
        menus = [(m.id, '%s' % m) for m in Menu.objects.root_nodes()]
        try:
            entry = kwargs['instance']
            menuEntries = MenuEntry.objects.filter(
                content_type=ContentType.objects.get_for_model(entry),
                object_id=entry.id
            )
            menuroot_ids = set([m.get_root().id for m in menuEntries])
        except (KeyError, AttributeError):
            menuroot_ids = set()
        self.fields['menus'] = forms.MultipleChoiceField(
            label=_('Menus'),
            choices=menus,
            required=False,
            initial=menuroot_ids,
            widget=forms.CheckboxSelectMultiple
        )

    def clean(self):
        s = super(EntrieableForm, self).clean()
        if self.instance and 'menus' in self.changed_data:
            obj = self.instance
            cmp_data = self.cleaned_data.copy()
            fmenu_ids = [int(m) for m in cmp_data.pop('menus', [])]
            self.sel_menus = Menu.objects.filter(id__in=fmenu_ids)
            existing_menuentries_for_obj = MenuEntry.objects.filter(
                content_type=ContentType.objects.get_for_model(
                    obj.__class__,),
                object_id=obj.pk
            )
            self.existing_menuentries = []
            for e in existing_menuentries_for_obj:
                self.existing_menuentries.append(e)
        return s

    class Media(TinyMCEMixin.Media):
        js = TinyMCEMixin.Media.js + [
            settings.STATIC_URL + 'pagetools/admin/js/pre_sel_menu.js']


class EntrieableAdmin(admin.ModelAdmin):

    form = EntrieableForm
    is_menu_entrieable = True

    def get_fields(self, request, obj):
        '''
        See :func:`pagetools.menus.admin.entrieable_admin_get_fields`
        '''
        '''Entrieable get_fields (for monkeypatching)'''
        # import pdb;pdb.set_trace()
        superfunc = super(self.__class__, self).get_fields
        if not getattr(superfunc, "for_entrieable",  False):
            fields = superfunc(request, obj)
        else:
            fields = admin.ModelAdmin.get_fields(self, request, obj)

        if "menus" not in fields:
            fields = fields + type(fields)(("menus",))
        return fields
    get_fields.for_entrieable = True

    def get_fieldsets(self, request, obj):
        # import pdb;pdb.set_trace()
        superfunc = super(self.__class__, self).get_fieldsets
        if not getattr(superfunc, "for_entrieable",  False):
            self.fieldsets = superfunc(request, obj)
        else:
            self.fieldsets = super(admin.ModelAdmin, self).get_fieldsets(request, obj)

        added = False
        for fs in self.fieldsets:
            if "menus" in fs[1]['fields']:
                added = True
                break

        if not added:
            self.fieldsets = self.fieldsets + type(self.fieldsets)((
                (_("In menus"), {'fields': ['menus', ]}),
            ),)

        return self.fieldsets
    get_fieldsets.for_entrieable = True

    def save_related(self, request, form, formsets, change):
        '''Entrieable save_related (for monkeypatching)'''
        superfunc = super(self.__class__, self).save_related
        if not getattr(superfunc, "for_entrieable",  False):
            superfunc(request, form, formsets, change)
        else:
            admin.ModelAdmin.save_related(self, request, form, formsets, change)

        obj = form.instance
        if 'menus' not in form.changed_data:
            return

        selected_menus = form.sel_menus
        existing_menuentries = form.existing_menuentries
        all_menus = Menu.objects.root_nodes()
        for am in all_menus:
            found = None
            for e in existing_menuentries:
                if e.get_root().pk == am.pk:
                    found = e
                    break

            is_selected = am in selected_menus
            if is_selected and not found:
                root = Menu.objects.get(pk=am.pk)
                title = getattr(obj, 'title', None)
                kwargs = {}
                if title:
                    kwargs['title'] = title

                e = Menu.objects.add_child(root, form.instance, **kwargs)
                e.move_to(root, 'last-child')
                e.save()

            elif found and not is_selected:
                e.delete()
    save_related.for_entrieable = True

    def _redirect(self, action, request, obj, *args, **kwargs):
        s = request.GET.get('menu', None)
        if s and '_save' in request.POST:
            return HttpResponseRedirect(
                reverse("admin:menus_menu_change", args=(s,))
            )
        else:
            # calling super may lead to recursive calls
            # todo: fix like entriable
            return getattr(admin.ModelAdmin,
                           "response_%s" % action)(
                self, request, obj, *args, **kwargs
            )

    def response_add(self, request, obj, *args, **kwargs):
        return self._redirect("add", request, obj, *args, **kwargs)

    def response_change(self, request, obj, *args, **kwargs):
        return self._redirect("change", request, obj, *args, **kwargs)


def make_entrieable_admin(clz):
    '''
    Monkeypatch an admin class

    Call this with an admin class to allow the instance class to
    be a menu entry.
    '''

    clz.is_menu_entrieable = True
    clz.save_related =  EntrieableAdmin.save_related
    clz.get_fields =  EntrieableAdmin.get_fields
    clz.get_fieldsets =  EntrieableAdmin.get_fieldsets
    clz.form = EntrieableForm


class MenuEntryAdmin(admin.ModelAdmin):
    list_display = ('title',  'lang', 'enabled')
    list_filter = ('lang', 'enabled',)

admin.site.register(Menu, MenuAdmin)
admin.site.register(Link, EntrieableAdmin)
admin.site.register(ViewLink, EntrieableAdmin)
admin.site.register(MenuEntry, MenuEntryAdmin)
admin.site.register(MenuCache)
admin.site.register(AutoPopulated, EntrieableAdmin)
