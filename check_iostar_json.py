from pathlib import Path

from loader.reports import GlobalReport
from loader.schemas import IostarJsonGcs, ShowUser

dance_path = Path("iostar_json_gcs_valid.json")
iostar_json_gcs = IostarJsonGcs.model_validate_json(dance_path.read_text())
iostar_json_gcs.model_dump_json()
show_user = ShowUser.from_iostar_json_gcs(iostar_json_gcs)

global_report = GlobalReport.generate(show_user)
print(global_report.summarize().model_dump_json(indent=2))  # noqa: T201
