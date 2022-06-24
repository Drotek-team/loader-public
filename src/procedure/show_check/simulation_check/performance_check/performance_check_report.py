class DronePerformanceCheckReport:
    def __init__(self):
        self.validation = False

    def update_value(self):
        

class PerformanceCheckReport:
    def __init__(self, nb_drones: int):
        self.validation = False
        self.drones_performance_check_report = [
            DronePerformanceCheckReport() for _ in range(nb_drones)
        ]

    def update(self):
        self.validation = all(
            drone_performance_check_report.validation
            for drone_performance_check_report in self.drones_performance_check_report
        )
