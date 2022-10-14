from dataclasses import dataclass
from typing import Tuple

### TO DO: this is 100% a parameter type, has nothing to do here
@dataclass(frozen=True)
class XyzConvertionStandard:
    CENTIMETER_TO_METER_FACTOR: float = 1e-2
    METER_TO_CENTIMETER_FACTOR: float = 1e2
    NORMAL_TO_COMPRESSED_FACTOR: float = 0.25
    COMPRESSED_TO_NORMAL_FACTOR: float = 4

    def from_px4_xyz_to_user_xyz(
        self, px4_xyz: Tuple[int, int, int]
    ) -> Tuple[float, float, float]:
        return (
            self.COMPRESSED_TO_NORMAL_FACTOR
            * self.CENTIMETER_TO_METER_FACTOR
            * px4_xyz[1],
            self.COMPRESSED_TO_NORMAL_FACTOR
            * self.CENTIMETER_TO_METER_FACTOR
            * px4_xyz[0],
            -self.COMPRESSED_TO_NORMAL_FACTOR
            * self.CENTIMETER_TO_METER_FACTOR
            * px4_xyz[2],
        )

    def from_user_xyz_to_px4_xyz(
        self, simulation_xyz: Tuple[float, float, float]
    ) -> Tuple[int, int, int]:
        return (
            int(
                self.NORMAL_TO_COMPRESSED_FACTOR
                * self.METER_TO_CENTIMETER_FACTOR
                * simulation_xyz[1]
            ),
            int(
                self.NORMAL_TO_COMPRESSED_FACTOR
                * self.METER_TO_CENTIMETER_FACTOR
                * simulation_xyz[0]
            ),
            int(
                self.NORMAL_TO_COMPRESSED_FACTOR
                * -self.METER_TO_CENTIMETER_FACTOR
                * simulation_xyz[2]
            ),
        )


@dataclass(frozen=True)
class RgbwConvertionStandard:
    UNIT_TO_OCTECT_FACTOR: float = 255.0
    OCTECT_TO_UNIT_FACTOR: float = 1.0 / 255.0

    def from_px4_rgbw_to_user_rgbw(
        self, px4_rgbw: Tuple[int, int, int, int]
    ) -> Tuple[float, float, float, float]:
        return (
            self.OCTECT_TO_UNIT_FACTOR * px4_rgbw[0],
            self.OCTECT_TO_UNIT_FACTOR * px4_rgbw[1],
            self.OCTECT_TO_UNIT_FACTOR * px4_rgbw[2],
            self.OCTECT_TO_UNIT_FACTOR * px4_rgbw[3],
        )

    def from_user_rgbw_to_px4_rgbw(
        self, user_rgbw: Tuple[float, float, float, float]
    ) -> Tuple[int, int, int, int]:
        return (
            int(self.UNIT_TO_OCTECT_FACTOR * user_rgbw[0]),
            int(self.UNIT_TO_OCTECT_FACTOR * user_rgbw[1]),
            int(self.UNIT_TO_OCTECT_FACTOR * user_rgbw[2]),
            int(self.UNIT_TO_OCTECT_FACTOR * user_rgbw[3]),
        )


@dataclass(frozen=True)
class FireDurationConvertionStandard:
    TIMECODE_TO_SECOND_FACTOR: float = 1e-3
    SECOND_TO_TIMECODE_FACTOR: float = 1e3

    def from_px4_fire_duration_to_user_fire_duration(
        self, px4_fire_duration: int
    ) -> float:
        return self.TIMECODE_TO_SECOND_FACTOR * px4_fire_duration

    def from_user_fire_duration_to_px4_fire_duration(
        self, user_fire_duration: float
    ) -> int:
        return int(self.SECOND_TO_TIMECODE_FACTOR * user_fire_duration)
