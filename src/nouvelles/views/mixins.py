from django.contrib import messages
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
    """
    This mixin allows applying filters to the queryset from the GET parameters.
    """

    allowed_filters = {}

    def get_queryset_filters(self):
        """
        Build a filter for a queryset.
        """
        filters = {}
        for item in self.allowed_filters:
            if self.request.GET.get(item):
                filters[self.allowed_filters[item]] = self.request.GET[item]
        return filters

    def get_queryset(self):
        """
        Return the list of filtered items for this view.
        """
        return super(FilterMixin, self).get_queryset().filter(**self.get_queryset_filters())


class FormFilterMixin(FormMixin, FilterMixin):
    """
    Allows the use of a form associated with a filter.
    """

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


class ArticleLineage(ContextMixin):
    """
    Build a list named "article_lineage" containing current article with his parents
    and prevent from article loops.
    """

    same_parent_message = "There was a problem with this article or one of its related elements. " \
                          "Please contact an administrator."

    def get_context_data(self, **kwargs):
        context = super(ArticleLineage, self).get_context_data(**kwargs)
        article_lineage = []
        article_to_check = self.object if self.object else self.parent_article

        while article_to_check:
            if article_to_check.parent_article and article_to_check.pk == article_to_check.parent_article.pk:
                article_to_check.parent_article = None
                messages.warning(self.request, self.same_parent_message)
            else:
                article_lineage.append(article_to_check)
                article_to_check = article_to_check.parent_article

        context['article_lineage'] = article_lineage
        return context


class ModelFormSetMixin(ContextMixin):
    """
    Mixin that helps to build a model formset.
    """

    formset_class = None

    def get_formset_class(self, **kwargs):
        """
        Returns the formset class to use in this view.
        """
        return self.formset_class

    def get_formset(self, form_set_class=None):
        """
        Returns an instance of the formset to be used in this view.
        """
        if form_set_class is None:
            form_set_class = self.get_formset_class()
        return form_set_class(**self.get_formset_kwargs())

    def get_formset_kwargs(self):
        """
        Returns the keyword arguments for instantiating the formset.
        """
        kwargs = {
            'instance': self.object,
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_context_data(self, **kwargs):
        """
        Insert the form into the context dict.
        """
        if 'formset' not in kwargs:
            kwargs['formset'] = self.get_formset()
        return super(ModelFormSetMixin, self).get_context_data(**kwargs)
