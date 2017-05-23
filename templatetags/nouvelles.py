from tokenize import group

from django import template
from django.core.urlresolvers import resolve

from nouvelles import settings

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
        'site_footer': settings.SITE_FOOTER
    }


@register.inclusion_tag('templatetags/site_title.html')
def site_title(page_title):
    """Build a browser title for the page"""
    return {'page_title': page_title, 'site_name': settings.SITE_NAME}


@register.inclusion_tag('templatetags/articles_list.html')
def articles_list(articles):
    return {'articles': articles}


@register.inclusion_tag('templatetags/articles_list_by_date.html')
def articles_list_by_date(articles):
    """Build a list of articles items"""
    from django.utils import formats
    import collections
    grouped_articles = {}

    for date in articles.dates('effective_date', 'day'):
        date_key = formats.date_format(date)
        grouped_articles.update({date_key: articles.filter(effective_date=date)})

    return {'articles': collections.OrderedDict(sorted(grouped_articles.items(), reverse=True))}


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
