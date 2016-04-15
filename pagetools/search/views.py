import os
import json
import operator
from functools import reduce

from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.utils.html import strip_tags

from pagetools.search import search_mods, extra_filter
from pagetools.core.views import PaginatorMixin

from .forms import AdvSearchForm
from . import settings


class SearchResultsView(PaginatorMixin):

    template_name = "search_results.html"
    context_object_name = 'results'
    search_params = {}
    _search_mods = [m for m in search_mods]
    sep = ''
    form_cls = AdvSearchForm
    _thisdir = os.path.dirname(os.path.realpath(__file__))
    if settings.SEARCH_REPLACEMENTS:
        replacements = json.load(
            open(os.path.join(_thisdir, settings.SEARCH_REPLACEMENTS_FILE)))

    def get(self, request, *args, **kwargs):
        self.form = self.form_cls(request.GET)
        is_valid = self.form.is_valid()
        cld = getattr(self.form, 'cleaned_data', None)
        if any(cld.values()):
            self.sep = '?%s&' % ('&'.join(
                ['%s=%s' % (k, v) for k, v in list(cld.items()) if v]
            ))
            self.search_params = cld
            model_pks = cld.get('models')
            if model_pks:
                int_pks = [int(s) for s in model_pks]
                self._search_mods = [search_mods[i] for i in int_pks]
        return super(SearchResultsView, self).get(request)

    def filtered_queryset(self, qs, fields):
        qs = extra_filter(qs)
        cnots = self.search_params.get('contains_not', '').split()
        if cnots:
            notlist = [Q(**{'%s__icontains' % field: cnot})
                       for cnot in cnots for field in fields]
            combined_notlist = reduce(operator.or_, notlist)
            qs = qs.exclude(combined_notlist)
        return qs

    def _convert(self, term):
        for k, v in self.replacements.items():
            term.replace(k, v)
        return term

    def result_(self, sterms, combine_op):
        result = set()
        if not sterms:
            return result
        if settings.SEARCH_REPLACEMENTS:
            for sterm in sterms:
                sterm = self._convert(sterm)
        for mod in self._search_mods:
            Cls = mod[0]
            fields = mod[1]
            queryset = self.filtered_queryset(Cls.objects, fields)
            qlists = []
            for sterm in sterms:
                if len(sterm) < 3:
                    continue
                qlist = reduce(operator.or_,
                               [Q(**{'%s__icontains' % field: sterm})
                                for field in fields])
                qlists.append(qlist)
            if qlists:
                combined_qlist = reduce(combine_op, qlists)
                queryset2 = queryset.filter(combined_qlist)
                result |= set(queryset2)
        return result

    def result_any(self):
        terms = self.search_params.get('contains_any', '').split()
        return self.result_(terms, operator.or_)

    def result_add(self):
        terms = self.search_params.get('contains_all', '').split()
        return self.result_(terms, operator.and_)

    def _stripped(self, txt):
        txt = strip_tags('%s' % txt).lower()
        return txt

    def get_queryset(self, **kwargs):
        if not self.search_params:
            return tuple()

        results_any = self.result_any()
        results_add = self.result_add()
        results_exact = set()
        exact = self.search_params.get('contains_exact').lower() or None
        if exact:
            for mod in self._search_mods:
                Cls = mod[0]
                fields = mod[1]
                queryset = self.filtered_queryset(Cls.objects, fields)
                for field in fields:
                    er = [r for r in queryset if exact in
                          self._stripped(getattr(r, field))]
                    results_exact |= set(er)
        rs = [f for f in (results_add, results_any, results_exact) if f]
        if not rs:
            return tuple()
        else:
            rq = reduce(operator.and_, rs)
            return list(rq)

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        context['view_url'] = reverse("search")
        context['form'] = self.form
        return context

search = SearchResultsView.as_view()
