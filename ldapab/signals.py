from django.dispatch import Signal

populate_user = Signal(providing_args=["user", "attributes"])
