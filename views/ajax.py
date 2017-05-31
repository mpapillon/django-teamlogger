from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from nouvelles.forms import UploadAttachmentForm
from nouvelles.models import Attachment


@method_decorator(login_required, name="dispatch")
class AttachmentUploadAjaxView(PermissionRequiredMixin, CreateView):
    model = Attachment
    form_class = UploadAttachmentForm

    permission_required = 'nouvelles.add_attachment'

    def form_invalid(self, form):
        response = super(AttachmentUploadAjaxView, self).form_invalid(form)
        return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        from django.db import IntegrityError
        form.instance.upload_by = self.request.user

        try:
            # Try to save the attachment
            super(AttachmentUploadAjaxView, self).form_valid(form)
        except IntegrityError as e:
            # The file already exists in database, we get it
            self.object = Attachment.objects.get(file_md5=form.instance.get_or_compute_file_md5())

        data = {
            'id': self.object.pk,
            'file_name': self.object.file_name,
            'file_md5': self.object.file_md5,
            'file_size': self.object.file.size
        }
        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name="dispatch")
class PreviewMarkdownAjaxView(View):
    def post(self, request, *args, **kwargs):
        from markdown_deux.templatetags.markdown_deux_tags import markdown_filter
        return HttpResponse(markdown_filter(request.POST['text']))
