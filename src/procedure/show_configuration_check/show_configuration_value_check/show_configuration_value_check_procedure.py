from .show_configuration_value_check_report import ShowConfigurationValueCheckReport
from ....parameter.parameter import IostarJsonConfigurationParameter
from ....iostar_json.show_configuration import ShowConfiguration


def apply_show_configuration_value_check(
    show_configuration: ShowConfiguration,
    iostar_json_configuration_parameter: IostarJsonConfigurationParameter,
    show_configuration_value_check_report: ShowConfigurationValueCheckReport,
) -> None:
    show_configuration_value_check_report.nb_x_value_check_report.validation = (
        iostar_json_configuration_parameter.nb_x_value_min <= show_configuration.nb_x
        and show_configuration.nb_x
        <= iostar_json_configuration_parameter.nb_x_value_max
    )
    show_configuration_value_check_report.nb_y_value_check_report.validation = (
        iostar_json_configuration_parameter.nb_y_value_min <= show_configuration.nb_y
        and show_configuration.nb_y
        <= iostar_json_configuration_parameter.nb_y_value_max
    )
    show_configuration_value_check_report.step_value_check_report.validation = (
        iostar_json_configuration_parameter.step_takeoff_value_min
        <= show_configuration.step
        and show_configuration.step
        <= iostar_json_configuration_parameter.step_takeoff_value_max
    )
    show_configuration_value_check_report.takeoff_angle_value_check_report.validation = (
        iostar_json_configuration_parameter.angle_takeoff_value_min
        <= show_configuration.angle_takeoff
        and show_configuration.angle_takeoff
        <= iostar_json_configuration_parameter.angle_takeoff_value_max
    )
    show_configuration_value_check_report.update()
