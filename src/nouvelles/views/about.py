import random

from django.views.generic import TemplateView
from nouvelles import __credits__, settings


class AboutView(TemplateView):
    """
    Displays information about the software.
    """

    template_name = "nouvelles/about/about.html"

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['peoples'] = random.sample(__credits__, len(__credits__))
        return context


class LicenceView(TemplateView):
    """
    Displays the software licence.
    """

    template_name = "nouvelles/about/licence.html"


class ThirdPartiesView(TemplateView):
    """
    Displays third-party software licenses.
    """

    template_name = "nouvelles/about/third_parties_licence.html"

    def get_context_data(self, **kwargs):
        context = super(ThirdPartiesView, self).get_context_data(**kwargs)
        context['licences'] = ""
        # Getting Third Party Software Licenses.
        with open(settings.ACKNOWLEDGMENTS_FILE, 'r', encoding='UTF-8') as f:
            context['title'] = f.readline()
            f.readline()  # ignore the 2nd line
            for line in f:
                context['licences'] += line
        return context
