from django.apps import AppConfig


class HistoricoConfig(AppConfig):
    name = 'historico'

    def ready(self):
        import historico.signals  # noqa: F401
