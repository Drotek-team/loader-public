from typing import List

import numpy as np

from ......parameter.parameter import IostarParameter, TakeoffParameter
from .metric import Metric
from .observed_metrics_report import ObservedMetricsCheckReport


class ObservedMetricsSlice:
    def __init__(
        self,
        nb_drones: int,
        iostar_parameter: IostarParameter,
        takeoff_parameter: TakeoffParameter,
    ):
        self.nb_drones = nb_drones
        self.vertical_positions = [
            Metric(drone_index, 0, takeoff_parameter.takeoff_altitude, False)
            for drone_index in range(nb_drones)
        ]
        self.horizontal_velocites = [
            Metric(drone_index, 0, iostar_parameter.horizontal_velocity_max)
            for drone_index in range(nb_drones)
        ]
        self.horizontal_accelerations = [
            Metric(drone_index, 0, iostar_parameter.horizontal_acceleration_max)
            for drone_index in range(nb_drones)
        ]
        self.up_forces = [
            Metric(drone_index, 0, iostar_parameter.force_up_max)
            for drone_index in range(nb_drones)
        ]
        self.down_forces = [
            Metric(drone_index, -iostar_parameter.force_down_max, 0, False)
            for drone_index in range(nb_drones)
        ]

    @staticmethod
    def force_evaluation(
        velocity: float, acceleration: float, mass: float, drag_coef: float
    ) -> float:
        return float(
            mass * acceleration + np.sign(velocity) * drag_coef * np.square(velocity)
        )

    def update_observed_metrics(
        self,
        drone_indices: List[int],
        positions: np.ndarray,
        velocities: np.ndarray,
        accelerations: np.ndarray,
        observed_metrics_report: ObservedMetricsCheckReport,
        iostar_parameter: IostarParameter,
    ) -> None:
        for drone_index in drone_indices:
            if not (
                self.vertical_positions[drone_index].validation(
                    positions[drone_index, 2]
                )
            ):
                observed_metrics_report.vertical_position_check_report.add_incident(
                    drone_index, positions[drone_index, 2]
                )
            if not (
                self.horizontal_velocites[drone_index].validation(
                    np.linalg.norm(velocities[drone_index, 0:2])
                )
            ):
                observed_metrics_report.horizontal_velocity_check_report.add_incident(
                    drone_index, np.linalg.norm(velocities[drone_index, 0:2])
                )
            if not (
                self.horizontal_accelerations[drone_index].validation(
                    np.linalg.norm(accelerations[drone_index, 0:2])
                )
            ):
                observed_metrics_report.horizontal_acceleration_check_report.add_incident(
                    drone_index, np.linalg.norm(accelerations[drone_index, 0:2])
                )
            if not (
                self.up_forces[drone_index].validation(
                    self.force_evaluation(
                        velocities[drone_index, 2],
                        accelerations[drone_index, 2],
                        iostar_parameter.iostar_mass,
                        iostar_parameter.iostar_drag_vertical_coef,
                    )
                )
            ):
                observed_metrics_report.up_force_check_report.add_incident(
                    drone_index,
                    self.force_evaluation(
                        velocities[drone_index, 2],
                        accelerations[drone_index, 2],
                        iostar_parameter.iostar_mass,
                        iostar_parameter.iostar_drag_vertical_coef,
                    ),
                )
            if not (
                self.down_forces[drone_index].validation(
                    self.force_evaluation(
                        velocities[drone_index, 2],
                        accelerations[drone_index, 2],
                        iostar_parameter.iostar_mass,
                        iostar_parameter.iostar_drag_vertical_coef,
                    )
                )
            ):
                observed_metrics_report.down_force_check_report.add_incident(
                    drone_index,
                    self.force_evaluation(
                        velocities[drone_index, 2],
                        accelerations[drone_index, 2],
                        iostar_parameter.iostar_mass,
                        iostar_parameter.iostar_drag_vertical_coef,
                    ),
                )
        observed_metrics_report.vertical_position_check_report.update()
        observed_metrics_report.horizontal_velocity_check_report.update()
        observed_metrics_report.horizontal_acceleration_check_report.update()
        observed_metrics_report.up_force_check_report.update()
        observed_metrics_report.down_force_check_report.update()
