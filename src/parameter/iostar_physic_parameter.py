from dataclasses import dataclass


@dataclass(frozen=True)
class IostarPhysicParameter:
    iostar_mass = 0.3
    iostar_drag_vertical_coef = 0.01
    horizontal_velocity_max = 6.0
    acceleration_max = 2.0
    velocity_up_max = 4.0
    velocity_down_max = 4.0
    security_distance_in_air = 1.0
    security_distance_on_ground = 0.3


IOSTAR_PHYSIC_PARAMETER = IostarPhysicParameter()
