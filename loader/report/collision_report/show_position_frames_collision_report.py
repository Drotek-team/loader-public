import itertools
from typing import List, Optional

from loader.parameter.iostar_physic_parameter import IOSTAR_PHYSIC_PARAMETER
from loader.report.base import BaseReport
from loader.show_env.show_user import ShowUser

from .collision_math import CollisionInfraction, get_optimized_collision_infractions
from .migration.show_position_frames import ShowPositionFrame, ShowPositionFrames


def get_collision_infractions(
    show_position_frame: ShowPositionFrame,
) -> List[CollisionInfraction]:
    on_ground_collision_infractions = get_optimized_collision_infractions(
        show_position_frame.frame,
        show_position_frame.on_ground_indices,
        show_position_frame.on_ground_positions,
        IOSTAR_PHYSIC_PARAMETER.security_distance_on_ground,
        in_air=False,
    )
    in_air_collision_infractions = get_optimized_collision_infractions(
        show_position_frame.frame,
        show_position_frame.in_air_indices,
        show_position_frame.in_air_positions,
        IOSTAR_PHYSIC_PARAMETER.security_distance_in_air,
        in_air=True,
    )
    return on_ground_collision_infractions + in_air_collision_infractions


def get_collision_infractions_from_show_position_frames(
    show_position_frames: ShowPositionFrames,
) -> List[CollisionInfraction]:
    return list(
        itertools.chain.from_iterable(
            [
                get_collision_infractions(show_position_frame)
                for show_position_frame in show_position_frames.show_position_frames
            ],
        ),
    )


class CollisionReport(BaseReport):
    collision_infractions: List[CollisionInfraction] = []


def su_to_spf(show_user: ShowUser) -> ShowPositionFrames:
    return ShowPositionFrames.create_from_show_user(show_user)


def get_collision_report(
    show_user: ShowUser,
) -> Optional[CollisionReport]:
    collision_infractions = get_collision_infractions_from_show_position_frames(
        su_to_spf(show_user),
    )
    if collision_infractions:
        return CollisionReport(collision_infractions=collision_infractions)
    return None
