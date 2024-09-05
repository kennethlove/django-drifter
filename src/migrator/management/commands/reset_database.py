from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.core.management import call_command
from django.conf import settings


class Command(BaseCommand):
    help = 'Drop all tables and run all migrations'

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("This command can only be run in DEBUG mode")

        with connection.cursor() as cursor:
            cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
            tables = cursor.fetchall()
            for table in tables:
                cursor.execute(f'DROP TABLE IF EXISTS "{table[0]}" CASCADE')
        self.stdout.write(self.style.SUCCESS('Successfully dropped all tables'))

        call_command('migrate')
