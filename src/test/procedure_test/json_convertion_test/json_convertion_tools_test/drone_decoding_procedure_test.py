import pytest

from .....parameter.parameter import Parameter
from .....procedure.json_conversion.json_convertion_tools.drone_decoding_procedure import (
    decode_drone,
)
from .....procedure.json_conversion.json_convertion_tools.drone_decoding_report import (
    DroneDecodingReport,
)
from .dance_example import DANCE_EXAMPLE


def test_valid_dance_decoding():
    parameter = Parameter()
    parameter.load_parameter()
    drone_decoding_report = DroneDecodingReport()
    decode_drone(
        DANCE_EXAMPLE, 0, parameter.json_format_parameter, drone_decoding_report
    )
    assert drone_decoding_report.header_format_report.validation
    assert len(drone_decoding_report.section_headers_format_report) == 0
