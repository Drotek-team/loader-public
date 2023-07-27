from pathlib import Path

import numpy as np
from loader.parameters import FRAME_PARAMETERS, IOSTAR_PHYSIC_PARAMETERS_MAX
from loader.reports import GlobalReport
from loader.schemas import IostarJsonGcs, ShowUser
from tqdm import tqdm

DURATION = 2.3 * 60 * 60
MAX_SPEEP = 5
RADIUS = 2
ALTITUDE = 2
ALT_OSCILLATION = 1
NB_POINTS_ON_CIRCLE = 3
CIRCLE_REVOLUTION_TIME = 2 * np.pi * RADIUS / MAX_SPEEP


def to_frame(time: float) -> int:
    return FRAME_PARAMETERS.from_second_to_frame(time)


if __name__ == "__main__":
    show_user = ShowUser.create(nb_drones=1, angle_takeoff=0, step=1)

    drone = show_user.drones_user[0]

    time = 0
    position = np.zeros(3)
    drone.add_position_event(time, tuple(position))
    drone.add_color_event(time, (0, 0, 0, 1))

    time = 10
    position[2] = 2
    drone.add_position_event(to_frame(time), tuple(position))

    for _ in tqdm(
        range(round(DURATION / CIRCLE_REVOLUTION_TIME)),
        desc="Draw circles",
        unit="circle",
    ):
        for angle in tqdm(
            np.linspace(0, 2 * np.pi, NB_POINTS_ON_CIRCLE, endpoint=False),
            desc="Draw circle",
            unit="point",
            leave=False,
        ):
            time += CIRCLE_REVOLUTION_TIME / NB_POINTS_ON_CIRCLE
            x = RADIUS * np.cos(angle)
            y = RADIUS * np.sin(angle)
            z = ALT_OSCILLATION * np.sin(angle) + ALTITUDE
            position = np.array([x, y, z])
            drone.add_position_event(to_frame(time), tuple(position))

    report = GlobalReport.generate(show_user, physic_parameters=IOSTAR_PHYSIC_PARAMETERS_MAX)
    if len(report):
        print(report.summarize().model_dump_json(indent=4))  # noqa: T201

    iostar_json_gcs = IostarJsonGcs.from_show_user(show_user)
    dance_path = Path("circle_test.json")
    dance_path.write_text(iostar_json_gcs.model_dump_json())
