from dataclasses import dataclass
from typing import List


@dataclass
class ErrorMessage:
    name: str = ""
    validation: str = False


@dataclass
class Displayer(ErrorMessage):
    annexe_message: str = ""

    def __hash__(self) -> int:
        return hash((self.name, self.annexe_message))

    def __eq__(self, __o: "Displayer") -> bool:
        return self.name == __o.name and self.annexe_message == __o.annexe_message

    @property
    def report(self) -> str:
        return self.name


@dataclass
class Contenor(ErrorMessage):
    def update_contenor_validation(self) -> None:
        displayer_validation = all(
            displayer.validation
            for displayer in self.__dict__.values()
            if isinstance(displayer, Displayer)
        )
        contenor_validation = all(
            contenor.validation
            for contenor in self.__dict__.values()
            if isinstance(contenor, Contenor)
        )
        error_message_list_validation = all(
            error_message.validation
            for attributes in self.__dict__.values()
            if isinstance(attributes, List)
            for error_message in attributes
            if isinstance(error_message, ErrorMessage)
        )
        self.validation = (
            displayer_validation
            and contenor_validation
            and error_message_list_validation
        )

    @staticmethod
    def displayer_formater(
        report: str, indentation_level: int, indentation_type: str
    ) -> str:
        return f"{indentation_level * indentation_type} [Displayer] {report}  \n"

    @staticmethod
    def contenor_formater(
        report: str, indentation_level: int, indentation_type: str
    ) -> str:
        return f"{indentation_level * indentation_type} [Contenor] {report}  \n"

    # TODO: place a test on that
    def get_children_report(self, indentation_level: int, indentation_type: str) -> str:
        children_report = ""
        for attribute in self.__dict__.values():
            if isinstance(attribute, list):
                for attribute_element in attribute:
                    if isinstance(attribute_element, Contenor) and not (
                        attribute_element.validation
                    ):
                        children_report += attribute_element.get_contenor_report(
                            indentation_level + 1, indentation_type
                        )
                    if isinstance(attribute_element, Displayer) and not (
                        attribute_element.validation
                    ):
                        children_report += self.displayer_formater(
                            attribute_element.report,
                            indentation_level + 1,
                            indentation_type,
                        )
            if isinstance(attribute, Contenor) and not (attribute.validation):
                children_report += attribute.get_contenor_report(
                    indentation_level + 1, indentation_type
                )
            if isinstance(attribute, Displayer) and not (attribute.validation):
                children_report += self.displayer_formater(
                    attribute.report,
                    indentation_level + 1,
                    indentation_type,
                )
        return children_report

    def get_contenor_report(self, indentation_level: int, indentation_type: str) -> str:
        return self.contenor_formater(
            self.name,
            indentation_level,
            indentation_type,
        ) + self.get_children_report(indentation_level, indentation_type)
