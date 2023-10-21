from django.apps import AppConfig


class MyAccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_account'

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        from . import signals
