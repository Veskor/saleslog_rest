from django.apps import AppConfig


class CoreApiConfig(AppConfig):
    name = 'core_api'

    def ready(self):
        import core_api.signals
