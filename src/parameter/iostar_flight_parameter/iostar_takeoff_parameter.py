from dataclasses import dataclass


@dataclass(frozen=True)
class TakeoffParameter:
    takeoff_altitude_meter = 1.0
    takeoff_elevation_duration_second = 3.0
    takeoff_stabilisation_duration_second = 7.0

    @property
    def takeoff_duration_second(self) -> float:
        return (
            self.takeoff_elevation_duration_second
            + self.takeoff_stabilisation_duration_second
        )


TAKEOFF_PARAMETER = TakeoffParameter()
