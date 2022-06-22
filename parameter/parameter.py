import json
from dataclasses import dataclass


@dataclass(frozen=True)
class TakeoffParameter:
    takeoff_altitude: int
    takeoff_duration: int


@dataclass(frozen=True)
class TimecodeParameter:
    show_time_begin: int
    position_frequence: int
    color_frequence: int


@dataclass(frozen=True)
class IostarParameter:
    iostar_mass: float
    iostar_drag_vertical_coef: float
    fire_chanel_format_min: int
    fire_chanel_format_max: int
    fire_duration_format_min: int
    fire_duration_format_max: int
    position_format_min: int
    position_format_max: int
    color_format_min: int
    color_format_max: int
    position_max: float
    horizontal_velocity_max: float
    horizontal_acceleration_max: float
    force_up_max: float
    force_down_max: float
    security_distance_in_air: float
    security_distance_on_ground: float
    dance_size_max: int


class Parameter:
    def load_export_parameter(self):
        f = open("export_setup.json", "r")
        data = json.load(f)
        self.timecode_parameter = TimecodeParameter(
            show_time_begin=data["FIRST_TIMECODE"],
            position_frequence=data["POSITION_TIMECODE_FREQUENCE"],
            color_frequence=data["COLOR_TIMECODE_FREQUENCE"],
        )

    def load_iostar_parameter(self):
        f = open("iostar_setup.json", "r")
        data = json.load(f)
        self.takeoff_parameter = TakeoffParameter(
            takeoff_altitude=int(1e-2 * data["TAKEOFF_ALTITUDE"]),
            takeoff_duration=int(1e-3 * data["TAKEOFF_DURATION"]),
        )
        self.iostar_parameter = IostarParameter(
            iostar_mass=data["IOSTAR_MASS"],
            iostar_drag_vertical_coef=data["VERTICAL_DRAG_COEF"],
            fire_chanel_format_min=data["FIRE_CHANEL_FORMAT_MIN"],
            fire_chanel_format_max=data["FIRE_CHANEL_FORMAT_MAX"],
            fire_duration_format_min=data["FIRE_DURATION_FORMAT_MIN"],
            fire_duration_format_max=data["FIRE_DURATION_FORMAT_MAX"],
            position_format_min=data["POSITION_MIN_FORMAT_CM"],
            position_format_max=data["POSITION_MAX_FORMAT_CM"],
            color_format_min=data["COLOR_MIN_FORMAT"],
            color_format_max=data["COLOR_MAX_FORMAT"],
            position_max=data["POSITION_MAX_METER"],
            horizontal_velocity_max=data["VEL_HOR_MAX_METER_PER_SECOND"],
            horizontal_acceleration_max=data["ACC_HOR_MAX_METER_PER_SECOND_SQUARE"],
            force_up_max=data["FORCE_UP_MAX_NEWTON"],
            force_down_max=data["FORCE_DOWN_MAX_NEWTON"],
            security_distance_in_air=data["MINIMAL_DISTANCE_BTW_DRONES_IN_AIR"],
            security_distance_on_ground=data["MINIMAL_DISTANCE_BTW_DRONES_ON_GROUND"],
            dance_size_max=data["DANCE_SIZE_MAX_OCTECT"],
        )
