from django.http import HttpResponse, Http404
from django.views import View
from django.views.generic.detail import SingleObjectMixin

from nouvelles.models import Attachment


class AttachmentDownloadView(SingleObjectMixin, View):
    model = Attachment

    def get(self, request, *args, **kwargs):
        attach = self.get_object()

        try:
            response = HttpResponse(attach.file, content_type=attach.content_type)
            response['Content-Disposition'] = 'attachment; filename="%s"' % attach.file_name

            return response
        except FileNotFoundError:
            raise Http404('Attachment not found')
