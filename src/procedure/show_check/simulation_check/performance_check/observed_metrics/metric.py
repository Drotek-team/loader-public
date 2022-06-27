from dataclasses import dataclass


@dataclass(frozen=True)
class Metric:
    drone_index: int
    min_value: float
    max_value: float
    standard_convention: bool = True

    def interpolation(self, value: float) -> float:
        ratio = (value - self.min_value) / (self.max_value - self.min_value)
        return min(1, max(ratio, 0))

    def validation(self, value: float) -> bool:
        ratio = self.interpolation(value)
        return ratio != int(self.standard_convention)
