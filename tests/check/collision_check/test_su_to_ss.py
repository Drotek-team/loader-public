import time

from loader.check.collision_check.show_simulation_collision_check import (
    sct_to_ss,
    su_to_sct,
)
from loader.show_env.show_user.generate_show_user import STANDARD_SHOW_USER

ACTIVE = False


# TODO: Use pytest-benchmark or similar
def test_su_to_ss_complexity() -> None:
    if not ACTIVE:
        return
    time_begin = time.time()
    sct = su_to_sct(STANDARD_SHOW_USER)
    first_time = time.time() - time_begin
    sct_to_ss(sct)
    second_time = time.time() - time_begin
    raise ValueError(first_time, second_time)
