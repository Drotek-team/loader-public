import os

from ....parameter.parameter import Parameter
from .drone_decoding_procedure import (
    decode_drone,
)
from .drone_decoding_report import (
    DroneDecodingReport,
)
from .dance_example import (
    COLORS_RAW_DATA,
    DANCE_EXAMPLE,
    FIRES_RAW_DATA,
    POSITIONS_RAW_DATA,
)


def test_valid_dance_decoding():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    drone_decoding_report = DroneDecodingReport(0)
    drone = decode_drone(
        DANCE_EXAMPLE,
        0,
        parameter.iostar_parameter,
        parameter.json_binary_parameter,
        drone_decoding_report,
    )
    # raise ValueError(
    #     drone.position_events.events[0].get_data(),
    #     drone.position_events.events[1].get_data(),
    #     drone.position_events.events[2].get_data(),
    # )
    assert drone_decoding_report.validation
    for decoded_position_event, theorical_position_raw_data in zip(
        drone.position_events.events, POSITIONS_RAW_DATA
    ):
        assert decoded_position_event.get_data() == theorical_position_raw_data
    for decoded_color_event, theorical_color_raw_data in zip(
        drone.color_events.events, COLORS_RAW_DATA
    ):
        assert decoded_color_event.get_data() == theorical_color_raw_data

    for decoded_fire_event, theorical_fire_raw_data in zip(
        drone.fire_events.events, FIRES_RAW_DATA
    ):
        assert decoded_fire_event.get_data() == theorical_fire_raw_data
