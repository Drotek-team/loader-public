from src.migration.migration_sp_ij.ij_to_sp_procedure import ij_to_sp_procedure
from src.migration.migration_sp_ijg.sp_to_ijg_procedure import sp_to_ijg_procedure
from src.procedure.export_procedure import apply_export_procedure
from src.show_user.show_user_generator import get_valid_show_user

NB_X = 2
NB_Y = 2
NB_DRONE_PER_FAMILY = 1
STEP_TAKEOFF = 1.5
ANGLE_TAKEOFF = 0
SHOW_DURATION_SECOND = 30.0


def main() -> None:
    show_user = get_valid_show_user(
        NB_X,
        NB_Y,
        NB_DRONE_PER_FAMILY,
        STEP_TAKEOFF,
        ANGLE_TAKEOFF,
        SHOW_DURATION_SECOND,
    )
    iostar_json, show_check_report = apply_export_procedure(
        show_user,
    )
    show_px4 = ij_to_sp_procedure(iostar_json)
    iostar_json_gcs = sp_to_ijg_procedure(show_px4)
    print(show_check_report.get_contenor_report(0, "   "))
    print(show_user)
    iostar_json_gcs.get_json()
    json_file = open("export_show_user_simulation.json", "w")
    json_file.write(iostar_json_gcs.get_json())


if __name__ == "__main__":
    main()
