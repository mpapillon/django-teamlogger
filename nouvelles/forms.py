from django import forms
from django.contrib.auth.models import User
from django.db.models.functions import Lower

from nouvelles.models import Article, Tag, Profile
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


class DetailsChangeForm(forms.Form):
    """
    A form that lets a user to change their personal information.
    """

    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)
    avatar = forms.ImageField(required=False)

    def __init__(self, user, initial=None, *args, **kwargs):
        self.user = user
        object_data = forms.model_to_dict(user, ['first_name', 'last_name', 'email'])
        # if initial was provided, it should override the values from instance
        if initial is not None:
            object_data.update(initial)

        super(DetailsChangeForm, self).__init__(initial=object_data, *args, **kwargs)

    def save(self, commit=True):
        if not hasattr(self.user, 'profile'):
            self.user.profile = Profile()

        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        self.user.email = self.cleaned_data['email']

        if 'avatar' in self.files:
            avatar = self.files['avatar']
            self.user.profile.avatar.save(avatar.name, avatar)
        if commit:
            self.user.profile.save()
            self.user.save()

        return self.user
