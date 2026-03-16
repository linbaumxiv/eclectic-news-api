from django.apps import AppConfig

class EclecticConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eclectic'

    def ready(self):
        # This import ensures the signals are registered when Django starts
        import eclectic.signals