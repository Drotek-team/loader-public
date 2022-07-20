from abc import abstractclassmethod
from dataclasses import dataclass


class Displayer:
    validation: bool = False

    @abstractclassmethod
    def get_report(self) -> str:
        pass


class Contenor:
    validation: bool = False

    def get_children_report(self) -> str:
        children_report = ""
        for attribute in self.__dict__.values():
            if isinstance(attribute, list):
                children_report += "\n".join(
                    attribute_element.get_children_report()
                    for attribute_element in attribute
                    if isinstance(attribute_element, Contenor)
                )
            if isinstance(attribute, Contenor):
                if not (attribute.validation):
                    children_report += attribute.get_children_report() + "\n"
            if isinstance(attribute, Displayer):
                if not (attribute.validation):
                    children_report += attribute.get_report() + "\n"
        return children_report
