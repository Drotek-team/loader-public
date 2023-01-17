from abc import ABC, abstractmethod
from typing import List


class ErrorMessage(ABC):
    name: str

    @property
    @abstractmethod
    def user_validation(self) -> bool:
        pass

    @abstractmethod
    def display_message(self, indentation_level: int, indentation_type: str) -> str:
        pass


class Displayer(ErrorMessage):
    def __init__(
        self, name: str, *, validation: bool = False, annexe_message: str = ""
    ):
        self.name = name
        self._validation = validation
        self._annexe_message = annexe_message

    def __hash__(self) -> int:  # pyright: ignore
        return hash((self.name, self._annexe_message))

    @property
    def user_validation(self) -> bool:
        return self._validation

    # TODO: put the indention part on the error message
    def display_message(self, indentation_level: int, indentation_type: str) -> str:
        if self.user_validation:
            return ""
        if self._annexe_message == "":
            return f"{indentation_level * indentation_type}[Displayer] {self.name} \n"
        return f"{indentation_level * indentation_type}[Displayer] {self.name}:{self._annexe_message} \n"

    def validate(self):
        self._validation = True

    def update_annexe_message(self, annexe_message: str) -> None:
        self._annexe_message += annexe_message


class ErrorMessageList(ErrorMessage):
    def __init__(self, name: str, error_messages: List[ErrorMessage]):
        self.name = name
        self._error_messages = error_messages

    def __iter__(self):
        yield from self._error_messages

    def __getitem__(self, error_message_index: int) -> ErrorMessage:
        return self._error_messages[error_message_index]

    def __len__(self) -> int:
        return len(self._error_messages)

    def add_error_message(self, error_message: ErrorMessage) -> None:
        self._error_messages.append(error_message)

    def add_error_messages(self, error_messages: List[ErrorMessage]) -> None:
        self._error_messages.extend(error_messages)

    @property
    def user_validation(self) -> bool:
        return all(
            error_message.user_validation for error_message in self._error_messages
        )

    def display_message(self, indentation_level: int, indentation_type: str) -> str:
        if self.user_validation:
            return ""
        initial_message = (
            f"{indentation_level * indentation_type}[Error Message List] {self.name} \n"
        )
        list_messages = "".join(
            [
                error_message.display_message(indentation_level + 1, indentation_type)
                for error_message in self._error_messages
            ]
        )
        return initial_message + list_messages


class Contenor(ErrorMessage):
    @property
    def user_validation(self) -> bool:
        return all(
            error_message.user_validation
            for error_message in self.__dict__.values()
            if isinstance(error_message, ErrorMessage)
        )

    def display_message(self, indentation_level: int, indentation_type: str) -> str:
        if self.user_validation:
            return ""
        initial_message = (
            f"{indentation_level * indentation_type}[Contenor] {self.name} \n"
        )
        children_message = "".join(
            [
                attribute.display_message(indentation_level + 1, indentation_type)
                for attribute in self.__dict__.values()
                if isinstance(attribute, ErrorMessage)
            ]
        )
        return initial_message + children_message
