# from ...parameter.parameter import Parameter
# from .IJ_to_SP_procedure import IJ_to_SP_procedure
# from .IJ_to_SP_report import IJ_to_SP_report

# def test_valid_json_extraction():
#     parameter = Parameter()
#     parameter.load_parameter(os.getcwd())
#     json_extraction_report = IJ_to_SP_report(
#         get_nb_drone_per_family(JSON_EXAMPLE["show"])
#         * len(JSON_EXAMPLE["show"]["families"])
#     )
#     IJ_to_SP_procedure(
#         JSON_EXAMPLE,
#         parameter.iostar_parameter,
#         parameter.json_binary_parameter,
#         json_extraction_report,
#     )
#     assert json_extraction_report.validation
