from ...report import Contenor, Displayer


class FamilyManagerFormatCheckReport(Displayer):
    def get_report(self) -> str:
        return "Family Manager Format Check Report"


class FamilyManagerValueCheckReport(Displayer):
    def get_report(self) -> str:
        return "Family Manager Value Check Report"


class NbDroneTheoricalCoherenceCheckReport(Displayer):
    def get_report(self) -> str:
        return f"The number of drones: {self.nb_drone_drones_manager} does not match the expectation of the families: {self.nb_drone_family_manager}"

    def update_report(
        self, nb_drone_family_manager: int, nb_drone_drones_manager: int
    ) -> None:
        self.nb_drone_family_manager = nb_drone_family_manager
        self.nb_drone_drones_manager = nb_drone_drones_manager


class PositionTheoricalCoherenceCheckReport(Displayer):
    def get_report(self) -> str:
        return f"The positions of the drones do not match the expectation of the families (distance max:{self.distance_max}"

    def update_report(self, distance_max: float) -> None:
        self.distance_max = distance_max


class TheoricalCoherenceCheckReport(Contenor):
    def __init__(self):
        self.name = "Theorical coherence check report"
        self.nb_drone_theorical_coherence_check_report = (
            NbDroneTheoricalCoherenceCheckReport()
        )
        self.position_theorical_coherence_check_report = (
            PositionTheoricalCoherenceCheckReport()
        )

    def update(self) -> None:
        self.validation = (
            self.nb_drone_theorical_coherence_check_report.validation
            and self.position_theorical_coherence_check_report.validation
        )


class FamilyManagerCheckReport(Contenor):
    def __init__(self):
        self.name = "Family Manager Check Report"
        self.family_manager_format_check_report = FamilyManagerFormatCheckReport()
        self.family_manager_value_check_report = FamilyManagerValueCheckReport()
        self.theorical_coherence_check_report = TheoricalCoherenceCheckReport()

    def update(self) -> None:
        self.validation = (
            self.family_manager_format_check_report.validation
            and self.family_manager_value_check_report.validation
            and self.theorical_coherence_check_report.validation
        )
