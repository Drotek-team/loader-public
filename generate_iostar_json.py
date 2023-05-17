from pathlib import Path

from loader import su_to_ijg
from loader.show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)


# TODO(jonathan): Generate show with performance infractions and another with collisions to use in README.md
def main() -> None:
    valid_show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2, step=2))

    collision_show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2, step=1.25))

    performance_show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2, step=2))
    for drone_user in performance_show_user.drones_user:
        x, y, _ = drone_user.position_events[-1].xyz
        drone_user.add_position_event(1000, (x, y, 6.0))

    dance_size_show_user = get_valid_show_user(ShowUserConfiguration(nb_x=1, nb_y=1, step=2))
    for drone_user in dance_size_show_user.drones_user:
        xyz = drone_user.position_events[-1].xyz
        for i in range(10000):
            drone_user.add_position_event(1000 + 42 * i, xyz)

    for name, show_user in [
        ("valid", valid_show_user),
        ("collision", collision_show_user),
        ("performance", performance_show_user),
        ("dance_size", dance_size_show_user),
    ]:
        iostar_json_gcs = su_to_ijg(show_user)
        Path(f"iostar_json_gcs_{name}.json").write_text(iostar_json_gcs.json() + "\n")


if __name__ == "__main__":
    main()
