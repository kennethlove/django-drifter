from django.apps import AppConfig


class MigratorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'migrator'
