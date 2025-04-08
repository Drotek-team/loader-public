from pathlib import Path

from loader.schemas.iostar_json_gcs.iostar_json_gcs import IostarJsonGcs
from loader.schemas.show_user.show_user import ShowUser

FPS = 24


def main() -> None:
    show_user = ShowUser.create(nb_drones=1, angle_takeoff=21, step_x=1.5, step_y=1.5)
    drone_user = show_user.drones_user[0]

    time = 0
    position = (0, 0, 0)
    drone_user.add_position_event(time, position)
    time += 10 * FPS
    position = (0, 0, 1)
    drone_user.add_position_event(time, position)
    time += 5 * FPS
    position = (-5, -5, 5)
    drone_user.add_position_event(time, position)
    time += 5 * FPS
    position = (5, -5, 5)
    drone_user.add_position_event(time, position)
    time += 5 * FPS
    position = (5, 5, 5)
    drone_user.add_position_event(time, position)
    time += 5 * FPS
    position = (-5, 5, 5)
    drone_user.add_position_event(time, position)
    time += 5 * FPS
    position = (0, 0, 2)
    drone_user.add_position_event(time, position)
    time += 5 * FPS
    position = (0, 0, 2)
    drone_user.add_position_event(time, position)
    time += 5 * FPS
    position = (0, 0, 1)
    drone_user.add_position_event(time, position)
    time += 10 * FPS
    position = (0, 0, -1)
    drone_user.add_position_event(time, position)

    iostar_json_gcs = IostarJsonGcs.from_show_user(show_user)
    Path("test_precision_landing_v2.json").write_text(iostar_json_gcs.model_dump_json())


if __name__ == "__main__":
    main()
