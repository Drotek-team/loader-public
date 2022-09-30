from ...show_user.drone_user.drone_user import DroneUser
from typing import List
from ...drones_px4.drones_px4 import DronesPx4, DronePx4
from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class XyzConvertionStandard:
    CENTIMETER_TO_METER_RATIO: float = 1e-2
    METER_TO_CENTIMETER_RATIO: float = 1e2

    def from_px4_xyz_to_user_xyz(
        self, px4_xyz: Tuple[int, int, int]
    ) -> Tuple[float, float, float]:
        return (
            self.CENTIMETER_TO_METER_RATIO * px4_xyz[1],
            self.CENTIMETER_TO_METER_RATIO * px4_xyz[0],
            -self.CENTIMETER_TO_METER_RATIO * px4_xyz[2],
        )

    def from_user_xyz_to_px4_xyz(
        self, simulation_xyz: Tuple[float, float, float]
    ) -> Tuple[int, int, int]:
        return (
            int(self.METER_TO_CENTIMETER_RATIO * simulation_xyz[1]),
            int(self.METER_TO_CENTIMETER_RATIO * simulation_xyz[0]),
            int(-self.METER_TO_CENTIMETER_RATIO * simulation_xyz[2]),
        )


@dataclass(frozen=True)
class RgbwConvertionStandard:
    UNIT_TO_OCTECT_RATIO: float = 255.0
    OCTECT_TO_UNIT_RATIO: float = 1.0 / 255.0

    def from_px4_rgbw_to_user_rgbw(
        self, px4_rgbw: Tuple[int, int, int, int]
    ) -> Tuple[float, float, float, float]:
        return (
            self.OCTECT_TO_UNIT_RATIO * px4_rgbw[0],
            self.OCTECT_TO_UNIT_RATIO * px4_rgbw[1],
            self.OCTECT_TO_UNIT_RATIO * px4_rgbw[2],
            self.OCTECT_TO_UNIT_RATIO * px4_rgbw[3],
        )

    def from_user_rgbw_to_px4_rgbw(
        self, user_rgbw: Tuple[float, float, float, float]
    ) -> Tuple[int, int, int, int]:
        return (
            int(self.UNIT_TO_OCTECT_RATIO * user_rgbw[0]),
            int(self.UNIT_TO_OCTECT_RATIO * user_rgbw[1]),
            int(self.UNIT_TO_OCTECT_RATIO * user_rgbw[2]),
            int(self.UNIT_TO_OCTECT_RATIO * user_rgbw[3]),
        )


@dataclass(frozen=True)
class FireDurationConvertionStandard:
    TIMECODE_TO_SECOND_RATIO: float = 1e-3
    SECOND_TO_TIMECODE_RATIO: float = 1e3

    def from_px4_fire_duration_to_user_fire_duration(
        self, px4_fire_duration: int
    ) -> float:
        return self.TIMECODE_TO_SECOND_RATIO * px4_fire_duration

    def from_user_fire_to_px4_fire(self, user_fire_duration: float) -> int:
        return int(self.SECOND_TO_TIMECODE_RATIO * user_fire_duration)


def drone_user_to_drone_px4_procedure(
    drone_user: DroneUser,
    xyz_convertion_standard: XyzConvertionStandard,
    rgbw_convertion_standard: RgbwConvertionStandard,
    fire_duration_convertion_standard: FireDurationConvertionStandard,
) -> DronePx4:
    drone_px4 = DronePx4()
    for position_event_user in drone_user.position_events:
        drone_px4.add_position(
            position_event_user.frame,
            xyz_convertion_standard.from_user_xyz_to_px4_xyz(
                (
                    position_event_user.x,
                    position_event_user.y,
                    position_event_user.z,
                )
            ),
        )
    for color_event_user in drone_user.color_events:
        drone_px4.add_color(
            color_event_user.frame,
            rgbw_convertion_standard.from_user_rgbw_to_px4_rgbw(
                (
                    color_event_user.r,
                    color_event_user.g,
                    color_event_user.b,
                    color_event_user.w,
                )
            ),
        )
    for fire_event_user in drone_user.fire_events:
        drone_px4.add_fire(
            fire_event_user.frame,
            fire_event_user.chanel,
            fire_duration_convertion_standard.from_user_fire_to_px4_fire(
                fire_event_user.duration
            ),
        )


def DU_to_DP_procedure(
    drones_user: List[DroneUser],
) -> DronesPx4:
    xyz_convertion_standard = XyzConvertionStandard()
    rgbw_convertion_standard = RgbwConvertionStandard()
    fire_duration_convertion_standard = FireDurationConvertionStandard()
    return DronesPx4(
        [
            drone_user_to_drone_px4_procedure(
                drone_user,
                xyz_convertion_standard,
                rgbw_convertion_standard,
                fire_duration_convertion_standard,
            )
            for drone_user in drones_user
        ]
    )
