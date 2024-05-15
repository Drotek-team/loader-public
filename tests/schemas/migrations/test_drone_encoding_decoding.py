from hypothesis import example, given
from hypothesis import strategies as st
from loader.parameters import LandType
from loader.parameters.json_binary_parameters import MagicNumber
from loader.schemas.drone_px4 import DronePx4

from tests.strategies import slow, st_land_type, st_scale


@given(
    first_frame=st.integers(0, 3),
    first_x=st.integers(-3, 3),
    first_y=st.integers(-3, 3),
    first_z=st.integers(-3, 3),
    first_r=st.integers(0, 3),
    first_g=st.integers(0, 3),
    first_b=st.integers(0, 3),
    first_w=st.integers(0, 3),
    first_interpolate=st.booleans(),
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
    second_interpolate=st.booleans(),
    second_channel=st.integers(0, 3),
    second_duration=st.integers(0, 3),
    scale=st_scale,
    land_type=st_land_type,
    magic_number=st.sampled_from(MagicNumber),
)
@slow
@example(
    first_frame=0,
    first_x=0,
    first_y=0,
    first_z=0,
    first_r=0,
    first_g=0,
    first_b=0,
    first_w=0,
    first_interpolate=False,
    first_channel=0,
    first_duration=0,
    second_frame=0,
    second_x=0,
    second_y=0,
    second_z=0,
    second_r=0,
    second_g=0,
    second_b=0,
    second_w=0,
    second_interpolate=False,
    second_channel=0,
    second_duration=0,
    scale=1,
    land_type=LandType.Land,
    magic_number=MagicNumber.v4,
)
def test_encode_decode_drone(
    first_frame: int,
    first_x: int,
    first_y: int,
    first_z: int,
    first_r: int,
    first_g: int,
    first_b: int,
    first_w: int,
    first_interpolate: bool,  # noqa: FBT001
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
    second_interpolate: bool,  # noqa: FBT001
    second_channel: int,
    second_duration: int,
    scale: int,
    land_type: LandType,
    magic_number: MagicNumber,
) -> None:
    drone_px4 = DronePx4(0, magic_number, scale, land_type)

    drone_px4.add_position(first_frame, (first_x, first_y, first_z))
    drone_px4.add_color(
        first_frame,
        (first_r, first_g, first_b, first_w * 2),
        interpolate=first_interpolate,
    )
    drone_px4.add_fire(first_frame, first_channel, first_duration)

    drone_px4.add_position(second_frame, (second_x, second_y, second_z))
    drone_px4.add_color(
        second_frame,
        (second_r, second_g, second_b, second_w * 2),
        interpolate=second_interpolate,
    )
    drone_px4.add_fire(second_frame, second_channel, second_duration)

    assert drone_px4 == DronePx4.from_binary(drone_px4.index, DronePx4.to_binary(drone_px4))
