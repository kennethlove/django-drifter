from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.db import connection


class Command(BaseCommand):
    """Undo and redo the last migration."""

    help = "Undo and redo the last migration"

    def add_arguments(self, parser: CommandParser) -> None:
        """Add optional app argument to the command."""
        parser.add_argument("--app", type=str, required=False)

    def handle(self, *args: object, **options: object) -> None:
        """Undo and redo the last migration.

        Get the last migration from the django_migrations table
        and then undo and redo that migration
        """
        if not settings.DEBUG:
            error = "This command can only be run in DEBUG mode"
            raise CommandError(error)

        cursor = connection.cursor()

        if settings.DATABASES["default"]["ENGINE"] == "django.db.backends.sqlite3":
            cursor.execute("PRAGMA foreign_keys = OFF")

        query = "SELECT * FROM django_migrations"
        app_name = options.get("app", None)
        if app_name:
            query += " WHERE app=%s "
        query += " ORDER BY id DESC LIMIT 1"

        cursor.execute(query, [app_name])
        last_migration = cursor.fetchone()
        if last_migration is None:
            print("No migrations to redo")
            return

        app_name = last_migration[1]
        query += " OFFSET 1"
        cursor.execute(query, [app_name])
        last_app_migration = cursor.fetchone()
        if last_app_migration is None:
            migration_name = last_migration[2]
            if migration_name.startswith("0001"):
                migration_name = "zero"
        else:
            migration_name = last_app_migration[2]

        try:
            print(f"Migrating {app_name} to {migration_name}")
            call_command("migrate", app_name, migration_name)
        except CommandError as err:
            msg = "Error redoing migration"
            raise CommandError(msg) from err
        else:
            print(f"Migrating {app_name} to newest migration")
            call_command("migrate", app_name)

