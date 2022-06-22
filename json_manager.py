from typing import Dict, Tuple

from drones_manager.drones_manager import DronesManager
from family_manager.family_manager import FamilyManager
from json_convertor.json_convertor import Show
from show_simulation.show_simulation import ShowSimulation


class JsonManager:
    @staticmethod
    def json_creation_procedure(
        drones_manager: DronesManager,
        family_manager: FamilyManager,
        json_creation_report: JsonCreationReport,
    ) -> None:
        show = Show()
        show.update_families(drones_manager, family_manager)
        show.update_parameter(
            family_manager.nb_x,
            family_manager.nb_y,
            family_manager.step,
            family_manager.angle_takeoff_degree(
                drones_manager.first_horizontal_positions
            ),
            drones_manager.convex_hull,
        )

    def export_procedure(
        self,
        drones_manager: DronesManager,
        family_manager: FamilyManager,
        export_report: ExportReport,
    ):
        self.check_procedure(drones_manager, family_manager, export_report.show_report)
        self.json_creation_procedure(
            drones_manager, family_manager, export_report.json_creation_report
        )

    @staticmethod
    def drones_creation_procedure(
        json_dict: Dict,
        drones_creation_report: DronesCreationReport,
    ) -> Tuple[DronesManager, FamilyManager]:
        return (DronesManager(), FamilyManager())

    def import_procedure(
        self,
        json_dict: Dict,
        import_report: ImportReport,
    ) -> Tuple[DronesManager, FamilyManager]:
        drones_manager, family_manager = self.drones_creation_procedure(
            json_dict, import_report.drones_creation_report
        )
        self.check_procedure(drones_manager, family_manager, import_report.show_report)
        return drones_manager, family_manager
