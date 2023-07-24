from pathlib import Path

from loader.reports import GlobalReport
from loader.schemas import IostarJsonGcs, ShowUser

iostar_json_gcs = IostarJsonGcs.parse_file(
    Path("/home/jonathan/Downloads/dances/BIGUGLIA 2023.json"),
)
show_user = ShowUser.from_iostar_json_gcs(iostar_json_gcs)

global_report = GlobalReport.generate(show_user)
print(global_report.summarize().json(indent=2))  # noqa: T201
