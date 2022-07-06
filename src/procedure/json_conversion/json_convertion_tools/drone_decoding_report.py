from typing import List


class HeaderSufficientSpaceReport:
    def __init__(self):
        self.validation = False


class MagicNumberFormatReport:
    def __init__(self):
        self.validation = False


class DanceSizeFormatReport:
    def __init__(self):
        self.validation = False


class HeaderFormatReport:
    def __init__(self):
        self.validation = False
        self.header_sufficient_space_report = HeaderSufficientSpaceReport()
        self.magic_number_format_report = MagicNumberFormatReport()
        self.dance_size_format_report = DanceSizeFormatReport()

    def update(self):
        self.validation = (
            self.header_sufficient_space_report.validation
            and self.magic_number_format_report.validation
            and self.dance_size_format_report.validation
        )


class SectionHeaderFormatReport:
    def __init__(self):
        self.validation = False


class DroneDecodingReport:
    def __init__(self):
        self.validation = False
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
