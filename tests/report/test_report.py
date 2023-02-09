from loader.report.report import (
    BaseReport,
    get_base_report_validation,
)


class DummyBaseReport(BaseReport):
    important_attribute: int


class DummierBaseReport(BaseReport):
    importanter_attribute: int


class DummestBaseReport(BaseReport):
    dummy_base_report: DummyBaseReport
    dummier_base_report: DummierBaseReport


def test_get_base_report_validation() -> None:
    dummest_base_report = DummestBaseReport(
        dummy_base_report=DummyBaseReport(important_attribute=0),
        dummier_base_report=DummierBaseReport(importanter_attribute=1),
    )
    assert not (get_base_report_validation(dummest_base_report))
    dummest_base_report.dummy_base_report = (
        None  # pyright:ignore[reportGeneralTypeIssues]
    )
    assert not (get_base_report_validation(dummest_base_report))
    dummest_base_report.dummier_base_report = (
        None  # pyright:ignore[reportGeneralTypeIssues]
    )
    assert get_base_report_validation(dummest_base_report)
    assert dummest_base_report.dict() == {
        "dummy_base_report": None,
        "dummier_base_report": None,
    }
