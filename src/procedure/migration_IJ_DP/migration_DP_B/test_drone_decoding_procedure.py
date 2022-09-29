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
    #     drone.position_events.event_list[0].get_raw_data(),
    #     drone.position_events.event_list[1].get_raw_data(),
    #     drone.position_events.event_list[2].get_raw_data(),
    # )
    assert drone_decoding_report.validation
    for decoded_position_event, theorical_position_raw_data in zip(
        drone.position_events.event_list, POSITIONS_RAW_DATA
    ):
        assert decoded_position_event.get_raw_data() == theorical_position_raw_data
    for decoded_color_event, theorical_color_raw_data in zip(
        drone.color_events.event_list, COLORS_RAW_DATA
    ):
        assert decoded_color_event.get_raw_data() == theorical_color_raw_data

    for decoded_fire_event, theorical_fire_raw_data in zip(
        drone.fire_events.event_list, FIRES_RAW_DATA
    ):
        assert decoded_fire_event.get_raw_data() == theorical_fire_raw_data
