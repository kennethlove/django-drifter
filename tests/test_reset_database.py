from unittest import mock

import pytest
from django.core.management import CommandError, call_command


@pytest.mark.django_db
def test_reset_database_yes(capsys, settings):
    """Resetting the database to its initial state, with the `yes` flag on."""
    settings.DEBUG = True
    call_command("reset_database", "--yes")
    captured = capsys.readouterr()
    assert "Successfully dropped all tables" in captured.out
    assert "Applying polls.0002" in captured.out


@pytest.mark.django_db
def test_reset_database(capsys, settings):
    """Resetting the database will ask for confirmation."""
    settings.DEBUG = True

    with mock.patch("builtins.input", return_value="q") as _:
        call_command("reset_database")

    captured = capsys.readouterr()
    assert "Reset cancelled" in captured.out


def test_fails_in_production():
    """The command should fail in production."""
    with pytest.raises(CommandError):
        call_command("reset_database")


@pytest.mark.django_db
def test_unsupported_engine(settings):
    """Command fails if the database engine is not supported."""
    original_engine = settings.DATABASES["default"]["ENGINE"]
    settings.DATABASES["default"]["ENGINE"] = "django.db.backends.oracle"
    with pytest.raises(CommandError):
        call_command("reset_database")
    settings.DATABASES["default"]["ENGINE"] = original_engine
