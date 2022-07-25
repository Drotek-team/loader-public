import struct
from typing import List

from ....drones_manager.drone.drone import DroneExport
from ....drones_manager.drone.events.events import Events
from ....parameter.parameter import JsonFormatParameter
from .drone_encoding_report import DroneEncodingReport
from .events_convertion import encode_events
from .json_format_convention import Header, SectionHeader


# TO DO: A cumsum will prevent the loop but it is kind of convulated for not very much
def get_section_headers(
    encoded_events_list: List[bytearray],
    non_empty_events_list: List[Events],
    json_format_parameter: JsonFormatParameter,
) -> List[SectionHeader]:
    byte_array_start_index = struct.calcsize(json_format_parameter.fmt_header)
    section_headers: List[SectionHeader] = []
    for non_empty_events, encoded_events in zip(
        non_empty_events_list, encoded_events_list
    ):
        section_header = SectionHeader(
            json_format_parameter.fmt_section_header,
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
    json_format_parameter: JsonFormatParameter,
) -> int:
    return (
        struct.calcsize(json_format_parameter.fmt_header)
        + len(section_headers)
        * struct.calcsize(json_format_parameter.fmt_section_header)
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
    drone: DroneExport,
    json_format_parameter: JsonFormatParameter,
    drone_encoding_report: DroneEncodingReport,
) -> List[int]:
    non_empty_events_list = drone.non_empty_events_list
    encoded_events_list = [
        encode_events(non_empty_events) for non_empty_events in non_empty_events_list
    ]
    section_headers = get_section_headers(
        encoded_events_list, non_empty_events_list, json_format_parameter
    )
    header = Header(
        json_format_parameter.fmt_header,
        json_format_parameter.magic_number,
        dance_size(section_headers, encoded_events_list, json_format_parameter),
        len(non_empty_events_list),
    )
    return assemble_dance(header, section_headers, encoded_events_list)
