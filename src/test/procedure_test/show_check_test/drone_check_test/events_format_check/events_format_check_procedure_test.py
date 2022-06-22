import pytest

from ......procedure.show_check.drone_check.events_format_check.events_format_check_procedure import (
    apply_events_format_check_procedure,
)


@pytest.fixture
def my_position_events():
    return 0


def test_position_events_check():
    assert apply_events_format_check_procedure()
