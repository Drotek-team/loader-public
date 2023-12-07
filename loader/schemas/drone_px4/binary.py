import struct

from pydantic import BaseModel

from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS, LandType, MagicNumber

from .events.events_order import EventsType


class BytesManager(BaseModel):
    @property
    def bytes_data(self) -> bytes:
        raise NotImplementedError


class Header(BytesManager):
    magic_number: MagicNumber  # Magic number with no purpose for the moment
    dance_size: int  # Dance size in bytes
    number_non_empty_events: int  # number of the events which contain at least one drone

    @property
    def bytes_data(self) -> bytes:
        return struct.pack(
            JSON_BINARY_PARAMETERS.fmt_header,
            self.magic_number,
            self.dance_size,
            self.number_non_empty_events,
        )

    @classmethod
    def from_bytes_data(cls, byte_array: bytearray) -> "Header":
        (
            magic_number,
            dance_size,
            number_non_empty_events,
        ) = struct.unpack(JSON_BINARY_PARAMETERS.fmt_header, byte_array)
        return cls(
            magic_number=MagicNumber(magic_number),
            dance_size=dance_size,
            number_non_empty_events=number_non_empty_events,
        )


class Config(BytesManager):
    scale: int
    land_type: LandType

    @property
    def bytes_data(self) -> bytes:
        return struct.pack(JSON_BINARY_PARAMETERS.fmt_config, self.scale, self.land_type.to_int())

    @classmethod
    def from_bytes_data(cls, byte_array: bytearray) -> "Config":
        scale, land_type = struct.unpack(JSON_BINARY_PARAMETERS.fmt_config, byte_array)
        return cls(scale=scale, land_type=LandType.from_int(land_type))


class SectionHeader(BytesManager):
    event_id: EventsType  # index associate to the type of events
    byte_array_start_index: int  # index which indicates the start of the section in the binary
    byte_array_end_index: int  # index which indicates the end of the section in the binary

    @property
    def bytes_data(self) -> bytes:
        return struct.pack(
            JSON_BINARY_PARAMETERS.fmt_section_header,
            self.event_id,
            self.byte_array_start_index,
            self.byte_array_end_index,
        )

    @classmethod
    def from_bytes_data(cls, byte_array: bytearray) -> "SectionHeader":
        (
            event_id,
            byte_array_start_index,
            byte_array_end_index,
        ) = struct.unpack(JSON_BINARY_PARAMETERS.fmt_section_header, byte_array)
        return cls(
            event_id=EventsType(event_id),
            byte_array_start_index=byte_array_start_index,
            byte_array_end_index=byte_array_end_index,
        )
