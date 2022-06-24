class PositionsTheoricalCoherenceCheckReport:
    def __init__(self):
        self.validation = False


class FamilyManagerFormatCheckReport:
    def __init__(self):
        self.validation = False


class FamilyManagerValueCheckReport:
    def __init__(self):
        self.validation = False


class FamilyManagerCheckReport:
    def __init__(self):
        self.validation = False
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
