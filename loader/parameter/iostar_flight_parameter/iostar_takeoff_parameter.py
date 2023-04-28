from dataclasses import dataclass


@dataclass(frozen=True)
class TakeoffParameter:
    takeoff_altitude_meter_min: float = 1.0
    takeoff_altitude_meter_max: float = 8.0
    takeoff_elevation_duration_second: float = 3.0
    takeoff_stabilisation_duration_second: float = 7.0
    takeoff_total_duration_tolerance: float = 4 / 24 + 1e-8

    @property
    def takeoff_duration_second(self) -> float:
        return self.takeoff_elevation_duration_second + self.takeoff_stabilisation_duration_second


TAKEOFF_PARAMETER = TakeoffParameter()
