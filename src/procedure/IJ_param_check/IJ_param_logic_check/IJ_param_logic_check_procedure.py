# from ....show_user.show_user import IostarJsonParameter
# from typing import List, Tuple
# import numpy as np
# from .IJ_param_logic_check_report import (
#     NbDroneLogicCheckReport,
#     FirstPositionLogicCheckReport,
#     AltitudeRangeLogicCheckReport,
#     ShowDurationLogicCheckReport,
#     IostarJsonParameterLogicCheckReport,
# )
# from ....drones_px4.drones_px4 import DronesPx4
# from ....parameter.parameter import FrameParameter


# def apply_nb_drone_logic_check_report(
#     iostar_json_parameter: IostarJsonParameter,
#     first_positions: List[Tuple],
#     nb_drone_logic_check_report: NbDroneLogicCheckReport,
# ) -> None:
#     if len(first_positions) != len(iostar_json_parameter.theorical_grid):
#         nb_drone_logic_check_report.update_report(
#             len(first_positions), iostar_json_parameter.theorical_grid.size
#         )
#     else:
#         nb_drone_logic_check_report.validation = True


# def apply_position_logic_check_report(
#     iostar_json_parameter: IostarJsonParameter,
#     first_positions: List[Tuple],
#     position_logic_check_report: FirstPositionLogicCheckReport,
# ) -> None:
#     ROW_ALIGNED_CENTIMETER_TOLERANCE = 1
#     if (
#         np.max(np.array(first_positions) - iostar_json_parameter.theorical_grid)
#         > ROW_ALIGNED_CENTIMETER_TOLERANCE
#     ):
#         position_logic_check_report.update_report(
#             np.max(np.array(first_positions) - iostar_json_parameter.theorical_grid)
#         )
#     else:
#         position_logic_check_report.validation = True


# def apply_show_duration_logic_check_report(
#     drones_px4: DronesPx4,
#     iostar_json_parameter: IostarJsonParameter,
#     frame_parameter: FrameParameter,
#     show_duration_logic_check_report: ShowDurationLogicCheckReport,
# ):
#     if (
#         int(frame_parameter.json_fps * drones_px4.duration)
#         != iostar_json_parameter.show_duration_second
#     ):
#         show_duration_logic_check_report.update_report(
#             drones_px4.duration, iostar_json_parameter.show_duration_second
#         )
#     else:
#         show_duration_logic_check_report.validation = True


# def apply_altitude_range_logic_check_report(
#     drones_px4: DronesPx4,
#     iostar_json_parameter: IostarJsonParameter,
#     altitude_range_logic_check_report: AltitudeRangeLogicCheckReport,
# ):
#     if (
#         drones_px4.altitude_range[0] != iostar_json_parameter.altitude_range_meter[0]
#         and drones_px4.altitude_range[1]
#         != iostar_json_parameter.altitude_range_meter[1]
#     ):
#         altitude_range_logic_check_report.update_report(
#             drones_px4.altitude_range, iostar_json_parameter.altitude_range_meter
#         )
#     else:
#         altitude_range_logic_check_report.validation = True


# def apply_iostar_json_parameter_logic_check_procedure(
#     drones_px4: DronesPx4,
#     iostar_json_parameter: IostarJsonParameter,
#     frame_parameter: FrameParameter,
#     iostar_json_parameter_logic_check_report: IostarJsonParameterLogicCheckReport,
# ) -> None:
#     apply_nb_drone_logic_check_report(
#         iostar_json_parameter,
#         drones_px4.first_horizontal_positions,
#         iostar_json_parameter_logic_check_report.nb_drone_logic_check_report,
#     )
#     if iostar_json_parameter_logic_check_report.nb_drone_logic_check_report.validation:
#         apply_position_logic_check_report(
#             iostar_json_parameter,
#             drones_px4.first_horizontal_positions,
#             iostar_json_parameter_logic_check_report.first_position_logic_check_report,
#         )
#         # apply_show_duration_logic_check_report(
#         #     drones_px4,
#         #     iostar_json_parameter,
#         #     frame_parameter,
#         #     iostar_json_parameter_logic_check_report.show_duration_logic_check_report,
#         # )
#         # apply_altitude_range_logic_check_report(
#         #     drones_px4,
#         #     iostar_json_parameter,
#         #     json_convertion_constant,
#         #     iostar_json_parameter_logic_check_report.altitude_range_logic_check_report,
#         # )
#     iostar_json_parameter_logic_check_report.update()
