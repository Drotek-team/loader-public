from hypothesis import given
from hypothesis import strategies as st
from loader.schemas.drone_px4 import DronePx4

from tests.strategies import slow


@given(
    first_frame=st.integers(0, 3),
    first_x=st.integers(-3, 3),
    first_y=st.integers(-3, 3),
    first_z=st.integers(-3, 3),
    first_r=st.integers(0, 3),
    first_g=st.integers(0, 3),
    first_b=st.integers(0, 3),
    first_w=st.integers(0, 3),
    first_channel=st.integers(0, 3),
    first_duration=st.integers(0, 3),
    second_frame=st.integers(0, 3),
    second_x=st.integers(-3, 3),
    second_y=st.integers(-3, 3),
    second_z=st.integers(-3, 3),
    second_r=st.integers(0, 3),
    second_g=st.integers(0, 3),
    second_b=st.integers(0, 3),
    second_w=st.integers(0, 3),
    second_channel=st.integers(0, 3),
    second_duration=st.integers(0, 3),
)
@slow
def test_encode_decode_drone(
    first_frame: int,
    first_x: int,
    first_y: int,
    first_z: int,
    first_r: int,
    first_g: int,
    first_b: int,
    first_w: int,
    first_channel: int,
    first_duration: int,
    second_frame: int,
    second_x: int,
    second_y: int,
    second_z: int,
    second_r: int,
    second_g: int,
    second_b: int,
    second_w: int,
    second_channel: int,
    second_duration: int,
) -> None:
    drone_px4 = DronePx4(0)

    drone_px4.add_position(first_frame, (first_x, first_y, first_z))
    drone_px4.add_color(first_frame, (first_r, first_g, first_b, first_w))
    drone_px4.add_fire(first_frame, first_channel, first_duration)

    drone_px4.add_position(second_frame, (second_x, second_y, second_z))
    drone_px4.add_color(second_frame, (second_r, second_g, second_b, second_w))
    drone_px4.add_fire(second_frame, second_channel, second_duration)

    assert drone_px4 == DronePx4.from_binary(drone_px4.index, DronePx4.to_binary(drone_px4))
