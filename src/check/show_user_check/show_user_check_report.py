from ...report import Contenor, Displayer


class TakeoffCheckReport(Contenor):
    def __init__(self):
        self.name = "Takeoff Check Report"
        self.takeoff_duration_check_report = Displayer("Takeoff Duration Check Report")
        self.takeoff_xyz_check_report = Displayer("Takeoff Position Check Report")


class DroneUserCheckReport(Contenor):
    def __init__(self, drone_index: int):
        self.name = f"Drone {drone_index} user check report"
        self.takeoff_check_report = TakeoffCheckReport()


class ShowUserCheckReport(Contenor):
    def __init__(self, nb_drones: int):
        self.name = "Show user check report"
        self.drones_user_check_report = [
            DroneUserCheckReport(drone_index) for drone_index in range(nb_drones)
        ]

    # TODO: I know this is very bad but I don't how to clean it
    @property
    def user_validation(self) -> bool:
        return all(
            drone_user_check_report.user_validation
            for drone_user_check_report in self.drones_user_check_report
        )

    # TODO: I know this is very bad but I don't how to clean it
    def display_message(self, indentation_level: int, indentation_type: str) -> str:
        if self.user_validation:
            return ""
        initial_message = (
            f"{indentation_level * indentation_type}[Error Message List] {self.name} \n"
        )
        list_messages = "".join(
            [
                drone_user_check_report.display_message(
                    indentation_level + 1, indentation_type
                )
                for drone_user_check_report in self.drones_user_check_report
            ]
        )
        return initial_message + list_messages
