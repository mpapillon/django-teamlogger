from collections import OrderedDict

from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time

from nouvelles.models import Article


@freeze_time("2017-06-01")
class ArticleCreationTestCase(TestCase):

    fixtures = ['nouvelles_dataset.json']

    def test_article_get_create_not_logged(self):
        response = self.client.get(reverse('create'))
        self.assertEquals(response.status_code, 302)

    def test_article_get_create_no_permissions(self):
        self.client.login(username="hschmucker", password="p@ssword")
        response = self.client.get(reverse('create'))
        self.assertEquals(response.status_code, 302)

    def test_article_get_create_success(self):
        self.client.login(username="bkane", password="p@ssword")
        response = self.client.get(reverse('create'))
        self.assertTemplateUsed(response, "nouvelles/article_form.html")
        self.assertEquals(response.status_code, 200)

    def test_article_post_create_not_logger(self):
        response = self.client.post(reverse('create'), {
            "title": "test_article_post_create_not_logger",
            "criticality": Article.CRITICALITY_LOW,
            "effective_date": "2017-05-30",
            "description": ""
        })
        self.assertEquals(response.status_code, 302)

    def test_article_post_create_no_permissions(self):
        self.client.login(username="hschmucker", password="p@ssword")
        response = self.client.post(reverse('create'), {
            "title": "test_article_post_create_not_logger",
            "criticality": Article.CRITICALITY_LOW,
            "effective_date": "2017-05-30",
            "description": ""
        })
        self.assertTrue(len(Article.objects.filter(title="test_article_post_create_not_logger")) == 0)
        self.assertEquals(response.status_code, 302)

    def test_article_post_create_success(self):
        self.client.login(username="bkane", password="p@ssword")
        response = self.client.post(reverse('create'), {
            "title": "test_article_post_create_not_logger",
            "criticality": Article.CRITICALITY_LOW,
            "effective_date": "2017-05-30",
            "description": ""
        })
        self.assertTrue(len(Article.objects.filter(title="test_article_post_create_not_logger")) > 0)
        self.assertEquals(response.status_code, 302)
