from django.conf.urls import include, url

from nouvelles import feeds
from nouvelles.views.about import AboutView, LicenceView, ThirdPartiesView
from nouvelles.views.ajax import PreviewMarkdownAjaxView, AttachmentUploadAjaxView
from nouvelles.views.articles import ArticleHeadlinesView, ArticleArchiveListView, ArticleCreateView, \
    ArticleDetailView, ArticleEditView, ArticleDeleteView, ArticleReplyView

app_name = 'nouvelles'
urlpatterns = [
    # ex: /nouvelles/
    url(r'^$', ArticleHeadlinesView.as_view(), name='index'),
    # ex: /nouvelles/archives
    url(r'^archives/$', ArticleArchiveListView.as_view(), name='archives'),
    # ex: /nouvelles/add
    url(r'^add/$', ArticleCreateView.as_view(), name='create'),
    # ex: /nouvelles/article/preview
    url(r'^article/preview/$', PreviewMarkdownAjaxView.as_view(), name='preview'),

    url(r'^article/(?P<slug>[\w-]+)/', include([
        # ex: /nouvelles/article/page-slug/view
        url(r'^view/$', ArticleDetailView.as_view(), name='detail'),
        # ex: /nouvelles/article/page-slug/edit
        url(r'^edit/$', ArticleEditView.as_view(), name='edit'),
        # ex: /nouvelles/article/page-slug/delete
        url(r'^delete/$', ArticleDeleteView.as_view(), name='delete'),
        # ex: /nouvelles/article/page-slug/reply
        url(r'^reply/$', ArticleReplyView.as_view(), name='reply'),
    ])),

    # ex: /nouvelles/attachment/upload
    url(r'^attachment/upload/$', AttachmentUploadAjaxView.as_view(), name='upload_attachment'),

    url(r'^about/', include([
        # ex: /nouvelles/about
        url(r'^$', AboutView.as_view(), name='about'),
        # ex: /nouvelles/about/licence
        url(r'^licence/$', LicenceView.as_view(), name='licence'),
        # ex: /nouvelles/about/third_parties
        url(r'^third_parties/$', ThirdPartiesView.as_view(), name='third_parties'),
    ], namespace='about')),

    # ex: /nouvelles/feeds/headlines
    url(r'^feeds/headlines/$', feeds.HeadlinesFeed(), name='headlines_feed'),
]
