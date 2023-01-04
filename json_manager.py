from dance_test_json import JSON_EXAMPLE
from src.procedure.import_procedure import apply_import_procedure


def main() -> None:
    show_user, import_report = apply_import_procedure(JSON_EXAMPLE)
    print(import_report.get_contenor_report(0, "   "))


if __name__ == "__main__":
    main()
