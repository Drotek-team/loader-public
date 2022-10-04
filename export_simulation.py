from dance_test_json import JSON_EXAMPLE
from src.parameter.parameter import Parameter
import os
from src.show_user.show_user_simulation import get_valid_show_user
from src.procedure.export_procedure import apply_export_procedure
from src.procedure.export_report import ExportReport

NB_X = 20
NB_Y = 20
NB_DRONE_PER_FAMILY = 1
STEP_TAKEOFF = 1.0
ANGLE_TAKEOFF = 0
SHOW_DURATION_FRAME = 29_000  # frame


def main() -> None:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    export_report = ExportReport()

    apply_export_procedure(
        get_valid_show_user(
            NB_X,
            NB_Y,
            NB_DRONE_PER_FAMILY,
            STEP_TAKEOFF,
            ANGLE_TAKEOFF,
            SHOW_DURATION_FRAME,
        )["show"],
        export_report,
        parameter,
    )
    # print(export_report.get_contenor_report(0, "   "))


if __name__ == "__main__":
    main()
