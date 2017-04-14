from django import forms

from django.forms import ModelForm

from django.contrib.auth.models import User

from nouvelles.models import Attachment, Article, Tag


class ArchiveFiltersForm(forms.Form):
    criticality_choices = [
        (None, "-- All criticalities --")
    ]

    criticality_choices += list(Article.CRITICALITY_CHOICES)

    title = forms.CharField(label='Title', required=False)
    author = forms.ModelChoiceField(
        label='Author',
        queryset=User.objects.all().order_by('username'),
        to_field_name='username',
        required=False,
        empty_label='-- All authors --')
    date = forms.DateField(required=False)
    criticality = forms.ChoiceField(
        label='Criticality',
        required=False,
        choices=criticality_choices)
    tag = forms.ModelChoiceField(
        label='Tag',
        queryset=Tag.objects.all().order_by('name'),
        to_field_name='slug',
        required=False,
        empty_label='-- All tags --')


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'criticality', 'effective_date', 'tags', 'description', 'attachments']


class UploadAttachmentForm(ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']
        labels = {
            'file': 'Add attachment'
        }
