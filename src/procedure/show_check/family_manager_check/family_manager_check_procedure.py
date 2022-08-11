import numpy as np

from ....drones_manager.drones_manager import DronesManager
from ....family_manager.family_manager import FamilyManager
from ....parameter.parameter import FamilyParameter
from .family_manager_check_report import (
    FamilyManagerCheckReport,
)
from .family_manager_format.family_manager_format_check_procedure import (
    apply_family_manager_format_check,
)
from .family_manager_value_check.family_manager_value_check_procedure import (
    apply_family_manager_value_check,
)


def apply_family_check_procedure(
    drones_manager: DronesManager,
    family_manager: FamilyManager,
    family_parameter: FamilyParameter,
    family_manager_check_report: FamilyManagerCheckReport,
) -> None:
    apply_family_manager_format_check(
        family_manager, family_manager_check_report.family_manager_format_check_report
    )
    apply_family_manager_value_check(
        family_manager, family_manager_check_report.family_manager_format_check_report
    )
    coherence_check(
        family_manager,
        drones_manager.first_horizontal_positions,
        family_manager_check_report.coherence_check_report,
    )
    family_manager_check_report.update()
