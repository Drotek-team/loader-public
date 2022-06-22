class TimecodeCheck:
    def __init__(self):
        self.validate = True

    def update(self, validation: bool) -> None:
        self.validation = validation


class XyzCheck:
    def __init__(self):
        self.validate = True

    def update(self, validation: bool) -> None:
        self.validation = validation


class RgbwCheck:
    def __init__(self):
        self.validate = True

    def update(self, validation: bool) -> None:
        self.validation = validation


class FireValueCheck:
    def __init__(self):
        self.validate = True

    def update(self, validation: bool) -> None:
        self.validation = validation


class TakeoffCheck:
    def __init__(self):
        self.validate = True

    def update(self, validation: bool) -> None:
        self.validation = validation


class FireChanelCheck:
    def __init__(self):
        self.validate = True

    def update(self, validation: bool) -> None:
        self.validation = validation


class FireDurationCheck:
    def __init__(self):
        self.validate = True

    def update(self, validation: bool) -> None:
        self.validation = validation


class PositionEventsCheck:
    def __init__(self):
        self.validation = True
        self.timecode_check = TimecodeCheck()
        self.xyz_check = XyzCheck()
        self.takeoff_check = TakeoffCheck()

    def update(self) -> None:
        self.validation = (
            self.timecode_check.validation
            and self.xyz_check.validation
            and self.takeoff_check
        )


class ColorEventsCheck:
    def __init__(self):
        self.validation = True
        self.timecode_check = TimecodeCheck()
        self.rgbw_check = RgbwCheck()

    def update(self) -> None:
        self.validation = self.timecode_check.validation and self.rgbw_check


class FireEventsCheck:
    def __init__(self):
        self.validation = True
        self.timecode_check = TimecodeCheck()
        self.fire_chanel_check = FireChanelCheck()
        self.fire_duration_check = FireDurationCheck()

    def update(self) -> None:
        self.validation = (
            self.timecode_check.validation
            and self.fire_chanel_check
            and self.fire_duration_check
        )


class EventsFormatCheckReport:
    def __init__(self):
        self.validation = True
        self.position_events_check = PositionEventsCheck()
        self.color_events_check = ColorEventsCheck()
        self.fire_events_check = FireEventsCheck()

    def update(self) -> None:
        self.validation = (
            self.position_events_check.validation
            and self.color_events_check.validation
            and self.fire_events_check
        )
