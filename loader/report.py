from typing import Any, Dict, List, Union, cast

from pydantic import BaseModel
from pydantic.fields import ModelField


class BaseMessage(BaseModel):
    def get_nb_errors(self) -> int:
        raise NotImplementedError


class BaseInfraction(BaseMessage):
    def get_nb_errors(self) -> int:
        return 1


class BaseReport(BaseMessage):
    def get_nb_errors(self) -> int:
        nb_errors = 0

        if len(self.__fields__) == 0:
            msg = f"Report has no fields: {self.__class__.__name__}"
            raise TypeError(msg)

        for field in self.__fields__.values():
            if getattr(self, field.name) is None:
                pass
            elif isinstance(getattr(self, field.name), BaseMessage):
                nb_errors += cast(
                    BaseMessage,
                    getattr(self, field.name),
                ).get_nb_errors()
            elif isinstance(getattr(self, field.name), (list, dict)):
                nb_errors += self._get_nb_errors_list_or_dict(field)
            else:
                msg = f"Report type not supported: {field.type_} for {field.name}"
                raise TypeError(msg)

        return nb_errors

    def _get_nb_errors_list_or_dict(
        self,
        field: ModelField,
    ) -> int:
        nb_errors = 0
        if isinstance(getattr(self, field.name), dict):
            type_ = Dict[Any, field.type_]
            reports_or_infractions = list(
                cast(
                    Dict[Any, BaseMessage],
                    getattr(self, field.name),
                ).values(),
            )
        else:
            type_ = List[field.type_]
            reports_or_infractions = cast(
                List[BaseMessage],
                getattr(self, field.name),
            )

        if len(reports_or_infractions) == 0:
            pass
        else:
            try:
                for item in reports_or_infractions:
                    nb_errors += item.get_nb_errors()
            except AttributeError:
                msg = f"Report type not supported: {type_} for {field.name}"
                raise TypeError(msg) from None

        return nb_errors


def get_base_report_validation(
    base_report: Union[BaseMessage, None],
) -> bool:
    if base_report is None:
        return True
    return base_report.get_nb_errors() == 0
