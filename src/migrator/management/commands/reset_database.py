from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Reset the database to its initial state'

    def handle(self, *args, **options):
        from django.db import connection
        from django.core.management import call_command
        from django.apps import apps

        for app in apps.get_app_configs():
            app_name = app.name.split('.')[-1]
            if app_name == 'migrator':
                continue
            try:
                call_command('migrate', app_name, 'zero')
            except CommandError:
                pass

        call_command('migrate')
