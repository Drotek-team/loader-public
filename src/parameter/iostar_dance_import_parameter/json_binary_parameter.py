from dataclasses import dataclass
from typing import Tuple

CENTIMETER_TO_METER_FACTOR = 1e-2
METER_TO_CENTIMETER_FACTOR = 1e2
UNIT_TO_OCTECT_FACTOR = 255.0
OCTECT_TO_UNIT_FACTOR = 1 / 255
SECOND_TO_TIMECODE_FACTOR = 1e3
TIMECODE_TO_SECOND_FACTOR = 1e-3


@dataclass(frozen=True)
class JsonBinaryParameter:
    magic_number = 43605
    fmt_header = ">HIB"
    fmt_section_header = ">BII"
    dance_size_max = 100_000
    frame_reformat_factor = 40
    position_reformat_factor = 4
    fire_chanel_value_min = 0
    fire_chanel_value_max = 2
    fire_duration_value_frame_min = 0
    fire_duration_value_frame_max = 28_800
    position_value_min = -32768
    position_value_max = 327687
    color_value_min = 0
    color_value_max = 255
    show_duration_min_second = 0.0
    show_duration_max_second = 1800.0

    def from_user_xyz_to_px4_xyz(
        self, simulation_xyz: Tuple[float, float, float]
    ) -> Tuple[int, int, int]:
        return (
            int(
                (METER_TO_CENTIMETER_FACTOR * simulation_xyz[1])
                / self.position_reformat_factor
            ),
            int(
                (METER_TO_CENTIMETER_FACTOR * simulation_xyz[0])
                / self.position_reformat_factor
            ),
            int(
                -(METER_TO_CENTIMETER_FACTOR * simulation_xyz[2])
                / self.position_reformat_factor
            ),
        )

    def from_px4_xyz_to_user_xyz(
        self, px4_xyz: Tuple[int, int, int]
    ) -> Tuple[float, float, float]:
        return (
            CENTIMETER_TO_METER_FACTOR * self.position_reformat_factor * px4_xyz[1],
            CENTIMETER_TO_METER_FACTOR * self.position_reformat_factor * px4_xyz[0],
            -CENTIMETER_TO_METER_FACTOR * self.position_reformat_factor * px4_xyz[2],
        )

    def from_user_rgbw_to_px4_rgbw(
        self, user_rgbw: Tuple[float, float, float, float]
    ) -> Tuple[int, int, int, int]:
        return (
            int(UNIT_TO_OCTECT_FACTOR * user_rgbw[0]),
            int(UNIT_TO_OCTECT_FACTOR * user_rgbw[1]),
            int(UNIT_TO_OCTECT_FACTOR * user_rgbw[2]),
            int(UNIT_TO_OCTECT_FACTOR * user_rgbw[3]),
        )

    def from_px4_rgbw_to_user_rgbw(
        self, px4_rgbw: Tuple[int, int, int, int]
    ) -> Tuple[float, float, float, float]:
        return (
            OCTECT_TO_UNIT_FACTOR * px4_rgbw[0],
            OCTECT_TO_UNIT_FACTOR * px4_rgbw[1],
            OCTECT_TO_UNIT_FACTOR * px4_rgbw[2],
            OCTECT_TO_UNIT_FACTOR * px4_rgbw[3],
        )

    def from_user_fire_duration_to_px4_fire_duration(
        self, user_fire_duration: float
    ) -> int:
        return int(SECOND_TO_TIMECODE_FACTOR * user_fire_duration)

    def from_px4_fire_duration_to_user_fire_duration(
        self, px4_fire_duration: int
    ) -> float:
        return TIMECODE_TO_SECOND_FACTOR * px4_fire_duration


JSON_BINARY_PARAMETER = JsonBinaryParameter()
