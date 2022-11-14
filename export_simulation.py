import os
import time

from src.parameter.parameter import Parameter
from src.procedure.export_procedure import apply_export_procedure
from src.show_user.show_user_generator import get_valid_show_user

NB_X = 1
NB_Y = 1
NB_DRONE_PER_FAMILY = 1
STEP_TAKEOFF = 1.5
ANGLE_TAKEOFF = 0
SHOW_DURATION_FRAME = 1


def main() -> None:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    time_begin = time.time()
    export_report, show_check_report = apply_export_procedure(
        get_valid_show_user(
            NB_X,
            NB_Y,
            NB_DRONE_PER_FAMILY,
            STEP_TAKEOFF,
            ANGLE_TAKEOFF,
            SHOW_DURATION_FRAME,
        )["show"],
        parameter,
    )
    print(time.time() - time_begin)
    print(show_check_report.get_contenor_report(0, "   "))


if __name__ == "__main__":
    main()
