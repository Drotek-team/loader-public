import io
from ....iostar_json.iostar_json import IostarJson
from ....iostar_json.show_configuration import ShowConfiguration


def IJ_to_SC_procedure(iostar_json: IostarJson) -> ShowConfiguration:
    return ShowConfiguration(
        iostar_json.show.nb_x,
        iostar_json.show.nb_y,
        len(iostar_json.show.families[0].drones),
        iostar_json.show.step,
        iostar_json.show.angle_takeoff,
        iostar_json.show.duration,
        iostar_json.show.hull,
        iostar_json.show.altitude_range,
    )
