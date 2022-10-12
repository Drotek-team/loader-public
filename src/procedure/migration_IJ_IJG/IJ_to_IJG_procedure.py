from ...iostar_json.iostar_json import IostarJson
from ...iostar_json_gcs.iostar_json_gcs import IostarJsonGCS
from .migration_SC.DP_to_SC_procedure import DP_to_SC_procedure
from ..migration_IJ_DP.IJ_to_DP_procedure import IJ_to_DP_procedure
from ...parameter.parameter import Parameter


def IJ_to_IJG_procedure(iostar_json: IostarJson, parameter: Parameter) -> IostarJsonGCS:

    drones_px4 = IJ_to_DP_procedure(
        iostar_json,
        parameter.iostar_parameter,
        parameter.json_binary_parameter,
    )
    show_configuration = DP_to_SC_procedure(drones_px4)
    return IostarJsonGCS(
        **{
            "show": {
                "families": [
                    {"drones": {"dance": 0}, "x": 0, "y": 0, "z": 0}
                    for drones_family in range()
                ]
            },
            "duration": show_configuration.duration,
            "hull": show_configuration.hull,
            "altitude_range": show_configuration.altitude_range,
            "step": show_configuration.step,
            "nb_x": show_configuration.nb_x,
            "nb_y": show_configuration.nb_y,
            "angle_takeoff": show_configuration.angle_takeoff,
        }
    )
