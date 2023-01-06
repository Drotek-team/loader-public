from typing import List

from ...report import Contenor, Displayer


class FrameCoherenceCheckReport(Contenor):
    def __init__(self):
        self.name = "Frame Coherence Check Report"
        self.incoherence_relative_absolute_time: List[Displayer]


class TakeoffCheckReport(Contenor):
    def __init__(self):
        self.name = "Takeoff Check Report"
        self.takeoff_duration_check_report = Displayer("Takeoff Duration Check Report")
        self.takeoff_xyz_check_report = Displayer("Takeoff Position Check Report")


class DroneUserCheckReport(Contenor):
    def __init__(self, drone_index: int):
        self.name = f"Drone {drone_index} user check report"
        self.frame_coherence_check_report = FrameCoherenceCheckReport()
        self.takeoff_check_report = TakeoffCheckReport()


class ShowUserCheckReport(Contenor):
    def __init__(self, nb_drones: int):
        self.name = "Show user check report"
        self.drones_user_check_report = [
            DroneUserCheckReport(drone_index) for drone_index in range(nb_drones)
        ]
