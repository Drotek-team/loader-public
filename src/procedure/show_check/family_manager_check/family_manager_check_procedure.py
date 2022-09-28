import numpy as np

from ....drones_manager.drones_manager import DronesUser
from ....family_manager.family_manager import FamilyManager
from ....parameter.parameter import (
    FamilyParameter,
    FrameParameter,
    JsonConvertionConstant,
)
from .family_manager_check_report import (
    FamilyManagerCheckReport,
)
from .family_manager_format.family_manager_format_check_procedure import (
    apply_family_manager_format_check,
)
from .family_manager_value_check.family_manager_value_check_procedure import (
    apply_family_manager_value_check,
)
from .family_manager_logic_check.family_manager_logic_check_procedure import (
    apply_family_manager_logic_check_procedure,
)


def apply_family_check_procedure(
    drones_manager: DronesUser,
    family_manager: FamilyManager,
    frame_parameter: FrameParameter,
    json_convertion_constant: JsonConvertionConstant,
    family_parameter: FamilyParameter,
    family_manager_check_report: FamilyManagerCheckReport,
) -> None:
    apply_family_manager_format_check(
        family_manager, family_manager_check_report.family_manager_format_check_report
    )
    apply_family_manager_value_check(
        family_manager,
        family_parameter,
        family_manager_check_report.family_manager_value_check_report,
    )
    apply_family_manager_logic_check_procedure(
        drones_manager,
        family_manager,
        frame_parameter,
        json_convertion_constant,
        family_manager_check_report.family_manager_logic_check_report,
    )
    family_manager_check_report.update()
