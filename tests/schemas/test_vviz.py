import pytest
from loader.schemas.show_user.generate_show_user import ShowUserConfiguration, get_valid_show_user
from loader.schemas.vviz import ExportType, Vviz


@pytest.mark.parametrize(
    "export_type, duration_before_takeoff",
    [
        (ExportType.VVIZ, 0.0),
        (ExportType.Finale3D, 1.0),
    ],
)
def test_vviz(export_type: ExportType, duration_before_takeoff: float) -> None:
    show_user = get_valid_show_user(
        ShowUserConfiguration(duration_before_takeoff=duration_before_takeoff)
    )
    Vviz.from_show_user(
        show_user=show_user,
        performance_name="Import drone show vviz 8 drones_2023-12-21_09-21-53",
        lat=39.905963,
        lon=-75.166393,
        alt=0.0,
        export_type=export_type,
        airframe="IOStar",
        lumens=900.0,
        source_type="Dome",
        vdl="10s Gold Glittering Gerb",
    )
