import struct
from dataclasses import dataclass
from typing import Tuple

from .frame_parameter import FRAME_PARAMETER


@dataclass(frozen=True)
class Bound:
    minimal: int
    maximal: int


@dataclass(frozen=True)
class JsonBinaryParameter:
    magic_number = 43605  # A signature add in the header of the binary
    fmt_header = ">HIB"  # Size in bits of the header
    fmt_section_header = ">BII"  # Size in bits of the section header
    timecode_format = "I"
    coordinate_format = "h"
    chrome_format = "B"
    fire_chanel_format = "B"
    fire_duration_format = "B"
    dance_size_max = 100_000  # Maximal size of the binary send to the drone in octect
    frame_reformat_factor = (
        1  # Factor apply to the frame before the import to compress the dance size
    )
    position_reformat_factor = (
        1  # Factor apply to the position before the import to compress the dance size
    )
    fire_chanel_number = 3

    @property
    def position_event_format(self) -> str:
        return f">{self.timecode_format}{self.coordinate_format}{self.coordinate_format}{self.coordinate_format}"

    @property
    def color_event_format(self) -> str:
        return f">{self.timecode_format}{self.chrome_format}{self.chrome_format}{self.chrome_format}{self.chrome_format}"

    @property
    def fire_event_format(self) -> str:
        return f">{self.timecode_format}{self.fire_chanel_format}{self.fire_duration_format}"

    @staticmethod
    def _binary_format_size(binary_format: str) -> int:
        return 2 ** (8 * struct.calcsize(f">{binary_format}"))

    # TODO Test these methods for documentation test
    @property
    def timecode_value_bound(self) -> Bound:
        return Bound(
            0,
            self._binary_format_size(self.timecode_format),
        )

    @property
    def coordinate_value_bound(self) -> Bound:
        return Bound(
            -self._binary_format_size(self.coordinate_format) // 2,
            self._binary_format_size(self.coordinate_format) // 2,
        )

    @property
    def chrome_value_bound(self) -> Bound:
        return Bound(
            0,
            self._binary_format_size(self.chrome_format),
        )

    @property
    def fire_chanel_value_bound(self) -> Bound:
        return Bound(
            0,
            self.fire_chanel_number - 1,
        )

    @property
    def fire_duration_value_bound(self) -> Bound:
        return Bound(
            0,
            self._binary_format_size(self.fire_duration_format),
        )

    @property
    def show_start_frame(self) -> int:
        return 0

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
JSON_BINARY_PARAMETER = JsonBinaryParameter()
JSON_BINARY_PARAMETER = JsonBinaryParameter()
