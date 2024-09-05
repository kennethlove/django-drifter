import pytest

from django.core.management import call_command


@pytest.mark.django_db()
def test_reset_database(capsys):
    call_command("reset_database")
    captured = capsys.readouterr()
    assert "Successfully dropped all tables" in captured.out
    assert "Applying polls.0002" in captured.out
