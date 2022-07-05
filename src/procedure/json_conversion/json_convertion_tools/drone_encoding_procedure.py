import struct
from dataclasses import dataclass
from typing import List

from ....drones_manager.drone.drone import Drone
from ....drones_manager.drone.events.events import Events
from ....parameter.parameter import JsonConvertionParameter
from .events_encoder import encode_events


class BytesManager:
    def __init__(self, fmt: str):
        self.fmt = fmt

    @property
    def bytes_data(self) -> bytes:
        data_list = [value for _, value in self.__dict__.items()]
        return struct.pack(self.fmt, *data_list)


@dataclass(frozen=True)
class Header(BytesManager):
    def __init__(
        self,
        fmt_header: str,
        magic_number: str,
        dance_size: int,
        number_non_empty_events: int,
    ):
        BytesManager.__init__(self, fmt_header)
        self.magic_number = magic_number
        self.dance_size = dance_size
        self.number_non_empty_events = number_non_empty_events


@dataclass(frozen=True)
class SectionHeader(BytesManager):
    def __init__(
        self,
        fmt_section_header: str,
        event_id: int,
        byte_array_start_index: int,
        byte_array_end_index: int,
    ):
        BytesManager.__init__(self, fmt_section_header)
        self.event_id = event_id
        self.byte_array_start_index = byte_array_start_index
        self.byte_array_end_index = byte_array_end_index


class DroneEncoder:
    # TO DO: A cumsum will prevent the for loop but it is kind of convulated for not very much
    def get_section_headers(
        self,
        encoded_events_list: List[bytearray],
        non_empty_events_list: List[Events],
        json_convertion_parameter: JsonConvertionParameter,
    ) -> List[SectionHeader]:
        byte_array_start_index = struct.calcsize(json_convertion_parameter.fmt_header)
        section_headers: List[SectionHeader] = []
        for non_empty_events, encoded_events in zip(
            non_empty_events_list, encoded_events_list
        ):
            section_header = SectionHeader(
                json_convertion_parameter.fmt_section_header,
                non_empty_events.id,
                byte_array_start_index,
                byte_array_start_index + len(encoded_events),
            )
            byte_array_start_index += len(encoded_events)
            section_headers.append(section_header)
        return section_headers

    @staticmethod
    def dance_size(
        section_headers: List[SectionHeader],
        encoded_events_list: List[bytearray],
        json_convertion_parameter: JsonConvertionParameter,
    ) -> int:
        return (
            struct.calcsize(json_convertion_parameter.fmt_header)
            + len(section_headers)
            * struct.calcsize(json_convertion_parameter.fmt_section_header)
            + sum(len(encoded_events) for encoded_events in encoded_events_list)
        )

    @staticmethod
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
        self, drone: Drone, json_convertion_parameter: JsonConvertionParameter
    ) -> List[int]:
        non_empty_events_list = drone.non_empty_events_list
        encoded_events_list = [
            encode_events(non_empty_events)
            for non_empty_events in non_empty_events_list
        ]
        section_headers = self.get_section_headers(
            encoded_events_list, non_empty_events_list, json_convertion_parameter
        )
        header = Header(
            json_convertion_parameter.fmt_header,
            json_convertion_parameter.magic_number,
            self.dance_size(
                section_headers, encoded_events_list, json_convertion_parameter
            ),
            len(non_empty_events_list),
        )
        return self.assemble_dance(header, section_headers, encoded_events_list)
