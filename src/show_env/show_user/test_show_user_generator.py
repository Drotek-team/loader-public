import math

from .show_user_generator import get_valid_show_user


def test_get_valid_show_user_nb_x_nb_y_variation():
    nb_x = 1
    nb_y = 1
    show_user = get_valid_show_user(nb_x=nb_x, nb_y=nb_y)
    assert len(show_user.drones_user) == 1
    assert show_user.drones_user[0].position_events[0].xyz == (
        0.0,
        0.0,
        0.0,
    )
    nb_x = 2
    nb_y = 2
    show_user = get_valid_show_user(nb_x=nb_x, nb_y=nb_y)
    assert len(show_user.drones_user) == 4
    assert show_user.drones_user[0].position_events[0].xyz == (
        -0.75,
        -0.75,
        0.0,
    )
    assert show_user.drones_user[1].position_events[0].xyz == (
        0.75,
        -0.75,
        0.0,
    )
    assert show_user.drones_user[2].position_events[0].xyz == (
        -0.75,
        0.75,
        0.0,
    )
    assert show_user.drones_user[3].position_events[0].xyz == (
        0.75,
        0.75,
        0.0,
    )


def test_get_valid_show_user_angle_variation():
    nb_x = 2
    nb_y = 2
    show_user = get_valid_show_user(nb_x=nb_x, nb_y=nb_y)
    assert len(show_user.drones_user) == 4
    assert show_user.drones_user[0].position_events[0].xyz == (
        -0.75,
        -0.75,
        0.0,
    )
    assert show_user.drones_user[1].position_events[0].xyz == (
        0.75,
        -0.75,
        0.0,
    )
    assert show_user.drones_user[2].position_events[0].xyz == (
        -0.75,
        0.75,
        0.0,
    )
    assert show_user.drones_user[3].position_events[0].xyz == (
        0.75,
        0.75,
        0.0,
    )
    show_user = get_valid_show_user(
        nb_x=nb_x, nb_y=nb_y, angle_takeoff=math.radians(90)
    )
    assert len(show_user.drones_user) == 4
    assert show_user.drones_user[0].position_events[0].xyz == (
        0.75,
        -0.75,
        0.0,
    )
    assert show_user.drones_user[1].position_events[0].xyz == (
        0.75,
        0.75,
        0.0,
    )
    assert show_user.drones_user[2].position_events[0].xyz == (
        -0.75,
        -0.75,
        0.0,
    )
    assert show_user.drones_user[3].position_events[0].xyz == (
        -0.75,
        0.75,
        0.0,
    )
