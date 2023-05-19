from typing import List, Optional

import pytest
from loader.reports.base import (
    BaseInfraction,
    BaseReport,
    get_report_validation,
)


class DummyBaseInfraction(BaseInfraction):
    important_attribute: int


class DummierBaseInfraction(BaseInfraction):
    importanter_attribute: int


class DummyReport(BaseReport):
    dummy_infraction: Optional[DummyBaseInfraction]


class DummyBaseReport(BaseReport):
    dummy_report: Optional[DummyReport]


class DummestBaseReport(BaseReport):
    dummy_base_infraction: Optional[DummyBaseInfraction]
    dummier_base_infraction: List[DummierBaseInfraction]
    dummy_base_reports: List[DummyBaseReport]


DUMMEST_BASE_REPORT = DummestBaseReport(
    dummy_base_infraction=DummyBaseInfraction(important_attribute=0),
    dummier_base_infraction=[
        DummierBaseInfraction(importanter_attribute=1),
        DummierBaseInfraction(importanter_attribute=2),
        DummierBaseInfraction(importanter_attribute=3),
    ],
    dummy_base_reports=[
        DummyBaseReport(dummy_report=DummyReport(dummy_infraction=None)),
        DummyBaseReport(
            dummy_report=DummyReport(
                dummy_infraction=DummyBaseInfraction(important_attribute=0),
            ),
        ),
        DummyBaseReport(dummy_report=DummyReport(dummy_infraction=None)),
    ],
)


def test_base_report_get_nb_errors_standard_case() -> None:
    assert DUMMEST_BASE_REPORT.get_nb_errors() == 5


def test_base_report_get_nb_errors_no_fields() -> None:
    class DummyBaseReportWithNoFields(BaseReport):
        pass

    with pytest.raises(TypeError):
        DummyBaseReportWithNoFields().get_nb_errors()


def test_base_report_get_nb_errors_list_unsupported_type() -> None:
    class DummyListUnsuportedType(BaseReport):
        dummy_list: List[int]

    with pytest.raises(TypeError):
        DummyListUnsuportedType(dummy_list=[1, 2, 3]).get_nb_errors()


def test_base_report_get_nb_errors_report_unsupported_type() -> None:
    class DummyReportUnsuportedType(BaseReport):
        dummy_report: int

    with pytest.raises(TypeError):
        DummyReportUnsuportedType(dummy_report=1).get_nb_errors()


class CleverBaseReport(BaseReport):
    clever_base_infractions: List[DummierBaseInfraction]


# TODO: change the name, they are funny but are to understand
def test_get_base_report_validation() -> None:
    assert get_report_validation(None)
    assert get_report_validation(DummyReport(dummy_infraction=None))
    assert not (
        get_report_validation(
            DummyReport(
                dummy_infraction=DummyBaseInfraction(important_attribute=0),
            ),
        )
    )
    assert get_report_validation(CleverBaseReport(clever_base_infractions=[]))
    assert not (
        get_report_validation(
            CleverBaseReport(
                clever_base_infractions=[
                    DummierBaseInfraction(importanter_attribute=0),
                ],
            ),
        )
    )
