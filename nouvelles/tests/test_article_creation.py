from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time

from nouvelles.models import Article


@freeze_time("2017-06-01")
class ArticleCreationTestCase(TestCase):

    fixtures = ['nouvelles_dataset.json']

    def test_article_get_not_logged(self):
        response = self.client.get(reverse('nouvelles:create'))
        self.assertEquals(response.status_code, 302)

    def test_get_no_permissions(self):
        self.client.login(username="hschmucker", password="p@ssword")
        response = self.client.get(reverse('nouvelles:create'))
        self.assertEquals(response.status_code, 302)

    def test_get_success(self):
        self.client.login(username="bkane", password="p@ssword")
        response = self.client.get(reverse('nouvelles:create'))
        self.assertTemplateUsed(response, "nouvelles/article_form.html")
        self.assertEquals(response.status_code, 200)

    def test_post_not_logged(self):
        response = self.client.post(reverse('nouvelles:create'), {
            "title": "test_post_not_logger",
            "criticality": Article.CRITICALITY_LOW,
            "effective_date": "2017-05-30",
            "content": ""
        })
        self.assertEquals(response.status_code, 302)

    def test_post_no_permissions(self):
        self.client.login(username="hschmucker", password="p@ssword")
        response = self.client.post(reverse('nouvelles:create'), {
            "title": "test_post_not_logger",
            "criticality": Article.CRITICALITY_LOW,
            "effective_date": "2017-05-30",
            "content": ""
        })
        self.assertTrue(len(Article.objects.filter(title="test_post_not_logger")) == 0)
        self.assertEquals(response.status_code, 302)

    def test_post_success(self):
        self.client.login(username="bkane", password="p@ssword")
        response = self.client.post(reverse('nouvelles:create'), {
            "title": "test_post_not_logger",
            "criticality": Article.CRITICALITY_LOW,
            "effective_date": "2017-05-30",
            "content": "",
            "_publish": "_publish",
            "attachments-TOTAL_FORMS": "0",
            "attachments-INITIAL_FORMS": "0",
            "attachments-MIN_NUM_FORMS": "0",
            "attachments-MAX_NUM_FORMS": "1000"
        })
        self.assertTrue(len(Article.objects.filter(title="test_post_not_logger")) > 0)
        self.assertEquals(response.status_code, 302)
