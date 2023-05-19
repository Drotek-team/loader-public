from typing import List, Optional

from loader.parameters import IostarPhysicParameters
from loader.report.base import BaseReport
from loader.shows.show_position_frame import ShowPositionFrame
from loader.shows.show_user import ShowUser

from .collision_math import CollisionInfraction


class CollisionReport(BaseReport):
    collision_infractions: List[CollisionInfraction] = []

    @classmethod
    def generate(
        cls,
        show_user: ShowUser,
        *,
        physic_parameters: Optional[IostarPhysicParameters] = None,
        is_partial: bool = False,
    ) -> Optional["CollisionReport"]:
        collision_infractions = CollisionInfraction.generate(
            ShowPositionFrame.from_show_user(show_user, is_partial=is_partial),
            collision_distance=(
                physic_parameters.security_distance_in_air if physic_parameters else None
            ),
        )
        if collision_infractions:
            return CollisionReport(collision_infractions=collision_infractions)
        return None
