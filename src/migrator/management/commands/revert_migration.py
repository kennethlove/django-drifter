from django.conf import settings
from django.core.management import CommandParser, call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import connection


class Command(BaseCommand):
    """Revert the last migration."""

    help = "Undo the last migration"

    def add_arguments(self, parser: CommandParser) -> None:
        """Add optional app and num arguments to the command."""
        parser.add_argument("--app", type=str, required=False)
        parser.add_argument("--num", type=int, required=False, default=1)

    def handle(self, *args: object, **options: object) -> None:
        """Undo migrations.

        Get the last `num` migrations from the django_migrations table
        and then undo those migrations.
        """
        if not settings.DEBUG:
            error = "This command can only be run in DEBUG mode"
            raise CommandError(error)

        # Get the last N migrations from the django_migrations table
        migrations = "SELECT * FROM django_migrations ORDER BY id DESC LIMIT %s"
        num = options.get("num")
        cursor = connection.cursor()
        cursor.execute(migrations, [num])
        last_n_migrations = cursor.fetchall()

        for migration in last_n_migrations:
            app_name = options.get("app") or migration[1]
            migration_name = migration[2]

            if migration_name.startswith("0001"):
                migration_name = "zero"  # Reset to initial state
            else:  # get previous migration name
                query = "SELECT * FROM django_migrations WHERE app=%s AND id < %s ORDER BY id DESC LIMIT 1"
                cursor.execute(query, [app_name, migration[0]])
                previous_migration = cursor.fetchone()
                if previous_migration is not None:
                    migration_name = previous_migration[2]

            try:
                print(f"Reverting {app_name} to {migration_name}")
                call_command("migrate", app_name, migration_name)
            except CommandError as err:
                error = "Error reverting migration"
                raise CommandError(error) from err
