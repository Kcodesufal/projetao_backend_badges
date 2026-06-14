from django.apps import AppConfig


class OngsConfig(AppConfig):
    name = 'ongs'

    def ready(self):
        import ongs.signals  # noqa: F401
