class FirstTimecodeCheckReport:
    def __init__(self):
        self.validation = False


class TimecodeFormatCheckReport:
    def __init__(self):
        self.validation = False


class IncreasingTimecodeCheckReport:
    def __init__(self):
        self.validation = False


class TimecodeRateCheckReport:
    def __init__(self):
        self.validation = False


class TimecodeCheckReport:
    def __init__(self):
        self.validation = False
        self.timecode_format_check_report = TimecodeFormatCheckReport()
        self.first_timecode_check_report = FirstTimecodeCheckReport()
        self.increasing_timecode_check_report = IncreasingTimecodeCheckReport()
        self.timecode_rate_check_report = TimecodeRateCheckReport()

    def update(self) -> None:
        self.validation = (
            self.timecode_format_check_report
            and self.first_timecode_check_report
            and self.increasing_timecode_check_report
            and self.timecode_rate_check_report
        )


class XyzCheckReport:
    def __init__(self):
        self.validation = False

    def update(self, validation: bool) -> None:
        self.validation = validation


class TakeoffCheckReport:
    def __init__(self):
        self.validation = False

    def update(self, validation: bool) -> None:
        self.validation = validation


class PositionEventsCheckReport:
    def __init__(self):
        self.validation = False
        self.timecode_check_report = TimecodeCheckReport()
        self.xyz_check_report = XyzCheckReport()
        self.takeoff_check_report = TakeoffCheckReport()

    def update(self) -> None:
        self.validation = (
            self.timecode_check_report.validation
            and self.xyz_check_report.validation
            and self.takeoff_check_report.validation
        )


class RgbwCheckReport:
    def __init__(self):
        self.validation = False

    def update(self, validation: bool) -> None:
        self.validation = validation


class ColorEventsCheckReport:
    def __init__(self):
        self.validation = False
        self.timecode_check = TimecodeCheckReport()
        self.rgbw_check = RgbwCheckReport()

    def update(self) -> None:
        self.validation = self.timecode_check.validation and self.rgbw_check


class FireChanelCheckReport:
    def __init__(self):
        self.validation = False

    def update(self, validation: bool) -> None:
        self.validation = validation


class FireDurationCheckReport:
    def __init__(self):
        self.validation = False

    def update(self, validation: bool) -> None:
        self.validation = validation


class FireEventsCheckReport:
    def __init__(self):
        self.validation = False
        self.timecode_check = TimecodeCheckReport()
        self.fire_chanel_check = FireChanelCheckReport()
        self.fire_duration_check = FireDurationCheckReport()

    def update(self) -> None:
        self.validation = (
            self.timecode_check.validation
            and self.fire_chanel_check
            and self.fire_duration_check
        )


class EventsFormatCheckReport:
    def __init__(self):
        self.validation = False
        self.position_events_check = PositionEventsCheckReport()
        self.color_events_check = ColorEventsCheckReport()
        self.fire_events_check = FireEventsCheckReport()

    def update(self) -> None:
        self.validation = (
            self.position_events_check.validation
            and self.color_events_check.validation
            and self.fire_events_check
        )
