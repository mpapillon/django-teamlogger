from tempfile import TemporaryFile

from django.core.files.storage import default_storage
from django.db.models import signals as models
from django.dispatch import receiver

from ldapab import signals as directory
from nouvelles.models import Article, Profile, Attachment
from nouvelles.settings import EMAIL_HIGH_ARTICLES
from nouvelles.utils import messages


@receiver(models.post_save, sender=Article, dispatch_uid="send_article_mail")
def send_article_mail(sender, instance, created, **kwargs):
    """
    Send a new article by email to all users if its criticality is HIGH.
    """
    if not EMAIL_HIGH_ARTICLES:
        return

    if created and instance.criticality == Article.CRITICALITY_HIGH:
        messages.send_article_to_all_users(instance)


@receiver(models.post_delete, sender=Profile, dispatch_uid="delete_avatar")
def delete_avatar(sender, instance, **kwargs):
    """
    Deletes file from filesystem when
    corresponding `Profile` object is deleted.
    """
    if instance.avatar:
        if default_storage.exists(instance.avatar):
            default_storage.delete(instance.avatar)


@receiver(models.pre_save, sender=Profile, dispatch_uid="update_avatar")
def update_avatar(sender, instance, **kwargs):
    """
    Deletes old avatar from filesystem
    when corresponding `Profile` object is updated
    with new avatar.
    """
    if not instance.pk:
        return False

    try:
        old_file = Profile.objects.get(pk=instance.pk).avatar
    except Profile.DoesNotExist:
        return False

    new_file = instance.avatar

    if not old_file == new_file and old_file.name:
        if default_storage.exists(old_file):
            default_storage.delete(old_file)


@receiver(directory.populate_user, dispatch_uid="update_profile_from_directory")
def update_profile_from_directory(user, attributes, **kwargs):
    """
    Updates the user Profile from LDAP directory data.
    """
    if not hasattr(user, 'profile'):
        profile = Profile()
        user.profile = profile

    if attributes.get('avatar'):
        with TemporaryFile() as tmp:
            tmp.write(attributes['avatar'])
            user.profile.avatar.save('%s.jpg' % user.username, tmp, True)

    user.profile.save()


@receiver(models.post_delete, sender=Attachment, dispatch_uid="delete_attachment")
def delete_attachment(sender, instance, **kwargs):
    """
    Deletes file from filesystem when
    corresponding `Attachment` object is deleted.
    """
    if instance.file:
        if default_storage.exists(instance.file):
            default_storage.delete(instance.file)
