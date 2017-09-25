from django.conf.urls import include, url
from django.contrib.auth import views as auth

from nouvelles import feeds
from nouvelles.views import about, ajax, articles, profile

app_name = 'nouvelles'

urlpatterns = [
    # ex: /nouvelles/
    url(r'^$', articles.ArticleHeadlinesView.as_view(), name='index'),

    # ex: /nouvelles/archives
    url(r'^archives/$', articles.ArticleArchiveListView.as_view(), name='archives'),

    # ex: /nouvelles/drafts
    url(r'^drafts/$', articles.ArticleDraftsView.as_view(), name='drafts'),

    # ex: /nouvelles/article/new
    url(r'^article/new/$', articles.ArticleCreateView.as_view(), name='create'),

    # ex: /nouvelles/article/new/preview
    url(r'^article/new/preview/$', ajax.PreviewMarkdownAjaxView.as_view(), name='preview'),

    # ex: /nouvelles/article/page-id
    url(r'^article/(?P<pk>[\w-]+)/', include([
        # ex: /nouvelles/article/page-id/view
        url(r'^$', articles.ArticleDetailView.as_view(), name='detail'),
        # ex: /nouvelles/article/page-id/edit
        url(r'^edit/$', articles.ArticleEditView.as_view(), name='edit'),
        # ex: /nouvelles/article/page-id/delete
        url(r'^delete/$', articles.ArticleDeleteView.as_view(), name='delete'),
        # ex: /nouvelles/article/page-id/reply
        url(r'^reply/$', articles.ArticleReplyView.as_view(), name='reply'),
    ])),

    # ex: /nouvelles/about
    url(r'^about/', include([
        # ex: /nouvelles/about
        url(r'^$', about.AboutView.as_view(), name='about'),
        # ex: /nouvelles/about/licence
        url(r'^licence/$', about.LicenceView.as_view(), name='licence'),
        # ex: /nouvelles/about/third_parties
        url(r'^third_parties/$', about.ThirdPartiesView.as_view(), name='third_parties'),
    ], namespace='about')),

    # ex: /nouvelles/feeds/headlines
    url(r'^feeds/headlines/$', feeds.HeadlinesFeed(), name='headlines_feed'),

    # ex: /nouvelles/profile
    url(r'^profile/', include([
        # ex: /nouvelles/profile/change
        url(r'^change/$', profile.DetailsChangeView.as_view(), name='change'),
        # ex: /nouvelles/profile/change/done
        url(r'^change/done$', profile.DetailsChangeDoneView.as_view(), name='change_done'),
        # ex: /nouvelles/profile/password_change
        url(r'^password_change/$', auth.PasswordChangeView.as_view(), name='password_change'),
        # ex: /nouvelles/profile/password_change/done
        url(r'^password_change/done/$', auth.PasswordChangeDoneView.as_view(), name='password_change_done'),
    ], namespace='profile')),
]
