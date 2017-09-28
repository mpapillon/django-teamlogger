from django import forms
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from django.forms import ClearableFileInput

from nouvelles.models import Article, Tag
from nouvelles.templatetags.nouvelles import user_full_name


class ArchiveFiltersForm(forms.Form):
    """
    A form used to filter articles.
    """

    class UserModelChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return user_full_name(obj)

    criticality_choices = [
        (None, "-- All criticalities --")
    ]

    criticality_choices += list(Article.CRITICALITY_CHOICES)

    q = forms.CharField(label='Contains', required=False)
    author = UserModelChoiceField(
        label='Author',
        queryset=User.objects.all().order_by('username'),
        to_field_name='username',
        required=False,
        empty_label='-- All authors --')
    criticality = forms.ChoiceField(
        label='Criticality',
        required=False,
        choices=criticality_choices)
    tag = forms.ModelChoiceField(
        label='Tag',
        queryset=Tag.objects.all().order_by(Lower('name')),
        to_field_name='slug',
        required=False,
        empty_label='-- All tags --')


class ArticleForm(forms.ModelForm):
    """
    A form that allows the publication of an article.
    """

    class Meta:
        model = Article
        fields = ['title', 'criticality', 'effective_date', 'tags', 'content']


class UserChangeForm(forms.ModelForm):
    """
    A form that lets a user to change their personal information.
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class AvatarInput(ClearableFileInput):
    template_name = 'nouvelles/forms/avatar_input.html'
