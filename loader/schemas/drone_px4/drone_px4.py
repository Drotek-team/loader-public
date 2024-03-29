import struct
from typing import TYPE_CHECKING, Any, List, Tuple

from tqdm import tqdm

from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS, MagicNumber

from .binary import Header, SectionHeader
from .events import ColorEvents, Events, EventsType, FireEvents, PositionEvents

if TYPE_CHECKING:
    from loader.schemas.iostar_json_gcs.iostar_json_gcs import IostarJsonGcs
    from loader.schemas.show_user import (
        ColorEventUser,
        DroneUser,
        FireEventUser,
        PositionEventUser,
        ShowUser,
    )


class DronePx4:
    def __init__(self, index: int, magic_number: MagicNumber) -> None:
        self.index = index
        self.position_events = PositionEvents(magic_number)
        self.color_events = ColorEvents(magic_number)
        self.fire_events = FireEvents(magic_number)
        self.events_dict = {
            events.id_: events
            for events in [self.position_events, self.color_events, self.fire_events]
        }
        self.magic_number = magic_number

    def __eq__(self, other_drone_px4: object) -> bool:
        if not isinstance(other_drone_px4, DronePx4):
            return False
        return self.index == self.index and self.events_dict == other_drone_px4.events_dict

    def add_position(self, frame: int, xyz: Tuple[int, int, int]) -> None:
        self.position_events.add_timecode_xyz(frame, xyz)

    def add_color(
        self,
        frame: int,
        rgbw: Tuple[int, int, int, int],
        *,
        interpolate: bool = False,
    ) -> None:
        self.color_events.add_timecode_rgbw(frame, rgbw, interpolate=interpolate)

    def add_fire(self, frame: int, channel: int, duration: int) -> None:
        self.fire_events.add_timecode_channel_duration(frame, channel, duration)

    def get_events_by_index(self, event_type: EventsType) -> Events[Any]:
        return self.events_dict[event_type]

    @property
    def non_empty_events_list(self) -> List[Events[Any]]:
        return [events for events in self.events_dict.values() if len(events) != 0]

    @classmethod
    def from_binary(cls, index: int, binary: List[int]) -> "DronePx4":
        byte_array = bytearray(binary)
        header, section_headers = get_header_section_header(byte_array)
        drone_px4 = DronePx4(index, header.magic_number)
        for section_header in section_headers:
            decode_events(
                drone_px4.get_events_by_index(section_header.event_id),
                byte_array[
                    section_header.byte_array_start_index : section_header.byte_array_end_index + 1
                ],
            )
        return drone_px4

    @classmethod
    def to_binary(cls, drone_px4: "DronePx4") -> List[int]:
        non_empty_events_list = drone_px4.non_empty_events_list
        encoded_events_list = [
            encode_events(non_empty_events) for non_empty_events in non_empty_events_list
        ]
        section_headers = get_section_headers(encoded_events_list, non_empty_events_list)
        header = Header(
            fmt_header=JSON_BINARY_PARAMETERS.fmt_header,
            magic_number=drone_px4.magic_number,
            dance_size=dance_size(section_headers, encoded_events_list),
            number_non_empty_events=len(non_empty_events_list),
        )
        return assemble_dance(header, section_headers, encoded_events_list)

    @classmethod
    def from_show_user(cls, show_user: "ShowUser") -> List["DronePx4"]:
        return [
            drone_user_to_drone_px4(drone_user)
            for drone_user in tqdm(
                show_user.drones_user,
                desc="Converting show user to autopilot format",
                unit="drone",
            )
        ]

    @classmethod
    def from_show_user_in_matrix(cls, show_user: "ShowUser") -> List[List[List["DronePx4"]]]:
        return [
            [
                [drone_user_to_drone_px4(drone_user) for drone_user in family_drones_user]
                for family_drones_user in row
            ]
            for row in tqdm(
                show_user.drones_user_in_matrix,
                desc="Converting show user to autopilot format",
                unit="row",
            )
        ]

    @classmethod
    def from_iostar_json_gcs(cls, iostar_json_gcs: "IostarJsonGcs") -> List["DronePx4"]:
        return [
            DronePx4.from_binary(
                family_index * iostar_json_gcs.nb_drones_per_family + drone_index,
                binary_dance.dance,
            )
            for family_index, family in tqdm(
                enumerate(iostar_json_gcs.show.families),
                total=len(iostar_json_gcs.show.families),
                desc="Converting iostar json gcs to autopilot format",
                unit="family",
            )
            for drone_index, binary_dance in enumerate(family.drones)
        ]


def get_header_section_header(
    byte_array: bytearray,
) -> Tuple[Header, List[SectionHeader]]:
    header_data = struct.unpack(
        JSON_BINARY_PARAMETERS.fmt_header,
        byte_array[: struct.calcsize(JSON_BINARY_PARAMETERS.fmt_header)],
    )
    header = Header(
        fmt_header=JSON_BINARY_PARAMETERS.fmt_header,
        magic_number=MagicNumber(header_data[0]),
        dance_size=header_data[1],
        number_non_empty_events=header_data[2],
    )

    section_headers: List[SectionHeader] = []
    byte_begin_index = struct.calcsize(JSON_BINARY_PARAMETERS.fmt_header)
    byte_step_index = struct.calcsize(JSON_BINARY_PARAMETERS.fmt_section_header)
    for event_index in range(header.number_non_empty_events):
        section_header_data = struct.unpack(
            JSON_BINARY_PARAMETERS.fmt_section_header,
            byte_array[
                byte_begin_index + byte_step_index * event_index : byte_begin_index
                + byte_step_index * (event_index + 1)
            ],
        )
        section_headers.append(
            SectionHeader(
                fmt_section_header=JSON_BINARY_PARAMETERS.fmt_section_header,
                event_id=section_header_data[0],
                byte_array_start_index=section_header_data[1],
                byte_array_end_index=section_header_data[2],
            ),
        )
    return header, section_headers


def decode_events(events: Events[Any], byte_array: bytearray) -> None:
    for event_index in range(0, len(byte_array), events.event_size):
        events.add_data(
            list(
                struct.unpack(
                    events.format_,
                    byte_array[event_index : event_index + events.event_size],
                ),
            ),
        )


def get_section_headers(
    encoded_events_list: List[bytearray],
    non_empty_events_list: List[Events[Any]],
) -> List[SectionHeader]:
    byte_array_start_index = struct.calcsize(JSON_BINARY_PARAMETERS.fmt_header) + len(
        non_empty_events_list,
    ) * struct.calcsize(JSON_BINARY_PARAMETERS.fmt_section_header)
    section_headers: List[SectionHeader] = []
    for non_empty_events, encoded_events in zip(
        non_empty_events_list,
        encoded_events_list,
    ):
        section_header = SectionHeader(
            fmt_section_header=JSON_BINARY_PARAMETERS.fmt_section_header,
            event_id=non_empty_events.id_,
            byte_array_start_index=byte_array_start_index,
            byte_array_end_index=byte_array_start_index + len(encoded_events) - 1,
        )
        byte_array_start_index += len(encoded_events)
        section_headers.append(section_header)
    return section_headers


def dance_size(
    section_headers: List[SectionHeader],
    encoded_events_list: List[bytearray],
) -> int:
    return (
        struct.calcsize(JSON_BINARY_PARAMETERS.fmt_header)
        + len(section_headers) * struct.calcsize(JSON_BINARY_PARAMETERS.fmt_section_header)
        + sum(len(encoded_events) for encoded_events in encoded_events_list)
    )


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
    return list(dance_binary)


def encode_events(events: Events[Any]) -> bytearray:
    event_size = events.event_size
    binary = bytearray(event_size * len(events))
    for cpt_event, event_data in enumerate(events):
        binary[cpt_event * event_size : (cpt_event + 1) * event_size] = struct.pack(
            events.format_,
            *event_data.get_data(events.magic_number),
        )
    return binary


def add_position_events_user(
    drone_px4: DronePx4,
    position_events_user: List["PositionEventUser"],
) -> None:
    for position_event_user in position_events_user:
        drone_px4.add_position(
            position_event_user.frame,
            JSON_BINARY_PARAMETERS.from_user_xyz_to_px4_xyz(
                position_event_user.xyz,
            ),
        )


def add_color_events_user(
    drone_px4: DronePx4,
    color_events_user: List["ColorEventUser"],
) -> None:
    for color_event_user in color_events_user:
        drone_px4.add_color(
            color_event_user.frame,
            JSON_BINARY_PARAMETERS.from_user_rgbw_to_px4_rgbw(
                color_event_user.rgbw,
            ),
            interpolate=color_event_user.interpolate,
        )


def add_fire_events_user(
    drone_px4: DronePx4,
    fire_events_user: List["FireEventUser"],
) -> None:
    for fire_event_user in fire_events_user:
        drone_px4.add_fire(
            fire_event_user.frame,
            fire_event_user.channel,
            fire_event_user.duration,
        )


def drone_user_to_drone_px4(
    drone_user: "DroneUser",
) -> DronePx4:
    # TODO(jonathan): switch to new magic number by default # noqa: FIX002
    drone_px4 = DronePx4(drone_user.index, MagicNumber.new)
    add_position_events_user(drone_px4, drone_user.position_events)
    add_color_events_user(
        drone_px4,
        drone_user.color_events,
    )
    add_fire_events_user(
        drone_px4,
        drone_user.fire_events,
    )
    return drone_px4
