from datetime import timedelta

from django.contrib.syndication.views import Feed
from django.utils import timezone

from .settings import SITE_NAME, HEADLINES_DAYS
from .models import Article


class HeadlinesFeed(Feed):
    """
    Represent the syndication feed of Headlines page.
    """
    title = "Headlines of %s" % SITE_NAME
    link = "/nouvelles/feeds/headlines/"
    description = "Latest Headlines"

    query_date = (timezone.now() - timedelta(HEADLINES_DAYS)).date()

    def items(self):
        return Article.objects.filter(effective_date__gte=self.query_date).order_by('-effective_date', '-creation_date')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        from django.template.loader import render_to_string
        return render_to_string('nouvelles/email/article_detail.html', {
            'article': item,
            'domain': ''
        })

    def item_pubdate(self, item: Article):
        return item.creation_date

    def item_author_name(self, item):
        return item.author.get_full_name()

    def item_author_email(self, item):
        return item.author.email