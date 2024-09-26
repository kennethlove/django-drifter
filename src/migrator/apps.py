from django.apps import AppConfig


class MigratorConfig(AppConfig):
    """Migrator app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "migrator"
