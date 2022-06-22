from .drone_check.drone_check_report import DroneCheckReport
from .simulation_check.simulation_check_report import SimulationCheckReport


class ShowCheckReport:
    def __init__(self, nb_drones: int):
        self.simulation_check_report = SimulationCheckReport()
        self.family_check_report = FamilyCheckReport()
        self.drones_check_report = [DroneCheckReport() for _ in range(nb_drones)]
