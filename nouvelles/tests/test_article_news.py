from collections import OrderedDict

from django.db.models import QuerySet
from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time


@freeze_time("2017-06-01")
class ArticleNewsTestCase(TestCase):

    fixtures = ['nouvelles_dataset.json']

    def test_headlines_success(self):
        response = self.client.get(reverse('nouvelles:index'))
        self.failUnless(isinstance(response.context['article_list'], QuerySet))
        self.assertTemplateUsed(response, "nouvelles/article_news_list.html")
        self.failUnlessEqual(response.status_code, 200)