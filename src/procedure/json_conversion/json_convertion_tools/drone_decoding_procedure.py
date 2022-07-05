import struct
from typing import List, Tuple

from ....drones_manager.drone.drone import Drone
from ....parameter.parameter import JsonConvertionParameter
from .events_convertion import decode_events


def decode_header(
    byte_array: bytearray, json_convention_parameter: JsonConvertionParameter
) -> int:
    magic_nb, dance_size, nb_section = struct.unpack(
        json_convention_parameter.fmt_header,
        byte_array[: struct.calcsize(json_convention_parameter.fmt_header)],
    )
    return nb_section


def decode_section_header(
    byte_array: bytearray,
    index: int,
    json_convention_parameter: JsonConvertionParameter,
) -> Tuple[int, int, int]:
    events_id, start, end = struct.unpack(
        json_convention_parameter.fmt_section_header,
        byte_array[
            struct.calcsize(json_convention_parameter.fmt_header)
            + struct.calcsize(json_convention_parameter.fmt_section_header)
            * index : struct.calcsize(json_convention_parameter.fmt_header)
            + struct.calcsize(json_convention_parameter.fmt_section_header)
            * (index + 1)
        ],
    )
    return events_id, start, end


def decode_drone(
    binary: List[int],
    drone_index: int,
    json_convention_parameter: JsonConvertionParameter,
) -> Drone:
    drone = Drone(drone_index)
    byte_array = bytearray(binary)
    nb_sections = decode_header(byte_array, json_convention_parameter)

    ### These check belong in the procedure, not the object !!!###
    # if magic_nb == json_convention_parameter.MAGIC_NB:
    #     decode_report.validation = True
    # if dance_size != len(binary):
    #     decode_report.validation = True

    # if start < end:
    #     decode_report.validation = True
    for index in range(nb_sections):
        (
            events_id,
            events_start_index,
            events_end_index,
        ) = decode_section_header(byte_array, index, json_convention_parameter)
        decode_events(
            drone.get_events_by_index(events_id),
            byte_array[events_start_index : events_end_index + 1],
        )
