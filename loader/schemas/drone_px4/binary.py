import struct

from pydantic import BaseModel

from .events.events_order import EventsType
from .events.magic_number import MagicNumber


class BytesManager(BaseModel):
    @property
    def bytes_data(self) -> bytes:
        raise NotImplementedError


class Header(BytesManager):
    fmt_header: str  # binary format of the header
    magic_number: MagicNumber  # Magic number with no purpose for the moment
    dance_size: int  # Dance size in bytes
    number_non_empty_events: int  # number of the events which contain at least one drone

    @property
    def bytes_data(self) -> bytes:
        return struct.pack(
            self.fmt_header,
            *[self.magic_number, self.dance_size, self.number_non_empty_events],
        )


class SectionHeader(BytesManager):
    fmt_section_header: str  # binary format of the section header
    event_id: EventsType  # index associate to the type of events
    byte_array_start_index: int  # index which indicates the start of the section in the binary
    byte_array_end_index: int  # index which indicates the end of the section in the binary

    @property
    def bytes_data(self) -> bytes:
        return struct.pack(
            self.fmt_section_header,
            *[self.event_id, self.byte_array_start_index, self.byte_array_end_index],
        )
