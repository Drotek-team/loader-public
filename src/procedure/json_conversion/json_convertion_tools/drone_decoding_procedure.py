import struct
from typing import List, Tuple

from ....drones_manager.drone.drone import DroneExport
from ....drones_manager.drone.events.position_events import PositionEvent
from ....parameter.parameter import JsonBinaryParameter, IostarParameter
from .drone_decoding_report import (
    DroneDecodingReport,
    HeaderFormatReport,
    SectionHeaderFormatReport,
)
from .events_convertion import decode_events
from .json_format_convention import Header, SectionHeader, unapply_reformat_events


def get_header_section_header(
    byte_array: bytearray,
    json_binary_parameter: JsonBinaryParameter,
    header_format_report: HeaderFormatReport,
) -> Tuple[Header, List[SectionHeader]]:
    header_format_report.header_sufficient_space_report.validation = struct.calcsize(
        json_binary_parameter.fmt_header
    ) * len(byte_array)
    header_data = struct.unpack(
        json_binary_parameter.fmt_header,
        byte_array[: struct.calcsize(json_binary_parameter.fmt_header)],
    )
    header = Header(
        json_binary_parameter.fmt_header,
        header_data[0],
        header_data[1],
        header_data[2],
    )

    section_headers = []
    byte_begin_index = struct.calcsize(json_binary_parameter.fmt_header)
    byte_step_index = struct.calcsize(json_binary_parameter.fmt_section_header)
    for event_index in range(header.number_non_empty_events):
        section_header_data = struct.unpack(
            json_binary_parameter.fmt_section_header,
            byte_array[
                byte_begin_index
                + byte_step_index * event_index : byte_begin_index
                + byte_step_index * (event_index + 1)
            ],
        )
        section_headers.append(
            SectionHeader(
                json_binary_parameter.fmt_section_header,
                section_header_data[0],
                section_header_data[1],
                section_header_data[2],
            )
        )
    return header, section_headers


def check_header(
    header: Header,
    byte_array: bytearray,
    json_binary_parameter: JsonBinaryParameter,
    header_format_report: HeaderFormatReport,
) -> None:

    header_format_report.magic_number_format_report.validation = (
        header.magic_number == json_binary_parameter.magic_number
    )
    header_format_report.dance_size_format_report.validation = header.dance_size == len(
        byte_array
    )
    header_format_report.update()


def check_section_header(
    section_header: SectionHeader,
    byte_array: bytearray,
    json_binary_parameter: JsonBinaryParameter,
    section_header_format_report: SectionHeaderFormatReport,
):
    section_header_format_report.validation = True


def decode_drone(
    binary: List[int],
    drone_index: int,
    iostar_parameter: IostarParameter,
    json_binary_parameter: JsonBinaryParameter,
    drone_decoding_report: DroneDecodingReport,
) -> DroneExport:
    drone = DroneExport(drone_index)
    byte_array = bytearray(binary)
    header, section_headers = get_header_section_header(
        byte_array, json_binary_parameter, drone_decoding_report.header_format_report
    )
    check_header(
        header,
        byte_array,
        json_binary_parameter,
        drone_decoding_report.header_format_report,
    )
    for section_header in section_headers:
        check_section_header(
            section_header,
            byte_array,
            json_binary_parameter,
            drone_decoding_report.add_section_header_format_report(),
        )
    drone_decoding_report.update()
    for section_header in section_headers:
        decode_events(
            drone.get_events_by_index(section_header.event_id),
            byte_array[
                section_header.byte_array_start_index : section_header.byte_array_end_index
            ],
        )
    second_position_event = drone.position_events.event_list[1]
    x, y, z = second_position_event.get_values()
    drone.position_events.event_list[1] = PositionEvent(
        second_position_event.frame, x, y, z
    )
    unapply_reformat_events(drone, iostar_parameter)
    return drone
