from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time

from nouvelles.models import Article


@freeze_time("2017-06-01")
class ArticleEditionTestCase(TestCase):

    fixtures = ['nouvelles_dataset.json']

    def test_get_not_logged(self):
        response = self.client.get(reverse('nouvelles:edit', kwargs={"slug": "lorem-ipsum-dolor-sit-amet"}))
        self.assertEquals(response.status_code, 302)

    def test_get_no_permissions(self):
        self.client.login(username="hschmucker", password="p@ssword")
        response = self.client.get(reverse('nouvelles:edit', kwargs={"slug": "lorem-ipsum-dolor-sit-amet"}))
        self.assertEquals(response.status_code, 302)

    def test_get_author(self):
        self.client.login(username="bkane", password="p@ssword")
        response = self.client.get(reverse('nouvelles:edit', kwargs={"slug": "lorem-ipsum-dolor-sit-amet"}))
        self.assertTemplateUsed(response, "nouvelles/article_form.html")
        self.assertEquals(response.status_code, 200)

    def test_get_editor(self):
        self.client.login(username="cgilmore", password="p@ssword")
        response = self.client.get(reverse('nouvelles:edit', kwargs={"slug": "lorem-ipsum-dolor-sit-amet"}))
        self.assertTemplateUsed(response, "nouvelles/article_form.html")
        self.assertEquals(response.status_code, 200)

    def test_post_not_logged(self):
        response = self.client.post(reverse('nouvelles:edit', kwargs={"slug": "lorem-ipsum-dolor-sit-amet"}), {
            "title": "test_not_logger",
            "criticality": Article.CRITICALITY_LOW,
            "effective_date": "2017-05-30",
            "description": ""
        })
        self.assertEquals(response.status_code, 302)

    def test_post_no_permissions(self):
        self.client.login(username="hschmucker", password="p@ssword")
        response = self.client.post(reverse('nouvelles:edit', kwargs={"slug": "lorem-ipsum-dolor-sit-amet"}), {
            "title": "test_no_permissions",
            "criticality": Article.CRITICALITY_LOW,
            "effective_date": "2017-05-30",
            "description": ""
        })
        self.assertTrue(Article.objects.get(slug="lorem-ipsum-dolor-sit-amet").title == "Lorem ipsum dolor sit amet")
        self.assertEquals(response.status_code, 302)

    def test_post_success(self):
        self.client.login(username="bkane", password="p@ssword")
        response = self.client.post(reverse('nouvelles:edit', kwargs={"slug": "lorem-ipsum-dolor-sit-amet"}), {
            "title": "test",
            "criticality": Article.CRITICALITY_LOW,
            "effective_date": "2017-05-30",
            "description": ""
        })
        self.assertTrue(Article.objects.get(slug="lorem-ipsum-dolor-sit-amet").title == "test")
        self.assertEquals(response.status_code, 302)
