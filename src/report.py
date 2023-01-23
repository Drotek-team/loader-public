from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Union


class ErrorMessage(ABC):
    name: str

    @property
    @abstractmethod
    def user_validation(self) -> bool:
        pass

    def display_message(self, indentation_level: int = 0) -> str:
        indentation_type = " "
        return f"{indentation_level * indentation_type}"


class Displayer(ErrorMessage):
    def __init__(self, name: str, annexe_message: str = ""):
        self.name = name
        self._validation = False
        self._annexe_message = annexe_message

    def __hash__(self) -> int:  # pyright: ignore
        return hash((self.name, self._annexe_message))

    def __getitem__(self, displayer_name: str) -> "Displayer":
        if self.name == displayer_name:
            msg = f"the name should be {self.name}"
            raise NameError(msg)
        return self

    @property
    def user_validation(self) -> bool:
        return self._validation

    def display_message(self, indentation_level: int = 0) -> str:
        if self.user_validation:
            return ""
        message_begin = super().display_message(indentation_level)
        if self._annexe_message == "":
            return f"{message_begin}[Displayer] {self.name} \n"
        return f"{message_begin}[Displayer] {self.name}:{self._annexe_message} \n"

    def validate(self):
        self._validation = True

    def update_annexe_message(self, annexe_message: str) -> None:
        self._annexe_message += annexe_message


@dataclass(frozen=True)
class PerformanceInfraction(ErrorMessage):
    name: str
    frame: int
    value: float
    threshold: float
    metric_convention: bool

    def __getitem__(self, displayer_name: str) -> "PerformanceInfraction":
        if self.name == displayer_name:
            msg = f"the name should be {self.name}"
            raise NameError(msg)
        return self

    @property
    def user_validation(self) -> bool:
        return False

    def display_message(self, indentation_level: int = 0) -> str:
        message_begin = super().display_message(indentation_level)
        metric_convention_name = "max" if self.metric_convention else "min"
        return (
            f"{message_begin}[Performance Infraction] The performance {self.name} has the value: {self.value:.2f}"
            f" ({metric_convention_name}: {self.threshold}) at the frame {self.frame}"
        )


@dataclass(frozen=True)
class CollisionInfraction(ErrorMessage):
    name: str
    drone_index_1: int
    drone_index_2: int
    distance: float
    in_air: bool

    def __getitem__(self, displayer_name: str) -> "CollisionInfraction":
        if self.name == displayer_name:
            msg = f"the name should be {self.name}"
            raise NameError(msg)
        return self

    @property
    def user_validation(self) -> bool:
        return False

    def display_message(self, indentation_level: int = 0) -> str:
        message_begin = super().display_message(indentation_level)
        return (
            f"{message_begin}[Collision Infraction] Collision between drone {self.drone_index_1} and drone {self.drone_index_2} "
            f"{'in air' if self.in_air else 'on ground'} with a distance of {self.distance}"
        )


class Contenor(ErrorMessage):
    def __init__(self, name: str):
        self.name = name
        self._error_messages: Dict[
            str,
            Union["Contenor", Displayer, PerformanceInfraction, CollisionInfraction],
        ] = {}

    def add_error_message(
        self,
        error_message: Union[
            "Contenor", Displayer, PerformanceInfraction, CollisionInfraction
        ],
    ) -> None:
        if error_message.name in self._error_messages:
            msg = f"{error_message.name} already exist in {self._error_messages.keys()}"
            raise NameError(msg)
        self._error_messages[error_message.name] = error_message

    def __getitem__(
        self, error_message_name: str
    ) -> Union["Contenor", Displayer, PerformanceInfraction, CollisionInfraction]:
        if error_message_name not in self._error_messages:
            msg = f"the name should be {self._error_messages.keys()}"
            raise KeyError(msg)
        return self._error_messages[error_message_name]

    @property
    def user_validation(self) -> bool:
        return all(
            error_message.user_validation
            for error_message in self._error_messages.values()
        )

    def display_message(self, indentation_level: int = 0) -> str:
        if self.user_validation:
            return ""
        message_begin = super().display_message(indentation_level)
        initial_message = f"{message_begin}[Contenor] {self.name} \n"
        children_message = "".join(
            [
                error_message.display_message(indentation_level + 1)
                for error_message in self._error_messages.values()
            ]
        )
        return initial_message + children_message
