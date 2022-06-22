class DronePerformanceCheckReport:
    def __init__(self):
        self.validate = True


class PerformanceCheckReport:
    def __init__(self, nb_drones: int):
        self.validate = True
        self.drones_performance_check_report = [
            DronePerformanceCheckReport() for _ in range(nb_drones)
        ]
