from six.moves import urllib

DEFAULT_DIRECTORY_ALIAS = 'default'


def parse_ldap_url(ldap_url=None):
    if not ldap_url:
        return

    url = urllib.parse.urlparse(ldap_url)

    # Remove query strings.
    path = url.path[1:]
    path = urllib.parse.unquote_plus(path.split('?', 2)[0])

    queries = {}

    for q in url.query.split('&'):
        if not q:
            continue
        a = q.split('=', 1)
        queries[a[0].upper()] = a[1]

    return {
        'HOST': url.hostname,
        'PORT': url.port,
        'USER': url.username,
        'PASSWORD': url.password,
        'BASE': path,
        'GROUP_BASE': queries.get('GROUP_BASE', None),
        'ADMIN_GROUP': queries.get('ADMIN_GROUP', None),
    }
