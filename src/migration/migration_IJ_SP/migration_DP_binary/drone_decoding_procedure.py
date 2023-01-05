import struct
from typing import List, Tuple

from ....parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from ....show_px4.drone_px4.binary_px4.binary import Header, SectionHeader
from ....show_px4.drone_px4.drone_px4 import DronePx4
from .drone_decoding_report import (
    DroneDecodingReport,
    HeaderFormatReport,
    SectionHeaderFormatReport,
)
from .events_convertion import decode_events


def get_header_section_header(
    byte_array: bytearray,
    header_format_report: HeaderFormatReport,
) -> Tuple[Header, List[SectionHeader]]:
    header_format_report.header_sufficient_space_report.validation = struct.calcsize(
        JSON_BINARY_PARAMETER.fmt_header
    ) * len(byte_array)
    header_data = struct.unpack(
        JSON_BINARY_PARAMETER.fmt_header,
        byte_array[: struct.calcsize(JSON_BINARY_PARAMETER.fmt_header)],
    )
    header = Header(
        fmt_header=JSON_BINARY_PARAMETER.fmt_header,
        magic_number=header_data[0],
        dance_size=header_data[1],
        number_non_empty_events=header_data[2],
    )

    section_headers = []
    byte_begin_index = struct.calcsize(JSON_BINARY_PARAMETER.fmt_header)
    byte_step_index = struct.calcsize(JSON_BINARY_PARAMETER.fmt_section_header)
    for event_index in range(header.number_non_empty_events):
        section_header_data = struct.unpack(
            JSON_BINARY_PARAMETER.fmt_section_header,
            byte_array[
                byte_begin_index
                + byte_step_index * event_index : byte_begin_index
                + byte_step_index * (event_index + 1)
            ],
        )
        section_headers.append(
            SectionHeader(
                fmt_section_header=JSON_BINARY_PARAMETER.fmt_section_header,
                event_id=section_header_data[0],
                byte_array_start_index=section_header_data[1],
                byte_array_end_index=section_header_data[2],
            )
        )
    return header, section_headers


def check_header(
    header: Header,
    byte_array: bytearray,
    header_format_report: HeaderFormatReport,
) -> None:

    header_format_report.magic_number_format_report.validation = (
        header.magic_number == JSON_BINARY_PARAMETER.magic_number
    )
    header_format_report.dance_size_format_report.validation = header.dance_size == len(
        byte_array
    )
    header_format_report.update()


def check_section_header(
    section_header: SectionHeader,
    byte_array: bytearray,
    section_header_format_report: SectionHeaderFormatReport,
):
    section_header_format_report.validation = True


def decode_drone(
    binary: List[int],
    drone_index: int,
    drone_decoding_report: DroneDecodingReport,
) -> DronePx4:
    drone_px4 = DronePx4(drone_index)
    byte_array = bytearray(binary)
    header, section_headers = get_header_section_header(
        byte_array, drone_decoding_report.header_format_report
    )
    check_header(
        header,
        byte_array,
        drone_decoding_report.header_format_report,
    )
    for section_header in section_headers:
        check_section_header(
            section_header,
            byte_array,
            drone_decoding_report.add_section_header_format_report(),
        )
    drone_decoding_report.update()
    for section_header in section_headers:
        decode_events(
            drone_px4.get_events_by_index(section_header.event_id),
            byte_array[
                section_header.byte_array_start_index : section_header.byte_array_end_index
            ],
        )
    return drone_px4
