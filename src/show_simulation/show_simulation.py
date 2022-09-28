from typing import List

import numpy as np

from ..drones_px4.trajectory_simulation_manager.trajectory_simulation_manager import (
    TrajectorySimulation,
    TrajectorySimulationManager,
)
from ..parameter.parameter import LandParameter, TakeoffParameter, FrameParameter
from .dance_simulation.convert_trajectory_to_dance_simulation import (
    convert_trajectory_to_dance_simulation,
)


class ShowSimulationSlice:
    def __init__(self, frame: int, nb_drones: int):
        self.frame = frame
        self.drone_indices = np.array([drone_index for drone_index in range(nb_drones)])
        self.positions = np.zeros((nb_drones, 3))
        self.velocities = np.zeros((nb_drones, 3))
        self.accelerations = np.zeros((nb_drones, 3))
        self.in_air_flags = np.array(nb_drones * [False])
        self.in_dance_flags = np.array(nb_drones * [False])

    @property
    def in_air_drone_indices(self) -> List[int]:
        return list(self.drone_indices[self.in_air_flags])

    @property
    def in_dance_drone_indices(self) -> List[int]:
        return list(self.drone_indices[self.in_dance_flags])


class ShowSimulation:
    def __init__(self, show_slices: List[ShowSimulationSlice]):
        self.nb_drones = len(show_slices[0].drone_indices)
        self.show_slices = show_slices

    @property
    def frames(self) -> List[float]:
        return [show_slice.frame for show_slice in self.show_slices]


def get_empty_show_slices(
    last_frame: int, nb_drones: int, frame_parameter: FrameParameter
) -> List[ShowSimulationSlice]:
    return [
        ShowSimulationSlice(
            frame,
            nb_drones,
        )
        for frame in range(
            frame_parameter.show_duration_min_frame,
            last_frame + frame_parameter.position_rate_frame,
            frame_parameter.position_rate_frame,
        )
    ]


def update_show_slices_from_trajectory_simulation(
    show_slices: List[ShowSimulationSlice],
    trajectory_simulation: TrajectorySimulation,
    frame_parameter: FrameParameter,
    takeoff_parameter: TakeoffParameter,
    land_parameter: LandParameter,
) -> None:
    dance_sequence = convert_trajectory_to_dance_simulation(
        trajectory_simulation,
        show_slices[-1].frame,
        frame_parameter,
        takeoff_parameter,
        land_parameter,
    ).dance_sequence
    for show_slice, drone_position, drone_in_air, drone_in_dance in zip(
        show_slices,
        dance_sequence.drone_positions,
        dance_sequence.drone_in_air,
        dance_sequence.drone_in_dance,
    ):
        show_slice.positions[trajectory_simulation.drone_index] = drone_position
        show_slice.in_air_flags[trajectory_simulation.drone_index] = drone_in_air
        show_slice.in_dance_flags[trajectory_simulation.drone_index] = drone_in_dance


def update_slices_implicit_values(
    show_slices: List[ShowSimulationSlice],
    position_fps: int,
) -> None:
    for slice_index in range(2, len(show_slices)):
        show_slices[slice_index].velocities = position_fps * (
            show_slices[slice_index].positions - show_slices[slice_index - 1].positions
        )
        show_slices[slice_index].accelerations = (
            position_fps
            * position_fps
            * (
                show_slices[slice_index].positions
                - 2 * show_slices[slice_index - 1].positions
                + show_slices[slice_index - 2].positions
            )
        )


def get_slices(
    trajectory_simulation_manager: TrajectorySimulationManager,
    frame_parameter: FrameParameter,
    takeoff_parameter: TakeoffParameter,
    land_parameter: LandParameter,
) -> List[ShowSimulationSlice]:
    show_slices = get_empty_show_slices(
        last_frame=trajectory_simulation_manager.get_last_frame(
            land_parameter, frame_parameter
        ),
        nb_drones=len(trajectory_simulation_manager.trajectories_simulation),
        frame_parameter=frame_parameter,
    )
    for trajectory_simulation in trajectory_simulation_manager.trajectories_simulation:
        update_show_slices_from_trajectory_simulation(
            show_slices=show_slices,
            trajectory_simulation=trajectory_simulation,
            frame_parameter=frame_parameter,
            takeoff_parameter=takeoff_parameter,
            land_parameter=land_parameter,
        )
    update_slices_implicit_values(
        show_slices, position_fps=frame_parameter.position_fps
    )
    return show_slices
