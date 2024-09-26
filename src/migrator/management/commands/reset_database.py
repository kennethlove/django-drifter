from django.conf import settings
from django.core.management import CommandParser, call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import DatabaseError, connection


class Command(BaseCommand):
    """Reset the database."""

    help = "Drop all tables and run all migrations"

    def add_arguments(self, parser: CommandParser) -> None:
        """Add optional app argument to the command."""
        parser.add_argument("-y", "--yes", action="store_true", help="Skip confirmation")

    def handle(self, *args: object, **options: object) -> None:
        """Drop all tables and run all migrations."""
        if not settings.DEBUG:
            error = "This command can only be run in DEBUG mode"
            raise CommandError(error)

        query: str = ""
        if settings.DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql":
            query += "SELECT tablename FROM pg_tables WHERE schemaname = 'public'"
        elif settings.DATABASES["default"]["ENGINE"] == "django.db.backends.mysql":
            query += "SHOW TABLES"
        else:
            breakpoint()
            error = "Database engine not supported"
            raise CommandError(error)

        if not options.get("yes"):
            response = input("Are you sure you want to reset the database? [y/N]: ")
            if response.lower() != "y":
                self.stdout.write(self.style.WARNING("Reset cancelled"))
                return

        with connection.cursor() as cursor:
            cursor.execute(query)
            tables = cursor.fetchall()
            for table in tables:
                try:
                    cursor.execute(f'DROP TABLE IF EXISTS "{table[0]}" CASCADE')
                except DatabaseError as e:
                    self.stdout.write(self.style.ERROR(f"Error dropping table {table[0]}: {e}"))
                    continue
        self.stdout.write(self.style.SUCCESS("Successfully dropped all tables"))

        call_command("migrate")
