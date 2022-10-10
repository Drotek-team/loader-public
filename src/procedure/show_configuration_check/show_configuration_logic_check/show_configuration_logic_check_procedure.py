from typing import List, Tuple
import numpy as np
from .show_configuration_logic_check_report import (
    NbDroneLogicCheckReport,
    FirstPositionLogicCheckReport,
    AltitudeRangeLogicCheckReport,
    ShowDurationLogicCheckReport,
    ShowConfigurationLogicCheckReport,
)
from ....drones_px4.drones_px4 import DronesPx4
from ....parameter.parameter import FrameParameter
from ....iostar_json.show_configuration import ShowConfiguration


def apply_nb_drone_logic_check_report(
    show_configuration: ShowConfiguration,
    first_positions: List[Tuple[int, int]],
    nb_drone_logic_check_report: NbDroneLogicCheckReport,
) -> None:
    if len(first_positions) != len(show_configuration.theorical_grid_from_parameter):
        nb_drone_logic_check_report.update_report(
            len(first_positions), show_configuration.theorical_grid_from_parameter.size
        )
    else:
        nb_drone_logic_check_report.validation = True


def apply_position_logic_check_report(
    show_configuration: ShowConfiguration,
    first_positions: List[Tuple[int, int]],
    position_logic_check_report: FirstPositionLogicCheckReport,
) -> None:
    ROW_ALIGNED_CENTIMETER_TOLERANCE = 1
    if (
        np.max(
            np.array(first_positions) - show_configuration.theorical_grid_from_parameter
        )
        > ROW_ALIGNED_CENTIMETER_TOLERANCE
    ):
        position_logic_check_report.update_report(
            np.max(
                np.array(first_positions)
                - show_configuration.theorical_grid_from_parameter
            )
        )
        return
    position_logic_check_report.validation = True


def apply_show_duration_logic_check_report(
    drones_px4: DronesPx4,
    show_configuration: ShowConfiguration,
    frame_parameter: FrameParameter,
    show_duration_logic_check_report: ShowDurationLogicCheckReport,
):
    if (
        int(frame_parameter.json_fps * drones_px4.duration)
        != show_configuration.duration
    ):
        show_duration_logic_check_report.update_report(
            drones_px4.duration, show_configuration.duration
        )
        return
    show_duration_logic_check_report.validation = True


def apply_altitude_range_logic_check_report(
    drones_px4: DronesPx4,
    show_configuration: ShowConfiguration,
    altitude_range_logic_check_report: AltitudeRangeLogicCheckReport,
):
    if (
        drones_px4.altitude_range[0] != show_configuration.altitude_range[0]
        and drones_px4.altitude_range[1] != show_configuration.altitude_range[1]
    ):
        altitude_range_logic_check_report.update_report(
            drones_px4.altitude_range, show_configuration.altitude_range
        )
        return
    altitude_range_logic_check_report.validation = True


def apply_show_configuration_logic_check_procedure(
    drones_px4: DronesPx4,
    show_configuration: ShowConfiguration,
    frame_parameter: FrameParameter,
    show_configuration_logic_check_report: ShowConfigurationLogicCheckReport,
) -> None:
    apply_nb_drone_logic_check_report(
        show_configuration,
        drones_px4.first_horizontal_positions,
        show_configuration_logic_check_report.nb_drone_logic_check_report,
    )
    if show_configuration_logic_check_report.nb_drone_logic_check_report.validation:
        apply_position_logic_check_report(
            show_configuration,
            drones_px4.first_horizontal_positions,
            show_configuration_logic_check_report.first_position_logic_check_report,
        )
        apply_show_duration_logic_check_report(
            drones_px4,
            show_configuration,
            frame_parameter,
            show_configuration_logic_check_report.show_duration_logic_check_report,
        )
        apply_altitude_range_logic_check_report(
            drones_px4,
            show_configuration,
            show_configuration_logic_check_report.altitude_range_logic_check_report,
        )
    show_configuration_logic_check_report.update()
