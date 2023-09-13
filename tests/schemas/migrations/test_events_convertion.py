from hypothesis import given
from hypothesis import strategies as st
from loader.parameters.json_binary_parameters import MagicNumber
from loader.schemas.drone_px4.drone_px4 import decode_events, encode_events
from loader.schemas.drone_px4.events import ColorEvents, FireEvents, PositionEvents

from tests.strategies import slow


@given(
    first_timecode=st.integers(0, 3),
    first_x=st.integers(-3, 3),
    first_y=st.integers(-3, 3),
    first_z=st.integers(-3, 3),
    second_timecode=st.integers(0, 3),
    second_x=st.integers(-3, 3),
    second_y=st.integers(-3, 3),
    second_z=st.integers(-3, 3),
    magic_number=st.sampled_from(MagicNumber),
)
@slow
def test_encode_decode_position_events(
    first_timecode: int,
    first_x: int,
    first_y: int,
    first_z: int,
    second_timecode: int,
    second_x: int,
    second_y: int,
    second_z: int,
    magic_number: MagicNumber,
) -> None:
    position_events = PositionEvents(magic_number)
    position_events.add_timecode_xyz(
        frame=first_timecode,
        xyz=(first_x, first_y, first_z),
    )
    position_events.add_timecode_xyz(
        frame=second_timecode,
        xyz=(second_x, second_y, second_z),
    )
    new_position_events = PositionEvents(magic_number)
    decode_events(new_position_events, encode_events(position_events))
    assert position_events == new_position_events


@given(
    first_timecode=st.integers(0, 3),
    first_r=st.integers(0, 3),
    first_g=st.integers(0, 3),
    first_b=st.integers(0, 3),
    first_w=st.integers(0, 3),
    second_timecode=st.integers(0, 3),
    second_r=st.integers(0, 3),
    second_g=st.integers(0, 3),
    second_b=st.integers(0, 3),
    second_w=st.integers(0, 3),
    magic_number=st.sampled_from(MagicNumber),
)
@slow
def test_encode_decode_color_events(
    first_timecode: int,
    first_r: int,
    first_g: int,
    first_b: int,
    first_w: int,
    second_timecode: int,
    second_r: int,
    second_g: int,
    second_b: int,
    second_w: int,
    magic_number: MagicNumber,
) -> None:
    color_events = ColorEvents(magic_number)
    color_events.add_timecode_rgbw(
        frame=first_timecode,
        rgbw=(first_r, first_g, first_b, first_w),
    )
    color_events.add_timecode_rgbw(
        frame=second_timecode,
        rgbw=(second_r, second_g, second_b, second_w),
    )
    new_color_events = ColorEvents(magic_number)
    decode_events(new_color_events, encode_events(color_events))
    assert color_events == new_color_events


@given(
    first_timecode=st.integers(0, 3),
    first_channel=st.integers(0, 3),
    first_duration=st.integers(0, 3),
    second_timecode=st.integers(0, 3),
    second_channel=st.integers(0, 3),
    second_duration=st.integers(0, 3),
    magic_number=st.sampled_from(MagicNumber),
)
@slow
def test_encode_decode_fire_events(
    first_timecode: int,
    first_channel: int,
    first_duration: int,
    second_timecode: int,
    second_channel: int,
    second_duration: int,
    magic_number: MagicNumber,
) -> None:
    fire_events = FireEvents(magic_number)
    fire_events.add_timecode_channel_duration(
        frame=first_timecode,
        channel=first_channel,
        duration=first_duration,
    )

    fire_events.add_timecode_channel_duration(
        frame=second_timecode,
        channel=second_channel,
        duration=second_duration,
    )
    new_fire_events = FireEvents(magic_number)
    decode_events(new_fire_events, encode_events(fire_events))
    assert fire_events == new_fire_events
