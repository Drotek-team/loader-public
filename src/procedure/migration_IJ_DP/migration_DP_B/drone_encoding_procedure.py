import struct
from typing import List

from .events_convertion import encode_events
from ....binary_px4.binary import Header, SectionHeader
import copy
from ....drones_px4.drone_px4.events.events import Events
from ....parameter.parameter import JsonBinaryParameter, IostarParameter
from ....drones_px4.drone_px4.drone_px4 import DronePx4

# TO DO: A cumsum will prevent the loop but it is kind of convulated for not very much
def get_section_headers(
    encoded_events_list: List[bytearray],
    non_empty_events_list: List[Events],
    json_binary_parameter: JsonBinaryParameter,
) -> List[SectionHeader]:
    byte_array_start_index = struct.calcsize(json_binary_parameter.fmt_header) + len(
        non_empty_events_list
    ) * struct.calcsize(json_binary_parameter.fmt_section_header)
    section_headers: List[SectionHeader] = []
    for non_empty_events, encoded_events in zip(
        non_empty_events_list, encoded_events_list
    ):
        section_header = SectionHeader(
            json_binary_parameter.fmt_section_header,
            non_empty_events.id,
            byte_array_start_index,
            byte_array_start_index + len(encoded_events),
        )
        byte_array_start_index += len(encoded_events)
        section_headers.append(section_header)
    return section_headers


def dance_size(
    section_headers: List[SectionHeader],
    encoded_events_list: List[bytearray],
    json_binary_parameter: JsonBinaryParameter,
) -> int:
    return (
        struct.calcsize(json_binary_parameter.fmt_header)
        + len(section_headers)
        * struct.calcsize(json_binary_parameter.fmt_section_header)
        + sum(len(encoded_events) for encoded_events in encoded_events_list)
    )


def assemble_dance(
    header: Header,
    section_headers: List[SectionHeader],
    encoded_events_list: List[bytearray],
) -> List[int]:
    dance_binary = bytearray()
    dance_binary.extend(header.bytes_data)
    for section_header in section_headers:
        dance_binary.extend(section_header.bytes_data)
    for encoded_events in encoded_events_list:
        dance_binary.extend(encoded_events)
    return list(map(int, dance_binary))


def encode_drone(
    drone_user: DronePx4,
    json_binary_parameter: JsonBinaryParameter,
) -> List[int]:
    ### No user report needed as this part is interne to the program
    ### ValueError and test is needed in this case
    drone_user_copy = copy.deepcopy(drone_user)
    non_empty_events_list = drone_user_copy.non_empty_events_list
    encoded_events_list = [
        encode_events(non_empty_events) for non_empty_events in non_empty_events_list
    ]
    section_headers = get_section_headers(
        encoded_events_list, non_empty_events_list, json_binary_parameter
    )
    header = Header(
        json_binary_parameter.fmt_header,
        json_binary_parameter.magic_number,
        dance_size(section_headers, encoded_events_list, json_binary_parameter),
        len(non_empty_events_list),
    )
    return assemble_dance(header, section_headers, encoded_events_list)
