from dataclasses import dataclass
from typing import List

from ....report import Contenor, Displayer


class HeaderSufficientSpaceReport(Displayer):
    def get_report(self) -> str:
        return "The header did not get sufficient space"


class MagicNumberFormatReport(Displayer):
    def get_report(self) -> str:
        return "The magic number is wrong"


class DanceSizeFormatReport(Displayer):
    def get_report(self) -> str:
        return "The dance size format is not proper"


@dataclass
class HeaderFormatReport(Contenor):
    name = "Header Format Report"

    def __init__(self):
        self.header_sufficient_space_report = HeaderSufficientSpaceReport()
        self.magic_number_format_report = MagicNumberFormatReport()
        self.dance_size_format_report = DanceSizeFormatReport()

    def update(self):
        self.validation = (
            self.header_sufficient_space_report.validation
            and self.magic_number_format_report.validation
            and self.dance_size_format_report.validation
        )


class SectionHeaderFormatReport(Displayer):
    def get_report(self) -> str:
        return "The section header does not has the proper format"


class DroneDecodingReport(Contenor):
    def __init__(self, drone_index: int):
        self.name = f"Drone {drone_index} Encoding Report"
        self.header_format_report = HeaderFormatReport()
        self.section_headers_format_report: List[SectionHeaderFormatReport] = []

    def add_section_header_format_report(self) -> SectionHeaderFormatReport:
        section_header_format_report = SectionHeaderFormatReport()
        self.section_headers_format_report.append(section_header_format_report)
        return section_header_format_report

    def update(self) -> None:
        self.validation = self.header_format_report.validation and all(
            section_header_format_report.validation
            for section_header_format_report in self.section_headers_format_report
        )
