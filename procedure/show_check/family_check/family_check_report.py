class FirstPositionCoherenceCheck:
    def __init__(self):
        self.validation = True

    def update(self, validation: bool) -> None:
        self.validation = validation


class VerticalityAlignedCheck:
    def __init__(self):
        self.validation = True

    def update(self, validation: bool) -> None:
        self.validation = validation


class RowColumnDistanceCheck:
    def __init__(self):
        self.validation = True

    def update(self, validation: bool) -> None:
        self.validation = validation


class FamilyCheckReport:
    def __init__(self):
        self.validation = True
        self.first_position_coherence_check = FirstPositionCoherenceCheck()
        self.verticality_aligned_check = VerticalityAlignedCheck()
        self.row_column_distance_check = RowColumnDistanceCheck()

    def update(self) -> None:
        self.validation = (
            self.first_position_coherence_check
            and self.verticality_aligned_check
            and self.row_column_distance_check
        )
