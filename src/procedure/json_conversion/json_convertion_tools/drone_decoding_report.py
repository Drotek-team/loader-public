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


class SectionNumberFormatReport:
    def __init__(self):
        self.validation = False


class HeaderFormatReport:
    def __init__(self):
        self.validation = False
        self.header_sufficient_space_report = HeaderSufficientSpaceReport()
        self.magic_number_format_report = MagicNumberFormatReport()
        self.dance_size_format_report = DanceSizeFormatReport()
        self.section_number_format_report = SectionNumberFormatReport()


class SectionHeaderFormatReport:
    def __init__(self):
        self.validation = False


class DroneDecodingReport:
    def __init__(self, nb_section_max: int):
        self.validation = False
        self.correct_header = HeaderFormatReport()
        self.correct_section_headers = nb_section_max * [SectionHeaderFormatReport()]
