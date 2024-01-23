from pathlib import Path

from loader.schemas import IostarJsonGcs, ShowUser
from loader.schemas.vviz import Vviz

if __name__ == "__main__":
    SHOW_PATH = Path("iostar_json_gcs_valid.json")

    iostar_json_gcs = IostarJsonGcs.model_validate_json(SHOW_PATH.read_text())
    show_user = ShowUser.from_iostar_json_gcs(iostar_json_gcs)
    vviz = Vviz.from_show_user(
        show_user=show_user,
        performance_name="Import drone show vviz 8 drones_2023-12-21_09-21-53",
    )
    show_vviz_path = SHOW_PATH.with_suffix(".vviz")
    show_vviz_path.write_text(vviz.model_dump_json(exclude_none=True))
