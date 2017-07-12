from django import forms

from django.forms import ModelForm

from django.contrib.auth.models import User

from nouvelles.models import Attachment, Article, Tag


class ArchiveFiltersForm(forms.Form):
    class UserModelChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            full_name = obj.get_full_name()
            return full_name if len(full_name) > 0 else obj.username

    criticality_choices = [
        (None, "-- All criticalities --")
    ]

    criticality_choices += list(Article.CRITICALITY_CHOICES)

    q = forms.CharField(label='Search', required=False)
    author = UserModelChoiceField(
        label='Author',
        queryset=User.objects.all().order_by('username'),
        to_field_name='username',
        required=False,
        empty_label='-- All authors --')
    date = forms.DateField(required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
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
