import numpy as np
import pytest
from loader.parameters import LandType, MagicNumber
from loader.schemas.matrix import get_matrix
from loader.schemas.show_user import ColorEventUser, DroneUser, PositionEventUser
from loader.schemas.show_user.generate_show_user import ShowUserConfiguration, get_valid_show_user


@pytest.fixture
def empty_drone_user() -> DroneUser:
    return DroneUser(index=0, position_events=[], color_events=[], fire_events=[], yaw_events=[])


def test_position_event_user_standard_case(empty_drone_user: DroneUser) -> None:
    empty_drone_user.add_position_event(
        frame=1,
        xyz=(1.0, 2.0, 3.0),
    )
    empty_drone_user.add_yaw_event(1, 90)
    assert empty_drone_user.position_events[0].frame == 1
    assert empty_drone_user.position_events[0].xyz == (1.0, 2.0, 3.0)
    empty_drone_user.apply_horizontal_rotation(np.pi / 2)
    np.testing.assert_allclose(
        np.array(empty_drone_user.position_events[0].xyz),
        np.array((-2.0, 1.0, 3.0)),
    )
    assert empty_drone_user.yaw_events[0].frame == 1
    assert empty_drone_user.yaw_events[0].angle == 180


def test_color_event_user_standard_case(empty_drone_user: DroneUser) -> None:
    empty_drone_user.add_color_event(
        frame=1,
        rgbw=(1.0, 2.0, 3.0, 4.0),
    )
    assert empty_drone_user.color_events[0].frame == 1
    assert empty_drone_user.color_events[0].rgbw == (1.0, 2.0, 3.0, 4.0)


def test_fire_event_user_standard_case(empty_drone_user: DroneUser) -> None:
    empty_drone_user.add_fire_event(frame=1, channel=0, duration=2)
    assert empty_drone_user.fire_events[0].frame == 1
    assert empty_drone_user.fire_events[0].channel == 0
    assert empty_drone_user.fire_events[0].duration == 2


def test_show_user_nb_drones_standard_case() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration())
    assert show_user.nb_drones == 1
    show_user = get_valid_show_user(
        ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=3, nb_drones_per_family=4)),
    )
    assert show_user.nb_drones == 2 * 3 * 4
    assert [drone_user.index for drone_user in show_user.drones_user] == list(
        range(show_user.nb_drones),
    )


def test_show_user_last_frame_standard_case() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration())
    assert show_user.last_frame == 1021
    show_user = get_valid_show_user(
        ShowUserConfiguration(show_duration_absolute_time=60),
    )
    assert show_user.last_frame == 1741


def test_show_user_duration_standard_case() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration())
    assert show_user.duration == 42.541666666666664
    show_user = get_valid_show_user(
        ShowUserConfiguration(show_duration_absolute_time=60),
    )
    assert show_user.duration == 72.54166666666667


def test_show_user_convex_hull_standard_case() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration())
    assert show_user.convex_hull == [(0.0, 0.0)]
    show_user = get_valid_show_user(
        ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2), step_x=2.0, step_y=2.0),
    )
    assert show_user.convex_hull == [(-1.0, -1.0), (1.0, -1.0), (1.0, 1.0), (-1.0, 1.0)]


def test_show_user_altitude_range_standard_case() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration())
    assert show_user.altitude_range == (0.0, 1.0)


@pytest.mark.parametrize(
    "show_duration_absolute_time",
    [0, -1, -2, -3],
)
def test_show_user_configuration_show_duration_absolute_time_must_be_strictly_positive(
    show_duration_absolute_time: int,
) -> None:
    with pytest.raises(
        ValueError,
        match=f"Show duration must be stricly positive, not {show_duration_absolute_time}",
    ):
        ShowUserConfiguration(
            show_duration_absolute_time=show_duration_absolute_time,
        )


@pytest.mark.parametrize(
    "takeoff_altitude",
    [-1, 0, 21, 50],
)
def test_show_user_configuration_takeoff_altitude_must_be_in_range(
    takeoff_altitude: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="Takeoff altitude must be between",
    ):
        ShowUserConfiguration(takeoff_altitude=takeoff_altitude)


@pytest.mark.parametrize(
    "duration_before_takeoff",
    [-1, -2, -3],
)
def test_show_user_configuration_duration_before_takeoff_must_be_positive(
    duration_before_takeoff: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="Duration before takeoff must be positive",
    ):
        ShowUserConfiguration(duration_before_takeoff=duration_before_takeoff)


def test_show_user_configuration_apply_horizontal_rotation() -> None:
    show_user = get_valid_show_user(
        ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2), step_x=2.0, step_y=2.0),
    )
    show_user.angle_show = 0

    assert show_user.drones_user[0].position_events[0].xyz == (-1.0, -1.0, 0.0)
    assert show_user.drones_user[1].position_events[0].xyz == (1.0, -1.0, 0.0)
    assert show_user.drones_user[2].position_events[0].xyz == (-1.0, 1.0, 0.0)
    assert show_user.drones_user[3].position_events[0].xyz == (1.0, 1.0, 0.0)

    angle = np.pi / 2
    new_show_user = show_user.model_copy(deep=True)
    new_show_user.apply_horizontal_rotation(angle)

    np.testing.assert_allclose(
        new_show_user.drones_user[2].position_events[0].xyz,
        (-1.0, -1.0, 0.0),
    )
    np.testing.assert_allclose(
        new_show_user.drones_user[0].position_events[0].xyz,
        (1.0, -1.0, 0.0),
    )
    np.testing.assert_allclose(
        new_show_user.drones_user[3].position_events[0].xyz,
        (-1.0, 1.0, 0.0),
    )
    np.testing.assert_allclose(
        new_show_user.drones_user[1].position_events[0].xyz,
        (1.0, 1.0, 0.0),
    )

    np.testing.assert_allclose(
        np.array(show_user.convex_hull),
        np.array(new_show_user.convex_hull[-1:] + new_show_user.convex_hull[:-1]),
    )

    assert show_user.angle_takeoff + angle == new_show_user.angle_takeoff


def test_update_drones_user_indices_standard_case() -> None:
    show_user = get_valid_show_user(
        ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2), step_x=2.0, step_y=2.0),
    )
    assert [drone_user.index for drone_user in show_user.drones_user] == list(
        range(show_user.nb_drones),
    )
    new_indices = [3, 2, 1, 0]
    show_user.update_drones_user_indices(new_indices)
    assert [drone_user.index for drone_user in show_user.drones_user] == new_indices


def test_update_drones_user_indices_wrong_length() -> None:
    show_user = get_valid_show_user(
        ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2), step_x=2.0, step_y=2.0),
    )
    new_indices = [3, 2, 1]
    with pytest.raises(
        ValueError,
        match="New indices: 3 must have the same length as the number of drones: 4",
    ):
        show_user.update_drones_user_indices(new_indices)


def test_update_drones_user_indices_not_unique() -> None:
    show_user = get_valid_show_user(
        ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2), step_x=2.0, step_y=2.0),
    )
    new_indices = [3, 2, 1, 1]
    with pytest.raises(
        ValueError,
        match=" are not unique",
    ):
        show_user.update_drones_user_indices(new_indices)


def test_show_user___eq__() -> None:  # noqa: PLR0915
    show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    other_show_user = 1
    assert show_user != other_show_user

    other_show_user = show_user.model_copy()
    other_show_user.magic_number = MagicNumber.v2
    assert show_user != other_show_user

    show_user = get_valid_show_user(
        ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2), angle_takeoff=-np.pi / 2),
    )
    other_show_user = get_valid_show_user(
        ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2), angle_takeoff=np.pi / 4),
    )
    assert show_user != other_show_user

    show_user = get_valid_show_user(
        ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2), angle_takeoff=-np.pi / 2),
    )
    other_show_user = show_user.model_copy()
    other_show_user.angle_show = np.pi / 4
    assert show_user != other_show_user

    show_user = get_valid_show_user(
        ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2), step_x=2, step_y=2),
    )
    other_show_user = get_valid_show_user(
        ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2), step_x=1, step_y=1),
    )
    assert show_user != other_show_user

    show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    other_show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=1)))
    assert show_user != other_show_user

    show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    other_show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    other_show_user.drones_user = other_show_user.drones_user[::-1]
    assert show_user != other_show_user

    show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    other_show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    other_show_user.drones_user[0].add_position_event(frame=1, xyz=(1.0, 1.0, 1.0))
    assert show_user != other_show_user

    show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    show_user.drones_user[0].add_position_event(frame=1, xyz=(1.0, 1.0, 1.0))
    other_show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    other_show_user.drones_user[0].add_position_event(frame=2, xyz=(1.0, 1.0, 1.0))
    assert show_user != other_show_user

    show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    show_user.drones_user[0].add_position_event(frame=1, xyz=(1.0, 1.0, 1.0))
    other_show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    other_show_user.drones_user[0].add_position_event(frame=1, xyz=(0.0, 1.0, 1.0))
    assert show_user != other_show_user

    show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    show_user.drones_user[0].add_color_event(frame=1, rgbw=(1.0, 1.0, 1.0, 1.0))
    other_show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    assert show_user != other_show_user

    show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    show_user.drones_user[0].add_fire_event(frame=1, channel=1, duration=1)
    other_show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    assert show_user != other_show_user

    show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    show_user.drones_user[0].add_yaw_event(frame=1, angle=1)
    other_show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    assert show_user != other_show_user

    other_show_user = show_user.model_copy()
    other_show_user.scale = 2
    assert show_user != other_show_user

    other_show_user = show_user.model_copy()
    other_show_user.land_type = LandType.RTL
    assert show_user != other_show_user

    assert show_user == show_user  # noqa: PLR0124


XYZ1 = (1.0, 2.0, 3.0)
XYZ2 = (4.0, 5.0, 6.0)
XYZ3 = (7.0, 8.0, 9.0)


@pytest.mark.parametrize(
    "position_events,cleaned_position_events",
    [
        ([], []),
        (
            [PositionEventUser(frame=1, xyz=XYZ1)],
            [PositionEventUser(frame=1, xyz=XYZ1)],
        ),
        (
            [
                PositionEventUser(frame=1, xyz=XYZ1),
                PositionEventUser(frame=2, xyz=XYZ1),
            ],
            [
                PositionEventUser(frame=1, xyz=XYZ1),
                PositionEventUser(frame=2, xyz=XYZ1),
            ],
        ),
        (
            [
                PositionEventUser(frame=0, xyz=XYZ1),
                PositionEventUser(frame=1, xyz=XYZ1),
                PositionEventUser(frame=2, xyz=XYZ1),
            ],
            [
                PositionEventUser(frame=0, xyz=XYZ1),
                PositionEventUser(frame=2, xyz=XYZ1),
            ],
        ),
        (
            [
                PositionEventUser(frame=0, xyz=XYZ1),
                PositionEventUser(frame=1, xyz=XYZ1),
                PositionEventUser(frame=2, xyz=XYZ2),
            ],
            [
                PositionEventUser(frame=0, xyz=XYZ1),
                PositionEventUser(frame=1, xyz=XYZ1),
                PositionEventUser(frame=2, xyz=XYZ2),
            ],
        ),
        (
            [
                PositionEventUser(frame=0, xyz=XYZ1),
                PositionEventUser(frame=1, xyz=XYZ1),
                PositionEventUser(frame=2, xyz=XYZ1),
                PositionEventUser(frame=3, xyz=XYZ2),
            ],
            [
                PositionEventUser(frame=0, xyz=XYZ1),
                PositionEventUser(frame=2, xyz=XYZ1),
                PositionEventUser(frame=3, xyz=XYZ2),
            ],
        ),
        (
            [
                PositionEventUser(frame=0, xyz=XYZ1),
                PositionEventUser(frame=1, xyz=XYZ1),
                PositionEventUser(frame=2, xyz=XYZ1),
                PositionEventUser(frame=3, xyz=XYZ2),
                PositionEventUser(frame=4, xyz=XYZ2),
                PositionEventUser(frame=5, xyz=XYZ2),
                PositionEventUser(frame=6, xyz=XYZ3),
                PositionEventUser(frame=7, xyz=XYZ3),
                PositionEventUser(frame=8, xyz=XYZ3),
            ],
            [
                PositionEventUser(frame=0, xyz=XYZ1),
                PositionEventUser(frame=2, xyz=XYZ1),
                PositionEventUser(frame=3, xyz=XYZ2),
                PositionEventUser(frame=5, xyz=XYZ2),
                PositionEventUser(frame=6, xyz=XYZ3),
                PositionEventUser(frame=8, xyz=XYZ3),
            ],
        ),
    ],
)
def test_drone_user_clean_position_events(
    position_events: list[PositionEventUser], cleaned_position_events: list[PositionEventUser]
) -> None:
    drone_user = DroneUser(
        index=0, position_events=position_events, color_events=[], fire_events=[], yaw_events=[]
    )
    drone_user.clean_position_events()
    assert drone_user.position_events == cleaned_position_events


RGBW1 = (1.0, 2.0, 3.0, 0.1)
RGBW2 = (4.0, 5.0, 6.0, 0.2)
RGBW3 = (7.0, 8.0, 9.0, 0.3)


@pytest.mark.parametrize(
    "color_events,cleaned_color_events",
    [
        ([], []),
        (
            [ColorEventUser(frame=1, rgbw=RGBW1)],
            [ColorEventUser(frame=1, rgbw=RGBW1)],
        ),
        (
            [
                ColorEventUser(frame=1, rgbw=RGBW1),
                ColorEventUser(frame=2, rgbw=RGBW1),
            ],
            [
                ColorEventUser(frame=1, rgbw=RGBW1),
                ColorEventUser(frame=2, rgbw=RGBW1),
            ],
        ),
        (
            [
                ColorEventUser(frame=0, rgbw=RGBW1),
                ColorEventUser(frame=1, rgbw=RGBW1),
                ColorEventUser(frame=2, rgbw=RGBW1),
            ],
            [
                ColorEventUser(frame=0, rgbw=RGBW1),
                ColorEventUser(frame=2, rgbw=RGBW1),
            ],
        ),
        (
            [
                ColorEventUser(frame=0, rgbw=RGBW1),
                ColorEventUser(frame=1, rgbw=RGBW1),
                ColorEventUser(frame=2, rgbw=RGBW2),
            ],
            [
                ColorEventUser(frame=0, rgbw=RGBW1),
                ColorEventUser(frame=2, rgbw=RGBW2),
            ],
        ),
        (
            [
                ColorEventUser(frame=0, rgbw=RGBW1),
                ColorEventUser(frame=1, rgbw=RGBW1),
                ColorEventUser(frame=2, rgbw=RGBW1),
                ColorEventUser(frame=3, rgbw=RGBW2),
            ],
            [
                ColorEventUser(frame=0, rgbw=RGBW1),
                ColorEventUser(frame=3, rgbw=RGBW2),
            ],
        ),
        (
            [
                ColorEventUser(frame=0, rgbw=RGBW1),
                ColorEventUser(frame=1, rgbw=RGBW1),
                ColorEventUser(frame=2, rgbw=RGBW1),
                ColorEventUser(frame=3, rgbw=RGBW2),
                ColorEventUser(frame=4, rgbw=RGBW2),
                ColorEventUser(frame=5, rgbw=RGBW2),
                ColorEventUser(frame=6, rgbw=RGBW3),
                ColorEventUser(frame=7, rgbw=RGBW3),
                ColorEventUser(frame=8, rgbw=RGBW3),
            ],
            [
                ColorEventUser(frame=0, rgbw=RGBW1),
                ColorEventUser(frame=3, rgbw=RGBW2),
                ColorEventUser(frame=6, rgbw=RGBW3),
                ColorEventUser(frame=8, rgbw=RGBW3),
            ],
        ),
        (
            [
                ColorEventUser(frame=0, rgbw=RGBW1, interpolate=True),
                ColorEventUser(frame=1, rgbw=RGBW1),
                ColorEventUser(frame=2, rgbw=RGBW2),
            ],
            [
                ColorEventUser(frame=0, rgbw=RGBW1),
                ColorEventUser(frame=2, rgbw=RGBW2),
            ],
        ),
        (
            [
                ColorEventUser(frame=0, rgbw=RGBW1),
                ColorEventUser(frame=1, rgbw=RGBW1, interpolate=True),
                ColorEventUser(frame=2, rgbw=RGBW2),
            ],
            [
                ColorEventUser(frame=0, rgbw=RGBW1),
                ColorEventUser(frame=1, rgbw=RGBW1, interpolate=True),
                ColorEventUser(frame=2, rgbw=RGBW2),
            ],
        ),
        (
            [
                ColorEventUser(frame=0, rgbw=RGBW1, interpolate=True),
                ColorEventUser(frame=1, rgbw=RGBW1, interpolate=True),
                ColorEventUser(frame=2, rgbw=RGBW2),
            ],
            [
                ColorEventUser(frame=0, rgbw=RGBW1, interpolate=True),
                ColorEventUser(frame=1, rgbw=RGBW1, interpolate=True),
                ColorEventUser(frame=2, rgbw=RGBW2),
            ],
        ),
        (
            [
                ColorEventUser(frame=0, rgbw=RGBW1),
                ColorEventUser(frame=1, rgbw=RGBW1, interpolate=True),
                ColorEventUser(frame=2, rgbw=RGBW1),
                ColorEventUser(frame=3, rgbw=RGBW2),
            ],
            [
                ColorEventUser(frame=0, rgbw=RGBW1),
                ColorEventUser(frame=3, rgbw=RGBW2),
            ],
        ),
    ],
)
def test_drone_user_clean_color_events(
    color_events: list[ColorEventUser], cleaned_color_events: list[ColorEventUser]
) -> None:
    drone_user = DroneUser(
        index=0, position_events=[], color_events=color_events, fire_events=[], yaw_events=[]
    )
    drone_user.clean_color_events()
    assert drone_user.color_events == cleaned_color_events
