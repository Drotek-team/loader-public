from src.parameter.parameter import Parameter
import os
from src.show_user.show_user_generator import get_valid_show_user
from src.check.export_procedure import apply_export_procedure
from src.check.export_report import ExportReport
import time

NB_X = 5
NB_Y = 5
NB_DRONE_PER_FAMILY = 1
STEP_TAKEOFF = 1.0
ANGLE_TAKEOFF = 0
SHOW_DURATION_FRAME = 4000


def main() -> None:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    export_report = ExportReport()
    time_begin = time.time()
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
    print(time.time() - time_begin)
    # print(export_report.get_contenor_report(0, "   "))


if __name__ == "__main__":
    main()
