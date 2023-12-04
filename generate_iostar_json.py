from pathlib import Path

from loader.schemas import IostarJsonGcs
from loader.schemas.matrix import get_matrix
from loader.schemas.show_user.generate_show_user import ShowUserConfiguration, get_valid_show_user
from tests.test_editor import VALID_SHOW_CONFIGURATION


def main() -> None:
    valid_show_user = get_valid_show_user(VALID_SHOW_CONFIGURATION)
    valid_show_user.scale = 2

    collision_show_user = get_valid_show_user(
        ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2), step=1.25),
    )

    performance_show_user = get_valid_show_user(
        ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2), step=2),
    )
    for drone_user in performance_show_user.drones_user:
        x, y, _ = drone_user.position_events[-1].xyz
        drone_user.add_position_event(1000, (x, y, 6.0))

    dance_size_show_user = get_valid_show_user(
        ShowUserConfiguration(matrix=get_matrix(nb_x=1, nb_y=1), step=2),
    )
    for drone_user in dance_size_show_user.drones_user:
        xyz = drone_user.position_events[-1].xyz
        for i in range(12500):
            drone_user.add_position_event(1000 + i, xyz)

    for name, show_user in [
        ("valid", valid_show_user),
        ("collision", collision_show_user),
        ("performance", performance_show_user),
        ("dance_size", dance_size_show_user),
    ]:
        iostar_json_gcs = IostarJsonGcs.from_show_user(show_user)
        Path(f"iostar_json_gcs_{name}.json").write_text(iostar_json_gcs.model_dump_json() + "\n")


if __name__ == "__main__":
    main()
