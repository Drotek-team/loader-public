import json
from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class JsonBinaryParameter:
    magic_number: str
    fmt_header: str
    fmt_section_header: str


@dataclass(frozen=True)
class TakeoffParameter:
    takeoff_altitude_meter: float
    takeoff_elevation_duration_second: float
    takeoff_stabilisation_duration_second: float

    @property
    def takeoff_duration_second(self) -> float:
        return (
            self.takeoff_elevation_duration_second
            + self.takeoff_stabilisation_duration_second
        )


@dataclass(frozen=True)
class LandParameter:
    land_fast_speed: float
    land_low_speed: float
    land_safe_hgt: float

    def get_first_land_second_delta(self, drone_hgt_meter: float) -> float:
        if drone_hgt_meter < self.land_safe_hgt:
            return drone_hgt_meter / self.land_low_speed
        else:
            return (drone_hgt_meter - self.land_safe_hgt) / self.land_fast_speed

    def get_first_land_altitude(self, drone_hgt_meter: float) -> float:
        if drone_hgt_meter < self.land_safe_hgt:
            return 0
        else:
            return self.land_safe_hgt

    def get_second_land_second_delta(self, drone_hgt_meter: float) -> float:
        if drone_hgt_meter < self.land_safe_hgt:
            return 0
        else:
            return self.land_safe_hgt / self.land_low_speed

    def get_second_land_altitude_start(self, drone_hgt_meter: float) -> float:
        if drone_hgt_meter < self.land_safe_hgt:
            return 0
        else:
            return self.land_safe_hgt

    def get_land_second_delta(self, drone_hgt_meter: float) -> float:
        return self.get_first_land_second_delta(
            drone_hgt_meter
        ) + self.get_second_land_second_delta(drone_hgt_meter)


@dataclass(frozen=True)
class FrameParameter:
    show_duration_min_second: float
    show_duration_max_second: float
    position_fps: int
    color_fps: int
    fire_fps: int
    json_fps: int

    @property
    def show_duration_min_frame(self) -> int:
        return int(self.show_duration_min_second * self.json_fps)

    @property
    def show_duration_max_frame(self) -> int:
        return int(self.show_duration_max_second * self.json_fps)

    @property
    def position_rate_frame(self) -> int:
        return int(self.json_fps / self.position_fps)

    @property
    def position_rate_second(self) -> float:
        return self.position_rate_frame / self.json_fps

    @property
    def color_rate_frame(self) -> int:
        return int(self.json_fps / self.color_fps)

    @property
    def color_rate_second(self) -> float:
        return self.color_rate_frame / self.json_fps

    @property
    def fire_rate_frame(self) -> int:
        return int(self.json_fps / self.fire_fps)

    @property
    def fire_rate_second(self) -> float:
        return self.fire_rate_frame / self.json_fps


@dataclass(frozen=True)
class FamilyParameter:
    nb_x_value_min: int
    nb_x_value_max: int
    nb_y_value_min: int
    nb_y_value_max: int
    nb_drone_per_family_min: int
    nb_drone_per_family_max: int
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
    fire_duration_value_frame_min: int
    fire_duration_value_frame_max: int
    position_value_min: int
    position_value_max: int
    color_value_min: int
    color_value_max: int
    position_max: float
    horizontal_velocity_max: float
    horizontal_velocity_lower_bound: float
    horizontal_velocity_upper_bound: float
    horizontal_acceleration_max: float
    force_up_max: float
    force_down_max: float
    security_distance_in_air: float
    security_distance_on_ground: float
    dance_size_max: int
    frame_reformat_factor: float
    position_reformat_factor: float


class Parameter:
    EXPORT_SETUP_LOCAL_PATH = "/src/parameter/export_setup.json"
    IOSTAR_SETUP_LOCAL_PATH = "/src/parameter/iostar_setup.json"
    FAMILY_SETUP_LOCAL_PATH = "/src/parameter/family_setup.json"

    def load_json_binary_parameter(self, local_path: str) -> None:
        f = open(f"{local_path}/{self.EXPORT_SETUP_LOCAL_PATH}", "r")
        data = json.load(f)
        self.json_binary_parameter = JsonBinaryParameter(
            magic_number=data["MAGIC_NUMBER_INTEGER"],
            fmt_header=data["FMT_HEADER"],
            fmt_section_header=data["FMT_SECTION_HEADER"],
        )

    def load_frame_parameter(self, local_path: str) -> None:
        f = open(f"{local_path}/{self.EXPORT_SETUP_LOCAL_PATH}", "r")
        data = json.load(f)
        self.frame_parameter = FrameParameter(
            show_duration_min_second=data["SHOW_DURATION_MIN_SECOND"],
            show_duration_max_second=data["SHOW_DURATION_MAX_SECOND"],
            position_fps=data["POSITION_FPS"],
            color_fps=data["COLOR_FPS"],
            fire_fps=data["FIRE_FPS"],
            json_fps=data["JSON_FPS"],
        )

    def load_iostar_parameter(self, local_path: str) -> None:
        f = open(f"{local_path}/{self.IOSTAR_SETUP_LOCAL_PATH}", "r")
        data = json.load(f)
        self.takeoff_parameter = TakeoffParameter(
            takeoff_altitude_meter=data["TAKEOFF_ALTITUDE_METER"],
            takeoff_elevation_duration_second=data["TAKEOFF_ELEVATION_DURATION_SECOND"],
            takeoff_stabilisation_duration_second=data[
                "TAKEOFF_STABILISATION_DURATION_SECOND"
            ],
        )

        self.land_parameter = LandParameter(
            land_fast_speed=data["LAND_FAST_SPEED_METER_PER_SECOND"],
            land_low_speed=data["LAND_LOW_SPEED_METER_PER_SECOND"],
            land_safe_hgt=data["LAND_SAFE_HGT_METER"],
        )
        self.iostar_parameter = IostarParameter(
            position_value_min=data["POSITION_VALUE_CM_MIN"],
            position_value_max=data["POSITION_VALUE_CM_MAX"],
            color_value_min=data["COLOR_VALUE_MIN"],
            color_value_max=data["COLOR_VALUE_MAX"],
            fire_chanel_value_min=data["FIRE_CHANEL_VALUE_MIN"],
            fire_chanel_value_max=data["FIRE_CHANEL_VALUE_MAX"],
            fire_duration_value_frame_min=data["FIRE_DURATION_VALUE_FRAME_MIN"],
            fire_duration_value_frame_max=data["FIRE_DURATION_VALUE_FRAME_MAX"],
            position_max=data["POS_METER_MAX"],
            horizontal_velocity_max=data["VEL_HOR_MAX_METER_PER_SECOND"],
            horizontal_velocity_lower_bound=data[
                "VEL_HOR_MAX_METER_PER_SECOND_DURING_ELEVATION_MAX"
            ],
            horizontal_velocity_upper_bound=data["VEL_HOR_MAX_METER_PER_SECOND"],
            horizontal_acceleration_max=data["ACC_HOR_MAX_METER_PER_SECOND_SQUARE"],
            force_up_max=data["FORCE_UP_MAX_NEWTON"],
            force_down_max=data["FORCE_DOWN_MAX_NEWTON"],
            security_distance_in_air=data["MINIMAL_DISTANCE_BTW_DRONES_IN_AIR"],
            security_distance_on_ground=data["MINIMAL_DISTANCE_BTW_DRONES_ON_GROUND"],
            dance_size_max=data["DANCE_SIZE_MAX_OCTECT"],
            iostar_mass=data["IOSTAR_MASS"],
            iostar_drag_vertical_coef=data["VERTICAL_DRAG_COEF"],
            frame_reformat_factor=1 / data["TIMECODE_REFORMAT_FACTOR"],
            position_reformat_factor=1 / data["POSITION_REFORMAT_FACTOR"],
        )

    def load_family_parameter(self, local_path: str) -> None:
        f = open(f"{local_path}/{self.FAMILY_SETUP_LOCAL_PATH}", "r")
        data = json.load(f)
        self.family_parameter = FamilyParameter(
            nb_x_value_min=data["NB_X_VALUE_MIN"],
            nb_x_value_max=data["NB_X_VALUE_MAX"],
            nb_y_value_min=data["NB_Y_VALUE_MIN"],
            nb_y_value_max=data["NB_Y_VALUE_MAX"],
            nb_drone_per_family_min=data["NB_DRONE_PER_FAMILY_MIN"],
            nb_drone_per_family_max=data["NB_DRONE_PER_FAMILY_MAX"],
            step_takeoff_value_min=data["STEP_TAKEOFF_VALUE_METER_MIN"],
            step_takeoff_value_max=data["STEP_TAKEOFF_VALUE_METER_MAX"],
            angle_takeoff_value_min=data["ANGLE_TAKEOFF_VALUE_MIN"],
            angle_takeoff_value_max=data["ANGLE_TAKEOFF_VALUE_MAX"],
        )

    def load_parameter(self, local_path: str) -> None:
        self.load_family_parameter(local_path)
        self.load_iostar_parameter(local_path)
        self.load_frame_parameter(local_path)
        self.load_json_binary_parameter(local_path)
