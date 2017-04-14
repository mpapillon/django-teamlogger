import itertools

from django.db import models
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth.models import User
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
        return reverse('download_attachment', kwargs={'pk': self.id})

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
    title = models.CharField(max_length=50)
    creation_date = models.DateTimeField(auto_now_add=True)
    effective_date = models.DateField(default=timezone.now)
    description = models.TextField(default=None, blank=True, null=True)
    slug = models.SlugField(editable=False)
    criticality = models.CharField(max_length=1, choices=CRITICALITY_CHOICES, default=CRITICALITY_LOW)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='articles')
    parent_article = models.ForeignKey("self", on_delete=models.CASCADE, default=None, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    edition_date = models.DateTimeField(blank=True, default=timezone.now)
    editor = models.ForeignKey(User, on_delete=models.PROTECT, default=None, blank=True, null=True, related_name='editions')
    attachments = models.ManyToManyField(Attachment, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            # creates slug if not yet saved
            max_length = Article._meta.get_field('slug').max_length
            self.slug = orig = slugify(self.title)[:max_length]

            for x in itertools.count(1):
                if not Article.objects.filter(slug=self.slug).exists():
                    break
                # Truncate the original slug dynamically. Minus 1 for the hyphen.
                self.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)

        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug})

    def __str__(self):
        return '[' + self.author.username + '] ' + self.title
