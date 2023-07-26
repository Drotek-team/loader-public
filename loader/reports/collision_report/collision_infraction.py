# pyright: reportIncompatibleMethodOverride=false

import itertools
from typing import TYPE_CHECKING, Generator, List, Optional, Set, TypeVar

import numpy as np
from tqdm import tqdm

from loader.parameters import IOSTAR_PHYSIC_PARAMETERS_MAX, IOSTAR_PHYSIC_PARAMETERS_RECOMMENDATION
from loader.reports.base import BaseInfraction, BaseInfractionsSummary, apply_func_on_optional_pair
from loader.schemas import ShowUser
from loader.schemas.show_user.show_position_frame import ShowPositionFrame

if TYPE_CHECKING:
    from numpy.typing import NDArray

T = TypeVar("T")


def get_couple_distance_matrix(
    positions_numpy: "NDArray[np.float64]",
) -> "NDArray[np.float64]":
    config_matrix = np.tril(1e8 * np.ones((len(positions_numpy), len(positions_numpy))))
    return config_matrix + np.linalg.norm(
        positions_numpy[:, None, :] - positions_numpy[None, :, :],
        axis=-1,
    )


class CollisionInfraction(BaseInfraction):
    frame: int
    drone_index_1: int
    drone_index_2: int
    distance: float

    @classmethod
    def _get_collision_infractions(
        cls,
        frame: int,
        local_drone_indices: "NDArray[np.intp]",
        local_drone_positions: "NDArray[np.float64]",
        endangered_distance: float,
    ) -> Generator["CollisionInfraction", None, None]:
        nb_drones_local = len(local_drone_indices)
        couples_distance_matrix_indices = np.array(
            list(range(nb_drones_local * nb_drones_local)),
            dtype=np.intp,
        )
        couple_distance_matrix = get_couple_distance_matrix(
            local_drone_positions,
        ).reshape(
            nb_drones_local * nb_drones_local,
        )
        endangered_couples_distance_matrix_indices = couples_distance_matrix_indices[
            (couple_distance_matrix < endangered_distance)
        ]
        return (
            CollisionInfraction(
                frame=frame,
                drone_index_1=int(
                    local_drone_indices[
                        endangered_couples_distance_matrix_index // nb_drones_local
                    ],
                ),
                drone_index_2=int(
                    local_drone_indices[endangered_couples_distance_matrix_index % nb_drones_local],
                ),
                distance=float(
                    couple_distance_matrix[endangered_couples_distance_matrix_index],
                ),
            )
            for (
                endangered_couples_distance_matrix_index
            ) in endangered_couples_distance_matrix_indices
        )

    @classmethod
    def generate(
        cls,
        show_user: ShowUser,
        *,
        collision_distance: Optional[float] = None,
        is_partial: bool = False,
    ) -> List["CollisionInfraction"]:
        show_position_frames = ShowPositionFrame.from_show_user(show_user, is_partial=is_partial)
        if collision_distance is None:
            collision_distance = IOSTAR_PHYSIC_PARAMETERS_RECOMMENDATION.minimum_distance
        elif collision_distance < IOSTAR_PHYSIC_PARAMETERS_MAX.minimum_distance:
            msg = (
                f"collision_distance ({collision_distance}) should be greater than or equal to "
                f"minimum_distance ({IOSTAR_PHYSIC_PARAMETERS_MAX.minimum_distance})",
            )
            raise ValueError(msg)
        if not is_partial:
            collision_distance *= 0.95
        return list(
            itertools.chain.from_iterable(
                cls._get_collision_infractions(
                    show_position_frame.frame,
                    show_position_frame.in_air_indices,
                    show_position_frame.in_air_positions,
                    collision_distance,
                )
                for show_position_frame in tqdm(
                    show_position_frames,
                    desc="Checking collisions",
                    unit="frame",
                )
            ),
        )

    def summarize(self) -> "CollisionInfractionsSummary":
        return CollisionInfractionsSummary(
            nb_infractions=len(self),
            drone_indices={self.drone_index_1, self.drone_index_2},
            min_collision_infraction=self,
            max_collision_infraction=self,
            first_collision_infraction=self,
            last_collision_infraction=self,
        )


class CollisionInfractionsSummary(BaseInfractionsSummary):
    drone_indices: Set[int] = set()
    min_collision_infraction: Optional[CollisionInfraction] = None
    max_collision_infraction: Optional[CollisionInfraction] = None
    first_collision_infraction: Optional[CollisionInfraction] = None
    last_collision_infraction: Optional[CollisionInfraction] = None

    def __add__(self, other: "CollisionInfractionsSummary") -> "CollisionInfractionsSummary":
        return CollisionInfractionsSummary(
            nb_infractions=self.nb_infractions + other.nb_infractions,
            drone_indices=self.drone_indices.union(
                other.drone_indices,
            ),
            min_collision_infraction=apply_func_on_optional_pair(
                self.min_collision_infraction,
                other.min_collision_infraction,
                lambda x, y: x if x.distance < y.distance else y,
            ),
            max_collision_infraction=apply_func_on_optional_pair(
                self.max_collision_infraction,
                other.max_collision_infraction,
                lambda x, y: x if x.distance > y.distance else y,
            ),
            first_collision_infraction=apply_func_on_optional_pair(
                self.first_collision_infraction,
                other.first_collision_infraction,
                lambda x, y: x if x.frame < y.frame else y,
            ),
            last_collision_infraction=apply_func_on_optional_pair(
                self.last_collision_infraction,
                other.last_collision_infraction,
                lambda x, y: x if x.frame > y.frame else y,
            ),
        )


def get_principal_axis(
    positions_numpy: "NDArray[np.float64]",
) -> "NDArray[np.float64]":
    x_meaned: NDArray[np.float64] = positions_numpy - np.mean(positions_numpy, axis=0)
    cov_mat = np.cov(x_meaned, rowvar=False)
    eigen_values, eigen_vectors = np.linalg.eigh(cov_mat)
    return eigen_vectors[:, np.argmax(eigen_values)]


def get_border_indices(
    sorted_positions_numpy: "NDArray[np.float64]",
    endangered_distance: float,
) -> "NDArray[np.intp]":
    middle_position_numpy: NDArray[np.float64] = sorted_positions_numpy[
        len(sorted_positions_numpy) // 2
    ]
    return np.arange(  # pyright: ignore[reportUnknownMemberType]
        np.searchsorted(
            sorted_positions_numpy,
            middle_position_numpy - endangered_distance,
            side="left",
        ),
        np.searchsorted(
            sorted_positions_numpy,
            middle_position_numpy + endangered_distance,
            side="right",
        ),
    )


def get_unique_list_from_list(
    non_unique_list: List[T],
) -> List[T]:
    return list(set(non_unique_list))
