from django.conf.urls import url

from nouvelles import feeds
from nouvelles.views.ajax import PreviewMarkdownAjaxView, AttachmentUploadAjaxView
from nouvelles.views.attachments import AttachmentDownloadView
from nouvelles.views.articles import ArticleNewsListView, ArticleArchiveListView, ArticleCreateView, ArticleDetailView, \
    ArticleEditView, ArticleDeleteView, ArticleReplyView

urlpatterns = [
    # ex: /nouvelles/
    url(r'^$', ArticleNewsListView.as_view(), name='index'),
    # ex: /nouvelles/archives
    url(r'^archives/$', ArticleArchiveListView.as_view(), name='archives'),
    # ex: /nouvelles/add
    url(r'^add/$', ArticleCreateView.as_view(), name='create'),
    # ex: /nouvelles/article/preview
    url(r'^article/preview/$', PreviewMarkdownAjaxView.as_view(), name='preview'),
    # ex: /nouvelles/article/page-slug/view
    url(r'^article/(?P<slug>[\w-]+)/view/$', ArticleDetailView.as_view(), name='detail'),
    # ex: /nouvelles/article/page-slug/edit
    url(r'^article/(?P<slug>[\w-]+)/edit/$', ArticleEditView.as_view(), name='edit'),
    # ex: /nouvelles/article/page-slug/delete
    url(r'^article/(?P<slug>[\w-]+)/delete/$', ArticleDeleteView.as_view(), name='delete'),
    # ex: /nouvelles/article/page-slug/reply
    url(r'^article/(?P<slug>[\w-]+)/reply/$', ArticleReplyView.as_view(), name='create_reply'),

    # ex: /nouvelles/attachment/upload
    url(r'^attachment/upload/$', AttachmentUploadAjaxView.as_view(), name='upload_attachment'),
    # ex: /nouvelles/attachment/download/12
    url(r'^attachment/download/(?P<pk>[0-9]+)/$', AttachmentDownloadView.as_view(), name='download_attachment'),

    # ex: /nouvelles/feeds/headlines
    url(r'^feeds/headlines/$', feeds.HeadlinesFeed(), name='headlines_feed'),
]
