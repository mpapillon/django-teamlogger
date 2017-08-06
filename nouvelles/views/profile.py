from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import UpdateView, FormView
from django.views.generic.base import ContextMixin, TemplateResponseMixin, View, TemplateView
from nouvelles.forms import DetailsChangeForm


class DetailsChangeView(LoginRequiredMixin, FormView):
    template_name = 'registration/details_change_form.html'
    success_url = reverse_lazy('nouvelles:profile:change_done')
    form_class = DetailsChangeForm

    def get_form_kwargs(self):
        kwargs = super(DetailsChangeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(DetailsChangeView, self).form_valid(form)


class DetailsChangeDoneView(TemplateView):
    template_name = 'registration/details_change_done.html'
