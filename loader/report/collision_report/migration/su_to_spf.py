from loader.show_env.show_user import ShowUser

from .show_position_frames import ShowPositionFrames


def su_to_spf(show_user: ShowUser, *, is_partial: bool = False) -> ShowPositionFrames:
    return ShowPositionFrames.create_from_show_user(show_user, is_partial=is_partial)
