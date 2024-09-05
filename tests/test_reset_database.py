import pytest

from django.core.management import call_command, CommandError


@pytest.mark.django_db()
def test_reset_database(capsys, settings):
    settings.DEBUG = True
    call_command("reset_database")
    captured = capsys.readouterr()
    assert "Successfully dropped all tables" in captured.out
    assert "Applying polls.0002" in captured.out

def test_fails_in_production():
    with pytest.raises(CommandError):
        call_command("reset_database")
