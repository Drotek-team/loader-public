from dataclasses import dataclass
from typing import Tuple

from .frame_parameter import FRAME_PARAMETER


@dataclass(frozen=True)
class JsonBinaryParameter:
    magic_number = 43605  # A signature add in the header of the binary
    fmt_header = ">HIB"  # Size in bits of the header
    fmt_section_header = ">BII"  # Size in bits of the section header
    dance_size_max = 100_000  # Maximal size of the binary send to the drone in octect
    frame_reformat_factor = (
        1  # Factor apply to the frame before the import to compress the dance size
    )
    position_reformat_factor = (
        1  # Factor apply to the position before the import to compress the dance size
    )
    fire_chanel_value_min = 0
    fire_chanel_value_max = 2
    fire_duration_value_frame_min = 0
    fire_duration_value_frame_max = 255
    # TODO: test unitaire + size("I")????
    position_value_min = -32_687
    position_value_max = 32_687
    # TODO: test unitaire ????
    color_value_min = 0
    color_value_max = 255
    # TODO: test unitaire ????
    show_duration_min_second = 0.0
    show_duration_max_second = 1800.0

    @staticmethod
    def _second_to_millisecond(second: float) -> int:
        return int(1e3 * second)

    @staticmethod
    def _millisecond_to_second(millisecond: int) -> float:
        return 1e-3 * millisecond

    @staticmethod
    def _centimer_to_meter(centimer: int) -> float:
        return 1e-2 * centimer

    @staticmethod
    def _meter_to_centimeter(meter: float) -> int:
        return int(1e2 * meter)

    @staticmethod
    def _unit_to_octect(unit: float) -> int:
        return int(255 * unit)

    @staticmethod
    def _octect_to_unit(octect: int) -> float:
        return 1 / 255 * octect

    def from_user_frame_to_px4_timecode(self, user_frame: int) -> int:
        return self._second_to_millisecond(
            FRAME_PARAMETER.from_frame_to_second(user_frame)
        )

    def from_px4_timecode_to_user_frame(self, px4_timecode: int) -> int:
        return FRAME_PARAMETER.from_second_to_frame(
            self._millisecond_to_second(px4_timecode)
        )

    def from_user_position_to_px4_position(self, user_position: float) -> int:
        return self._meter_to_centimeter(user_position / self.position_reformat_factor)

    def from_user_xyz_to_px4_xyz(
        self, user_xyz: Tuple[float, float, float]
    ) -> Tuple[int, int, int]:
        return (
            self.from_user_position_to_px4_position(user_xyz[1]),
            self.from_user_position_to_px4_position(user_xyz[0]),
            -self.from_user_position_to_px4_position(user_xyz[2]),
        )

    def from_px4_position_to_user_position(self, px4_position: int) -> float:
        return self._centimer_to_meter(self.position_reformat_factor * px4_position)

    def from_px4_xyz_to_user_xyz(
        self, px4_xyz: Tuple[int, int, int]
    ) -> Tuple[float, float, float]:
        return (
            self.from_px4_position_to_user_position(px4_xyz[1]),
            self.from_px4_position_to_user_position(px4_xyz[0]),
            -self.from_px4_position_to_user_position(px4_xyz[2]),
        )

    def from_user_rgbw_to_px4_rgbw(
        self, user_rgbw: Tuple[float, float, float, float]
    ) -> Tuple[int, int, int, int]:
        return (
            self._unit_to_octect(user_rgbw[0]),
            self._unit_to_octect(user_rgbw[1]),
            self._unit_to_octect(user_rgbw[2]),
            self._unit_to_octect(user_rgbw[3]),
        )

    def from_px4_rgbw_to_user_rgbw(
        self, px4_rgbw: Tuple[int, int, int, int]
    ) -> Tuple[float, float, float, float]:
        return (
            self._octect_to_unit(px4_rgbw[0]),
            self._octect_to_unit(px4_rgbw[1]),
            self._octect_to_unit(px4_rgbw[2]),
            self._octect_to_unit(px4_rgbw[3]),
        )


JSON_BINARY_PARAMETER = JsonBinaryParameter()
