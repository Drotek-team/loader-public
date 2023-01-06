import struct
from typing import List, Tuple

from ....parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from ....show_px4.drone_px4.binary_px4.binary import Header, SectionHeader
from ....show_px4.drone_px4.drone_px4 import DronePx4
from .events_convertion import decode_events


def get_header_section_header(
    byte_array: bytearray,
) -> Tuple[Header, List[SectionHeader]]:
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


def decode_drone(
    binary: List[int],
    drone_index: int,
) -> DronePx4:
    drone_px4 = DronePx4(drone_index)
    byte_array = bytearray(binary)
    _, section_headers = get_header_section_header(byte_array)
    for section_header in section_headers:
        decode_events(
            drone_px4.get_events_by_index(section_header.event_id),
            byte_array[
                section_header.byte_array_start_index : section_header.byte_array_end_index
            ],
        )
    return drone_px4
