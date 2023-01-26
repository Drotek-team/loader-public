import time

from ...show_env.show_user.generate_show_user import STANDARD_SHOW_USER
from .show_simulation_collision_check import stc_to_ss, su_to_stc

ACTIVE = False


def test_su_to_ss_complexity():
    if not ACTIVE:
        return
    time_begin = time.time()
    stc = su_to_stc(STANDARD_SHOW_USER)
    first_time = time.time() - time_begin
    stc_to_ss(stc)
    second_time = time.time() - time_begin
    raise ValueError(first_time, second_time)
