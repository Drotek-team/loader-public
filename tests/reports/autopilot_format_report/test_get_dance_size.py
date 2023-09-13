import pytest
from loader.parameters.json_binary_parameters import MagicNumber
from loader.reports import DanceSizeInfraction
from loader.schemas.drone_px4 import DronePx4


def test_dance_size_information_standard_case() -> None:
    dance_size_information = DanceSizeInfraction(
        drone_index=0,
        dance_size=50,
        position_percent=12,
        color_percent=24,
        fire_percent=36,
    )
    assert dance_size_information.total_percent == 72


@pytest.mark.parametrize(
    "magic_number, position_percent, color_percent, fire_percent, dance_size_after_position, dance_size_after_color, dance_size_after_fire",
    [
        (MagicNumber.old, 10, 8, 6, 10_016, 18_025, 24_034),
        (MagicNumber.new, 8, 6, 4, 8016, 14025, 18034),
    ],
)
def test_get_dance_size_information_standard_case(
    magic_number: MagicNumber,
    position_percent: int,
    color_percent: int,
    fire_percent: int,
    dance_size_after_position: int,
    dance_size_after_color: int,
    dance_size_after_fire: int,
) -> None:
    empty_drone_px4 = DronePx4(0, magic_number)

    assert DanceSizeInfraction.generate(empty_drone_px4) == DanceSizeInfraction(
        drone_index=0,
        dance_size=7,
        position_percent=0,
        color_percent=0,
        fire_percent=0,
    )

    for _ in range(1_000):
        empty_drone_px4.add_position(0, (0, 0, 0))
    assert DanceSizeInfraction.generate(empty_drone_px4) == DanceSizeInfraction(
        drone_index=0,
        dance_size=dance_size_after_position,
        position_percent=position_percent,
        color_percent=0,
        fire_percent=0,
    )

    for _ in range(1_000):
        empty_drone_px4.add_color(0, (0, 0, 0, 0))
    assert DanceSizeInfraction.generate(empty_drone_px4) == DanceSizeInfraction(
        drone_index=0,
        dance_size=dance_size_after_color,
        position_percent=position_percent,
        color_percent=color_percent,
        fire_percent=0,
    )

    for _ in range(1_000):
        empty_drone_px4.add_fire(0, 0, 0)
    assert DanceSizeInfraction.generate(empty_drone_px4) == DanceSizeInfraction(
        drone_index=0,
        dance_size=dance_size_after_fire,
        position_percent=position_percent,
        color_percent=color_percent,
        fire_percent=fire_percent,
    )
