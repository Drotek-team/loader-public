from dance_test_json import JSON_EXAMPLE
from src.procedure.import_procedure import apply_import_procedure
from src.procedure.import_report import ImportReport


def main() -> None:
    import_report = ImportReport()
    apply_import_procedure(JSON_EXAMPLE, import_report)


if __name__ == "__main__":
    main()
