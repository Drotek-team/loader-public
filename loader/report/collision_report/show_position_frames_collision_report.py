from typing import List, Optional

from loader.report.base import BaseReport
from loader.show_env.show_user import ShowUser

from .collision_math import CollisionInfraction
from .migration.su_to_spf import su_to_spf


class CollisionReport(BaseReport):
    collision_infractions: List[CollisionInfraction] = []

    @classmethod
    def generate(
        cls,
        show_user: ShowUser,
    ) -> Optional["CollisionReport"]:
        collision_infractions = CollisionInfraction.generate(
            su_to_spf(show_user),
        )
        if collision_infractions:
            return CollisionReport(collision_infractions=collision_infractions)
        return None
