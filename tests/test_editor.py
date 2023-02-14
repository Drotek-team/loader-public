from pathlib import Path

import pytest
from loader import (
    IostarJsonGcs,
    Metric,
    MetricRange,
    convert_iostar_json_gcs_string_to_show_user,
    convert_show_user_to_iostar_json_gcs,
    create_empty_show_user,
    create_show_simulation,
    generate_report_from_iostar_json_gcs_string,
    generate_report_from_show_user,
    generate_report_summary_from_iostar_json_gcs_string,
    generate_report_summary_from_show_user,
    get_collision_infractions,
    get_dance_size_infractions,
    get_performance_infractions,
    get_show_configuration_from_iostar_json_gcs_string,
    get_verified_iostar_json_gcs,
    su_to_ss,
)
from loader.show_env.migration_sp_ijg.su_to_ijg import su_to_ijg
from loader.show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)


def test_create_show_user_standard_case() -> None:
    drone_number = 5
    show_user = create_empty_show_user(drone_number)
    assert len(show_user) == drone_number
    for drone_index in range(drone_number):
        assert len(show_user[drone_index].position_events) == 0
        assert len(show_user[drone_index].color_events) == 0
        assert len(show_user[drone_index].fire_events) == 0


def test_create_show_simulation_standard_user_case() -> None:
    show_simulation = create_show_simulation(
        frame_start=10,
        frame_end=13,
        drone_indices=[2, 4, 5],
        frames_positions=[
            [(1.0, 0.0, 0.0), (1.0, 1.0, 1.0), (2.0, 2.0, 2.0)],
            [(3.0, 3.0, 3.0), (0.0, 2.0, 0.0), (5.0, 5.0, 0.0)],
            [(6.0, 6.0, 6.0), (7.0, 7.0, 7.0), (1.0, 0.0, 0.0)],
        ],
    )
    first_show_simulation_slice = show_simulation.show_slices[0]
    assert first_show_simulation_slice.frame == 10
    assert list(first_show_simulation_slice.on_ground_indices) == [2]
    assert list(first_show_simulation_slice.in_air_indices) == [4, 5]
    assert tuple(first_show_simulation_slice.on_ground_positions[0]) == (1.0, 0.0, 0.0)
    assert tuple(first_show_simulation_slice.in_air_positions[0]) == (1.0, 1.0, 1.0)
    assert tuple(first_show_simulation_slice.in_air_positions[1]) == (2.0, 2.0, 2.0)

    second_show_simulation_slice = show_simulation.show_slices[1]
    assert second_show_simulation_slice.frame == 11
    assert list(second_show_simulation_slice.on_ground_indices) == [4, 5]
    assert list(second_show_simulation_slice.in_air_indices) == [2]
    assert tuple(second_show_simulation_slice.on_ground_positions[0]) == (0.0, 2.0, 0.0)
    assert tuple(second_show_simulation_slice.on_ground_positions[1]) == (5.0, 5.0, 0.0)
    assert tuple(second_show_simulation_slice.in_air_positions[0]) == (3.0, 3.0, 3.0)

    third_show_simulation_slice = show_simulation.show_slices[2]
    assert third_show_simulation_slice.frame == 12
    assert list(third_show_simulation_slice.on_ground_indices) == [5]
    assert list(third_show_simulation_slice.in_air_indices) == [2, 4]
    assert tuple(third_show_simulation_slice.on_ground_positions[0]) == (1.0, 0.0, 0.0)
    assert tuple(third_show_simulation_slice.in_air_positions[0]) == (6.0, 6.0, 6.0)
    assert tuple(third_show_simulation_slice.in_air_positions[1]) == (7.0, 7.0, 7.0)


def test_create_show_simulation_frame_start_superior_or_equal_to_frame_end() -> None:
    frame_start = 0
    frame_end = 0
    with pytest.raises(
        ValueError,
        match=f"frame_start must be strictly smaller than frame_end, not {frame_start} and {frame_end}",
    ):
        create_show_simulation(frame_start, frame_end, [], [[]])


def test_create_show_simulation_incoherence_frame_start_end_and_frame_positions() -> (
    None
):
    frame_start = 0
    frame_end = 2
    frames_positions = [[(1.0, 1.0, 1.0)]]
    with pytest.raises(
        ValueError,
        match=f"frame_end - frame_start must be equal to the length of frames_positions, "
        f"not {frame_end - frame_start} and {len(frames_positions)}",
    ):
        create_show_simulation(frame_start, frame_end, [], frames_positions)


def test_create_show_simulation_incoherence_frame_indices_and_frame_positions() -> None:
    frame_start = 0
    frame_end = 1
    frame_indices = [0, 1]
    frames_positions = [[(1.0, 1.0, 1.0)]]
    with pytest.raises(
        ValueError,
        match="drone_indices and frames_positions items must have the same length",
    ):
        create_show_simulation(frame_start, frame_end, frame_indices, frames_positions)


def test_get_performance_infractions() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration())
    assert len(get_performance_infractions(show_user, {})) == 0
    assert (
        len(
            get_performance_infractions(
                show_user,
                {
                    Metric.VERTICAL_POSITION: MetricRange(
                        threshold=1.5,
                        standard_convention=False,
                    ),
                },
            ),
        )
        != 0
    )

    assert len(get_performance_infractions(show_user, {})) == 0


def test_get_collisions() -> None:
    show_simulation = su_to_ss(
        get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2)),
    )
    assert get_collision_infractions(show_simulation) == []


def test_get_dance_size_report() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    assert len(get_dance_size_infractions(show_user)) == 0


def test_get_drotek_check_from_show_user_standard_case() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    assert generate_report_from_show_user(show_user).dict() == {
        "show_user": None,
        "show_px4": None,
        "performance": None,
        "collision": None,
    }


def test_generate_report_summary_from_show_user_standard_case() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    assert generate_report_summary_from_show_user(show_user).dict() == {
        "show_user": 0,
        "show_px4": 0,
        "performance": 0,
        "collision": 0,
    }


def test_global_check_iostar_json_gcs() -> None:
    iostar_json_gcs_string = su_to_ijg(
        get_valid_show_user(ShowUserConfiguration()),
    ).json()
    assert generate_report_from_iostar_json_gcs_string(
        iostar_json_gcs_string,
    ).dict() == {
        "show_user": None,
        "show_px4": None,
        "performance": None,
        "collision": None,
    }


def test_get_drotek_check_summary_from_iostar_json_gcs_string_standard_case() -> None:
    iostar_json_gcs_string = su_to_ijg(
        get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2)),
    ).json()
    assert generate_report_summary_from_iostar_json_gcs_string(
        iostar_json_gcs_string,
    ).dict() == {
        "show_user": 0,
        "show_px4": 0,
        "performance": 0,
        "collision": 0,
    }


def test_get_show_configuration_from_iostar_json_gcs_string() -> None:
    iostar_json_gcs_string = su_to_ijg(
        get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=3)),
    ).json()
    assert get_show_configuration_from_iostar_json_gcs_string(
        iostar_json_gcs_string,
    ).dict() == {
        "nb_x": 2,
        "nb_y": 3,
        "nb_drone_per_family": 1,
        "step": 100,
        "angle_takeoff": 0,
        "duration": 42541,
        "hull": [(100, -50), (0, -50), (-100, 50), (100, 50)],
        "altitude_range": (-100, 0),
    }


# WARNING: this test is fondamental as it is the only one which proves that the loader is compatible with px4 and the gcs
def test_convert_show_user_to_iostar_json_gcs_standard_case() -> None:
    iostar_json_gcs_string = convert_show_user_to_iostar_json_gcs(
        get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2, step=2.0)),
    )
    with (Path() / "iostar_json_gcs_reference.json").open() as f:
        assert iostar_json_gcs_string == IostarJsonGcs.parse_raw(f.read())


def test_convert_iostar_json_gcs_string_to_show_user() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration())
    iostar_json_gcs_string = su_to_ijg(show_user).json()
    assert (
        convert_iostar_json_gcs_string_to_show_user(iostar_json_gcs_string) == show_user
    )


def test_get_verified_iostar_json_gcs() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration())
    iostar_json_gcs = su_to_ijg(show_user)
    assert get_verified_iostar_json_gcs(iostar_json_gcs.json()) == iostar_json_gcs
