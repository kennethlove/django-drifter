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
    with pytest.raises(OSError):
        call_command("reset_database")
    captured = capsys.readouterr()
    assert "Are you sure you want to reset the database? [y/N]: " in captured.out


def test_fails_in_production():
    """The command should fail in production."""
    with pytest.raises(CommandError):
        call_command("reset_database")


@pytest.mark.django_db
def test_unsupported_engine(settings):
    """Command fails if the database engine is not supported."""
    settings.DATABASES["default"]["ENGINE"] = "django.db.backends.oracle"
    with pytest.raises(CommandError):
        call_command("reset_database")
