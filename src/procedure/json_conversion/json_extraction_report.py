from .json_convertion_tools.drone_decoding_report import DroneDecodingReport


class JsonExtractionReport:
    def __init__(self):
        self.validation = False

    def initialize_drones_decoding_report(self, nb_drones: int) -> None:
        self.drones_decoding_report = [DroneDecodingReport() for _ in range(nb_drones)]

    def update(self) -> None:
        if not (hasattr(self, "drones_decoding_report")):
            raise ValueError
        self.validation = all(
            drone_decoding_report.validation
            for drone_decoding_report in self.drones_decoding_report
        )
