import struct
from typing import List, Tuple

from ....drones_manager.drone.drone import Drone
from ....parameter.parameter import JsonFormatParameter
from .drone_decoding_report import DroneDecodingReport, HeaderFormatReport
from .events_convertion import decode_events
from .json_format_convention import Header, SectionHeader


def get_header_section_header(
    byte_array: bytearray,
    json_format_parameter: JsonFormatParameter,
) -> Tuple[Header, List[SectionHeader]]:
    header_data = struct.unpack(
        json_format_parameter.fmt_header,
        byte_array[: struct.calcsize(json_format_parameter.fmt_header)],
    )
    header = Header(
        json_format_parameter.fmt_header,
        header_data[0],
        header_data[1],
        header_data[2],
    )
    section_header_data = struct.unpack(
        json_format_parameter.fmt_header,
        byte_array[
            struct.calcsize(json_format_parameter.fmt_header) : struct.calcsize(
                json_format_parameter.fmt_section_header
                * header.number_non_empty_events
            )
        ],
    )
    section_headers = [
        SectionHeader(
            json_format_parameter.fmt_section_header,
            section_header_data[0],
            section_header_data[1],
            section_header_data[2],
        )
    ]
    return header, section_headers


def check_header(
    header: Header,
    byte_array: bytearray,
    json_format_parameter: JsonFormatParameter,
    header_format_report: HeaderFormatReport,
) -> None:
    header_format_report.magic_number_format_report.validation = (
        header.magic_number == json_format_parameter.magic_number
    )
    header_format_report.dance_size_format_report.validation = header.dance_size == len(
        byte_array
    )


def check_section_header(section_header: SectionHeader):
    section_header.byte_array_start_index


def decode_drone(
    binary: List[int],
    drone_index: int,
    json_format_parameter: JsonFormatParameter,
    drone_decoding_report: DroneDecodingReport,
) -> Drone:
    drone = Drone(drone_index)
    byte_array = bytearray(binary)
    header, section_headers = get_header_section_header(
        byte_array, json_format_parameter
    )
    check_header(header, byte_array, json_format_parameter, drone_decoding_report)
    for section_header in section_headers:
        check_section_header(section_header)
    for section_header in section_headers:
        decode_events(
            drone.get_events_by_index(section_header.event_id),
            byte_array[
                section_header.byte_array_start_index : section_header.byte_array_end_index
            ],
        )
    return drone
