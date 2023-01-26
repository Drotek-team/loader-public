import time

from src.check.performance_check.migration.su_to_stp import su_to_stp

from ...show_env.show_user.generate_show_user import STANDARD_SHOW_USER

ACTIVE = False


def test_show_trajectory_performance_check_complexity():
    if not ACTIVE:
        return
    time_begin = time.time()
    su_to_stp(STANDARD_SHOW_USER)
    second_time = time.time() - time_begin
    raise ValueError(second_time)
