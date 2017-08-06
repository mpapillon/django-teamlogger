import itertools

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class Attachment(models.Model):
    file = models.FileField(upload_to='attachments/%Y/%m/%d/')
    file_name = models.CharField(max_length=255, editable=False)
    file_md5 = models.CharField(max_length=40, unique=True, editable=False)
    content_type = models.CharField(max_length=100, editable=False)
    upload_date = models.DateTimeField(auto_now_add=True)
    upload_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='uploads')

    def get_or_compute_file_md5(self):
        if not self.file_md5:
            from nouvelles.utils import compute_file_md5
            self.file_md5 = compute_file_md5(self.file.file)

        return self.file_md5

    def get_absolute_url(self):
        return self.file.url

    def save(self, *args, **kwargs):
        # if the attachment was not yet in the database
        self.file_name = self.file.name
        self.content_type = self.file.file.content_type
        self.file_md5 = self.get_or_compute_file_md5()

        super(Attachment, self).save(*args, **kwargs)

    def __str__(self):
        return self.file_name


class Tag(models.Model):
    name = models.CharField(max_length=35)
    slug = models.SlugField(max_length=40, editable=False, unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            # creates slug if not yet saved
            max_length = Tag._meta.get_field('slug').max_length
            self.slug = orig = slugify(self.name)[:max_length]

            for x in itertools.count(1):
                if not Tag.objects.filter(slug=self.slug).exists():
                    break
                # Truncate the original slug dynamically. Minus 1 for the hyphen.
                self.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)

        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(models.Model):
    # Criticality definition
    CRITICALITY_LOW = 'L'
    CRITICALITY_MEDIUM = 'M'
    CRITICALITY_HIGH = 'H'

    CRITICALITY_CHOICES = (
        (CRITICALITY_LOW, 'Low'),
        (CRITICALITY_MEDIUM, 'Medium'),
        (CRITICALITY_HIGH, 'High')
    )

    # Fields definition
    title = models.CharField(max_length=90)
    content = models.TextField(default=None, blank=True, null=True)
    criticality = models.CharField(max_length=1, choices=CRITICALITY_CHOICES, default=CRITICALITY_LOW)

    publication_date = models.DateTimeField(blank=True, null=True)
    edition_date = models.DateTimeField(blank=True, default=timezone.now)
    creation_date = models.DateTimeField(auto_now_add=True)
    effective_date = models.DateField(default=timezone.now)

    # Foreign keys
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='articles')
    editor = models.ForeignKey(User, on_delete=models.PROTECT, default=None, blank=True, null=True, related_name='editions')
    parent_article = models.ForeignKey("self", on_delete=models.CASCADE, default=None, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    attachments = models.ManyToManyField(Attachment, blank=True)

    def get_absolute_url(self):
        return reverse('nouvelles:detail', kwargs={'pk': self.pk})

    def get_responses(self):
        return self.article_set.exclude(publication_date__isnull=True).order_by('-effective_date', '-creation_date')

    def is_published(self):
        return self.publication_date is not None

    is_published.boolean = True
    is_published.short_description = 'Published ?'

    def __str__(self):
        return '[' + self.author.username + '] ' + self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="profile")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
