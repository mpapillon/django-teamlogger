from django.db.models.signals import post_save
from django.dispatch import receiver

from nouvelles.models import Article
from nouvelles.utils import messages
from nouvelles.settings import EMAIL_HIGH_ARTICLES


@receiver(post_save, sender=Article, dispatch_uid="send_article_mail")
def send_article_mail(sender, instance, created, **kwargs):
    """
    Send a new article by email to all users if its criticality is HIGH.
    """
    if not EMAIL_HIGH_ARTICLES:
        return

    if created and instance.criticality == Article.CRITICALITY_HIGH:
        messages.send_article_to_all_users(instance)
