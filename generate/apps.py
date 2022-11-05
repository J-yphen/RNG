from django.apps import AppConfig


class GenerateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'generate'
    
    def ready(self):
        from task_scheduler import tasks
        tasks.start()