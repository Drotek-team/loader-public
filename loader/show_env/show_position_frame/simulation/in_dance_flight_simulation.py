from typing import List

import numpy as np

from loader.show_env.show_user import PositionEventUser

from .position_simulation import SimulationInfo, apply_decimal_number_tolerance


def in_dance_flight_simulation(
    position_events_user: List[PositionEventUser],
) -> List[SimulationInfo]:
    position_events_user_frame = [
        position_event_user.frame for position_event_user in position_events_user
    ]
    position_events_user_x = [
        position_event_user.xyz[0] for position_event_user in position_events_user
    ]
    position_events_user_y = [
        position_event_user.xyz[1] for position_event_user in position_events_user
    ]
    position_events_user_z = [
        position_event_user.xyz[2] for position_event_user in position_events_user
    ]
    desired_frames = list(
        range(
            position_events_user[0].frame,
            position_events_user[-1].frame,
        ),
    )
    flight_positions_x = apply_decimal_number_tolerance(
        np.interp(  # pyright: ignore[reportUnknownMemberType]
            desired_frames,
            position_events_user_frame,
            position_events_user_x,
        ),
    )
    flight_positions_y = apply_decimal_number_tolerance(
        np.interp(  # pyright: ignore[reportUnknownMemberType]
            desired_frames,
            position_events_user_frame,
            position_events_user_y,
        ),
    )
    flight_positions_z = apply_decimal_number_tolerance(
        np.interp(  # pyright: ignore[reportUnknownMemberType]
            desired_frames,
            position_events_user_frame,
            position_events_user_z,
        ),
    )
    return [
        SimulationInfo(
            frame=desired_frame,
            position=np.array(
                (flight_position_x, flight_position_y, flight_position_z),
                dtype=np.float64,
            ),
            in_air=True,
        )
        for desired_frame, flight_position_x, flight_position_y, flight_position_z in zip(
            desired_frames,
            flight_positions_x,
            flight_positions_y,
            flight_positions_z,
        )
    ]