from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import get_connection
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string

from nouvelles.models import Article
from nouvelles.settings import SITE_NAME


def send_article_to_all_users(article: Article):
    """
    Send by email an Article to all users registered.
    
    :param article: the article to send.
    """
    def _get_raw_message(art: Article):
        from io import StringIO
        from django.utils import formats

        def _get_header_for(name: str, value: str):
            return name.ljust(10) + value + "\n"

        buff = StringIO()

        buff.write("-----\n")
        buff.write(_get_header_for('Title', article.title))
        buff.write(_get_header_for('Date', formats.date_format(article.effective_date)))
        buff.write(_get_header_for('Author', article.author.get_full_name()))
        buff.write("-----\n\n")
        buff.write(art.content)

        msg = buff.getvalue()
        buff.close()

        return msg

    connection = get_connection()  # uses SMTP server specified in settings.py
    mails = []

    for user in User.objects.exclude(email=''):
        html_message = render_to_string('nouvelles/email/article_detail.html', {
            'article': article,
            'domain': getattr(settings, 'SITE_DOMAIN')
        })

        subject = "[%s] %s by %s" % (SITE_NAME, article.title, article.author.get_full_name())
        raw_message = _get_raw_message(article)

        mail = EmailMultiAlternatives(subject, raw_message, settings.SERVER_EMAIL, [user.email])
        mail.attach_alternative(html_message, 'text/html')

        mails.append(mail)

    connection.send_messages(mails)