from django.apps import AppConfig

class StoreappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'storeapp'

    def ready(self):
        import storeapp.signals
