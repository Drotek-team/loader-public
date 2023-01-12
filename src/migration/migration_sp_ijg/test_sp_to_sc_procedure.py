import pytest

from show_px4.show_px4 import DronePx4, ShowPx4

from .sp_to_sc_procedure import sp_to_sc_procedure


@pytest.fixture
def valid_one_drone_show_px4():
    drone_px4 = DronePx4(0)
    drone_px4.add_position(0, (0, 0, 0))
    drone_px4.add_position(1000, (0, 0, -10))
    return ShowPx4([drone_px4])


def test_sp_to_sc_procedure_one_drone(valid_one_drone_show_px4: ShowPx4):
    show_configuration = sp_to_sc_procedure(valid_one_drone_show_px4)
    assert show_configuration.nb_x == 1
    assert show_configuration.nb_y == 1
    assert show_configuration.nb_drone_per_family == 1
    assert show_configuration.step == 0
    assert show_configuration.angle_takeoff == 0
    assert show_configuration.duration == 1000
    assert show_configuration.hull == [(0, 0)]
    assert show_configuration.altitude_range == (-10, 0)


@pytest.fixture
def valid_east_west_lign_drone_show_px4():
    first_drone_px4 = DronePx4(0)
    first_drone_px4.add_position(0, (-1, 0, 0))
    first_drone_px4.add_position(1000, (-1, 0, -10))

    second_drone_px4 = DronePx4(1)
    second_drone_px4.add_position(0, (1, 0, 0))
    second_drone_px4.add_position(1000, (1, 0, -10))
    return ShowPx4([first_drone_px4, second_drone_px4])

    # TODO: de manière générale le grid_angle_estimation est pas très lisible donc autant le refaire bien (virer le 90...)


def test_sp_to_sc_procedure_east_west_lign_drone(
    valid_east_west_lign_drone_show_px4: ShowPx4,
):
    show_configuration = sp_to_sc_procedure(valid_east_west_lign_drone_show_px4)
    assert show_configuration.nb_x == 1
    assert show_configuration.nb_y == 2
    assert show_configuration.nb_drone_per_family == 1
    assert show_configuration.step == 2.0
    assert show_configuration.angle_takeoff == 0
    assert show_configuration.duration == 1000
    assert show_configuration.hull == [(-1, 0), (1, 0)]
    assert show_configuration.altitude_range == (-10, 0)


@pytest.fixture
def valid_north_south_lign_drone_show_px4():
    first_drone_px4 = DronePx4(0)
    first_drone_px4.add_position(0, (0, -1, 0))
    first_drone_px4.add_position(1000, (0, -1, -10))

    second_drone_px4 = DronePx4(1)
    second_drone_px4.add_position(0, (0, 1, 0))
    second_drone_px4.add_position(1000, (0, 1, -10))
    return ShowPx4([first_drone_px4, second_drone_px4])

    # TODO: de manière générale le grid_angle_estimation est pas très lisible donc autant le refaire bien (virer le 90...)


def test_sp_to_sc_procedure_north_south_lign_drone_show_px4(
    valid_north_south_lign_drone_show_px4: ShowPx4,
):
    show_configuration = sp_to_sc_procedure(valid_north_south_lign_drone_show_px4)
    assert show_configuration.nb_x == 2
    assert show_configuration.nb_y == 1
    assert show_configuration.nb_drone_per_family == 1
    assert show_configuration.step == 2.0
    assert show_configuration.angle_takeoff == 0
    assert show_configuration.duration == 1000
    assert show_configuration.hull == [(0, 1), (0, -1)]
    assert show_configuration.altitude_range == (-10, 0)


@pytest.fixture
def valid_square_drone_show_px4():
    first_drone_px4 = DronePx4(0)
    first_drone_px4.add_position(0, (-1, -1, 0))
    first_drone_px4.add_position(1000, (-1, -1, -10))

    second_drone_px4 = DronePx4(1)
    second_drone_px4.add_position(0, (-1, 1, 0))
    second_drone_px4.add_position(1000, (1, -1, -10))

    thrid_drone_px4 = DronePx4(2)
    thrid_drone_px4.add_position(0, (1, -1, 0))
    thrid_drone_px4.add_position(1000, (-1, 1, -10))

    fourth_drone_px4 = DronePx4(3)
    fourth_drone_px4.add_position(0, (1, 1, 0))
    fourth_drone_px4.add_position(1000, (1, 1, -10))
    return ShowPx4(
        [first_drone_px4, second_drone_px4, thrid_drone_px4, fourth_drone_px4]
    )


def test_sp_to_sc_procedure_square(valid_square_drone_show_px4: ShowPx4):
    show_configuration = sp_to_sc_procedure(valid_square_drone_show_px4)
    assert show_configuration.nb_x == 2
    assert show_configuration.nb_y == 2
    assert show_configuration.nb_drone_per_family == 1
    assert abs(show_configuration.step - 2.0) < 1e-6
    assert show_configuration.angle_takeoff == 0
    assert show_configuration.duration == 1000
    assert show_configuration.hull == [(-1, 1), (-1, -1), (1, -1), (1, 1)]
    assert show_configuration.altitude_range == (-10, 0)
