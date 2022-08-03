from .json_convertion_tools.drone_encoding_report import DroneEncodingReport


class JsonCreationReport:
    def __init__(self, nb_drones: int = 0):
        self.validation = False
        self.drones_encoding_report = [DroneEncodingReport() for _ in range(nb_drones)]

    def update(self) -> None:
        if not (hasattr(self, "drones_encoding_report")):
            raise ValueError
        self.validation = all(
            drone_encoding_report.validation
            for drone_encoding_report in self.drones_encoding_report
        )
