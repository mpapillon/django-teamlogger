import random

from django.views.generic import TemplateView
from nouvelles import __credits__


class AboutView(TemplateView):
    template_name = "nouvelles/about/about.html"

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['peoples'] = random.sample(__credits__, len(__credits__))
        return context


class LicenceView(TemplateView):
    template_name = "nouvelles/about/licence.html"

