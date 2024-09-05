import pytest
from django.core.management import call_command, CommandError


@pytest.mark.django_db()
def test_revert_migration_default(capsys, settings):
    settings.DEBUG = True

    call_command("migrate", "polls", "zero")
    call_command("migrate", "polls")
    call_command("revert_migration")
    captured = capsys.readouterr()
    assert "Reverting polls" in captured.out

@pytest.mark.django_db()
def test_revert_migration_num(capsys, settings):
    settings.DEBUG = True
    call_command("migrate", "polls", "zero")
    call_command("migrate", "polls")
    call_command("revert_migration", num=2)
    captured = capsys.readouterr()
    assert "Reverting polls to zero" in captured.out

@pytest.mark.django_db()
def test_revert_migration_app(capsys, settings):
    settings.DEBUG = True
    call_command("revert_migration", app="polls")
    captured = capsys.readouterr()
    assert "Reverting polls" in captured.out

def test_fails_in_production():
    with pytest.raises(CommandError):
        call_command("revert_migration")
