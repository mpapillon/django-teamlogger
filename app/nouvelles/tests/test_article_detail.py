from collections import OrderedDict

from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time

from nouvelles.models import Article


@freeze_time("2017-06-01")
class ArticleDetailTestCase(TestCase):

    fixtures = ['nouvelles_dataset.json']

    def test_headlines_success(self):
        response = self.client.get(reverse('index'))
        self.failUnless(isinstance(response.context['articles'], OrderedDict))
        self.assertTemplateUsed(response, "nouvelles/article_news_list.html")
        self.failUnlessEqual(response.status_code, 200)

    def test_article_detail_success(self):
        response = self.client.get(reverse('detail', kwargs={"slug": "lorem-ipsum-dolor-sit-amet"}))
        self.failUnless(isinstance(response.context['article'], Article))
        self.assertTemplateUsed(response, "nouvelles/article_detail.html")
        self.failUnlessEqual(response.status_code, 200)

    def test_article_detail_404(self):
        response = self.client.get(reverse('detail', kwargs={"slug": "none"}))
        self.failUnlessEqual(response.status_code, 404)
