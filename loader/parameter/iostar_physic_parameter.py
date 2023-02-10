from dataclasses import dataclass


@dataclass(frozen=True)
class IostarPhysicParameter:
    iostar_mass = 0.3  # kilogram
    horizontal_velocity_max = 5.0  # meter per second
    acceleration_max = 2.0  # meter per second square
    velocity_up_max = 4.0  # meter per second
    velocity_down_max = 4.0  # meter per second
    security_distance_in_air = 1.0  # meter
    # TODO: discuss this problem
    security_distance_on_ground = -1  # meter


IOSTAR_PHYSIC_PARAMETER = IostarPhysicParameter()
