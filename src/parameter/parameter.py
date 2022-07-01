import json
import os
from dataclasses import dataclass
from typing import Tuple

import numpy as np


@dataclass(frozen=True)
class JsonConventionConstant:
    CENTIMETER_TO_METER_RATIO: float = 1e-2
    METER_TO_CENTIMETER_RATIO: float = 1e2
    TIMECODE_TO_SECOND_RATIO: float = 1e-3
    SECOND_TO_TIMECODE_RATIO: float = 1e3

    def from_json_position_to_simulation_position(
        self, json_position: Tuple[int, int, int]
    ) -> np.ndarray:
        return self.CENTIMETER_TO_METER_RATIO * np.array(json_position)


@dataclass(frozen=True)
class TakeoffParameter:
    takeoff_altitude: int
    takeoff_elevation_duration: int
    takeoff_stabilisation_duration: int

    @property
    def takeoff_duration(self) -> int:
        return self.takeoff_elevation_duration + self.takeoff_stabilisation_duration


@dataclass(frozen=True)
class LandParameter:
    land_fast_speed: float
    land_low_speed: float
    land_safe_hgt: int

    def get_first_land_timecode_delta(self, drone_hgt_centimeter: int) -> int:
        if drone_hgt_centimeter < self.land_safe_hgt:
            return int(drone_hgt_centimeter / self.land_low_speed)
        else:
            return int(
                (drone_hgt_centimeter - self.land_safe_hgt) / self.land_fast_speed
            )

    def get_first_land_altitude(self, drone_hgt_centimeter: int) -> int:
        if drone_hgt_centimeter < self.land_safe_hgt:
            return 0
        else:
            return self.land_safe_hgt

    def get_second_land_timecode_delta(self, drone_hgt_centimeter: int) -> int:
        if drone_hgt_centimeter < self.land_safe_hgt:
            return 0
        else:
            return int(self.land_safe_hgt / self.land_low_speed)

    def get_second_land_altitude_start(self, drone_hgt_centimeter: int) -> int:
        if drone_hgt_centimeter < self.land_safe_hgt:
            return 0
        else:
            return self.land_safe_hgt

    def get_land_timecode_delta(self, drone_hgt_centimeter: int) -> int:
        return self.get_first_land_timecode_delta(
            drone_hgt_centimeter
        ) + self.get_second_land_timecode_delta(drone_hgt_centimeter)


@dataclass(frozen=True)
class TimecodeParameter:
    show_timecode_begin: int
    timecode_value_max: int
    position_timecode_rate: int
    color_timecode_rate: int


@dataclass(frozen=True)
class FamilyParameter:
    nb_x_value_min: int
    nb_x_value_max: int
    nb_y_value_min: int
    nb_y_value_max: int
    step_takeoff_value_min: int
    step_takeoff_value_max: int
    angle_takeoff_value_min: int
    angle_takeoff_value_max: int


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
    FAMILY_SETUP_LOCAL_PATH = "/src/parameter/family_setup.json"
    json_convention_constant = JsonConventionConstant()

    def load_export_parameter(self) -> None:
        f = open(f"{os.getcwd()}/{self.EXPORT_SETUP_LOCAL_PATH}", "r")
        data = json.load(f)
        self.timecode_parameter = TimecodeParameter(
            show_timecode_begin=int(
                self.json_convention_constant.SECOND_TO_TIMECODE_RATIO
                * data["FIRST_TIMECODE_SECOND"]
            ),
            timecode_value_max=int(
                self.json_convention_constant.SECOND_TO_TIMECODE_RATIO
                * data["TIMECODE_VALUE_MAX_SECOND"]
            ),
            position_timecode_rate=int(
                self.json_convention_constant.SECOND_TO_TIMECODE_RATIO
                // data["POSITION_TIMECODE_FREQUENCE"]
            ),
            color_timecode_rate=int(
                self.json_convention_constant.SECOND_TO_TIMECODE_RATIO
                // data["COLOR_TIMECODE_FREQUENCE"]
            ),
        )

    def load_iostar_parameter(self) -> None:
        f = open(f"{os.getcwd()}/{self.IOSTAR_SETUP_LOCAL_PATH}", "r")
        data = json.load(f)
        self.takeoff_parameter = TakeoffParameter(
            takeoff_altitude=int(
                self.json_convention_constant.METER_TO_CENTIMETER_RATIO
                * data["TAKEOFF_ALTITUDE_METER"]
            ),
            takeoff_elevation_duration=int(
                self.json_convention_constant.SECOND_TO_TIMECODE_RATIO
                * data["TAKEOFF_ELEVATION_DURATION_SECOND"]
            ),
            takeoff_stabilisation_duration=int(
                self.json_convention_constant.SECOND_TO_TIMECODE_RATIO
                * data["TAKEOFF_STABILISATION_DURATION_SECOND"]
            ),
        )
        self.land_parameter = LandParameter(
            land_fast_speed=(
                self.json_convention_constant.METER_TO_CENTIMETER_RATIO
                / self.json_convention_constant.SECOND_TO_TIMECODE_RATIO
            )
            * data["LAND_FAST_SPEED_METER_PER_SECOND"],
            land_low_speed=(
                (
                    self.json_convention_constant.METER_TO_CENTIMETER_RATIO
                    / self.json_convention_constant.SECOND_TO_TIMECODE_RATIO
                )
                * data["LAND_LOW_SPEED_METER_PER_SECOND"]
            ),
            land_safe_hgt=int(
                self.json_convention_constant.METER_TO_CENTIMETER_RATIO
                * data["LAND_SAFE_HGT_METER"]
            ),
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

    def load_family_parameter(self) -> None:
        f = open(f"{os.getcwd()}/{self.FAMILY_SETUP_LOCAL_PATH}", "r")
        data = json.load(f)
        self.family_parameter = FamilyParameter(
            nb_x_value_min=data["NB_X_VALUE_MIN"],
            nb_x_value_max=data["NB_X_VALUE_MAX"],
            nb_y_value_min=data["NB_Y_VALUE_MIN"],
            nb_y_value_max=data["NB_Y_VALUE_MAX"],
            step_takeoff_value_min=self.json_convention_constant.METER_TO_CENTIMETER_RATIO
            * data["STEP_TAKEOFF_VALUE_METER_MIN"],
            step_takeoff_value_max=self.json_convention_constant.METER_TO_CENTIMETER_RATIO
            * data["STEP_TAKEOFF_VALUE_METER_MAX"],
            angle_takeoff_value_min=data["ANGLE_TAKEOFF_VALUE_MIN"],
            angle_takeoff_value_max=data["ANGLE_TAKEOFF_VALUE_MAX"],
        )

    def load_parameter(self) -> None:
        self.load_family_parameter()
        self.load_iostar_parameter()
        self.load_export_parameter()
