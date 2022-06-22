import struct
from typing import List

from .drone import Drone
from .events.events import Events


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

    @staticmethod
    def encode_drone_events(dance_binary: bytearray, events: List[Events]):
        for event in events:
            dance_binary.extend(event.encode())

    def encode(self, drone: Drone) -> List[int]:
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

    # def decode(self, binary, parameter={}):
    #     self._binary = binary
    #     self._parameter = defaultdict(dict, parameter)
    #     self._events_list = []
    #     _, nb_sections = self._decode_header()
    #     for index in range(nb_sections):
    #         events_id, start, end = self._decode_section_header(index)
    #         events = create_events(events_id)
    #         events.decode(
    #             self._get_section_binary(start, end), **self._parameter[events.id]
    #         )
    #         self._events_list.append(events)
    #     return make_events_group(self._events_list)

    # def _decode_header(self):
    #     magic_nb, dance_size, nb_section = struct.unpack(
    #         self.FMT_HEADER, self._get_header_binary()
    #     )
    #     if magic_nb != self.MAGIC_NB:
    #         raise DanceMagicNumberError
    #     elif len(self._binary) > self.max_size:
    #         raise DanceMaxSizeError
    #     elif dance_size != len(self._binary):
    #         raise DanceSizeError
    #     return dance_size, nb_section

    # def _decode_section_header(self, index):
    #     events_id, start, end = struct.unpack(
    #         self.FMT_SECTION_HEADER, self._get_section_header_binary(index)
    #     )
    #     if start >= end:
    #         raise DanceSectionHeaderIndexError
    #     return events_id, start, end

    # def _get_header_binary(self):
    #     return self._binary[: struct.calcsize(self.FMT_HEADER)]

    # def _get_section_header_binary(self, index):
    #     return self._binary[
    #         struct.calcsize(self.FMT_HEADER)
    #         + self.struct.calcsize(self.FMT_SECTION_HEADER)
    #         * index : struct.calcsize(self.FMT_HEADER)
    #         + self.struct.calcsize(self.FMT_SECTION_HEADER) * (index + 1)
    #     ]

    # def _get_section_binary(self, start, end):
    #     return self._binary[start : end + 1]

    # def decode(show, parameter={}):
    #     show = json.loads(show)["show"]
    #     families = []
    #     for family_id, family in enumerate(show["families"]):
    #         drones = []
    #         for drone_id, drone in enum
