from ....report import Contenor, Displayer


class FrameCheckReport(Contenor):
    name = "Frame Check Report"
    frame_value_check_report = Displayer("Frame Value Check Report")
    increasing_frame_check_report = Displayer("Increasing Frame Check Report")


class XyzCheckReport(Contenor):
    def __init__(self):
        self.name = "Xyz Check Report"
        self.xyz_value_check_report = Displayer("Xyz Value Check Report")


class PositionEventsCheckReport(Contenor):
    def __init__(self):
        self.name = "Position Events Check Report"
        self.frame_check_report = FrameCheckReport()
        self.xyz_check_report = XyzCheckReport()


class RgbwCheckReport(Contenor):
    def __init__(self):
        self.name = "Rgbw Check Report"
        self.rgbw_value_check_report = Displayer("Rgbw Value Check Report")


class ColorEventsCheckReport(Contenor):
    def __init__(self):
        self.name = "Color Events Check Report"
        self.frame_check_report = FrameCheckReport()
        self.rgbw_check_report = RgbwCheckReport()


class FireFrameCheckReport(Contenor):
    def __init__(self):
        self.name = "Frame Check Report"
        self.frame_value_check_report = Displayer("Frame Value Check Report")
        # TODO: add increasing frame


class FireChanelCheckReport(Contenor):
    def __init__(self):
        self.name = "Fire Chanel Check Report"
        self.fire_chanel_value_check_report = Displayer(
            "Fire Chanel Value Check Report"
        )
        # TODO: supprimer unicity pour le moment
        self.fire_chanel_unicty_check_report = Displayer(
            "Fire Chanel Unicty Check Report"
        )


class FireDurationCheckReport(Contenor):
    def __init__(self):
        self.name = "Fire Duration Check Report"
        self.fire_duration_value_check_report = Displayer(
            "Fire Duration Value Check Report"
        )


class FireEventsCheckReport(Contenor):
    def __init__(self):
        self.name = "Fire Events Check Report"
        self.fire_frame_check_report = FireFrameCheckReport()
        self.fire_chanel_check_report = FireChanelCheckReport()
        self.fire_duration_check_report = FireDurationCheckReport()


class EventsFormatCheckReport(Contenor):
    def __init__(self):
        self.name = "Events format check report"
        self.position_events_check = PositionEventsCheckReport()
        self.color_events_check = ColorEventsCheckReport()
        self.fire_events_check = FireEventsCheckReport()
