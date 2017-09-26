import operator
from datetime import timedelta
from functools import reduce

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import SuspiciousOperation
from django.db.models import Q
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from nouvelles.forms import ArticleForm, ArchiveFiltersForm
from nouvelles.models import Article, Attachment
from nouvelles.settings import HEADLINES_DAYS
from nouvelles.views.mixins import ViewTitleMixin, FilterMixin, FormFilterMixin, ArticleLineage, ModelFormSetMixin


class AttachmentsFormSetMixin(ModelFormSetMixin):
    """
    A mixin that provides a support to manage Attachments formsets.
    """

    def get_formset_class(self, **kwargs):
        """
        Returns the form set class to use in this view
        """
        return inlineformset_factory(self.model, Attachment, fields=('file',), extra=0)

    def form_valid(self, form):
        """
        If the form is valid, saves formset data.
        """
        # Apply the treatment on the parent form to avoid persistence problems
        success_redirection = super(AttachmentsFormSetMixin, self).form_valid(form)
        formset = self.get_formset()
        if formset.is_valid():
            # Set the user who uploaded the new files
            for attach_form in formset.forms:
                attach = attach_form.instance
                if not hasattr(attach, 'upload_by'):
                    attach.upload_by = self.request.user
            formset.save()
            return success_redirection
        else:
            # Something is wrong in the formset, returning to the main form
            self.form_invalid(form)


class DraftSaveArticleMixin(object):
    """
    This mixin allows the user to save the article in his drafts.
    """

    draft_saved_message = 'The article "{title}" was saved in your drafts.'

    def form_valid(self, form):
        if self.request.POST.get('_publish'):
            # The user wants to publish the post
            form.instance.publication_date = timezone.now()
            return super(DraftSaveArticleMixin, self).form_valid(form)
        elif self.request.POST.get('_draft'):
            # The user wants to save the post as draft
            success_msg = self.get_draft_saved_message(form.cleaned_data)
            messages.success(self.request, success_msg)
            # Calls validation & save
            super(DraftSaveArticleMixin, self).form_valid(form)
            # Returning to the editor
            return HttpResponseRedirect(reverse('nouvelles:edit', kwargs={'pk': self.object.pk}))

    def get_draft_saved_message(self, cleaned_data):
        """
        Returns the formatted success message.
        """
        return self.draft_saved_message.format(**cleaned_data)


class ArticleHeadlinesView(ViewTitleMixin, FilterMixin, ListView):
    query_date = (timezone.now() - timedelta(HEADLINES_DAYS)).date()

    title = 'Headlines'
    context_object_name = 'article_list'
    template_name = 'nouvelles/article_headlines.html'
    queryset = Article.objects \
        .filter(effective_date__gte=query_date) \
        .exclude(publication_date__isnull=True) \
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
                    'url': self.url('criticality', criticality_id)}

            elif criticality_id == Article.CRITICALITY_MEDIUM:
                criticalities[1] = {
                    'id': criticality_id,
                    'name': criticality_choices[criticality_id],
                    'url': self.url('criticality', criticality_id)}

            elif criticality_id == Article.CRITICALITY_LOW:
                criticalities[2] = {
                    'id': criticality_id,
                    'name': criticality_choices[criticality_id],
                    'url': self.url('criticality', criticality_id)}

        # Gets articles authors
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
        context = super(ArticleHeadlinesView, self).get_context_data(**kwargs)

        new_context = context.copy()
        new_context.update(self.get_filters())

        return new_context


class ArticleArchiveListView(ViewTitleMixin, FormFilterMixin, ListView):
    title = "Archives"
    context_object_name = 'article_list'
    template_name = 'nouvelles/article_archives.html'
    form_class = ArchiveFiltersForm
    queryset = Article.objects \
        .exclude(publication_date__isnull=True) \
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
                reduce(operator.and_, (Q(title__icontains=q) for q in query_list))
                | reduce(operator.and_, (Q(content__icontains=q) for q in query_list))
            )
        return result


class ArticleDetailView(UserPassesTestMixin, DetailView, ArticleLineage):
    model = Article

    def test_func(self):
        user = self.request.user
        article = self.get_object()

        # If the article is not published, the connected user need to be the author.
        return article.is_published() or not (article.author != user)


class ArticleCreateView(PermissionRequiredMixin, ViewTitleMixin, DraftSaveArticleMixin, AttachmentsFormSetMixin,
                        CreateView):
    title = "New article"
    model = Article
    form_class = ArticleForm

    permission_required = 'nouvelles.add_article'

    def form_valid(self, form):
        # Add connected user as author
        form.instance.author = self.request.user
        return super(ArticleCreateView, self).form_valid(form)


class ArticleReplyView(PermissionRequiredMixin, ViewTitleMixin, DraftSaveArticleMixin, AttachmentsFormSetMixin,
                       CreateView, ArticleLineage):
    title = 'New reply'
    model = Article
    form_class = ArticleForm
    permission_required = 'nouvelles.add_article'
    parent_article = None

    def dispatch(self, request, *args, **kwargs):
        self.parent_article = get_object_or_404(Article, id=kwargs['pk'])

        if not self.parent_article.is_published():
            raise SuspiciousOperation("You can't reply to an unpublished article.")

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
        return context

    def form_valid(self, form):
        # Add connected user as author
        form.instance.author = self.request.user
        # Add parent article
        form.instance.parent_article = self.parent_article
        return super(ArticleReplyView, self).form_valid(form)


class ArticleEditView(UserPassesTestMixin, ViewTitleMixin, DraftSaveArticleMixin, AttachmentsFormSetMixin, UpdateView,
                      ArticleLineage):
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
        del context['article_lineage'][0]  # Removes the current article from lineage
        return context


class ArticleDeleteView(UserPassesTestMixin, ViewTitleMixin, SuccessMessageMixin, DeleteView, ArticleLineage):
    model = Article
    success_url = reverse_lazy('nouvelles:index')
    title = 'Delete confirmation'
    success_message = 'The article "%(title)s" has been deleted.'

    def test_func(self):
        user = self.request.user
        article = self.get_object()
        return user.has_perm('nouvelles.delete_article') or (article.author == user and not article.is_published())

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


class ArticleDraftsView(PermissionRequiredMixin, ViewTitleMixin, ListView):
    title = "My drafts"
    template_name = 'nouvelles/article_drafts.html'

    permission_required = 'nouvelles.add_article'

    model = Article
    ordering = ('-effective_date', '-creation_date')

    def get_queryset(self):
        queryset = super(ArticleDraftsView, self).get_queryset()
        # Fetch only not published user's articles
        return queryset.filter(author=self.request.user).filter(publication_date__isnull=True)
