import time

from ...show_env.show_user.generate_show_user import STANDARD_SHOW_USER
from .show_trajectory_performance_check import apply_show_trajectory_performance_check

ACTIVE = False


def test_show_trajectory_performance_check_complexity():
    if not ACTIVE:
        return
    time_begin = time.time()
    apply_show_trajectory_performance_check(STANDARD_SHOW_USER)
    second_time = time.time() - time_begin
    raise ValueError(second_time)
