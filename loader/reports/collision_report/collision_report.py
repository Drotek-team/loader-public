from typing import List, Optional

from loader.parameters import IostarPhysicParameters
from loader.reports.base import BaseReport
from loader.shows.show_user import ShowUser

from .collision_infraction import CollisionInfraction


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
            show_user,
            collision_distance=(
                physic_parameters.security_distance_in_air if physic_parameters else None
            ),
            is_partial=is_partial,
        )
        if collision_infractions:
            return CollisionReport(collision_infractions=collision_infractions)
        return None
