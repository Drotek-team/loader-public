class PositionsTheoricalCoherenceCheckReport:
    def __init__(self):
        self.validation = False


class FamilyManagerValuesCheckReport:
    def __init__(self):
        self.validation = False


class FamilyManagerCheckReport:
    def __init__(self):
        self.validation = False
        self.positions_theorical_coherence_check_report = (
            PositionsTheoricalCoherenceCheckReport()
        )
        self.family_manager_values_check_report = FamilyManagerValuesCheckReport()
