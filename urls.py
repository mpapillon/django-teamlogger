from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /nouvelles/
    url(r'^$', views.ArticleNewsListView.as_view(), name='index'),
    # ex: /nouvelles/archives
    url(r'^archives/$', views.ArticleArchiveListView.as_view(), name='archives'),
    # ex: /nouvelles/add
    url(r'^add/$', views.ArticleCreateView.as_view(), name='create'),
    # ex: /nouvelles/article/preview
    url(r'^article/preview/$', views.PreviewMarkdownAjaxView.as_view(), name='preview'),
    # ex: /nouvelles/article/page-slug/view
    url(r'^article/(?P<slug>[\w-]+)/view/$', views.ArticleDetailView.as_view(), name='detail'),
    # ex: /nouvelles/article/page-slug/edit
    url(r'^article/(?P<slug>[\w-]+)/edit/$', views.ArticleEditView.as_view(), name='edit'),
    # ex: /nouvelles/article/page-slug/delete
    url(r'^article/(?P<slug>[\w-]+)/delete/$', views.ArticleDeleteView.as_view(), name='delete'),
    # ex: /nouvelles/article/page-slug/reply
    url(r'^article/(?P<slug>[\w-]+)/reply/$', views.ArticleReplyView.as_view(), name='create_reply'),

    # ex: /nouvelles/attachment/upload
    url(r'^attachment/upload/$', views.AttachmentUploadAjaxView.as_view(), name='upload_attachment'),
    # ex: /nouvelles/attachment/download/12
    url(r'^attachment/download/(?P<pk>[0-9]+)/$', views.AttachmentDownloadView.as_view(), name='download_attachment'),
]
