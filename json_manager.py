import os

from dance_test_json import JSON_EXAMPLE
from src.parameter.parameter import Parameter
from src.procedure.import_procedure import apply_import_procedure


def main() -> None:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    show_user, import_report = apply_import_procedure(JSON_EXAMPLE, parameter)
    print(import_report.get_contenor_report(0, "   "))


if __name__ == "__main__":
    main()
