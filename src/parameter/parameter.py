import json
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class TakeoffParameter:
    takeoff_altitude: int
    takeoff_duration: int


@dataclass(frozen=True)
class TimecodeParameter:
    show_timecode_begin: int
    position_rate: int
    color_rate: int


@dataclass(frozen=True)
class FamilyParameter:
    nb_x_value_min: int
    nb_x_value_max: int
    nb_y_value_min: int
    nb_y_value_max: int
    step_value_min: int
    step_value_max: int
    angle_value_min: int
    angle_value_max: int


@dataclass(frozen=True)
class IostarParameter:
    iostar_mass: float
    iostar_drag_vertical_coef: float
    fire_chanel_value_min: int
    fire_chanel_value_max: int
    fire_duration_value_min: int
    fire_duration_value_max: int
    position_value_min: int
    position_value_max: int
    color_value_min: int
    color_value_max: int
    position_max: float
    horizontal_velocity_max: float
    horizontal_acceleration_max: float
    force_up_max: float
    force_down_max: float
    security_distance_in_air: float
    security_distance_on_ground: float
    dance_size_max: int


class Parameter:
    EXPORT_SETUP_LOCAL_PATH = "/src/parameter/export_setup.json"
    IOSTAR_SETUP_LOCAL_PATH = "/src/parameter/iostar_setup.json"

    def load_export_parameter(self):
        f = open(f"{os.getcwd()}/{self.EXPORT_SETUP_LOCAL_PATH}", "r")
        data = json.load(f)
        self.timecode_parameter = TimecodeParameter(
            show_timecode_begin=int(1e3 * data["FIRST_TIMECODE"]),
            position_rate=int(1e3 // data["POSITION_TIMECODE_FREQUENCE"]),
            color_rate=int(1e3 // data["COLOR_TIMECODE_FREQUENCE"]),
        )

    def load_iostar_parameter(self):
        f = open(f"{os.getcwd()}/{self.IOSTAR_SETUP_LOCAL_PATH}", "r")
        data = json.load(f)
        self.takeoff_parameter = TakeoffParameter(
            takeoff_altitude=int(1e2 * data["TAKEOFF_ALTITUDE"]),
            takeoff_duration=int(1e3 * data["TAKEOFF_DURATION"]),
        )
        self.iostar_parameter = IostarParameter(
            position_value_min=data["POSITION_VALUE_CM_MIN"],
            position_value_max=data["POSITION_VALUE_CM_MAX"],
            color_value_min=data["COLOR_VALUE_MIN"],
            color_value_max=data["COLOR_VALUE_MAX"],
            fire_chanel_value_min=data["FIRE_CHANEL_VALUE_MIN"],
            fire_chanel_value_max=data["FIRE_CHANEL_VALUE_MAX"],
            fire_duration_value_min=data["FIRE_DURATION_VALUE_SECOND_MIN"],
            fire_duration_value_max=data["FIRE_DURATION_VALUE_SECOND_MAX"],
            position_max=data["POS_METER_MAX"],
            horizontal_velocity_max=data["VEL_HOR_MAX_METER_PER_SECOND"],
            horizontal_acceleration_max=data["ACC_HOR_MAX_METER_PER_SECOND_SQUARE"],
            force_up_max=data["FORCE_UP_MAX_NEWTON"],
            force_down_max=data["FORCE_DOWN_MAX_NEWTON"],
            security_distance_in_air=data["MINIMAL_DISTANCE_BTW_DRONES_IN_AIR"],
            security_distance_on_ground=data["MINIMAL_DISTANCE_BTW_DRONES_ON_GROUND"],
            dance_size_max=data["DANCE_SIZE_MAX_OCTECT"],
            iostar_mass=data["IOSTAR_MASS"],
            iostar_drag_vertical_coef=data["VERTICAL_DRAG_COEF"],
        )

    def load_family_parameter(self):
        f = open(f"{os.getcwd()}/{self.IOSTAR_SETUP_LOCAL_PATH}", "r")
        data = json.load(f)
