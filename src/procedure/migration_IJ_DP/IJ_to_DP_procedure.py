from ...parameter.parameter import JsonBinaryParameter, IostarParameter
from .IJ_to_DP_report import IJ_to_DP_report
from ...drones_px4.drones_px4 import DronesPx4
from .migration_DP_binary.drone_decoding_procedure import decode_drone
from ...iostar_json.iostar_json import IostarJson


def IJ_to_DP_procedure(
    iostar_json: IostarJson,
    iostar_parameter: IostarParameter,
    json_binary_parameter: JsonBinaryParameter,
    json_extraction_report: IJ_to_DP_report,
) -> DronesPx4:
    drones_px4 = DronesPx4(
        [
            decode_drone(
                binary_dance,
                dance_index,
                iostar_parameter,
                json_binary_parameter,
                json_extraction_report.drones_decoding_report[dance_index],
            )
            for dance_index, binary_dance in enumerate(iostar_json.show.binary_dances)
        ]
    )
    return drones_px4
