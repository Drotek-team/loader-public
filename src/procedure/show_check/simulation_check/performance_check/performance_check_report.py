from typing import List

from ....report import Contenor
from .observed_metrics.observed_metrics_report import ObservedMetricsCheckReport


class PerformanceCheckReport(Contenor):
    def __init__(self, seconds: List[float] = [0]):
        self.name = "Performance Check Report"
        self.observed_metrics_slices_check_report = [
            ObservedMetricsCheckReport(second) for second in seconds
        ]

    def update(self) -> None:
        self.validation = all(
            observed_metrics_check_report.validation
            for observed_metrics_check_report in self.observed_metrics_slices_check_report
        )
