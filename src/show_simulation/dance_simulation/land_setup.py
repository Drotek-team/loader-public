from dataclasses import dataclass

from ...parameter.export_setup import ExportSetup


@dataclass(frozen=True)
class LandSetup:
    LAND_SPEED_FAST: float = 4.0
    LAND_SPEED_SLOW: float = 0.4
    LAND_HGT_SAFE: float = 3.0

    def __init__(self, export_setup: ExportSetup):
        self.fps = scene_setup.SCENE_FPS

    def get_first_land_frame_delta(self, drone_hgt: float) -> int:
        if drone_hgt < self.LAND_HGT_SAFE:
            return int(self.fps * drone_hgt / self.LAND_SPEED_SLOW)
        else:
            return int(
                self.fps * (drone_hgt - self.LAND_HGT_SAFE) / self.LAND_SPEED_FAST
            )

    def get_first_land_altitude(self, drone_hgt: float) -> float:
        if drone_hgt < self.LAND_HGT_SAFE:
            return 0
        else:
            return self.LAND_HGT_SAFE

    def get_second_land_frame_delta(self, drone_hgt: float) -> int:
        if drone_hgt < self.LAND_HGT_SAFE:
            return 1
        else:
            return int(self.fps * self.LAND_HGT_SAFE / self.LAND_SPEED_SLOW)

    def get_second_land_altitude_start(self, drone_hgt: float) -> float:
        if drone_hgt < self.LAND_HGT_SAFE:
            return 0.0
        else:
            return self.LAND_HGT_SAFE
