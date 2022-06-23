class DanceSizeCheckReport:
    def __init__(self):
        self.validation = False


class ShowSizeCheckReport:
    def __init__(self, nb_drones: int):
        self.validation = False
        self.dances_size_check_report = [
            DanceSizeCheckReport() for _ in range(nb_drones)
        ]
