from dataclasses import dataclass
import struct


@dataclass(frozen=True)
class BytesManager:
    def __init__(self, fmt: str):
        self.fmt = fmt

    @property
    def bytes_data(self) -> bytes:
        data_list = [value for _, value in self.__dict__.items()][1:]
        return struct.pack(self.fmt, *data_list)


class Header(BytesManager):
    def __init__(
        self,
        fmt_header: str,  # binary format of the header
        magic_number: int,  # Magic number with no purpose for the moment
        dance_size: int,  # Dance size in bytes
        number_non_empty_events: int,  # number of the events which contain at least one drone
    ):
        BytesManager.__init__(self, fmt_header)
        self.magic_number = magic_number
        self.dance_size = dance_size
        self.number_non_empty_events = number_non_empty_events


class SectionHeader(BytesManager):
    def __init__(
        self,
        fmt_section_header: str,  # binary format of the section header
        event_id: int,  # index associate to the type of events
        byte_array_start_index: int,  # index which indicates the start of the section in the binary
        byte_array_end_index: int,  # index which indicates the end of the section in the binary
    ):
        BytesManager.__init__(self, fmt_section_header)
        self.event_id = event_id
        self.byte_array_start_index = byte_array_start_index
        self.byte_array_end_index = byte_array_end_index
