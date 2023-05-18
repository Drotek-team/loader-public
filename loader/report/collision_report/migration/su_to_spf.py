from typing import List

from loader.show_env.show_user import ShowUser

from .show_position_frames import ShowPositionFrame


def su_to_spf(show_user: ShowUser, *, is_partial: bool = False) -> List[ShowPositionFrame]:
    return ShowPositionFrame.create_from_show_user(show_user, is_partial=is_partial)
