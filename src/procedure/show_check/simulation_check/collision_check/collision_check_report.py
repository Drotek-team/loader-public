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

    def update(self) -> None:
        self.validation = len(self.collisions_info) == 0

    def update_collisions_info(
        self,
        timecode: int,
        endangered_couples: List[Tuple[int, int]],
        in_air: bool,
    ) -> None:
        for endangered_couple in endangered_couples:
            self.collisions_info.append(
                CollisionInfo(
                    timecode=timecode,
                    first_drone_index=endangered_couple[0],
                    second_drone_index=endangered_couple[1],
                    in_air=in_air,
                )
            )
