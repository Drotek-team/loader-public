from typing import List

import numpy as np

from ...parameter.parameter import TakeoffParameter, TimecodeParameter
from .position_simulation import PositionSimulation


class TakeoffSimulationTools(PositionSimulation):
    def generate_first_part_takeoff(
        self,
        takeoff_start_timecode: int,
        takeoff_start_position: np.ndarray,
        takeoff_end_position: np.ndarray,
        timecode_parameter: TimecodeParameter,
        takeoff_parameter: TakeoffParameter,
    ) -> List[np.ndarray]:
        truncated_takeoff_start_timecode = self.truncated_integer(
            takeoff_start_timecode,
            timecode_parameter.position_timecode_frequence,
        )
        takeoff_first_part_frames = list(
            np.arange(
                truncated_takeoff_start_timecode,
                truncated_takeoff_start_timecode
                + takeoff_parameter.takeoff_duration_timecode,
                timecode_parameter.position_timecode_frequence,
            )
        )
        return self.linear_interpolation(
            takeoff_start_position,
            takeoff_end_position,
            takeoff_first_part_frames / takeoff_parameter.takeoff_duration_timecode,
        )

    def generate_takeoff_second_part(
        self,
        takeoff_start_timecode: int,
        takeoff_end_timecode: int,
        takeoff_end_position: np.ndarray,
        timecode_parameter: TimecodeParameter,
        takeoff_parameter: TakeoffParameter,
    ) -> List[np.ndarray]:
        truncated_takeoff_second_part_start_frame = self.truncated_integer(
            takeoff_start_timecode + takeoff_parameter.takeoff_duration_timecode,
            timecode_parameter.position_timecode_frequence,
        )
        takeoff_second_part_frames = list(
            np.arange(
                truncated_takeoff_second_part_start_frame,
                takeoff_end_timecode,
                timecode_parameter.position_timecode_frequence,
            )
        )
        return len(takeoff_second_part_frames) * [takeoff_end_position]


def takeoff_simulation(
    takeoff_start_timecode: int,
    takeoff_end_timecode: int,
    takeoff_start_position: np.ndarray,
    takeoff_end_position: np.ndarray,
    timecode_parameter: TimecodeParameter,
    takeoff_parameter: TakeoffParameter,
):
    takeoff_simulation_tools = TakeoffSimulationTools()
    return takeoff_simulation_tools.generate_first_part_takeoff(
        takeoff_start_timecode,
        takeoff_start_position,
        takeoff_end_position,
        timecode_parameter,
        takeoff_parameter,
    ) + takeoff_simulation_tools.generate_takeoff_second_part(
        takeoff_start_timecode,
        takeoff_end_timecode,
        takeoff_end_position,
        timecode_parameter,
        takeoff_parameter,
    )
