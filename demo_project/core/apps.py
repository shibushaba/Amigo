from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'demo_project.core'

    def ready(self):
        try:
            import demo_project.core.signals
        except Exception:
            pass
