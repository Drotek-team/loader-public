from typing import List

from .observed_metrics.observed_metrics_report import ObservedMetricsSliceCheckReport


class PerformanceCheckReport:
    def __init__(self, timecodes: List[int]):
        self.validation = False
        self.observed_metrics_slices_check_report = [
            ObservedMetricsSliceCheckReport(timecode) for timecode in timecodes
        ]

    def update(self) -> None:
        self.validation = all(
            observed_metrics_check_report.validation
            for observed_metrics_check_report in self.observed_metrics_slices_check_report
        )
