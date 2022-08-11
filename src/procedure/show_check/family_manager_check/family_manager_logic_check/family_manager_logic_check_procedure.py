from .....family_manager.family_manager import FamilyManager
from typing import List, Tuple
from ....report import Contenor, Displayer


def apply_nb_drone_coherence_check_report(
    family_manager: FamilyManager,
    first_positions: List[Tuple],
    nb_drone_coherence_check_report: NbDroneLogicCheckReport,
) -> None:
    if len(first_positions) != len(family_manager.theorical_grid):
        nb_drone_coherence_check_report.update_report(
            len(first_positions), family_manager.theorical_grid.size
        )
    else:
        nb_drone_coherence_check_report.validation = True


def update_position_coherence_check_report(
    family_manager: FamilyManager,
    first_positions: List[Tuple],
    position_coherence_check_report: PositionCoherenceCheckReport,
) -> None:
    ROW_ALIGNED_CENTIMETER_TOLERANCE = 1
    if (
        np.max(np.array(first_positions) - family_manager.theorical_grid)
        > ROW_ALIGNED_CENTIMETER_TOLERANCE
    ):
        position_coherence_check_report.update_report(
            np.max(np.array(first_positions) - family_manager.theorical_grid)
        )
    else:
        position_coherence_check_report.validation = True


def update_show_duration_coherence_check_report(
    drones_manager: DronesManager,
    theorical_show_duration: int,
    show_duration_coherence_check_report: ShowDurationCoherenceCheckReport,
):
    if drones_manager.duration != theorical_show_duration:
        show_duration_coherence_check_report.update_report(
            drones_manager.duration, theorical_show_duration
        )
    else:
        show_duration_coherence_check_report.validation = True


def update_altitude_range_coherence_check_report(
    drones_manager: DronesManager,
    theorical_altitude_range: int,
    altitude_range_coherence_check_report: AltitudeRangeCoherenceCheckReport,
):
    if drones_manager.duration != theorical_altitude_range:
        altitude_range_coherence_check_report.update_report(
            drones_manager.duration, theorical_altitude_range
        )
    else:
        altitude_range_coherence_check_report.validation = True


def apply_family_manager_logic_check_procedure(
    family_manager: FamilyManager,
    first_positions: List[Tuple],
    coherence_check_report: CoherenceCheckReport,
) -> None:
    update_nb_drone_coherence_check_report(
        family_manager,
        first_positions,
        coherence_check_report.nb_drone_coherence_check_report,
    )
    if coherence_check_report.nb_drone_coherence_check_report.validation:
        update_position_coherence_check_report(
            family_manager,
            first_positions,
            coherence_check_report.position_coherence_check_report,
        )
    ### TO DO: create a class for this kind of parameter like JsonParameter or something else i dont know im tired
    # update_show_duration_coherence_check_report(
    #     family_manager,
    #     first_positions,
    #     coherence_check_report.position_coherence_check_report,
    # )
    # update_altitude_range_coherence_check_report(
    #     family_manager,
    #     first_positions,
    #     coherence_check_report.position_coherence_check_report,
    # )
    coherence_check_report.update()
