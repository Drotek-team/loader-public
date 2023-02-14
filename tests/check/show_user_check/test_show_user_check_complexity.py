import time

from loader.check.show_user_check import get_show_user_report
from loader.show_env.show_user.generate_show_user import STANDARD_SHOW_USER

ACTIVE = False


def test_su_to_ss_complexity() -> None:
    if not ACTIVE:
        return
    time_begin = time.time()
    get_show_user_report(STANDARD_SHOW_USER)
    second_time = time.time() - time_begin
    raise ValueError(second_time)
