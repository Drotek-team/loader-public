from .dance_example import *
from .drone_decoding_procedure import decode_drone


# TODO: this phase is extremely critical: test it properly
def test_valid_dance_decoding():
    drone = decode_drone(
        DANCE_EXAMPLE,
        0,
    )
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
