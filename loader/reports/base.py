from typing import Any, List, Optional, Type, TypeVar, cast

from pydantic import BaseModel
from pydantic.fields import ModelField

TBaseInfraction = TypeVar("TBaseInfraction", bound="BaseInfraction")
TBaseReport = TypeVar("TBaseReport", bound="BaseReport")


class BaseMessage(BaseModel):
    def __len__(self) -> int:
        raise NotImplementedError


class BaseInfraction(BaseMessage):
    def __len__(self) -> int:
        return 1

    @classmethod
    def generate(
        cls: Type[TBaseInfraction],
        *args: Any,  # noqa: ANN401
        **kwargs: Any,  # noqa: ANN401
    ) -> Optional[TBaseInfraction]:
        raise NotImplementedError


class BaseReport(BaseMessage):
    def __len__(self) -> int:
        nb_errors = 0

        if len(self.__fields__) == 0:
            msg = f"Report has no fields: {self.__class__.__name__}"
            raise TypeError(msg)

        for field in self.__fields__.values():
            if getattr(self, field.name) is None or (
                isinstance(getattr(self, field.name), int) and field.name == "drone_index"
            ):
                pass
            elif isinstance(getattr(self, field.name), BaseMessage):
                nb_errors += len(cast(BaseMessage, getattr(self, field.name)))
            elif isinstance(getattr(self, field.name), list):
                nb_errors += self._get_nb_errors_list(field)
            else:
                msg = f"Report type not supported: {field.type_} for {self.__class__.__name__}.{field.name}"
                raise TypeError(msg)

        return nb_errors

    def _get_nb_errors_list(self, field: ModelField) -> int:
        nb_errors = 0
        type_ = List[field.type_]
        reports_or_infractions = cast(List[BaseMessage], getattr(self, field.name))

        if len(reports_or_infractions) == 0:
            pass
        else:
            try:
                for item in reports_or_infractions:
                    nb_errors += len(item)
            except TypeError:
                msg = (
                    f"Report type not supported: {type_} for {self.__class__.__name__}.{field.name}"
                )
                raise TypeError(msg) from None

        return nb_errors

    @classmethod
    def generate(cls: Type[TBaseReport], *args: Any, **kwargs: Any) -> TBaseReport:  # noqa: ANN401
        raise NotImplementedError

    @classmethod
    def generate_or_none(
        cls: Type[TBaseReport],
        *args: Any,  # noqa: ANN401
        **kwargs: Any,  # noqa: ANN401
    ) -> Optional[TBaseReport]:
        report = cls.generate(*args, **kwargs)
        return report if len(report) else None
