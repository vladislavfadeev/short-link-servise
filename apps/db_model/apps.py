from django.apps import AppConfig


class DbModelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.db_model'
    label = 'db_model'
