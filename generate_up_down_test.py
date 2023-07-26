from pathlib import Path

import numpy as np
from loader.parameters import FRAME_PARAMETERS, IOSTAR_PHYSIC_PARAMETERS_MAX
from loader.reports import GlobalReport
from loader.schemas import IostarJsonGcs, ShowUser

DURATION = 0.69 * 60 * 60
TAKEOFF_ALTITUDE = 1
TAKEOFF_DURATION = 10
ACCELERATION = 1.0
EVENT_TIME_STEP = 1 / 4
MAX_ALTITUDE = 5
HALF_OSCILLATION_DURATION = np.sqrt((MAX_ALTITUDE - TAKEOFF_ALTITUDE) / ACCELERATION)


def to_frame(time: float) -> int:
    return FRAME_PARAMETERS.from_second_to_frame(time)


def calculate_altitude(time: float) -> float:
    """Calculate the altitude at a given time.

    The drone is supposed to oscillate between TAKEOFF_ALTITUDE and MAX_ALTITUDE.
    With a constant acceleration of ACCELERATION.
    During the first half of the ascent, the drone accelerates.
    During the second half of the ascent, the drone decelerates.
    During the first half of the descent, the drone accelerates.
    During the second half of the descent, the drone decelerates.
    """
    time -= TAKEOFF_DURATION
    time = time % (4 * HALF_OSCILLATION_DURATION)
    if time < HALF_OSCILLATION_DURATION:
        return TAKEOFF_ALTITUDE + ACCELERATION * time**2 / 2
    if time < 2 * HALF_OSCILLATION_DURATION:
        time = 2 * HALF_OSCILLATION_DURATION - time
        return MAX_ALTITUDE - ACCELERATION * time**2 / 2
    if time < 3 * HALF_OSCILLATION_DURATION:
        time -= 2 * HALF_OSCILLATION_DURATION
        return MAX_ALTITUDE - ACCELERATION * time**2 / 2
    time = 4 * HALF_OSCILLATION_DURATION - time
    return TAKEOFF_ALTITUDE + ACCELERATION * time**2 / 2


show_user = ShowUser.create(nb_drones=1, angle_takeoff=0, step=1)

drone = show_user.drones_user[0]

time = 0
position = np.zeros(3)
drone.add_position_event(time, tuple(position))
drone.add_color_event(time, (1, 1, 1, 1))

for time in np.arange(  # pyright: ignore[reportUnknownMemberType]
    TAKEOFF_DURATION,
    DURATION,
    EVENT_TIME_STEP,
):
    position[2] = calculate_altitude(time)
    drone.add_position_event(to_frame(time), tuple(position))

report = GlobalReport.generate(show_user, physic_parameters=IOSTAR_PHYSIC_PARAMETERS_MAX)
if len(report):
    print(report.summarize().model_dump_json(indent=4))  # noqa: T201

iostar_json_gcs = IostarJsonGcs.from_show_user(show_user)
dance_path = Path("up_down_test.json")
dance_path.write_text(iostar_json_gcs.model_dump_json())
