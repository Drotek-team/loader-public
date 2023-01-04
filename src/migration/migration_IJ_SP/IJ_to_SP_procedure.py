from ...iostar_json.iostar_json import IostarJson
from ...show_px4.show_px4 import ShowPx4
from .IJ_to_SP_report import IJ_to_SP_report
from .migration_DP_binary.drone_decoding_procedure import decode_drone


def IJ_to_SP_procedure(
    iostar_json: IostarJson,
    json_extraction_report: IJ_to_SP_report,
) -> ShowPx4:
    show_px4 = ShowPx4(
        [
            decode_drone(
                binary_dance,
                dance_index,
                json_extraction_report.drones_decoding_report[dance_index],
            )
            for dance_index, binary_dance in enumerate(iostar_json.show.binary_dances)
        ]
    )
    return show_px4
