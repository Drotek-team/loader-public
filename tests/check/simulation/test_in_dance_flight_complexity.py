import time

from loader.check.simulation.in_dance_flight_simulation import (
    PositionEventUser,
    in_dance_flight_simulation,
)

NB_ITERATION = 28_800
ACTIVE = False


def test_get_flight_simulation_complexity() -> None:
    if not ACTIVE:
        return
    position_events = [
        PositionEventUser(frame=240 + iteration_index, xyz=(0.0, 0.0, 1.0))
        for iteration_index in range(NB_ITERATION)
    ]
    time_begin = time.time()
    in_dance_flight_simulation(position_events)
    second_time = time.time() - time_begin
    raise ValueError(
        second_time,
    )
