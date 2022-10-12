from ...report import Contenor
from .migration_DP_binary.drone_decoding_report import DroneDecodingReport


class IJ_to_DP_report(Contenor):
    name = "Json Extraction Report"

    def __init__(self, nb_drones: int = 1) -> None:
        self.drones_decoding_report = [
            DroneDecodingReport(drone_index) for drone_index in range(nb_drones)
        ]

    def update(self) -> None:
        self.validation = all(
            drone_decoding_report.validation
            for drone_decoding_report in self.drones_decoding_report
        )
