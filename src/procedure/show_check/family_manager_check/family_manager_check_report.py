from ...report import Contenor, Displayer


class FamilyManagerFormatCheckReport(Displayer):
    def get_report(self) -> str:
        return "Family Manager Format Check Report"


class FamilyManagerValueCheckReport(Displayer):
    def get_report(self) -> str:
        return "Family Manager Value Check Report"


class PositionsTheoricalCoherenceCheckReport(Displayer):
    def get_report(self) -> str:
        return "Positions Theorical Coherence Check Report"


class FamilyManagerCheckReport(Contenor):
    def __init__(self):
        self.name = "Family Manager Check Report"
        self.family_manager_format_check_report = FamilyManagerFormatCheckReport()
        self.family_manager_value_check_report = FamilyManagerValueCheckReport()
        self.positions_theorical_coherence_check_report = (
            PositionsTheoricalCoherenceCheckReport()
        )

    def update(self) -> None:
        self.validation = (
            self.family_manager_format_check_report.validation
            and self.family_manager_value_check_report.validation
            and self.positions_theorical_coherence_check_report.validation
        )
