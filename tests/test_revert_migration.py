import pytest
from django.core.management import call_command


@pytest.mark.django_db()
def test_revert_migration_default(capsys):
    call_command("migrate", "polls", "zero")
    call_command("migrate", "polls")
    call_command("revert_migration")
    captured = capsys.readouterr()
    assert "Reverting polls" in captured.out

@pytest.mark.django_db()
def test_revert_migration_num(capsys):
    call_command("migrate", "polls", "zero")
    call_command("migrate", "polls")
    call_command("revert_migration", num=2)
    captured = capsys.readouterr()
    assert "Reverting polls to zero" in captured.out

@pytest.mark.django_db()
def test_revert_migration_app(capsys):
    call_command("revert_migration", app="polls")
    captured = capsys.readouterr()
    assert "Reverting polls" in captured.out
