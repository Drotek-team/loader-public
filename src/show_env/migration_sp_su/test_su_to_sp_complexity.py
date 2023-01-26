import time

from ...show_env.show_user.generate_show_user import STANDARD_SHOW_USER
from .su_to_sp import su_to_sp

ACTIVE = False


def test_su_to_ss_complexity():
    if not ACTIVE:
        return
    time_begin = time.time()
    su_to_sp(STANDARD_SHOW_USER)
    second_time = time.time() - time_begin
    raise ValueError(second_time)
