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


@dataclass(frozen=True)
class SectionHeader(BytesManager):
    fmt_section_header: str
    event_id: int
    byte_array_start_index: int
    byte_array_end_index: int


class DroneEncoder:
    MAGIC_NUMBER = 0xAA55
    FMT_HEADER = ">HIB"
    FMT_SECTION_HEADER = ">BII"

    def encode_drone(self, drone: Drone) -> List[int]:
        dance_binary = bytearray()
        non_empty_events_list = drone.non_empty_events_list
        header = Header(
            self.FMT_HEADER, self.MAGIC_NUMBER, 0, len(non_empty_events_list)
        )
        dance_binary.extend(header.bytes_data)

        for non_empty_events in non_empty_events_list:
            section_header = SectionHeader(
                self.FMT_SECTION_HEADER, non_empty_events.id, header.size
            )
            dance_binary.extend(section_header.bytes_data)
        for non_empty_events in non_empty_events_list:
            dance_binary.extend(encode_events(non_empty_events))
        return list(map(int, dance_binary))

    def decode_header(self, binary: bytearray) -> int:
        magic_nb, dance_size, nb_section = struct.unpack(
            self.FMT_HEADER, binary[: struct.calcsize(self.FMT_HEADER)]
        )
        ### These check belong in the procedure, not the object ###
        # if magic_nb == self.MAGIC_NB:
        #     decode_report.validation = True
        # if dance_size != len(binary):
        #     decode_report.validation = True
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
        # if start < end:
        #     decode_report.validation = True
        return events_id, start, end

    def decode_drone(self, binary: List[int], drone_index: int) -> Drone:
        drone = Drone(drone_index)
        byte_array = bytearray(binary)
        nb_sections = self.decode_header(byte_array)
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
