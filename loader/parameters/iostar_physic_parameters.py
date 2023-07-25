from dataclasses import dataclass


@dataclass(frozen=True)
class IostarPhysicParameters:
    horizontal_velocity_max: float = 3.5  # meter per second
    acceleration_max: float = 1.5  # meter per second square
    velocity_up_max: float = 3.5  # meter per second
    velocity_down_max: float = 3.5  # meter per second
    minimum_distance: float = 1.5  # meter


IOSTAR_PHYSIC_PARAMETERS_RECOMMENDATION = IostarPhysicParameters()
IOSTAR_PHYSIC_PARAMETERS_MAX = IostarPhysicParameters(
    horizontal_velocity_max=5.0,
    acceleration_max=2.0,
    velocity_up_max=4.0,
    velocity_down_max=4.0,
    minimum_distance=1.0,
)
