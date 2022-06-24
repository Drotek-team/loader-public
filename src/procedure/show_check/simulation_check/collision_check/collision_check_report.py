from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class CollisionInfo:
    timecode: int
    first_drone_index: int
    second_drone_index: int
    in_air: bool


class CollisionCheckReport:
    def __init__(self):
        self.validation = False
        self.collisions_info: List[CollisionInfo] = []

    def update_collisions(
        self,
        timecode: int,
        endangered_couples_on_ground: List[Tuple[int, int]],
        in_air: bool,
    ) -> None:
        for endangered_couple_on_ground in endangered_couples_on_ground:
            self.collisions_info.append(
                CollisionInfo(
                    timecode=timecode,
                    first_drone_index=endangered_couple_on_ground[0],
                    second_drone_index=endangered_couple_on_ground[1],
                    in_air=in_air,
                )
            )
