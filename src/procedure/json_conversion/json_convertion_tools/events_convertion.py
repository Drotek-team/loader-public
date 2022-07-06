import struct

import numpy as np

from ....drones_manager.drone.events.events import Events


def encode_events(events: Events) -> bytearray:
    event_size = events.event_size
    binary = bytearray(event_size * len(events.event_list))
    for cpt_event, event_data in enumerate(events.event_list):
        binary[cpt_event * event_size : (cpt_event + 1) * event_size] = struct.pack(
            events.format, *event_data.get_raw_data()
        )
    return binary


def decode_events(events: Events, byte_array: bytearray) -> None:
    for event_index in range(0, len(byte_array), events.event_size):
        # if (
        #     struct.calcsize(events.format)
        #     != len(byte_array[event_index : event_index + events.event_size]) - 1
        # ):
        #     raise SalaryNotInRangeError(
        #         len(byte_array[event_index : event_index + events.event_size])
        #     )
        events.add_raw_data(
            struct.unpack(
                events.format, byte_array[event_index : event_index + events.event_size]
            )
        )
