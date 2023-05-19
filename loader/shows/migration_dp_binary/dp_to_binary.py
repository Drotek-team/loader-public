import copy
import struct
from typing import List

from loader.parameters import JSON_BINARY_PARAMETERS
from loader.shows.drone_px4 import DronePx4
from loader.shows.drone_px4.binary import Header, SectionHeader
from loader.shows.drone_px4.events import Events


def get_section_headers(
    encoded_events_list: List[bytearray],
    non_empty_events_list: List[Events],
) -> List[SectionHeader]:
    byte_array_start_index = struct.calcsize(JSON_BINARY_PARAMETERS.fmt_header) + len(
        non_empty_events_list,
    ) * struct.calcsize(JSON_BINARY_PARAMETERS.fmt_section_header)
    section_headers: List[SectionHeader] = []
    for non_empty_events, encoded_events in zip(
        non_empty_events_list,
        encoded_events_list,
    ):
        section_header = SectionHeader(
            fmt_section_header=JSON_BINARY_PARAMETERS.fmt_section_header,
            event_id=non_empty_events.id_,
            byte_array_start_index=byte_array_start_index,
            byte_array_end_index=byte_array_start_index + len(encoded_events) - 1,
        )
        byte_array_start_index += len(encoded_events)
        section_headers.append(section_header)
    return section_headers


def dance_size(
    section_headers: List[SectionHeader],
    encoded_events_list: List[bytearray],
) -> int:
    return (
        struct.calcsize(JSON_BINARY_PARAMETERS.fmt_header)
        + len(section_headers) * struct.calcsize(JSON_BINARY_PARAMETERS.fmt_section_header)
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


def encode_events(events: Events) -> bytearray:
    event_size = events.event_size
    binary = bytearray(event_size * len(events))
    for cpt_event, event_data in enumerate(events):
        binary[cpt_event * event_size : (cpt_event + 1) * event_size] = struct.pack(
            events.format_,
            *event_data.get_data,
        )
    return binary


def encode_drone(
    drone_user: DronePx4,
) -> List[int]:
    drone_user_copy = copy.deepcopy(drone_user)
    non_empty_events_list = drone_user_copy.non_empty_events_list
    encoded_events_list = [
        encode_events(non_empty_events) for non_empty_events in non_empty_events_list
    ]
    section_headers = get_section_headers(encoded_events_list, non_empty_events_list)
    header = Header(
        fmt_header=JSON_BINARY_PARAMETERS.fmt_header,
        magic_number=JSON_BINARY_PARAMETERS.magic_number,
        dance_size=dance_size(section_headers, encoded_events_list),
        number_non_empty_events=len(non_empty_events_list),
    )
    return assemble_dance(header, section_headers, encoded_events_list)
