from abc import abstractclassmethod
from dataclasses import dataclass


class RatioManager:
    @staticmethod
    def bounded_ratio(ratio: float) -> float:
        return min(1, max(ratio, 0))

    @staticmethod
    def interpolation(
        value: float, min_value: float, max_value: float, convention: bool = True
    ) -> float:
        if convention:
            return (value - min_value) / (max_value - min_value)
        return (max_value - value) / (max_value - min_value)

    @abstractclassmethod
    def get_ratio(self, value: float) -> float:
        pass


@dataclass
class OneSizedRatio(RatioManager):
    min_value: float
    max_value: float
    standard_convention: bool = True

    def get_ratio(self, value: float) -> float:
        ratio = self.interpolation(value, self.min_value, self.max_value)
        ratio = self.bounded_ratio(ratio)
        return ratio if self.standard_convention else 1 - ratio


@dataclass
class TwoSizedRatio(RatioManager):
    min_value: float
    middle_value: float
    max_value: float
    standard_convention: bool = True

    def get_ratio(self, value: float) -> float:
        first_ratio = self.interpolation(
            value, self.min_value, self.middle_value, False
        )
        first_ratio = self.bounded_ratio(first_ratio)
        second_ratio = self.interpolation(value, self.middle_value, self.max_value)
        second_ratio = self.bounded_ratio(second_ratio)
        ratio = max(first_ratio, second_ratio)
        return ratio if self.standard_convention else 1 - ratio


class Metric:
    value: float = 0
    validation_ratio: float = 0

    def __init__(self, name: str, ratio_manager: RatioManager):
        self.name = name
        self.ratio_manager = ratio_manager

    def update(self, value: float):
        self.value = value
        self.validation_ratio = self.ratio_manager.get_ratio(value)
