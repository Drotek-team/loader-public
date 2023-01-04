from dataclasses import dataclass


@dataclass(frozen=True)
class JsonBinaryParameter:
    magic_number = 43605
    fmt_header = ">HIB"
    fmt_section_header = ">BII"
    dance_size_max = 100_000
    frame_reformat_factor = 40
    position_reformat_factor = 4
    fire_chanel_value_min = 0
    fire_chanel_value_max = 2
    fire_duration_value_frame_min = 0
    fire_duration_value_frame_max = 28_800
    position_value_min = -32768
    position_value_max = 327687
    color_value_min = 0
    color_value_max = 255
    show_duration_min_second = 0.0
    show_duration_max_second = 1800.0


JSON_BINARY_PARAMETER = JsonBinaryParameter()
