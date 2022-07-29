from ...report import Contenor, Displayer
from typing import Tuple


class FamilyManagerFormatCheckReport(Displayer):
    def get_report(self) -> str:
        return "Family Manager Format Check Report"


class FamilyManagerValueCheckReport(Displayer):
    def get_report(self) -> str:
        return "Family Manager Value Check Report"


class NbDroneCoherenceCheckReport(Displayer):
    def get_report(self) -> str:
        return f"The number of drones: {self.nb_drone_drones_manager} does not match the expectation of the families: {self.nb_drone_family_manager}"

    def update_report(
        self, nb_drone_family_manager: int, nb_drone_drones_manager: int
    ) -> None:
        self.nb_drone_family_manager = nb_drone_family_manager
        self.nb_drone_drones_manager = nb_drone_drones_manager


class PositionCoherenceCheckReport(Displayer):
    def get_report(self) -> str:
        return f"The positions of the drones do not match the expectation of the families (distance max:{self.distance_max}"

    def update_report(self, distance_max: float) -> None:
        self.distance_max = distance_max


class ShowDurationCoherenceCheckReport(Displayer):
    def get_report(self) -> str:
        return f"The family manager show duration is {self.family_manager_show_duration} and the drones manager show duration is {self.drones_manager_show_duration}"

    def update_report(
        self, family_manager_show_duration: int, drones_manager_show_duration: int
    ) -> None:
        self.family_manager_show_duration = family_manager_show_duration
        self.drones_manager_show_duration = drones_manager_show_duration


class AltitudeRangeCoherenceCheckReport(Displayer):
    def get_report(self) -> str:
        return f"The family manager altitude range is {self.family_manager_altitude_range} and the drones manager altitude range is {self.drones_manager_altitude_range}"

    def update_report(
        self,
        family_manager_altitude_range: Tuple[int, int],
        drones_manager_altitude_range: Tuple[int, int],
    ) -> None:
        self.family_manager_altitude_range = family_manager_altitude_range
        self.drones_manager_altitude_range = drones_manager_altitude_range


class CoherenceCheckReport(Contenor):
    def __init__(self):
        self.name = " coherence check report"
        self.nb_drone_coherence_check_report = NbDroneCoherenceCheckReport()
        self.position_coherence_check_report = PositionCoherenceCheckReport()

    def update(self) -> None:
        self.validation = (
            self.nb_drone_coherence_check_report.validation
            and self.position_coherence_check_report.validation
        )


class FamilyManagerCheckReport(Contenor):
    def __init__(self):
        self.name = "Family Manager Check Report"
        self.family_manager_format_check_report = FamilyManagerFormatCheckReport()
        self.family_manager_value_check_report = FamilyManagerValueCheckReport()
        self.coherence_check_report = CoherenceCheckReport()

    def update(self) -> None:
        self.validation = (
            self.family_manager_format_check_report.validation
            and self.family_manager_value_check_report.validation
            and self.coherence_check_report.validation
        )
