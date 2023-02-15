from loader.show_env.show_user import ShowUser

from .show_position_frames import ShowPositionFrames


def su_to_spf(show_user: ShowUser) -> ShowPositionFrames:
    return ShowPositionFrames.create_from_show_user(show_user)
