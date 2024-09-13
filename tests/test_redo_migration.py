import pytest
from django.core.management import CommandError, call_command


@pytest.mark.django_db
def test_redo_migration_no_migrations(capsys, settings):
    """Redoing migrations when there are no migrations."""
    settings.DEBUG = True
    call_command("migrate", "polls", "zero")
    call_command("redo_migration", app="polls")
    captured = capsys.readouterr()
    assert "No migrations to redo" in captured.out


@pytest.mark.django_db
def test_redo_migration_first_migration(capsys, settings):
    """Redoing the first migration."""
    settings.DEBUG = True
    call_command("migrate", "polls", "zero")
    call_command("migrate", "polls", "0001")
    call_command("redo_migration", app="polls")
    captured = capsys.readouterr()
    assert "Migrating polls to zero" in captured.out


@pytest.mark.django_db
def test_redo_migration_multiple_migrations(capsys, settings):
    """Redoing the last migration out of multiple migrations."""
    settings.DEBUG = True
    call_command("migrate", "polls")
    call_command("redo_migration", app="polls")
    captured = capsys.readouterr()
    assert "Migrating polls to 0001" in captured.out


@pytest.mark.django_db
def test_redo_migration_multiple_migrations_no_app_name(capsys, settings):
    """Redoing the last migration without specifying the app name."""
    settings.DEBUG = True
    call_command("migrate", "polls", "zero")
    call_command("migrate", "polls")
    call_command("redo_migration")
    captured = capsys.readouterr()
    assert "Migrating polls to 0001" in captured.out


def test_fails_in_production():
    """The command should fail in production."""
    with pytest.raises(CommandError):
        call_command("redo_migration")
