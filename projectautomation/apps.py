from django.apps import AppConfig


class ProjectAutomationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projectautomation'

    def ready(self):
        import projectautomation.signals
