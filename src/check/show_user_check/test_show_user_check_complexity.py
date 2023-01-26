import time

from ...show_env.show_user.generate_show_user import STANDARD_SHOW_USER
from .show_user_check import apply_show_user_check

ACTIVE = False


def test_su_to_ss_complexity():
    if not ACTIVE:
        return
    time_begin = time.time()
    apply_show_user_check(STANDARD_SHOW_USER)
    second_time = time.time() - time_begin
    raise ValueError(second_time)
