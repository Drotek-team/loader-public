from dataclasses import dataclass
from typing import List, Tuple

from ...parameter.parameter import JsonConvertionConstant, LandParameter, FrameParameter
from ..drone_px4.events.position_events import PositionEvent


@dataclass(frozen=True)
class PositionSimulation:
    frame: int
    xyz: Tuple[float, float, float]


class TrajectorySimulation:
    def __init__(
        self, drone_index: int, position_simulation_list: List[PositionSimulation]
    ):
        self.drone_index = drone_index
        self.position_simulation_list = position_simulation_list

    @property
    def flight_positions(self) -> List[PositionSimulation]:
        return self.position_simulation_list[1:]

    @property
    def last_frame(self) -> int:
        return self.position_simulation_list[-1].frame

    @property
    def last_height(self) -> float:
        return self.position_simulation_list[-1].xyz[2]

    def get_frame_by_index(self, index: int) -> float:
        return self.position_simulation_list[index].frame

    def get_position_by_index(self, index: int) -> Tuple[float, float, float]:
        return self.position_simulation_list[index].xyz


def get_trajectory_simulation(
    drone_index: int,
    position_events: List[PositionEvent],
    json_convertion_constant: JsonConvertionConstant,
) -> TrajectorySimulation:
    return TrajectorySimulation(
        drone_index,
        [
            PositionSimulation(
                position_event.frame,
                json_convertion_constant.from_json_position_to_simulation_position(
                    position_event.get_values()
                ),
            )
            for position_event in position_events
        ],
    )


class TrajectorySimulationManager:
    def __init__(self, trajectories_simulation: List[TrajectorySimulation]):
        self.trajectories_simulation = trajectories_simulation

    def get_last_frame(
        self, land_parameter: LandParameter, frame_parameter: FrameParameter
    ) -> int:
        # raise ValueError(
        #     self.trajectories_simulation[0].last_frame,
        #     int(
        #         frame_parameter.json_fps
        #         * land_parameter.get_land_second_delta(
        #             self.trajectories_simulation[0].last_height
        #         )
        #     ),
        #     max(
        #         trajectory_simulation.last_frame
        #         + int(
        #             frame_parameter.json_fps
        #             * land_parameter.get_land_second_delta(
        #                 trajectory_simulation.last_height
        #             )
        #         )
        #         for trajectory_simulation in self.trajectories_simulation
        #     ),
        # )
        return max(
            [
                trajectory_simulation.last_frame
                + int(
                    frame_parameter.json_fps
                    * land_parameter.get_land_second_delta(
                        trajectory_simulation.last_height
                    )
                )
                for trajectory_simulation in self.trajectories_simulation
            ]
        )
