import struct

from ....drones_px4.drone_px4.events.events import Events

### TO DO: get_data unrecognized, it is not very pretty but only here and the cause of a "good" architecture choice, see if it can be help easily or just leave it
def encode_events(events: Events) -> bytearray:
    event_size = events.event_size
    binary = bytearray(event_size * len(events.events))
    for cpt_event, event_data in enumerate(events.events):
        try:
            binary[cpt_event * event_size : (cpt_event + 1) * event_size] = struct.pack(
                events.format, *event_data.get_data()
            )
        except struct.error:
            raise ValueError(
                cpt_event, event_size, events.format, *event_data.get_data()
            )
    return binary


def decode_events(events: Events, byte_array: bytearray) -> None:
    for event_index in range(0, len(byte_array), events.event_size):
        events.add_data(
            struct.unpack(
                events.format, byte_array[event_index : event_index + events.event_size]
            )
        )
