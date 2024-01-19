import pytest
from loader.reports.base import BaseInfraction, BaseReport


class DummyBaseInfraction(BaseInfraction):
    important_attribute: int


class DummierBaseInfraction(BaseInfraction):
    importanter_attribute: int


class DummyReport(BaseReport):
    dummy_infraction: DummyBaseInfraction | None


class DummyBaseReport(BaseReport):
    dummy_report: DummyReport | None


class DummestBaseReport(BaseReport):
    dummy_base_infraction: DummyBaseInfraction | None
    dummier_base_infraction: list[DummierBaseInfraction]
    dummy_base_reports: list[DummyBaseReport]


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
    assert len(DUMMEST_BASE_REPORT) == 5


def test_base_report_get_nb_errors_no_fields() -> None:
    class DummyBaseReportWithNoFields(BaseReport):
        pass

    with pytest.raises(TypeError, match="^Report has no fields: DummyBaseReportWithNoFields$"):
        len(DummyBaseReportWithNoFields())


def test_base_report_get_nb_errors_list_unsupported_type() -> None:
    class DummyListUnsuportedType(BaseReport):
        dummy_list: list[int]

    with pytest.raises(
        TypeError,
        match=r"^Report type not supported: list\[int\] for DummyListUnsuportedType.dummy_list$",
    ):
        len(DummyListUnsuportedType(dummy_list=[1, 2, 3]))


def test_base_report_get_nb_errors_report_unsupported_type() -> None:
    class DummyReportUnsuportedType(BaseReport):
        dummy_report: int

    with pytest.raises(
        TypeError,
        match="^Report type not supported: <class 'int'> for DummyReportUnsuportedType.dummy_report$",
    ):
        len(DummyReportUnsuportedType(dummy_report=1))


def test_base_report_get_nb_errors_report_width_drone_index() -> None:
    class DummyReportWidthDroneIndex(BaseReport):
        drone_index: int

    assert not len(DummyReportWidthDroneIndex(drone_index=1))


class CleverBaseReport(BaseReport):
    clever_base_infractions: list[DummierBaseInfraction]


def test_get_base_report_validation() -> None:
    assert not len(DummyReport(dummy_infraction=None))
    assert len(
        DummyReport(
            dummy_infraction=DummyBaseInfraction(important_attribute=0),
        ),
    )
    assert not len(CleverBaseReport(clever_base_infractions=[]))
    assert len(
        CleverBaseReport(
            clever_base_infractions=[
                DummierBaseInfraction(importanter_attribute=0),
            ],
        ),
    )
