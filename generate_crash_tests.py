from pathlib import Path

import numpy as np
from loader.parameters import FRAME_PARAMETERS, IOSTAR_PHYSIC_PARAMETERS_MAX
from loader.reports import GlobalReport
from loader.schemas import IostarJsonGcs, ShowUser

TAKEOFF_ALTITUDE = 2
TAKEOFF_DURATION = 10
MAX_HORIZONTAL_ACCELERATION = 3
MAX_HORIZONTAL_VELOCITY = 12
MAX_UP_ACCELERATION = 2
MAX_UP_VELOCITY = 3
PAUSE_DURATION = 10

DISTANCE = 100
ALTITUDES = [60, 120]
POSITION_DELTAS = (
    np.array(
        [
            [1, 0, 0],
            [-1, 0, 0],
            [0, 1, 0],
            [0, -1, 0],
        ],
    )
    * DISTANCE
)


def get_time_to_distance(distance: float, max_speed: float, max_acceleration: float) -> float:
    if distance < max_speed**2 / max_acceleration:
        return np.sqrt(distance / max_acceleration)
    distance -= max_speed**2 / max_acceleration
    return max_speed * 2 / max_acceleration + distance / max_speed


def get_time_to_altitude(altitude: float) -> float:
    return get_time_to_distance(altitude, MAX_UP_VELOCITY, MAX_UP_ACCELERATION)


def get_time_to_horizontal_distance(distance: float) -> float:
    return get_time_to_distance(distance, MAX_HORIZONTAL_VELOCITY, MAX_HORIZONTAL_ACCELERATION)


def to_frame(time: float) -> int:
    return FRAME_PARAMETERS.from_second_to_frame(time)


def to_second(frame: int) -> float:
    return FRAME_PARAMETERS.from_frame_to_second(frame)


if __name__ == "__main__":
    for altitude in ALTITUDES:
        for delta_position, direction in zip(POSITION_DELTAS, ["east", "west", "north", "south"]):
            show_user = ShowUser.create(nb_drones=1, angle_takeoff=0, step=1)

            drone = show_user.drones_user[0]

            # Start takeoff
            time = 0
            position = np.zeros(3)
            drone.add_position_event(time, tuple(position))
            drone.add_color_event(time, (0, 1, 0, 0))

            # End takeoff
            time += TAKEOFF_DURATION
            position[2] = TAKEOFF_ALTITUDE
            drone.add_position_event(to_frame(time), tuple(position))

            # Go to altitude
            time += get_time_to_altitude(altitude - TAKEOFF_ALTITUDE) + PAUSE_DURATION
            position[2] = altitude
            drone.add_position_event(to_frame(time), tuple(position))

            # Go to opposite direction
            time += to_second(1)
            position -= delta_position
            drone.add_position_event(to_frame(time), tuple(position))

            # Wait to get to opposite direction
            time += get_time_to_horizontal_distance(DISTANCE) + PAUSE_DURATION
            drone.add_position_event(to_frame(time), tuple(position))

            # Go to direction
            time += to_second(1)
            position += delta_position * 2
            drone.add_position_event(to_frame(time), tuple(position))

            # Switch color to red to indicate when to kill the drone
            time += get_time_to_horizontal_distance(DISTANCE * 2) / 2
            drone.add_color_event(to_frame(time), (1, 0, 0, 0))

            time += get_time_to_horizontal_distance(DISTANCE * 2) / 2
            drone.add_position_event(to_frame(time), tuple(position))

            show_user.physic_parameters = IOSTAR_PHYSIC_PARAMETERS_MAX
            report = GlobalReport.generate(show_user)
            if len(report):
                print(report.summarize().model_dump_json(indent=4))  # noqa: T201

            iostar_json_gcs = IostarJsonGcs.from_show_user(show_user)
            dance_path = Path(f"crash_test_{altitude}_alt_{direction}.json")
            dance_path.write_text(iostar_json_gcs.model_dump_json())
