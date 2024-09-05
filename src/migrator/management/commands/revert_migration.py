from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Undo the last migration'

    def add_arguments(self, parser):
        parser.add_argument("app", type=str, required=False)

    def handle(self, *args, **options):
        """
        Get the last migration from the django_migrations table
        and then undo and redo that migration
        """
        from django.db import connection
        from django.core.management import call_command

        query = "SELECT * FROM django_migrations"
        app_name = options.get("app")
        if app_name:
            query += " WHERE app=%s "
        query += " ORDER BY id DESC LIMIT 1"

        cursor = connection.cursor()
        cursor.execute(query, [app_name])
        last_migration = cursor.fetchone()
        if last_migration is None:
            print("No migrations to redo")
            return

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
            print(f"Reverting {app_name} to {migration_name}")
            call_command('migrate', app_name, migration_name)
        except CommandError:
            raise CommandError('Error reverting migration')

