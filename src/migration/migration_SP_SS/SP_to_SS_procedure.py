from ...show_px4.show_px4 import ShowPx4
from ...parameter.parameter import (
    FrameParameter,
    TakeoffParameter,
    LandParameter,
)
from ...show_simulation.show_simulation import ShowSimulationSlice
from typing import List
from ...show_simulation.show_simulation import ShowSimulation
from .SP_to_DS_procedure import SP_to_SD_procedure
from ..migration_DS_TS.DD_to_DT_procedure import DD_to_DT_procedure
from ...show_dev.show_dev import DroneDev


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


def update_show_slices_from_drone_dev_simulation(
    show_slices: List[ShowSimulationSlice],
    drone_dev: DroneDev,
    frame_parameter: FrameParameter,
    takeoff_parameter: TakeoffParameter,
    land_parameter: LandParameter,
) -> None:
    drone_trajectory = DD_to_DT_procedure(
        drone_dev,
        show_slices[-1].frame,
        frame_parameter,
        takeoff_parameter,
        land_parameter,
    )
    for show_slice, drone_position, drone_in_air, drone_in_dance in zip(
        show_slices,
        drone_trajectory.drone_positions,
        drone_trajectory.drone_in_air,
        drone_trajectory.drone_in_dance,
    ):
        show_slice.positions[drone_dev.drone_index] = drone_position
        show_slice.in_air_flags[drone_dev.drone_index] = drone_in_air
        show_slice.in_dance_flags[drone_dev.drone_index] = drone_in_dance


VELOCITY_ESTIMATION_INDEX = 1
ACCELERATION_ESTIMATION_INDEX = 2


def update_slices_implicit_values(
    show_slices: List[ShowSimulationSlice],
    frame_parameter: FrameParameter,
) -> None:
    for slice_index in range(ACCELERATION_ESTIMATION_INDEX, len(show_slices)):
        show_slices[slice_index].velocities = frame_parameter.position_fps * (
            show_slices[slice_index].positions
            - show_slices[slice_index - VELOCITY_ESTIMATION_INDEX].positions
        )
        show_slices[slice_index].accelerations = (
            frame_parameter.position_fps
            * frame_parameter.position_fps
            * (
                show_slices[slice_index].positions
                - 2 * show_slices[slice_index - VELOCITY_ESTIMATION_INDEX].positions
                + show_slices[slice_index - ACCELERATION_ESTIMATION_INDEX].positions
            )
        )


def DP_to_SS_procedure(
    show_px4: ShowPx4,
    frame_parameter: FrameParameter,
    takeoff_parameter: TakeoffParameter,
    land_parameter: LandParameter,
) -> ShowSimulation:
    drones_dev = SP_to_SD_procedure(show_px4)
    show_slices = get_empty_show_slices(
        last_frame=drones_dev.get_last_frame(land_parameter, frame_parameter),
        nb_drones=len(drones_dev),
        frame_parameter=frame_parameter,
    )
    for drone_dev in drones_dev:
        update_show_slices_from_drone_dev_simulation(
            show_slices=show_slices,
            drone_dev=drone_dev,
            frame_parameter=frame_parameter,
            takeoff_parameter=takeoff_parameter,
            land_parameter=land_parameter,
        )
    update_slices_implicit_values(show_slices, frame_parameter)
    return ShowSimulation(show_slices)
