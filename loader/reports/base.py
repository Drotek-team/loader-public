from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, cast

from pydantic import BaseModel
from pydantic.fields import FieldInfo

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

        if len(self.model_fields) == 0:
            msg = f"Report has no fields: {self.__class__.__name__}"
            raise TypeError(msg)

        for field_name, field in self.model_fields.items():
            field_value = getattr(self, field_name)
            if (
                field_value is None
                or (isinstance(field_value, int) and field_name == "drone_index")
                or (isinstance(field_value, set) and field_name == "drone_indices")
            ):
                pass
            elif isinstance(field_value, BaseMessage):
                nb_errors += len(field_value)
            elif isinstance(field_value, (list, dict)):
                nb_errors += self._get_nb_errors_list_or_dict(field_name, field)
            else:
                msg = f"Report type not supported: {field.annotation} for {self.__class__.__name__}.{field_name}"
                raise TypeError(msg)

        return nb_errors

    def _get_nb_errors_list_or_dict(
        self,
        field_name: str,
        field: FieldInfo,
    ) -> int:
        nb_errors = 0
        field_value = getattr(self, field_name)
        assert field.annotation is not None
        if isinstance(field_value, dict):
            reports_or_infractions = list(
                cast(Dict[Any, BaseMessage], field_value).values(),
            )
        else:
            reports_or_infractions = cast(List[BaseMessage], field_value)

        if len(reports_or_infractions) == 0:
            pass
        else:
            try:
                for item in reports_or_infractions:
                    nb_errors += len(item)
            except TypeError:
                msg = f"Report type not supported: {field.annotation} for {self.__class__.__name__}.{field_name}"
                raise TypeError(msg) from None

        return nb_errors


class BaseSummary(BaseMessage):
    def __add__(self, other: TBaseSummary) -> TBaseSummary:
        raise NotImplementedError


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
