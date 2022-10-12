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
    def displayer_formater(
        report: str, indentation_level: int, indentation_type: str
    ) -> str:
        return f"{indentation_level * indentation_type} [Displayer] {report}  \n"

    @staticmethod
    def contenor_formater(
        report: str, indentation_level: int, indentation_type: str
    ) -> str:
        return f"{indentation_level * indentation_type} [Contenor] {report}  \n"

    ### TO DO: decompose the 3 parts of this function
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
                            attribute_element.get_report(),
                            indentation_level + 1,
                            indentation_type,
                        )
            if isinstance(attribute, Contenor):
                if not (attribute.validation):
                    children_report += attribute.get_contenor_report(
                        indentation_level + 1, indentation_type
                    )
            if isinstance(attribute, Displayer):
                if not (attribute.validation):
                    children_report += self.displayer_formater(
                        attribute.get_report(),
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
