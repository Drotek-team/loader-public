import struct
from dataclasses import dataclass


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
