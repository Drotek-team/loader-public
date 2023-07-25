from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, cast

from pydantic import BaseModel
from pydantic.fields import ModelField

from .ranges import get_ranges_from_drone_indices

TBaseMessage = TypeVar("TBaseMessage", bound="BaseMessage")
TBaseSummary = TypeVar("TBaseSummary", bound="BaseSummary")
TBaseInfraction = TypeVar("TBaseInfraction", bound="BaseInfraction")
TBaseReport = TypeVar("TBaseReport", bound="BaseReport")
T = TypeVar("T")


def apply_func_on_optional_pair(
    optional1: Optional[T],
    optional2: Optional[T],
    func: Callable[[T, T], T],
) -> Optional[T]:
    if optional1 is None:
        return optional2
    if optional2 is None:
        return optional1
    return func(optional1, optional2)


class BaseMessage(BaseModel):
    def __len__(self) -> int:
        nb_errors = 0

        if len(self.__fields__) == 0:
            msg = f"Report has no fields: {self.__class__.__name__}"
            raise TypeError(msg)

        for field in self.__fields__.values():
            if (
                getattr(self, field.name) is None
                or (isinstance(getattr(self, field.name), int) and field.name == "drone_index")
                or (isinstance(getattr(self, field.name), set) and field.name == "drone_indices")
            ):
                pass
            elif isinstance(getattr(self, field.name), BaseMessage):
                nb_errors += len(cast(BaseMessage, getattr(self, field.name)))
            elif isinstance(getattr(self, field.name), (list, dict)):
                nb_errors += self._get_nb_errors_list_or_dict(field)
            else:
                msg = f"Report type not supported: {field.type_} for {self.__class__.__name__}.{field.name}"
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
                cast(Dict[Any, BaseMessage], getattr(self, field.name)).values(),
            )
        else:
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


class BaseSummary(BaseMessage):
    def __add__(self, other: TBaseSummary) -> TBaseSummary:
        raise NotImplementedError

    class Config:
        json_encoders: Dict[Any, Callable[[Any], Any]] = {set: get_ranges_from_drone_indices}


class BaseInfractionsSummary(BaseSummary):
    nb_infractions: int = 0

    def __len__(self) -> int:
        return self.nb_infractions


class BaseReportSummary(BaseSummary):
    pass


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

    def summarize(self) -> BaseInfractionsSummary:
        raise NotImplementedError


class BaseReport(BaseMessage):
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

    def summarize(self) -> BaseReportSummary:
        raise NotImplementedError
