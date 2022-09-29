from typing import List
from ...drones_px4.drones_px4 import DronesPx4
from ...parameter.parameter import JsonConvertionConstant
from ...show_simulation.drone_simulation import DroneSimulation, PositionEventSimulation
from ...drones_px4.drone_px4.events.position_events import PositionEvent


def get_drone_simulation(
    drone_index: int,
    position_events: List[PositionEvent],
    json_convertion_constant: JsonConvertionConstant,
) -> DroneSimulation:
    return DroneSimulation(
        drone_index,
        [
            PositionEventSimulation(
                position_event.frame,
                json_convertion_constant.from_json_position_to_simulation_position(
                    position_event.get_values()
                ),
            )
            for position_event in position_events
        ],
    )


def DP_to_DS_procedure(
    drones_px4: DronesPx4, json_convertion_constant: JsonConvertionConstant
) -> List[DroneSimulation]:
    return [
        get_drone_simulation(
            drone_px4.index,
            drone_px4.position_events.event_list,
            json_convertion_constant,
        )
        for drone_px4 in drones_px4.drones
    ]
