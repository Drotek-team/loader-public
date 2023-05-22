from loader.schemas.iostar_json_gcs.show_configuration import ShowConfiguration


def test_show_configuration___eq___standard_case() -> None:
    show_configuration = ShowConfiguration(
        nb_x=1,
        nb_y=1,
        nb_drone_per_family=1,
        step=1,
        angle_takeoff=1,
        duration=1,
        hull=[],
        altitude_range=(1, 2),
    )
    assert show_configuration == show_configuration


def test_show_configuration___eq___different_nb_x() -> None:
    show_configuration = ShowConfiguration(
        nb_x=1,
        nb_y=1,
        nb_drone_per_family=1,
        step=1,
        angle_takeoff=1,
        duration=1,
        hull=[],
        altitude_range=(1, 2),
    )
    assert show_configuration != ShowConfiguration(
        nb_x=2,
        nb_y=1,
        nb_drone_per_family=1,
        step=1,
        angle_takeoff=1,
        duration=1,
        hull=[],
        altitude_range=(1, 2),
    )
    assert show_configuration != ShowConfiguration(
        nb_x=1,
        nb_y=2,
        nb_drone_per_family=1,
        step=1,
        angle_takeoff=1,
        duration=1,
        hull=[],
        altitude_range=(1, 2),
    )


def test_show_configuration___eq___with_other_type() -> None:
    show_configuration = ShowConfiguration(
        nb_x=1,
        nb_y=1,
        nb_drone_per_family=1,
        step=1,
        angle_takeoff=1,
        duration=1,
        hull=[],
        altitude_range=(1, 2),
    )
    assert show_configuration != 1
