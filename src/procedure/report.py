from abc import abstractclassmethod


class Displayer:
    validation: bool = False

    @abstractclassmethod
    def get_report(self) -> str:
        pass


class Contenor:
    validation: bool = False
    name: str

    @staticmethod
    def report_formater(
        report: str, indentation_level: int, indentation_type: str
    ) -> str:
        return indentation_level * indentation_type + report + "\n"

    ### TO DO: decompose the 3 parts of this function
    def get_children_report(self, indentation_level: int, indentation_type: str) -> str:
        children_report = ""
        for attribute in self.__dict__.values():
            if isinstance(attribute, list):
                for attribute_element in attribute:
                    if isinstance(attribute_element, Contenor):
                        children_report += attribute_element.get_children_report(
                            indentation_level + 1, indentation_type
                        )
            if isinstance(attribute, Contenor):
                if attribute.validation:
                    children_report += self.report_formater(
                        attribute.name,
                        indentation_level,
                        indentation_type,
                    )
                    children_report += self.report_formater(
                        attribute.get_children_report(
                            indentation_level + 1, indentation_type
                        ),
                        indentation_level,
                        indentation_type,
                    )
            if isinstance(attribute, Displayer):
                if attribute.validation:
                    children_report += self.report_formater(
                        attribute.get_report(),
                        indentation_level,
                        indentation_type,
                    )
        return children_report
