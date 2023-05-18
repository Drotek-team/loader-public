import struct
from typing import List, Tuple

from loader.parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from loader.show_env.drone_px4 import DronePx4
from loader.show_env.drone_px4.binary import Header, SectionHeader
from loader.show_env.drone_px4.events.events import Events


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

    section_headers: List[SectionHeader] = []
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
            ),
        )
    return header, section_headers


def decode_events(events: Events, byte_array: bytearray) -> None:
    for event_index in range(0, len(byte_array), events.event_size):
        events.add_data(
            list(
                struct.unpack(
                    events.format_,
                    byte_array[event_index : event_index + events.event_size],
                ),
            ),
        )


def decode_drone(
    drone_index: int,
    binary: List[int],
) -> DronePx4:
    drone_px4 = DronePx4(drone_index)
    byte_array = bytearray(binary)
    _, section_headers = get_header_section_header(byte_array)
    for section_header in section_headers:
        decode_events(
            drone_px4.get_events_by_index(section_header.event_id),
            byte_array[
                section_header.byte_array_start_index : section_header.byte_array_end_index + 1
            ],
        )
    return drone_px4
