from ...iostar_json.iostar_json import IostarJson
from ...parameter.parameter import IostarParameter, JsonBinaryParameter
from ...show_px4.show_px4 import ShowPx4
from .IJ_to_SP_report import IJ_to_SP_report
from .migration_DP_binary.drone_decoding_procedure import decode_drone


def IJ_to_SP_procedure(
    iostar_json: IostarJson,
    iostar_parameter: IostarParameter,
    json_binary_parameter: JsonBinaryParameter,
    json_extraction_report: IJ_to_SP_report,
) -> ShowPx4:
    show_px4 = ShowPx4(
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
    return show_px4
