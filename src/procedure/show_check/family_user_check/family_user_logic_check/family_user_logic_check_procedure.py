from .....family_user.family_user import FamilyUser
from typing import List, Tuple
import numpy as np
from .family_user_logic_check_report import (
    NbDroneLogicCheckReport,
    FirstPositionLogicCheckReport,
    AltitudeRangeLogicCheckReport,
    ShowDurationLogicCheckReport,
    FamilyUserLogicCheckReport,
)
from .....drones_px4.drones_user import DronesPx4
from .....parameter.parameter import FrameParameter, JsonConvertionConstant


def apply_nb_drone_logic_check_report(
    family_user: FamilyUser,
    first_positions: List[Tuple],
    nb_drone_logic_check_report: NbDroneLogicCheckReport,
) -> None:
    if len(first_positions) != len(family_user.theorical_grid):
        nb_drone_logic_check_report.update_report(
            len(first_positions), family_user.theorical_grid.size
        )
    else:
        nb_drone_logic_check_report.validation = True


def apply_position_logic_check_report(
    family_user: FamilyUser,
    first_positions: List[Tuple],
    position_logic_check_report: FirstPositionLogicCheckReport,
) -> None:
    ROW_ALIGNED_CENTIMETER_TOLERANCE = 1
    if (
        np.max(np.array(first_positions) - family_user.theorical_grid)
        > ROW_ALIGNED_CENTIMETER_TOLERANCE
    ):
        position_logic_check_report.update_report(
            np.max(np.array(first_positions) - family_user.theorical_grid)
        )
    else:
        position_logic_check_report.validation = True


def apply_show_duration_logic_check_report(
    drones_user: DronesPx4,
    family_user: FamilyUser,
    frame_parameter: FrameParameter,
    show_duration_logic_check_report: ShowDurationLogicCheckReport,
):
    if (
        int(frame_parameter.json_fps * drones_user.duration)
        != family_user.show_duration_second
    ):
        show_duration_logic_check_report.update_report(
            drones_user.duration, family_user.show_duration_second
        )
    else:
        show_duration_logic_check_report.validation = True


def apply_altitude_range_logic_check_report(
    drones_user: DronesPx4,
    family_user: FamilyUser,
    json_convertion_constant: JsonConvertionConstant,
    altitude_range_logic_check_report: AltitudeRangeLogicCheckReport,
):
    if (
        drones_user.altitude_range[0]
        != family_user.altitude_range_meter[0]
        * json_convertion_constant.METER_TO_CENTIMETER_RATIO
        and drones_user.altitude_range[1]
        != family_user.altitude_range_meter[1]
        * json_convertion_constant.METER_TO_CENTIMETER_RATIO
    ):
        altitude_range_logic_check_report.update_report(
            drones_user.altitude_range, family_user.altitude_range_meter
        )
    else:
        altitude_range_logic_check_report.validation = True


def apply_family_user_logic_check_procedure(
    drones_user: DronesPx4,
    family_user: FamilyUser,
    frame_parameter: FrameParameter,
    json_convertion_constant: JsonConvertionConstant,
    family_user_logic_check_report: FamilyUserLogicCheckReport,
) -> None:
    apply_nb_drone_logic_check_report(
        family_user,
        drones_user.first_horizontal_positions,
        family_user_logic_check_report.nb_drone_logic_check_report,
    )
    if family_user_logic_check_report.nb_drone_logic_check_report.validation:
        apply_position_logic_check_report(
            family_user,
            drones_user.first_horizontal_positions,
            family_user_logic_check_report.first_position_logic_check_report,
        )
        apply_show_duration_logic_check_report(
            drones_user,
            family_user,
            frame_parameter,
            family_user_logic_check_report.show_duration_logic_check_report,
        )
        apply_altitude_range_logic_check_report(
            drones_user,
            family_user,
            json_convertion_constant,
            family_user_logic_check_report.altitude_range_logic_check_report,
        )
    family_user_logic_check_report.update()
