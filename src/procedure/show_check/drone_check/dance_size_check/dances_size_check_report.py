from ....json_conversion.json_convertion_tools.drone_encoding_report import (
    DroneEncodingReport,
)


class DanceSizeCheckReport:
    def __init__(self):
        self.validation = False
        self.drone_encoding_report = DroneEncodingReport()
