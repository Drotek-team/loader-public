class FirstPositionCoherenceCheck:
    def __init__(self):
        self.validation = False


class VerticalityAlignedCheck:
    def __init__(self):
        self.validation = False


class RowColumnDistanceCheck:
    def __init__(self):
        self.validation = False


class FamilyManagerCheckReport:
    def __init__(self):
        self.validation = False
        self.first_position_coherence_check = FirstPositionCoherenceCheck()
        self.verticality_aligned_check = VerticalityAlignedCheck()
        self.row_column_distance_check = RowColumnDistanceCheck()

    def update(self) -> None:
        self.validation = (
            self.first_position_coherence_check
            and self.verticality_aligned_check
            and self.row_column_distance_check
        )
