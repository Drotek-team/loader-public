import struct

from ..show_px4.drone_px4.events.events import Events


def encode_events(events: Events) -> bytearray:
    event_size = events.event_size
    binary = bytearray(event_size * len(events.events))
    for cpt_event, event_data in enumerate(events.events):
        try:
            # IMPROVE: An append() would be more elegant here
            binary[cpt_event * event_size : (cpt_event + 1) * event_size] = struct.pack(
                events.format_, *event_data.get_data()
            )
        except struct.error:
            msg = f"{cpt_event} {event_size}  {events.format_}"
            raise ValueError(msg) from None
    return binary


def decode_events(events: Events, byte_array: bytearray) -> None:
    for event_index in range(0, len(byte_array), events.event_size):
        events.add_data(
            struct.unpack(
                events.format_,
                byte_array[event_index : event_index + events.event_size],
            )
        )
