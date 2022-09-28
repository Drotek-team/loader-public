import struct
from dataclasses import dataclass
from ....drones_user.drone.drone import DroneExport
from ....parameter.parameter import IostarParameter


def apply_reformat_events(
    drone_export: DroneExport, iostar_parameter: IostarParameter
) -> None:
    drone_export.position_events.scale_data_events(
        iostar_parameter.position_reformat_factor
    )


def unapply_reformat_events(
    drone_export: DroneExport, iostar_parameter: IostarParameter
) -> None:
    drone_export.position_events.scale_data_events(
        1 / iostar_parameter.position_reformat_factor
    )


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
        fmt_header: str,
        magic_number: int,
        dance_size: int,
        number_non_empty_events: int,
    ):
        BytesManager.__init__(self, fmt_header)
        self.magic_number = magic_number
        self.dance_size = dance_size
        self.number_non_empty_events = number_non_empty_events


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
