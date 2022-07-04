import struct
from typing import List, Tuple

from .drone import Drone
from .drone_encoder_report import DecodeReport
from .events.events import Events
from .events.events_encoder import decode_events, encode_events


class DroneEncoder:
    MAGIC_NB = 0xAA55
    FMT_HEADER = ">HIB"
    FMT_SECTION_HEADER = ">BII"

    def encode_header(
        self, dance_binary: bytearray, dance_size: int, nb_non_empty_events: int
    ) -> None:
        dance_binary.extend(
            struct.pack(
                self.FMT_HEADER,
                self.MAGIC_NB,
                dance_size,
                nb_non_empty_events,
            )
        )

    def encode_section_headers(
        self,
        dance_binary: bytearray,
        section_start: int,
        non_empty_events: List[Events],
    ) -> None:
        binary_start = section_start
        for events in non_empty_events:
            binary_end = binary_start + events.events_size() - 1
            dance_binary.extend(
                struct.pack(
                    self.FMT_SECTION_HEADER, events.id, binary_start, binary_end
                )
            )
            binary_start = binary_end + 1

    def encode_drone_events(dance_binary: bytearray, all_events: List[Events]) -> None:
        for events in all_events:
            dance_binary.extend(encode_events(events))

    def dance_size(self, drone: Drone) -> int:
        non_empty_events = [event for event in drone.events_list if event.event_size()]
        section_start = struct.calcsize(self.FMT_HEADER) + struct.calcsize(
            self.FMT_SECTION_HEADER
        ) * len(non_empty_events)
        return section_start + sum(events.events_size() for events in drone.events_list)

    def encode_drone(self, drone: Drone) -> List[int]:
        dance_binary = bytearray()
        non_empty_events = [event for event in drone.events_list if event.event_size()]
        section_start = struct.calcsize(self.FMT_HEADER) + struct.calcsize(
            self.FMT_SECTION_HEADER
        ) * len(non_empty_events)
        dance_size = section_start + sum(
            event.event_size() for event in drone.events_list
        )
        self.encode_header(dance_binary, dance_size, len(non_empty_events))
        self.encode_section_headers(dance_binary, section_start, non_empty_events)
        self.encode_drone_events(dance_binary, drone.events_list)
        return list(map(int, dance_binary))

    def decode_header(self, binary: bytearray, decode_report: DecodeReport) -> int:
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

    def _get_section_binary(self, start, end):
        return self._binary[start : end + 1]

    def decode_drone(
        self, binary: List[int], drone_index: int, decode_report: DecodeReport
    ) -> Drone:
        drone = Drone(drone_index)
        byte_array = bytearray(binary)
        nb_sections = self.decode_header(byte_array, decode_report)
        for index in range(nb_sections):
            events_id, start, end = self.decode_section_header(byte_array, index)
            events = drone.get_events_by_index(events_id)
            events.decode(byte_array[start : end + 1])
            self._events_list.append(events)
