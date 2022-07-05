from .json_convertion_tools.drone_encoding_report import DroneEncodingReport


class JsonCreationReport:
    def __init__(self):
        self.validation = False

    def initialize_drones_encoding_report(self, nb_drones: int) -> None:
        self.drones_encoding_report = [DroneEncodingReport() for _ in range(nb_drones)]

    def update(self) -> None:
        if hasattr(self, "drones_encoding_report"):
            raise ValueError
        self.validation = all(
            drone_encoding_report.validation
            for drone_encoding_report in self.drones_encoding_report
        )
