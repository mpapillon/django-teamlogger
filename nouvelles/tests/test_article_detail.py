from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time

from nouvelles.models import Article


@freeze_time("2017-06-01")
class ArticleDetailTestCase(TestCase):

    fixtures = ['nouvelles_dataset.json']

    def test_article_detail_success(self):
        response = self.client.get(reverse('nouvelles:detail', kwargs={"pk": "1"}))
        self.failUnless(isinstance(response.context['article'], Article))
        self.assertTemplateUsed(response, "nouvelles/article_detail.html")
        self.failUnlessEqual(response.status_code, 200)

    def test_article_detail_404(self):
        response = self.client.get(reverse('nouvelles:detail', kwargs={"pk": "-1"}))
        self.failUnlessEqual(response.status_code, 404)
