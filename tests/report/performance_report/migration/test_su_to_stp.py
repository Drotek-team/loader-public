from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from loader.report.performance_report.migration.su_to_stp import (
    get_trajectory_performance_info_from_position_events,
    su_to_stp,
)
from loader.show_env.show_user import PositionEventUser
from loader.show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)

if TYPE_CHECKING:
    from numpy.typing import NDArray


def from_ca_to_ct(
    coordinate_array: NDArray[np.float64],
) -> tuple[float, float, float]:
    return (coordinate_array[0], coordinate_array[1], coordinate_array[2])


def test_get_trajectory_performance_info_from_position_events() -> None:
    position_events = [
        PositionEventUser(frame=0, xyz=(0.0, 0.0, 0.0)),
        PositionEventUser(frame=24, xyz=(0.0, 0.0, 1.0)),
        PositionEventUser(frame=48, xyz=(0.0, 0.0, 2.0)),
        PositionEventUser(frame=96, xyz=(0.0, 0.0, 3.0)),
    ]
    trajectory_performance_infos = get_trajectory_performance_info_from_position_events(
        position_events,
    )
    for position_index in range(4):
        assert (
            trajectory_performance_infos[position_index].frame
            == position_events[position_index].frame
        )
        assert (
            from_ca_to_ct(trajectory_performance_infos[position_index].position)
            == position_events[position_index].xyz
        )
    assert from_ca_to_ct(trajectory_performance_infos[0].velocity) == (0.0, 0.0, 0.0)
    assert from_ca_to_ct(trajectory_performance_infos[1].velocity) == (0.0, 0.0, 1.0)
    assert from_ca_to_ct(trajectory_performance_infos[2].velocity) == (0.0, 0.0, 1.0)
    assert from_ca_to_ct(trajectory_performance_infos[3].velocity) == (0.0, 0.0, 0.5)

    assert from_ca_to_ct(trajectory_performance_infos[0].acceleration) == (
        0.0,
        0.0,
        0.0,
    )
    assert from_ca_to_ct(trajectory_performance_infos[1].acceleration) == (
        0.0,
        0.0,
        1.0,
    )
    assert from_ca_to_ct(trajectory_performance_infos[2].acceleration) == (
        0.0,
        0.0,
        0.0,
    )
    assert from_ca_to_ct(trajectory_performance_infos[3].acceleration) == (
        0.0,
        0.0,
        -0.25,
    )


def test_su_to_stp() -> None:
    show_trajectory_performance = su_to_stp(
        get_valid_show_user(ShowUserConfiguration()),
    )
    drone_trajectory_performance = (
        show_trajectory_performance.drones_trajectory_performance[0]
    )
    assert len(drone_trajectory_performance.trajectory_performance_infos) == 3
