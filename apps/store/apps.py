from django.apps import AppConfig


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.store'

    def ready(self):
        from ..store.signals import create_cart, post_login
