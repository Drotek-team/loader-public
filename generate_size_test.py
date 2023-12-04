import struct
from pathlib import Path

import numpy as np
from loader.parameters import FRAME_PARAMETERS, IOSTAR_PHYSIC_PARAMETERS_MAX
from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS, MagicNumber
from loader.reports import GlobalReport
from loader.schemas import IostarJsonGcs, ShowUser
from tqdm import tqdm

MAX_SIZE = 233472
ANGLE = np.deg2rad(21)
NB_X = 5
NB_Y = 1
STEP = 2

DURATION = 6 * 60 * 60
TAKEOFF_ALTITUDE = 1
TAKEOFF_DURATION = 10

NB_FRAMES = (
    (
        MAX_SIZE
        - struct.calcsize(JSON_BINARY_PARAMETERS.fmt_header)
        - struct.calcsize(JSON_BINARY_PARAMETERS.fmt_section_header) * 2
        - struct.calcsize(
            JSON_BINARY_PARAMETERS.position_event_format(MagicNumber.v2),
        )
        * 2
    )
    // (
        struct.calcsize(JSON_BINARY_PARAMETERS.position_event_format(MagicNumber.v2))
        + struct.calcsize(JSON_BINARY_PARAMETERS.color_event_format(MagicNumber.v2)) * 6
    )
    * 6
)
positions = (
    np.array([[x, y, 0] for y in range(NB_Y) for x in range(NB_X)])
    - np.array([(NB_X - 1) / 2, (NB_Y - 1) / 2, 0])
) * STEP
positions = positions @ np.array(
    [[np.cos(ANGLE), np.sin(ANGLE), 0], [-np.sin(ANGLE), np.cos(ANGLE), 0], [0, 0, 1]],
)


def to_frame(time: float) -> int:
    return FRAME_PARAMETERS.from_second_to_frame(time)


if __name__ == "__main__":
    show_user = ShowUser.create(nb_drones=NB_X * NB_Y, angle_takeoff=ANGLE, step=STEP)

    for drone, position in tqdm(
        zip(show_user.drones_user, positions),
        desc="Generating events",
        total=NB_X * NB_Y,
        unit="drone",
    ):
        frame = 0
        drone.add_position_event(frame, position)

        frame += to_frame(TAKEOFF_DURATION)
        position[2] = TAKEOFF_ALTITUDE
        drone.add_position_event(frame, position)

        for _ in range(NB_FRAMES):
            frame += 1
            if frame % 6 == 0:
                drone.add_position_event(
                    frame,
                    position,
                )
            drone.add_color_event(
                frame,
                np.random.random(4),  # pyright: ignore[reportGeneralTypeIssues]
            )

    show_user.physic_parameters = IOSTAR_PHYSIC_PARAMETERS_MAX
    report = GlobalReport.generate(show_user)
    if len(report):
        print(report.summarize().model_dump_json(indent=4))  # noqa: T201

    iostar_json_gcs = IostarJsonGcs.from_show_user(show_user)
    dance_path = Path("size_test.json")
    dance_path.write_text(iostar_json_gcs.model_dump_json())
