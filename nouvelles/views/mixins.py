from django.views.generic.base import ContextMixin, View
from django.views.generic.edit import FormMixin
from django.views.generic.list import MultipleObjectMixin


class ViewTitleMixin(ContextMixin):
    """
    Mixin that add a title context variable
    """
    title = None
    context_title_name = 'title'

    def get_page_title(self):
        import re
        if self.title:
            return self.title
        else:
            return re.sub(r"(?<=\w)([A-Z])", r" \1", self.__class__.__name__)

    def get_context_data(self, **kwargs):
        context = super(ViewTitleMixin, self).get_context_data(**kwargs)
        context[self.context_title_name] = self.get_page_title()
        return context


class FilterMixin(MultipleObjectMixin, View):
    allowed_filters = {}

    def get_queryset_filters(self):
        filters = {}
        for item in self.allowed_filters:
            if item in self.request.GET:
                filters[self.allowed_filters[item]] = self.request.GET[item]
        return filters

    def get_queryset(self):
        return super(FilterMixin, self).get_queryset().filter(**self.get_queryset_filters())


class FormFilterMixin(FormMixin, FilterMixin):
    def get_form_kwargs(self):
        kwargs = super(FormFilterMixin, self).get_form_kwargs()

        if self.request.method == 'GET':
            kwargs.update({'data': self.request.GET})

        return kwargs

    def get_queryset(self):
        queryset = super(FilterMixin, self).get_queryset()
        form = self.get_form()

        if form.is_valid():
            return queryset.filter(**self.get_queryset_filters())
        else:
            return queryset
