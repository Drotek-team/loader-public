from ....json_conversion.json_convertion_tools.drone_encoding_report import (
    DroneEncodingReport,
)
from ....report import Contenor


class DanceSizeCheckReport(Contenor):
    def __init__(self):
        self.name = f"Dance size check report"
        self.drone_encoding_report = DroneEncodingReport()
