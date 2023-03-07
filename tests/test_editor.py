from pathlib import Path
from typing import List, Tuple

import pytest
from loader import (
    IostarJsonGcs,
    PerformanceKind,
    PerformanceRange,
    convert_iostar_json_gcs_string_to_show_user,
    convert_show_user_to_iostar_json_gcs,
    create_empty_show_user,
    create_show_position_frames_from_frames_positions,
    create_show_position_frames_from_show_user,
    generate_report_from_iostar_json_gcs_string,
    generate_report_from_show_user,
    get_collision_infractions,
    get_dance_size_infractions,
    get_performance_infractions,
    get_show_configuration_from_iostar_json_gcs_string,
    get_verified_iostar_json_gcs,
)
from loader.editor import DanceSizeInformation, ReportError, get_dance_size_informations
from loader.show_env.migration_sp_ijg.su_to_ijg import su_to_ijg
from loader.show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)


def test_create_show_user_standard_case() -> None:
    nb_drones = 5
    show_user = create_empty_show_user(nb_drones)
    assert len(show_user) == nb_drones
    for drone_index in range(nb_drones):
        assert len(show_user[drone_index].position_events) == 0
        assert len(show_user[drone_index].color_events) == 0
        assert len(show_user[drone_index].fire_events) == 0


@pytest.mark.parametrize("nb_drones", [0, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10])
def test_create_show_user_invalid_nb_drones(nb_drones: int) -> None:
    with pytest.raises(
        ValueError,
        match=f"nb_drones must be positive, not {nb_drones}",
    ):
        create_empty_show_user(nb_drones)


def test_create_show_position_frames_standard_user_case() -> None:
    show_position_frames = create_show_position_frames_from_frames_positions(
        frame_start=10,
        frame_end=13,
        drone_indices=[2, 4, 5],
        frames_positions=[
            [(1.0, 0.0, 0.0), (1.0, 1.0, 1.0), (2.0, 2.0, 2.0)],
            [(3.0, 3.0, 3.0), (0.0, 2.0, 0.0), (5.0, 5.0, 0.0)],
            [(6.0, 6.0, 6.0), (7.0, 7.0, 7.0), (1.0, 0.0, 0.0)],
        ],
    )
    first_show_position_frame = show_position_frames.show_position_frames[0]
    assert first_show_position_frame.frame == 10
    assert list(first_show_position_frame.on_ground_indices) == [2]
    assert list(first_show_position_frame.in_air_indices) == [4, 5]
    assert tuple(first_show_position_frame.on_ground_positions[0]) == (1.0, 0.0, 0.0)
    assert tuple(first_show_position_frame.in_air_positions[0]) == (1.0, 1.0, 1.0)
    assert tuple(first_show_position_frame.in_air_positions[1]) == (2.0, 2.0, 2.0)

    second_show_position_frame = show_position_frames.show_position_frames[1]
    assert second_show_position_frame.frame == 11
    assert list(second_show_position_frame.on_ground_indices) == [4, 5]
    assert list(second_show_position_frame.in_air_indices) == [2]
    assert tuple(second_show_position_frame.on_ground_positions[0]) == (0.0, 2.0, 0.0)
    assert tuple(second_show_position_frame.on_ground_positions[1]) == (5.0, 5.0, 0.0)
    assert tuple(second_show_position_frame.in_air_positions[0]) == (3.0, 3.0, 3.0)

    third_show_position_frame = show_position_frames.show_position_frames[2]
    assert third_show_position_frame.frame == 12
    assert list(third_show_position_frame.on_ground_indices) == [5]
    assert list(third_show_position_frame.in_air_indices) == [2, 4]
    assert tuple(third_show_position_frame.on_ground_positions[0]) == (1.0, 0.0, 0.0)
    assert tuple(third_show_position_frame.in_air_positions[0]) == (6.0, 6.0, 6.0)
    assert tuple(third_show_position_frame.in_air_positions[1]) == (7.0, 7.0, 7.0)


def test_create_show_position_frames_frame_start_superior_or_equal_to_frame_end() -> (
    None
):
    frame_start = 0
    frame_end = 0
    with pytest.raises(
        ValueError,
        match=f"frame_start must be strictly smaller than frame_end, not {frame_start} and {frame_end}",
    ):
        create_show_position_frames_from_frames_positions(
            frame_start,
            frame_end,
            [],
            [[]],
        )


def test_create_show_position_frames_incoherence_frame_start_end_and_frame_positions() -> (
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
        create_show_position_frames_from_frames_positions(
            frame_start,
            frame_end,
            [],
            frames_positions,
        )


def test_create_show_position_frames_incoherence_frame_indices_and_frame_positions() -> (
    None
):
    frame_start = 0
    frame_end = 1
    frame_indices = [0, 1]
    frames_positions = [[(1.0, 1.0, 1.0)]]
    with pytest.raises(
        ValueError,
        match="drone_indices and frames_positions items must have the same length",
    ):
        create_show_position_frames_from_frames_positions(
            frame_start,
            frame_end,
            frame_indices,
            frames_positions,
        )


def test_create_show_position_frames_0_drones() -> None:
    frame_start = 0
    frame_end = 1
    frame_indices = []
    frames_positions: List[List[Tuple[float, float, float]]] = [[]]
    with pytest.raises(
        ValueError,
        match="nb_drones must be at least 1",
    ):
        create_show_position_frames_from_frames_positions(
            frame_start,
            frame_end,
            frame_indices,
            frames_positions,
        )


def test_get_performance_infractions() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration())
    show_user.drones_user[0].add_position_event(frame=1000, xyz=(0.0, 0.0, 0.0))
    assert len(get_performance_infractions(show_user, {})) == 0
    assert (
        len(
            get_performance_infractions(
                show_user,
                {
                    PerformanceKind.ACCELERATION: PerformanceRange(threshold=0.0001),
                },
            ),
        )
        != 0
    )

    assert len(get_performance_infractions(show_user, {})) == 0


def test_get_collisions() -> None:
    show_position_frames = create_show_position_frames_from_show_user(
        get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2)),
    )
    assert get_collision_infractions(show_position_frames) == []


def test_get_dance_size_report() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    assert len(get_dance_size_infractions(show_user)) == 0


def test_get_dance_size_informations() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    assert all(
        dance_size_information == DanceSizeInformation(drone_index, 0, 0, 0)
        for drone_index, dance_size_information in enumerate(
            get_dance_size_informations(show_user),
        )
    )


def test_generate_report_from_show_user_standard_case() -> None:
    show_user = get_valid_show_user(
        ShowUserConfiguration(nb_x=2, nb_y=2, show_duration_absolute_time=3),
    )
    global_report = generate_report_from_show_user(show_user)
    assert global_report.dict() == {
        "takeoff_format": None,
        "autopilot_format": None,
        "performance": None,
        "collision": None,
    }
    assert global_report.summary().dict() == {
        "takeoff_format": 0,
        "autopilot_format": 0,
        "performance": 0,
        "collision": 0,
    }


def test_generate_report_from_iostar_json_gcs_string() -> None:
    iostar_json_gcs_string = su_to_ijg(
        get_valid_show_user(ShowUserConfiguration()),
    ).json()
    global_report = generate_report_from_iostar_json_gcs_string(
        iostar_json_gcs_string,
    )
    assert global_report.dict() == {
        "takeoff_format": None,
        "autopilot_format": None,
        "performance": None,
        "collision": None,
    }
    assert global_report.summary().dict() == {
        "takeoff_format": 0,
        "autopilot_format": 0,
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


def test_get_verified_iostar_json_gcs_invalid() -> None:
    show_user = get_valid_show_user(
        ShowUserConfiguration(nb_x=2, nb_y=2, step=0.3, show_duration_absolute_time=3),
    )
    iostar_json_gcs = su_to_ijg(show_user)
    with pytest.raises(ReportError):
        get_verified_iostar_json_gcs(iostar_json_gcs.json())
