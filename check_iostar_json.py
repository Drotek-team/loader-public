from pathlib import Path

from loader.reports import GlobalReport
from loader.schemas import IostarJsonGcs, ShowUser

iostar_json_gcs = IostarJsonGcs.parse_file(Path("iostar_json_gcs_valid.json"))
show_user = ShowUser.from_iostar_json_gcs(iostar_json_gcs)

global_report = GlobalReport.generate(show_user)
