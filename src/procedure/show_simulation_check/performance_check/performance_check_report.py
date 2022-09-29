from typing import List

from ...report import Contenor
from .observed_metrics.observed_metrics_report import PerformanceSliceCheckReport


class PerformanceCheckReport(Contenor):
    def __init__(self, frames: List[float] = [0]):
        self.name = "Performance check report"
        self.performance_slices_check_report = [
            PerformanceSliceCheckReport(frame) for frame in frames
        ]

    def update(self) -> None:
        self.validation = all(
            performance_slice_check_report.validation
            for performance_slice_check_report in self.performance_slices_check_report
        )
