from pathlib import Path

import numpy as np
from loader.parameters import FRAME_PARAMETERS
from loader.reports import GlobalReport
from loader.schemas import IostarJsonGcs, ShowUser

DURATION = 60
TAKEOFF_ALTITUDE = 1
TAKEOFF_DURATION = 10
COLOR_DELTA_TIME = 2


def to_frame(time: float) -> int:
    return FRAME_PARAMETERS.from_second_to_frame(time)


if __name__ == "__main__":
    show_user = ShowUser.create(nb_drones=1, angle_takeoff=0, step=1)

    drone = show_user.drones_user[0]

    time = 0
    position = np.zeros(3)
    drone.add_position_event(to_frame(time), position)  # pyright: ignore[reportGeneralTypeIssues]

    time += TAKEOFF_DURATION
    position[2] = TAKEOFF_ALTITUDE
    drone.add_position_event(to_frame(time), position)  # pyright: ignore[reportGeneralTypeIssues]
    drone.add_color_event(to_frame(time), (1, 0, 0, 0), interpolate=True)

    time += COLOR_DELTA_TIME
    drone.add_color_event(to_frame(time), (0, 1, 0, 0), interpolate=True)

    time += COLOR_DELTA_TIME
    drone.add_color_event(to_frame(time), (0, 0, 1, 0), interpolate=True)

    time += COLOR_DELTA_TIME
    drone.add_color_event(to_frame(time), (0, 0, 0, 1), interpolate=True)

    time += COLOR_DELTA_TIME
    drone.add_color_event(to_frame(time), (1, 0, 0, 0), interpolate=True)
    drone.add_position_event(to_frame(time), position)  # pyright: ignore[reportGeneralTypeIssues]

    report = GlobalReport.generate(show_user)
    if len(report):
        print(report.summarize().model_dump_json(indent=4))  # noqa: T201

    iostar_json_gcs = IostarJsonGcs.from_show_user(show_user)
    dance_path = Path("color_interpolation.json")
    dance_path.write_text(iostar_json_gcs.model_dump_json())
