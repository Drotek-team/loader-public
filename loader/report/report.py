import json
from typing import Any, Dict, Optional

from pydantic import BaseModel


class BaseReport(BaseModel):
    pass


def get_base_report_validation(base_report: Optional[BaseReport]) -> bool:
    if base_report is None:
        return True
    base_report_json: Dict[str, Any] = json.loads(base_report.json())
    return all(
        (base_report_value is None) for base_report_value in base_report_json.values()
    )
