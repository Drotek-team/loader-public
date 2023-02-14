import time

from loader.check.show_px4_check import apply_show_px4_report
from loader.show_env.show_user.generate_show_user import STANDARD_SHOW_USER

ACTIVE = False


def test_su_to_ss_complexity() -> None:
    if not ACTIVE:
        return
    time_begin = time.time()
    apply_show_px4_report(STANDARD_SHOW_USER)
    second_time = time.time() - time_begin
    raise ValueError(second_time)
