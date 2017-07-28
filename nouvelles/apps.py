from django.apps import AppConfig


class NouvellesConfig(AppConfig):
    name = 'nouvelles'
    verbose_name = 'Articles management'

    def ready(self):
        import nouvelles.signals
