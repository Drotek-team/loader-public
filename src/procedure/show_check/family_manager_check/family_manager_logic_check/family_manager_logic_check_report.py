from ....report import Contenor, Displayer
from typing import Tuple


class NbDroneLogicCheckReport(Displayer):
    ### TO DO: Redefine init so the miss "update_report" can be handle
    def get_report(self) -> str:
        return f"The number of drones: {self.nb_drone_drones_user} does not match the expectation of the families: {self.nb_drone_family_manager}"

    def update_report(
        self, nb_drone_family_manager: int, nb_drone_drones_user: int
    ) -> None:
        self.nb_drone_family_manager = nb_drone_family_manager
        self.nb_drone_drones_user = nb_drone_drones_user


class FirstPositionLogicCheckReport(Displayer):
    def get_report(self) -> str:
        return f"The positions of the drones do not match the expectation of the families (distance max:{self.distance_max}"

    def update_report(self, distance_max: float) -> None:
        self.distance_max = distance_max


class ShowDurationLogicCheckReport(Displayer):
    def get_report(self) -> str:
        return f"The family manager show duration is {self.family_manager_show_duration} and the drones manager show duration is {self.drones_user_show_duration}"

    def update_report(
        self, family_manager_show_duration: int, drones_user_show_duration: int
    ) -> None:
        self.family_manager_show_duration = family_manager_show_duration
        self.drones_user_show_duration = drones_user_show_duration


class AltitudeRangeLogicCheckReport(Displayer):
    def get_report(self) -> str:
        return f"The family manager altitude range is {self.family_manager_altitude_range} and the drones manager altitude range is {self.drones_user_altitude_range}"

    def update_report(
        self,
        family_manager_altitude_range: Tuple[int, int],
        drones_user_altitude_range: Tuple[int, int],
    ) -> None:
        self.family_manager_altitude_range = family_manager_altitude_range
        self.drones_user_altitude_range = drones_user_altitude_range


class FamilyManagerLogicCheckReport(Contenor):
    def __init__(self):
        self.name = " logic check report"
        self.nb_drone_logic_check_report = NbDroneLogicCheckReport()
        self.first_position_logic_check_report = FirstPositionLogicCheckReport()
        self.show_duration_logic_check_report = ShowDurationLogicCheckReport()
        self.altitude_range_logic_check_report = AltitudeRangeLogicCheckReport()

    def update(self) -> None:
        self.validation = (
            self.nb_drone_logic_check_report.validation
            and self.first_position_logic_check_report.validation
            and self.show_duration_logic_check_report
            and self.altitude_range_logic_check_report
        )
