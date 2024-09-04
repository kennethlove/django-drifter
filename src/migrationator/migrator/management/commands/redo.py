from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Undo and redo that last migration'

    def handle(self, *args, **options):
        """
        Get the last migration from the django_migrations table
        and then undo and redo that migration
        """
        from django.db import connection
        from django.core.management import call_command

        cursor = connection.cursor()
        last_migration = cursor.execute('SELECT * FROM django_migrations ORDER BY id DESC LIMIT 1').fetchone()
        if last_migration is None:
            raise CommandError('No migrations to redo')

        app_name = last_migration[1]
        last_app_migration = cursor.execute('SELECT * FROM django_migrations WHERE app=%s ORDER BY id DESC LIMIT 1', [app_name]).fetchone()
        if last_app_migration is None:
            raise CommandError('No migrations to redo')

        migration_name = last_app_migration[2]
        if migration_name.startswith("0001"):
            migration_name = "zero"

        call_command('migrate', app_name, migration_name)
        call_command('migrate', app_name)

