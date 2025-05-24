from django.apps import AppConfig


class CakeryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cakery'

    def ready(self):
        from . import signals