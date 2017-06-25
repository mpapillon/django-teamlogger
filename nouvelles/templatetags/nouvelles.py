from django import template
from django.core.urlresolvers import resolve
from django.db.models import QuerySet

from nouvelles import settings, __version__
from nouvelles.models import Article

register = template.Library()


@register.inclusion_tag('templatetags/nouvelles_header.html', takes_context=True)
def nouvelles_header(context):
    """Build a navigation bar"""
    request = context['request']
    path_name = resolve(request.path_info).url_name
    redirect_path = request.path

    if path_name == 'login':
        redirect_path = None

    return {
        'path_name': path_name,
        'redirect_path': redirect_path,
        'user': request.user,
        'perms': context.get('perms', None),
        'site_name': settings.SITE_NAME
    }


@register.inclusion_tag('templatetags/nouvelles_footer.html')
def nouvelles_footer():
    """Build the footer"""
    return {
        'site_name': settings.SITE_NAME,
        'site_footer': settings.SITE_FOOTER,
        'app_version': __version__,
    }


@register.inclusion_tag('templatetags/site_title.html')
def site_title(page_title):
    """Build a browser title for the page"""
    return {'page_title': page_title, 'site_name': settings.SITE_NAME}


@register.inclusion_tag('templatetags/format_articles_list.html')
def format_articles_list(articles: QuerySet, show_dates: bool = False):
    ordered_articles = []

    if show_dates:
        paginated_articles = Article.objects.filter(article__in=articles)\
            .filter(effective_date__in=articles.values_list('effective_date'))
        for date in paginated_articles.dates('effective_date', 'day', order='DESC'):
            ordered_articles.append(date)
            ordered_articles.extend(paginated_articles.filter(effective_date=date))
    else:
        ordered_articles = articles

    return {'articles': ordered_articles}


@register.inclusion_tag('templatetags/article.html')
def article(article, show_parents=True):
    return {'article': article, 'show_parents': show_parents}


@register.inclusion_tag('templatetags/article_name.html')
def article_name(article):
    return {'article': article}


@register.simple_tag(takes_context=True)
def paginated_url(context, view_name, page, page_arg_name='page'):
    from django.urls import reverse
    req_params = context.request.GET.copy()

    if req_params.get(page_arg_name):
        req_params.pop(page_arg_name)
        req_params.update({page_arg_name: page})
    else:
        req_params.update({page_arg_name: page})

    return "%s?%s" % (reverse(view_name), req_params.urlencode())


@register.filter
def class_name(obj):
    return obj.__class__.__name__
