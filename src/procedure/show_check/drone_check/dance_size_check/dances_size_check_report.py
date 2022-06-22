class DanceSizeCheckReport:
    def __init__(self):
        self.validation = True

    def update(self, validation: bool) -> None:
        self.validation = validation


class ShowSizeCheckReport:
    def __init__(self, nb_drones: int):
        self.validation = True
        self.dances_size_check_report = [
            DanceSizeCheckReport() for _ in range(nb_drones)
        ]
