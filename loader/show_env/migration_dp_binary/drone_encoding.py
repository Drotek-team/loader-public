import copy
import struct
from typing import List

from pydantic import BaseModel

from loader.parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from loader.show_env.autopilot_format.drone_px4 import DronePx4
from loader.show_env.autopilot_format.drone_px4.binary import Header, SectionHeader
from loader.show_env.autopilot_format.drone_px4.events import Events

from .events_convertion import encode_events


def get_section_headers(
    encoded_events_list: List[bytearray],
    non_empty_events_list: List[Events],
) -> List[SectionHeader]:
    byte_array_start_index = struct.calcsize(JSON_BINARY_PARAMETER.fmt_header) + len(
        non_empty_events_list,
    ) * struct.calcsize(JSON_BINARY_PARAMETER.fmt_section_header)
    section_headers: List[SectionHeader] = []
    for non_empty_events, encoded_events in zip(
        non_empty_events_list,
        encoded_events_list,
    ):
        section_header = SectionHeader(
            fmt_section_header=JSON_BINARY_PARAMETER.fmt_section_header,
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
        struct.calcsize(JSON_BINARY_PARAMETER.fmt_header)
        + len(section_headers)
        * struct.calcsize(JSON_BINARY_PARAMETER.fmt_section_header)
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
) -> List[int]:
    drone_user_copy = copy.deepcopy(drone_user)
    non_empty_events_list = drone_user_copy.non_empty_events_list
    encoded_events_list = [
        encode_events(non_empty_events) for non_empty_events in non_empty_events_list
    ]
    section_headers = get_section_headers(encoded_events_list, non_empty_events_list)
    header = Header(
        fmt_header=JSON_BINARY_PARAMETER.fmt_header,
        magic_number=JSON_BINARY_PARAMETER.magic_number,
        dance_size=dance_size(section_headers, encoded_events_list),
        number_non_empty_events=len(non_empty_events_list),
    )
    return assemble_dance(header, section_headers, encoded_events_list)


class DanceSizeInformation(BaseModel):
    drone_index: int
    dance_size: int
    position_events_size_pct: int
    color_events_size_pct: int
    fire_events_size_pct: int

    @property
    def total_events_size_pct(self) -> int:
        return (
            self.position_events_size_pct
            + self.color_events_size_pct
            + self.fire_events_size_pct
        )


def get_dance_size_information(drone_px4: DronePx4) -> DanceSizeInformation:
    header_size = struct.calcsize(JSON_BINARY_PARAMETER.fmt_header)
    header_section_size = len(drone_px4.non_empty_events_list) * struct.calcsize(
        JSON_BINARY_PARAMETER.fmt_section_header,
    )
    position_size = len(drone_px4.position_events) * struct.calcsize(
        JSON_BINARY_PARAMETER.position_event_format,
    )
    color_size = len(drone_px4.color_events) * struct.calcsize(
        JSON_BINARY_PARAMETER.color_event_format,
    )
    fire_size = len(drone_px4.fire_events) * struct.calcsize(
        JSON_BINARY_PARAMETER.fire_event_format,
    )
    return DanceSizeInformation(
        drone_index=drone_px4.index,
        dance_size=header_size
        + header_section_size
        + position_size
        + color_size
        + fire_size,
        position_events_size_pct=int(
            100 * position_size / JSON_BINARY_PARAMETER.dance_size_max,
        ),
        color_events_size_pct=int(
            100 * color_size / JSON_BINARY_PARAMETER.dance_size_max,
        ),
        fire_events_size_pct=int(
            100 * fire_size / JSON_BINARY_PARAMETER.dance_size_max,
        ),
    )
