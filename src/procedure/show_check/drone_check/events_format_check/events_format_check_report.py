class TimecodeCheckReport:
    def __init__(self):
        self.validate = True

    def update(self, validation: bool) -> None:
        self.validation = validation


class XyzCheckReport:
    def __init__(self):
        self.validate = True

    def update(self, validation: bool) -> None:
        self.validation = validation


class RgbwCheckReport:
    def __init__(self):
        self.validate = True

    def update(self, validation: bool) -> None:
        self.validation = validation


class FireValueCheckReport:
    def __init__(self):
        self.validate = True

    def update(self, validation: bool) -> None:
        self.validation = validation


class TakeoffCheckReport:
    def __init__(self):
        self.validate = True

    def update(self, validation: bool) -> None:
        self.validation = validation


class FireChanelCheckReport:
    def __init__(self):
        self.validate = True

    def update(self, validation: bool) -> None:
        self.validation = validation


class FireDurationCheckReport:
    def __init__(self):
        self.validate = True

    def update(self, validation: bool) -> None:
        self.validation = validation


class PositionEventsCheckReport:
    def __init__(self):
        self.validation = True
        self.timecode_check = TimecodeCheckReport()
        self.xyz_check = XyzCheckReport()
        self.takeoff_check = TakeoffCheckReport()

    def update(self) -> None:
        self.validation = (
            self.timecode_check.validation
            and self.xyz_check.validation
            and self.takeoff_check
        )


class ColorEventsCheckReport:
    def __init__(self):
        self.validation = True
        self.timecode_check = TimecodeCheckReport()
        self.rgbw_check = RgbwCheckReport()

    def update(self) -> None:
        self.validation = self.timecode_check.validation and self.rgbw_check


class FireEventsCheckReport:
    def __init__(self):
        self.validation = True
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
        self.validation = True
        self.position_events_check = PositionEventsCheckReport()
        self.color_events_check = ColorEventsCheckReport()
        self.fire_events_check = FireEventsCheckReport()

    def update(self) -> None:
        self.validation = (
            self.position_events_check.validation
            and self.color_events_check.validation
            and self.fire_events_check
        )
