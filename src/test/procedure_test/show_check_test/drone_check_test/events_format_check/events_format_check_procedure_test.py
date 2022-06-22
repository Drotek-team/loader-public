import pytest

from ......drones_manager.drone.events.position_events import PositionEvents
from ......parameter.parameter import Parameter
from ......procedure.show_check.drone_check.events_format_check.events_format_check_procedure import (
    apply_events_format_check_procedure,
)
from ......procedure.show_check.drone_check.events_format_check.events_format_check_report import (
    PositionEventsCheckReport,
)


@pytest.fixture
def my_position_events():
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    takeoff_parameter = parameter.takeoff_parameter
    timecode_parameter = parameter.timecode_parameter
    position_events = PositionEvents()
    position_events.add(timecode_parameter.show_time_begin, (0, 0, 0))
    position_events.add(
        timecode_parameter.show_time_begin + takeoff_parameter.takeoff_duration,
        (0, 0, takeoff_parameter.takeoff_altitude),
    )
    return position_events


@pytest.fixture
def my_position_events_report():
    return PositionEventsCheckReport()


def test_position_events_timecode_check(
    my_position_events: PositionEvents,
    my_position_events_check_report: PositionEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    apply_events_format_check_procedure(
        my_position_events,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
        parameter.timecode_parameter,
        my_position_events_check_report,
    )
    assert my_position_events_check_report.timecode_check
