import time

from loader.report.collision_report.show_position_frames_collision_report import (
    su_to_spf,
)
from loader.show_env.show_user.generate_show_user import STANDARD_SHOW_USER

ACTIVE = False


# TODO: Use pytest-benchmark or similar
def test_su_to_spf_complexity() -> None:
    if not ACTIVE:
        return
    time_begin = time.time()
    su_to_spf(STANDARD_SHOW_USER)
    first_time = time.time() - time_begin
    raise ValueError(first_time)
