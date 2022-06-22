from dataclasses import dataclass

from ...parameter.export_setup import ExportSetup


@dataclass(frozen=True)
class TakeoffSetup:
    TAKEOFF_ELEVATION_DURATION: float = 3.0
    TAKEOFF_STABILISATION_DURATION: float = 7.0
    # TAKEOFF_ALTITUDE: float = 1.0

    def __init__(self, export_setup: ExportSetup):
        self.fps = scene_setup.SCENE_FPS

    def get_takeoff_elevation_frame_delta(self) -> int:
        return int(self.TAKEOFF_ELEVATION_DURATION * self.fps)

    def get_takeoff_stabilisation_frame_delta(self) -> int:
        return int(self.TAKEOFF_STABILISATION_DURATION * self.fps)
