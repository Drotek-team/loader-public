from .json_convertion_tools.drone_decoding_report import DroneDecodingReport


class JsonExtractionReport:
    def __init__(self):
        self.validation = False

    def initialize_drones_encoding_report(self, nb_drones: int) -> None:
        self.drones_decoding_report = [
            DroneDecodingReport(drone_index) for drone_index in range(nb_drones)
        ]

    def update(self) -> None:
        if hasattr(self, "drones_encoding_report"):
            raise ValueError
        self.validation = all(
            drone_encoding_report.validation
            for drone_encoding_report in self.drones_decoding_report
        )
