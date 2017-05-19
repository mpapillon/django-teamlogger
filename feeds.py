from datetime import timedelta

from django.contrib.syndication.views import Feed
from django.utils import timezone
from django.urls import reverse

from .settings import SITE_NAME, HEADLINES_DAYS
from .models import Article, Tag


class HeadlinesFeed(Feed):
    title = "Headlines of %s" % SITE_NAME
    link = "/feeds/headlines/"
    description = "Latest headlines"

    query_date = (timezone.now() - timedelta(HEADLINES_DAYS)).date()

    def items(self):
        return Article.objects.filter(effective_date__gte=self.query_date).order_by('-effective_date', '-creation_date')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        from markdown_deux.templatetags.markdown_deux_tags import markdown_filter
        return markdown_filter(item.description)
