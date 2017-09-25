from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name="dispatch")
class PreviewMarkdownAjaxView(View):
    def post(self, request, *args, **kwargs):
        from markdown_deux.templatetags.markdown_deux_tags import markdown_filter
        return HttpResponse(markdown_filter(request.POST['text']))
