from dance_test_json import JSON_EXAMPLE
from src.procedure.import_procedure import apply_import_procedure
from src.procedure.import_report import ImportReport
from src.parameter.parameter import Parameter
import os


def main() -> None:
    import_report = ImportReport()
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    apply_import_procedure(JSON_EXAMPLE, import_report, parameter)
    print(import_report.get_contenor_report(0, "   "))


if __name__ == "__main__":
    main()
