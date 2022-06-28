from typing import List

import numpy as np

from ...parameter.parameter import TimecodeParameter
from .land_setup import LandSetup
from .position_simulation import PositionSimulation


class LandSimulation(PositionSimulation):
    land_setup = LandSetup()

    def generate_land_first_part(
        self,
        land_start_position: np.ndarray,
        land_start_timecode: int,
        timecode_parameter: TimecodeParameter,
    ) -> List[np.ndarray]:
        truncated_first_land_start_timecode = self.truncated_integer(
            land_start_timecode,
            timecode_parameter.position_timecode_rate,
        )
        land_first_part_frames = list(
            np.arange(
                truncated_first_land_start_timecode,
                self.land_setup.get_first_land_frame_delta(),
                timecode_parameter.position_timecode_rate,
            )
        )
        return self.linear_interpolation(
            land_start_position,
            np.array(
                [
                    land_start_position[0],
                    land_start_position[1],
                    self.land_setup.get_first_land_altitude(land_start_position[2]),
                ]
            ),
            land_first_part_frames / self.land_setup.get_first_land_frame_delta(),
        )

    def generate_land_second_part(
        self,
        land_start_timecode: int,
        timecode_parameter: TimecodeParameter,
    ) -> List[np.ndarray]:
        truncated_second_land_start_timecode = self.truncated_integer(
            land_start_timecode + self.land_setup.get_first_land_frame_delta(),
            timecode_parameter.position_timecode_rate,
        )
        land_second_part_frames = list(
            np.arange(
                truncated_second_land_start_timecode,
                self.land_setup.get_second_land_frame_delta(),
                timecode_parameter.position_timecode_rate,
            )
        )
        return self.linear_interpolation(
            self.land_setup.get_second_land_altitude_start(),
            0,
            land_second_part_frames / self.land_setup.get_second_land_frame_delta(),
        )

    def generate_land_third_part(
        self,
        land_start_timecode: int,
        timecode_parameter: TimecodeParameter,
    ) -> List[np.ndarray]:
        truncated_second_land_start_timecode = self.truncated_integer(
            land_start_timecode + self.land_setup.get_first_land_frame_delta(),
            timecode_parameter.position_timecode_rate,
        )
        land_second_part_frames = list(
            np.arange(
                truncated_second_land_start_timecode,
                self.land_setup.get_second_land_frame_delta(),
                timecode_parameter.position_timecode_rate,
            )
        )
        return self.linear_interpolation(
            self.land_setup.get_second_land_altitude_start(),
            0,
            land_second_part_frames / self.land_setup.get_second_land_frame_delta(),
        )


def land_simulation(
    land_start_timecode: int,
    land_start_position: np.ndarray,
    timecode_parameter: TimecodeParameter,
) -> List[np.ndarray]:
    land_simulation = LandSimulation()
    return (
        land_simulation.generate_land_first_part(
            land_start_position, land_start_timecode, timecode_parameter
        )
        + land_simulation.generate_land_second_part(
            land_start_timecode, timecode_parameter
        )
        + land_simulation.generate_land_third_part(
            land_start_timecode, timecode_parameter
        )
    )
