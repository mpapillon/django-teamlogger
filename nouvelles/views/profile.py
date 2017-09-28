from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.views.generic.base import TemplateView

from nouvelles.forms import UserChangeForm, AvatarInput
from nouvelles.models import Profile
from nouvelles.views.mixins import ModelFormSetMixin


class DetailsChangeView(LoginRequiredMixin, ModelFormSetMixin, UpdateView):
    template_name = 'registration/details_change_form.html'
    success_url = reverse_lazy('nouvelles:profile:change_done')
    model = User
    form_class = UserChangeForm

    def get_formset_class(self, **kwargs):
        """
        Returns the form set class to use in this view
        """
        return inlineformset_factory(self.model, Profile, fields=('avatar',),
                                     widgets={'avatar': AvatarInput()},
                                     can_delete=False)

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        formset = self.get_formset()
        if formset.is_valid():
            formset.save()
            return super(DetailsChangeView, self).form_valid(form)
        else:
            return self.form_invalid(form)


class DetailsChangeDoneView(TemplateView):
    template_name = 'registration/details_change_done.html'
