import struct
from dataclasses import dataclass
from typing import List, Tuple

from .drone import Drone
from .events.events import Events
from .events.events_encoder import decode_events, encode_events


class BytesManager:
    @property
    def bytes_data(self) -> bytes:
        data_list = [value for _, value in self.__dict__.items()]
        return struct.pack(*data_list)

    @property
    def size(self) -> int:
        return len(self.bytes_data)


@dataclass(frozen=True)
class Header(BytesManager):
    fmt_header: str
    magic_number: int
    dance_size: int
    number_non_empty_events: int


@dataclass
class SectionHeader(BytesManager):
    fmt_section_header: str
    event_id: int
    byte_array_start_index: int
    byte_array_end_index: int


class DroneEncoder:
    MAGIC_NUMBER = 0xAA55
    FMT_HEADER = ">HIB"
    FMT_SECTION_HEADER = ">BII"

    def get_section_headers(
        self, encoded_events_list: List[bytearray], non_empty_events_list: List[Events]
    ) -> List[SectionHeader]:
        byte_array_start_index = 0
        section_headers: List[SectionHeader] = []
        for encoded_events, non_empty_events in zip(
            encoded_events_list, non_empty_events_list
        ):
            section_header = SectionHeader(
                self.FMT_SECTION_HEADER,
                non_empty_events.id,
                byte_array_start_index,
                byte_array_start_index + len(encoded_events),
            )
            byte_array_start_index += len(encoded_events)
            section_headers.append(section_header)
        return section_headers

    @staticmethod
    def update_section_headers(
        section_headers: List[SectionHeader], header: Header
    ) -> None:
        section_headers_size = sum(
            section_header.size for section_header in section_headers
        )
        for section_header in section_headers:
            section_header.byte_array_start_index += header.size + section_headers_size
            section_header.byte_array_end_index += header.size + section_headers_size

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

    def encode_drone(self, drone: Drone) -> List[int]:
        non_empty_events_list = drone.non_empty_events_list
        encoded_events_list = [
            encode_events(non_empty_events)
            for non_empty_events in non_empty_events_list
        ]
        section_headers = self.get_section_headers(
            encoded_events_list, non_empty_events_list
        )
        dance_size = sum(
            len(encoded_events) for encoded_events in encoded_events_list
        ) + sum(len(section_header.bytes_data) for section_header in section_headers)
        header = Header(
            self.FMT_HEADER,
            self.MAGIC_NUMBER,
            dance_size,
            len(non_empty_events_list),
        )
        self.update_section_headers(section_headers, header)
        return self.assemble_dance(header, section_headers, encoded_events_list)

    def decode_header(self, byte_array: bytearray) -> int:
        magic_nb, dance_size, nb_section = struct.unpack(
            self.FMT_HEADER, byte_array[: struct.calcsize(self.FMT_HEADER)]
        )
        return nb_section

    def decode_section_header(
        self,
        byte_array: bytearray,
        index: int,
    ) -> Tuple[int, int, int]:
        events_id, start, end = struct.unpack(
            self.FMT_SECTION_HEADER,
            byte_array[
                struct.calcsize(self.FMT_HEADER)
                + struct.calcsize(self.FMT_SECTION_HEADER)
                * index : struct.calcsize(self.FMT_HEADER)
                + struct.calcsize(self.FMT_SECTION_HEADER) * (index + 1)
            ],
        )
        return events_id, start, end

    def decode_drone(
        self,
        binary: List[int],
        drone_index: int,
    ) -> Drone:
        drone = Drone(drone_index)
        byte_array = bytearray(binary)
        nb_sections = self.decode_header(byte_array)

        ### These check belong in the procedure, not the object !!!###
        # if magic_nb == self.MAGIC_NB:
        #     decode_report.validation = True
        # if dance_size != len(binary):
        #     decode_report.validation = True

        # if start < end:
        #     decode_report.validation = True
        for index in range(nb_sections):
            (
                events_id,
                events_start_index,
                events_end_index,
            ) = self.decode_section_header(byte_array, index)
            decode_events(
                drone.get_events_by_index(events_id),
                byte_array[events_start_index : events_end_index + 1],
            )
