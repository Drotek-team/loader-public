from ....report import Contenor, Displayer


class TimecodeFormatCheckReport(Displayer):
    def get_report(self) -> str:
        return "Timecode Format Check Report"


class TimecodeValueCheckReport(Displayer):
    def get_report(self) -> str:
        return "Timecode Vakue Check Report"


class IncreasingTimecodeCheckReport(Displayer):
    def get_report(self) -> str:
        return "Increasing Timecode Check Report"


class TimecodeRateCheckReport(Displayer):
    def get_report(self) -> str:
        return "Timecode Rate Check Report"


class TimecodeCheckReport(Contenor):
    def __init__(self):
        self.name = "Timecode Check Report"
        self.frame_format_check_report = TimecodeFormatCheckReport()
        self.frame_value_check_report = TimecodeValueCheckReport()
        self.increasing_frame_check_report = IncreasingTimecodeCheckReport()
        self.frame_rate_check_report = TimecodeRateCheckReport()

    def update(self) -> None:
        self.validation = (
            self.frame_format_check_report.validation
            and self.frame_value_check_report.validation
            and self.increasing_frame_check_report.validation
            and self.frame_rate_check_report.validation
        )


class XyzFormatCheckReport(Displayer):
    def get_report(self) -> str:
        return "Xyz Format Check Report"


class XyzValueCheckReport(Displayer):
    def get_report(self) -> str:
        return "Xyz Value Check Report"


class XyzCheckReport(Contenor):
    def __init__(self):
        self.name = "Xyz Check Report"
        self.xyz_format_check_report = XyzFormatCheckReport()
        self.xyz_value_check_report = XyzValueCheckReport()

    def update(self):
        self.validation = (
            self.xyz_format_check_report.validation
            and self.xyz_value_check_report.validation
        )


class TakeoffDurationCheckReport(Displayer):
    def get_report(self) -> str:
        return "Takeoff Duration Check Report"


class TakeoffPositionCheckReport(Displayer):
    def get_report(self) -> str:
        return "Takeoff Position Check Report"


class TakeoffCheckReport(Contenor):
    def __init__(self):
        self.name = "Takeoff Check Report"
        self.takeoff_duration_check_report = TakeoffDurationCheckReport()
        self.takeoff_position_check_report = TakeoffPositionCheckReport()

    def update(self):
        self.validation = (
            self.takeoff_duration_check_report.validation
            and self.takeoff_position_check_report.validation
        )


class PositionEventsCheckReport(Contenor):
    def __init__(self):
        self.name = "Position Events Check Report"
        self.frame_check_report = TimecodeCheckReport()
        self.xyz_check_report = XyzCheckReport()
        self.takeoff_check_report = TakeoffCheckReport()

    def update(self) -> None:
        self.validation = (
            self.frame_check_report.validation
            and self.xyz_check_report.validation
            and self.takeoff_check_report.validation
        )


class RgbwFormatCheckReport(Displayer):
    def get_report(self) -> str:
        return "Rgbw Format Check Report"


class RgbwValueCheckReport(Displayer):
    def get_report(self) -> str:
        return "Rgbw Value Check Report"


class RgbwCheckReport(Contenor):
    def __init__(self):
        self.name = "Rgbw Check Report"
        self.rgbw_format_check_report = RgbwFormatCheckReport()
        self.rgbw_value_check_report = RgbwValueCheckReport()

    def update(self):
        self.validation = (
            self.rgbw_format_check_report.validation
            and self.rgbw_value_check_report.validation
        )


class ColorEventsCheckReport(Contenor):
    def __init__(self):
        self.name = "Color Events Check Report"
        self.frame_check_report = TimecodeCheckReport()
        self.rgbw_check_report = RgbwCheckReport()

    def update(self) -> None:
        self.validation = self.frame_check_report.validation and self.rgbw_check_report


class FireTimecodeCheckReport(Contenor):
    def __init__(self):
        self.name = "Fire Timecode Check Report"
        self.frame_format_check_report = TimecodeFormatCheckReport()
        self.frame_value_check_report = TimecodeValueCheckReport()
        self.increasing_frame_check_report = IncreasingTimecodeCheckReport()

    def update(self) -> None:
        self.validation = (
            self.frame_format_check_report.validation
            and self.frame_value_check_report.validation
            and self.increasing_frame_check_report
        )


class FireChanelFormatCheckReport(Displayer):
    def get_report(self) -> str:
        return "Fire Chanel Format Check Report"


class FireChanelValueCheckReport(Displayer):
    def get_report(self) -> str:
        return "Fire Chanel Value Check Report"


class FireChanelUncityCheckReport(Displayer):
    def get_report(self) -> str:
        return "Fire Chanel Uncity Check Report"


class FireChanelCheckReport(Contenor):
    def __init__(self):
        self.name = "Fire Chanel Check Report"
        self.fire_chanel_format_check_report = FireChanelFormatCheckReport()
        self.fire_chanel_value_check_report = FireChanelValueCheckReport()
        self.fire_chanel_unicty_check_report = FireChanelUncityCheckReport()

    def update(self) -> None:
        self.validation = (
            self.fire_chanel_format_check_report and self.fire_chanel_value_check_report
        )


class FireDurationFormatCheckReport(Displayer):
    def get_report(self) -> str:
        return "Fire Duration Format Check Report"


class FireDurationValueCheckReport(Displayer):
    def get_report(self) -> str:
        return "Fire Duration Value Check Report"


class FireDurationCheckReport(Contenor):
    def __init__(self):
        self.name = "Fire Duration Check Report"
        self.fire_duration_format_check_report = FireDurationFormatCheckReport()
        self.fire_duration_value_check_report = FireDurationValueCheckReport()

    def update(self) -> None:
        self.validation = (
            self.fire_duration_format_check_report.validation
            and self.fire_duration_value_check_report.validation
        )


class FireEventsCheckReport(Contenor):
    def __init__(self):
        self.name = "Fire Events Check Report"
        self.fire_frame_check_report = FireTimecodeCheckReport()
        self.fire_chanel_check_report = FireChanelCheckReport()
        self.fire_duration_check_report = FireDurationCheckReport()

    def update(self) -> None:
        self.validation = (
            self.fire_frame_check_report.validation
            and self.fire_chanel_check_report.validation
            and self.fire_duration_check_report.validation
        )


class EventsFormatCheckReport(Contenor):
    def __init__(self):
        self.name = "Events format check report"
        self.position_events_check = PositionEventsCheckReport()
        self.color_events_check = ColorEventsCheckReport()
        self.fire_events_check = FireEventsCheckReport()

    def update(self) -> None:
        self.validation = (
            self.position_events_check.validation
            and self.color_events_check.validation
            and self.fire_events_check.validation
        )
