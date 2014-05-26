'''
Created on 14.12.2013

@author: lotek
'''

import sys

from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from pagetools.admin import TinyMCEMixin
from pagetools.menus.models import MenuEntry, Menu, Link, ViewLink
from pagetools.menus.utils import entrieable_models
from pagetools.utils import get_adminadd_url, get_classname


class MenuAdmin(TinyMCEMixin, admin.ModelAdmin):
    exclude = ('parent', 'enabled', 'content_type', 'object_id')
    save_as = True
    def queryset(self, request):
        return Menu.tree.root_nodes()

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
            context['menu_entries'] = obj.children_list(for_admin=True)

        return admin.ModelAdmin.render_change_form(
            self, request, context, add=add, change=change,
            form_url=form_url, obj=obj)
        
    
    def save_related(self, request, form, formsets, change):
        obj = form.instance
        entry_order = form.data.get('entry-order')
        if entry_order:
            obj.update_entries(entry_order)
        if form.cleaned_data.get('addeentry'):
            modulename, classname, id = form.cleaned_data['addentry'].split("#")
            o = getattr(sys.modules[modulename], classname).objects.get(pk=id)
            MenuEntry.tree.create(
                content_type=ContentType.objects.get_for_model(o),
                object_id=o.pk,
                parent=form.instance,
                status='draft'
            )
        cnt = 0
        while True:
            try:
                eid = form.data['entry-order-id-%s' % cnt]
                name = form.data['entry-text-%s' % cnt]
                ispub = form.data.get('entry-published-%s' % cnt, 0)
            except KeyError:
                break
            entry = MenuEntry.tree.get(pk=eid)
            entry.title = name
            entry.enabled = ispub == "1"
            entry.save()
            cnt += 1
        if obj.enabled:
            obj.update_cache()

    class Meta:
        model = Menu
        


class EntrieableForm(forms.ModelForm):
    menus = forms.Field()

    def __init__(self, *args, **kwargs):
        super(EntrieableForm, self).__init__(*args, **kwargs)
        menus = [(m.id, u'%s' % m) for m in Menu.tree.root_nodes()]
        try:
            entry = kwargs['instance']
            menuEntries = MenuEntry.tree.filter(
                content_type=ContentType.objects.get_for_model(entry),
                object_id=entry.id
            )
            menuroot_ids = set([m.get_root().id for m in menuEntries])
        except KeyError:
            menuroot_ids = set()
        self.fields['menus'] = forms.MultipleChoiceField(
            label=_('Menus'),
            choices=menus,
            required=False,
            initial=menuroot_ids
        )

    def clean(self):
        s = super(EntrieableForm, self).clean()
        if self.instance and 'menus' in self.changed_data:
            obj = self.instance
            cmp_data = self.cleaned_data.copy()
            fmenu_ids = [int(m) for m in cmp_data.pop('menus', [])]
            self.sel_menus = Menu.tree.filter(id__in=fmenu_ids)
            existing_menuentries_for_obj = MenuEntry.tree.filter(
                    content_type=ContentType.objects.get_for_model(
                        obj.__class__,
                    ),
                    object_id= obj.pk
            )
            self.existing_menuentries = []
            for e in existing_menuentries_for_obj:
                self.existing_menuentries.append(e)
        return s

    class Media(TinyMCEMixin.Media):
        js = TinyMCEMixin.Media.js + [settings.STATIC_URL + 'pagetools/admin/js/pre_sel_menu.js']



class EntrieableAdmin(admin.ModelAdmin):
    form = EntrieableForm
    # readonly_fields = ('status_changed',)

    def save_related(self, request, form, formsets, change):
        super(EntrieableAdmin, self).save_related(request, form,
                                                  formsets, change)
        obj = form.instance
        if not 'menus' in form.changed_data:
            return
        selected_menus = form.sel_menus
        existing_menuentries = form.existing_menuentries
        all_menus = Menu.tree.root_nodes()
        for  am in all_menus:
            found = None
            for e in existing_menuentries:
                if e.get_root().pk == am.pk:
                    found = e
                    break
            is_selected = am in selected_menus
            if is_selected and not found:
                root = Menu.tree.get(pk=am.pk)
                title = getattr(obj, 'title', None)
                kwargs = {}
                if title:
                    kwargs['title'] = title
                    e = Menu.tree.add_child(root, form.instance, **kwargs)
                # e = root.entry_from_obj(form.instance)
                e.move_to(root, 'last-child')
                e.save()
            elif found and not is_selected:
                e.delete()
        
        
    def _redirect(self, action, request, obj, *args, **kwargs):
        s = request.GET.get('menu', None)
        if s and '_save' in request.POST:
            return HttpResponseRedirect(
                reverse("admin:menus_menu_change", args=(s,))
            )
        else:
            return getattr(super(EntrieableAdmin, self), "response_%s" % action)(
                request, obj, *args, **kwargs
            )

    def response_add(self, request, obj, *args, **kwargs):
        return self._redirect("add", request, obj, *args, **kwargs)

    def response_change(self, request, obj, *args, **kwargs):
        return self._redirect("change", request, obj, *args, **kwargs)
    
   
admin.site.register(Menu, MenuAdmin)
admin.site.register(Link, EntrieableAdmin)
admin.site.register(ViewLink, EntrieableAdmin)

admin.site.register([MenuEntry, ])
