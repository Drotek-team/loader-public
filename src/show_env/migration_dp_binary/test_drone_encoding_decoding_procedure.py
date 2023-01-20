from hypothesis import given
from hypothesis import strategies as st

from ..show_px4.drone_px4.drone_px4 import DronePx4
from .drone_decoding_procedure import decode_drone
from .drone_encoding_procedure import encode_drone


@given(
    first_timecode=st.integers(0, 3),
    first_x=st.integers(-3, 3),
    first_y=st.integers(-3, 3),
    first_z=st.integers(-3, 3),
    first_r=st.integers(0, 3),
    first_g=st.integers(0, 3),
    first_b=st.integers(0, 3),
    first_w=st.integers(0, 3),
    first_chanel=st.integers(0, 3),
    first_duration=st.integers(0, 3),
    second_timecode=st.integers(0, 3),
    second_x=st.integers(-3, 3),
    second_y=st.integers(-3, 3),
    second_z=st.integers(-3, 3),
    second_r=st.integers(0, 3),
    second_g=st.integers(0, 3),
    second_b=st.integers(0, 3),
    second_w=st.integers(0, 3),
    second_chanel=st.integers(0, 3),
    second_duration=st.integers(0, 3),
)
def test_encode_decode_drone(
    first_timecode: int,
    first_x: int,
    first_y: int,
    first_z: int,
    first_r: int,
    first_g: int,
    first_b: int,
    first_w: int,
    first_chanel: int,
    first_duration: int,
    second_timecode: int,
    second_x: int,
    second_y: int,
    second_z: int,
    second_r: int,
    second_g: int,
    second_b: int,
    second_w: int,
    second_chanel: int,
    second_duration: int,
):
    drone_px4 = DronePx4(0)

    drone_px4.add_position(first_timecode, (first_x, first_y, first_z))
    drone_px4.add_color(first_timecode, (first_r, first_g, first_b, first_w))
    drone_px4.add_fire(first_timecode, first_chanel, first_duration)

    drone_px4.add_position(second_timecode, (second_x, second_y, second_z))
    drone_px4.add_color(second_timecode, (second_r, second_g, second_b, second_w))
    drone_px4.add_fire(second_timecode, second_chanel, second_duration)

    assert drone_px4 == decode_drone(drone_px4.index, encode_drone(drone_px4))
