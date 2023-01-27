import struct

from ..show_px4.drone_px4.events.events import Events


def encode_events(events: Events) -> bytearray:
    event_size = events.event_size
    binary = bytearray(event_size * len(events))
    for cpt_event, event_data in enumerate(events):
        try:
            binary[cpt_event * event_size : (cpt_event + 1) * event_size] = struct.pack(
                events.format_, *event_data.get_data
            )
        except struct.error:
            msg = f"{cpt_event} {event_size}  {events.format_} {event_data.get_data}"
            raise ValueError(msg) from None
    return binary


def decode_events(events: Events, byte_array: bytearray) -> None:
    for event_index in range(0, len(byte_array), events.event_size):
        try:
            events.add_data(
                list(
                    struct.unpack(
                        events.format_,
                        byte_array[event_index : event_index + events.event_size],
                    )
                )
            )
        except struct.error:
            msg = (
                f"{events.format_} {event_index}  {events.event_size} {len(byte_array)}"
            )
            raise ValueError(msg) from None
