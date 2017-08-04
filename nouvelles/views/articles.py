import operator
from datetime import timedelta
from functools import reduce

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from nouvelles.forms import ArticleForm, UploadAttachmentForm, ArchiveFiltersForm
from nouvelles.models import Article
from nouvelles.settings import HEADLINES_DAYS
from nouvelles.views.mixins import ViewTitleMixin, FilterMixin, FormFilterMixin, ArticleLineage


class ArticleNewsListView(ViewTitleMixin, FilterMixin, ListView):
    query_date = (timezone.now() - timedelta(HEADLINES_DAYS)).date()

    title = 'Headlines'
    context_object_name = 'article_list'
    template_name = 'nouvelles/article_headlines.html'
    queryset = Article.objects \
        .filter(effective_date__gte=query_date) \
        .order_by('-effective_date', '-creation_date')
    allowed_filters = {
        'criticality': 'criticality',
        'author': 'author__username',
        'tag': 'tags__slug'
    }

    def url(self, field, value):
        req_params = self.request.GET.copy()
        if req_params.get(field) == value:
            req_params.pop(field)
        elif req_params.get(field) is not None:
            req_params.pop(field)
            req_params.update({field: value})
        else:
            req_params.update({field: value})

        if len(req_params):
            return "%s?%s" % (reverse('nouvelles:index'), req_params.urlencode())
        else:
            return "%s" % reverse('nouvelles:index')

    def get_filters(self):
        criticalities = [None] * 3
        authors = []
        tags = []

        criticality_choices = dict(Article.CRITICALITY_CHOICES)

        # Gets all criticality
        for criticality_id in self.queryset.values_list('criticality', flat=True):
            if criticality_id == Article.CRITICALITY_HIGH:
                criticalities[0] = {
                    'id': criticality_id,
                    'name': criticality_choices[criticality_id],
                    'icon': 'i-exclamation',
                    'url': self.url('criticality', criticality_id)}

            elif criticality_id == Article.CRITICALITY_MEDIUM:
                criticalities[1] = {
                    'id': criticality_id,
                    'name': criticality_choices[criticality_id],
                    'icon': 'i-error',
                    'url': self.url('criticality', criticality_id)}

            elif criticality_id == Article.CRITICALITY_LOW:
                criticalities[2] = {
                    'id': criticality_id,
                    'name': criticality_choices[criticality_id],
                    'icon': 'i-information',
                    'url': self.url('criticality', criticality_id)}

        # Gets articles authors
        from django.contrib.auth.models import User

        for author in User.objects.filter(id__in=self.queryset.values('author')):
            if not any(d['username'] == author.username for d in authors):
                full_name = author.get_full_name()
                authors.append({
                    'username': author.username,
                    'full_name': full_name if len(full_name) > 0 else author.username,
                    'url': self.url('author', author.username)})

        # Gets articles tags
        for (tag_slug, tag_name) in self.queryset.values_list('tags__slug', 'tags__name'):
            if (tag_slug is not None) and (not any(d['slug'] == tag_slug for d in tags)):
                tags.append({'slug': tag_slug, 'name': tag_name, 'url': self.url('tag', tag_slug)})

        return {'criticality_filters': criticalities, 'author_filters': authors, 'tag_filters': tags}

    def get_context_data(self, **kwargs):
        context = super(ArticleNewsListView, self).get_context_data(**kwargs)
        context['query_date'] = self.query_date

        new_context = context.copy()
        new_context.update(self.get_filters())

        return new_context


class ArticleArchiveListView(ViewTitleMixin, FormFilterMixin, ListView):
    title = "Archives"
    context_object_name = 'article_list'
    template_name = 'nouvelles/article_archives.html'
    form_class = ArchiveFiltersForm
    queryset = Article.objects \
        .order_by('-effective_date', '-creation_date')
    paginate_by = 10
    allowed_filters = {
        'criticality': 'criticality',
        'author': 'author__username',
        'date': 'effective_date',
        'tag': 'tags__slug'
    }

    def get_queryset(self):
        result = super(ArticleArchiveListView, self).get_queryset()

        # gets words in the search field and searches for articles
        # that have at least one of the words in title or content.
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.or_, (Q(title__icontains=q) for q in query_list))
                | reduce(operator.or_, (Q(description__icontains=q) for q in query_list))
            )
        return result

    def get_queryset_filters(self):
        filters = super(ArticleArchiveListView, self).get_queryset_filters()
        # Ignore empty filters
        return dict((k, v) for (k, v) in filters.items() if v)


class ArticleDetailView(DetailView, ArticleLineage):
    model = Article


@method_decorator(login_required, name="dispatch")
class ArticleCreateView(PermissionRequiredMixin, ViewTitleMixin, CreateView):
    title = "New article"
    model = Article
    form_class = ArticleForm

    permission_required = 'nouvelles.add_article'

    def form_valid(self, form):
        # Add connected user as author
        form.instance.author = self.request.user
        return super(ArticleCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ArticleCreateView, self).get_context_data(**kwargs)
        context['attachment_form'] = UploadAttachmentForm()
        return context


@method_decorator(login_required, name="dispatch")
class ArticleReplyView(PermissionRequiredMixin, ViewTitleMixin, CreateView, ArticleLineage):
    title = 'New reply'
    model = Article
    form_class = ArticleForm
    permission_required = 'nouvelles.add_article'
    parent_article = None

    def dispatch(self, request, *args, **kwargs):
        self.parent_article = get_object_or_404(Article, slug=kwargs['slug'])
        return super(ArticleReplyView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(ArticleReplyView, self).get_initial().copy()

        if self.parent_article.title.find('Re: ') >= 0:
            initial.update({'title': self.parent_article.title})
        else:
            initial.update({'title': 'Re: %s' % self.parent_article.title})

        initial.update({'tags': self.parent_article.tags.all()})
        return initial

    def get_context_data(self, **kwargs):
        context = super(ArticleReplyView, self).get_context_data(**kwargs)
        context['parent_article'] = self.parent_article
        context['attachment_form'] = UploadAttachmentForm()
        return context

    def form_valid(self, form):
        # Add connected user as author
        form.instance.author = self.request.user
        # Add parent article
        form.instance.parent_article = self.parent_article
        return super(ArticleReplyView, self).form_valid(form)


@method_decorator(login_required, name="dispatch")
class ArticleEditView(UserPassesTestMixin, ViewTitleMixin, UpdateView, ArticleLineage):
    title = "Edit article"
    model = Article
    form_class = ArticleForm

    def test_func(self):
        user = self.request.user
        article = self.get_object()
        return user.has_perm('nouvelles.change_article') or article.author == user

    def form_valid(self, form):
        form.instance.editor = self.request.user
        form.instance.edition_date = timezone.now()
        return super(ArticleEditView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ArticleEditView, self).get_context_data(**kwargs)
        context['attachment_form'] = UploadAttachmentForm()
        del context['article_lineage'][0]  # Removes the current article from lineage
        return context


@method_decorator(login_required, name="dispatch")
class ArticleDeleteView(PermissionRequiredMixin, ViewTitleMixin, SuccessMessageMixin, DeleteView, ArticleLineage):
    model = Article
    success_url = reverse_lazy('nouvelles:index')
    title = 'Delete confirmation'
    success_message = 'The article "%(title)s" has been deleted.'

    permission_required = 'nouvelles.delete_article'

    def delete(self, request, *args, **kwargs):
        from django.contrib import messages
        success_message = self.get_success_message(self.get_object())
        response = super(ArticleDeleteView, self).delete(request, *args, **kwargs)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, instance):
        from django.forms.models import model_to_dict
        return super(ArticleDeleteView, self).get_success_message(model_to_dict(instance))
