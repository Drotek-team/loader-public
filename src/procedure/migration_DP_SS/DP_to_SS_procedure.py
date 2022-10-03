from ...drones_px4.drones_px4 import DronesPx4
from ...parameter.parameter import (
    FrameParameter,
    TakeoffParameter,
    LandParameter,
)
from ...show_simulation.show_simulation import ShowSimulationSlice
from typing import List
from ...show_simulation.show_simulation import ShowSimulation
from .DP_to_DS_procedure import DP_to_DS_procedure
from ...show_simulation.drone_simulation import get_last_frame, DroneSimulation
from .migration_DS_TS.DS_to_TS_procedure import DS_to_TS_procedure


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


def update_show_slices_from_drone_simulation_simulation(
    show_slices: List[ShowSimulationSlice],
    drone_simulation: DroneSimulation,
    frame_parameter: FrameParameter,
    takeoff_parameter: TakeoffParameter,
    land_parameter: LandParameter,
) -> None:
    trajectory_simulation = DS_to_TS_procedure(
        drone_simulation,
        show_slices[-1].frame,
        frame_parameter,
        takeoff_parameter,
        land_parameter,
    )
    for show_slice, drone_position, drone_in_air, drone_in_dance in zip(
        show_slices,
        trajectory_simulation.drone_positions,
        trajectory_simulation.drone_in_air,
        trajectory_simulation.drone_in_dance,
    ):
        show_slice.positions[drone_simulation.drone_index] = drone_position
        show_slice.in_air_flags[drone_simulation.drone_index] = drone_in_air
        show_slice.in_dance_flags[drone_simulation.drone_index] = drone_in_dance


MINIMAL_ACCELERATION_ESTIMATION_INDEX = 2


def update_slices_implicit_values(
    show_slices: List[ShowSimulationSlice],
    frame_parameter: FrameParameter,
) -> None:
    for slice_index in range(MINIMAL_ACCELERATION_ESTIMATION_INDEX, len(show_slices)):
        show_slices[slice_index].velocities = frame_parameter.position_fps * (
            show_slices[slice_index].positions - show_slices[slice_index - 1].positions
        )
        show_slices[slice_index].accelerations = (
            frame_parameter.position_fps
            * frame_parameter.position_fps
            * (
                show_slices[slice_index].positions
                - 2 * show_slices[slice_index - 1].positions
                + show_slices[slice_index - 2].positions
            )
        )


def DP_to_SS_procedure(
    drones_px4: DronesPx4,
    frame_parameter: FrameParameter,
    takeoff_parameter: TakeoffParameter,
    land_parameter: LandParameter,
) -> ShowSimulation:
    drones_simulation = DP_to_DS_procedure(drones_px4)
    show_slices = get_empty_show_slices(
        last_frame=get_last_frame(drones_simulation, land_parameter, frame_parameter)
        + 1,
        nb_drones=len(drones_simulation),
        frame_parameter=frame_parameter,
    )
    for drone_simulation in drones_simulation:
        update_show_slices_from_drone_simulation_simulation(
            show_slices=show_slices,
            drone_simulation=drone_simulation,
            frame_parameter=frame_parameter,
            takeoff_parameter=takeoff_parameter,
            land_parameter=land_parameter,
        )
    update_slices_implicit_values(show_slices, frame_parameter)
    return ShowSimulation(show_slices)
