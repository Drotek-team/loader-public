from typing import List, Optional

from loader.parameter.iostar_physic_parameter import IostarPhysicParameter
from loader.report.base import BaseReport
from loader.show_env.show_position_frame import ShowPositionFrame
from loader.show_env.show_user import ShowUser

from .collision_math import CollisionInfraction


class CollisionReport(BaseReport):
    collision_infractions: List[CollisionInfraction] = []

    @classmethod
    def generate(
        cls,
        show_user: ShowUser,
        *,
        physic_parameter: Optional[IostarPhysicParameter] = None,
        is_partial: bool = False,
    ) -> Optional["CollisionReport"]:
        collision_infractions = CollisionInfraction.generate(
            ShowPositionFrame.from_show_user(show_user, is_partial=is_partial),
            collision_distance=(
                physic_parameter.security_distance_in_air if physic_parameter else None
            ),
        )
        if collision_infractions:
            return CollisionReport(collision_infractions=collision_infractions)
        return None
