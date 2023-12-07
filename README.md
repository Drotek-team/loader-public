# Loader

This project provides standard tools for the creation and verification of Drotek dance file.
The Loader minimum supported version is Python 3.8.

## Installation

To install the Loader:

1. Download the Loader on your computer.
1. Install the Loader with pip, you should use pip with the python interpreter of your project:

```console
python -m pip install <path_to_the_loader>
```

## Show Creation

```python
from pathlib import Path

from loader.parameters import LandType
from loader.schemas import IostarJsonGcs, ShowUser

# Create an empty show user
show_user = ShowUser.create(nb_drones=1, angle_takeoff=0.0, step=2)

# Add position events
show_user.drones_user[0].add_position_event(frame=0, xyz=(0.0, 0.0, 0.0))
show_user.drones_user[0].add_position_event(frame=240, xyz=(0.0, 0.0, 10.0))
show_user.drones_user[0].add_position_event(frame=360, xyz=(2.0, 0.0, 10.0))

# Add color events
show_user.drones_user[0].add_color_event(
    frame=250,
    rgbw=(1.0, 0.0, 0.0, 0.0),
    interpolate=True,
)
show_user.drones_user[0].add_color_event(frame=300, rgbw=(0.0, 0.0, 1.0, 0.0))

# Add fire events
show_user.drones_user[0].add_fire_event(frame=210, channel=0, duration=0)
show_user.drones_user[0].add_fire_event(frame=280, channel=1, duration=0)

# Set the position scale
# The range is multiplied by the scale
# The default value is 1
show_user.scale = 2

# Set the land type at the end of the show
# The default value is LandType.Land
# Use LandType.RTL to return to the takeoff position precisely
show_user.land_type = LandType.RTL

# Export the show user to the iostar json gcs format and save it in a file
iostart_json_gcs_string = IostarJsonGcs.from_show_user(show_user).model_dump_json()
show_path = Path("show.json")
show_path.write_text(iostart_json_gcs_string)
```

## Show Reports

### Generate the global report of the show

```python
from pathlib import Path

from loader.reports import GlobalReport
from loader.schemas import IostarJsonGcs, ShowUser

dance_path = Path("iostar_json_gcs_valid.json")
iostar_json_gcs = IostarJsonGcs.model_validate_json(dance_path.read_text())
show_user = ShowUser.from_iostar_json_gcs(iostar_json_gcs)
report = GlobalReport.generate(show_user)
print(f"The global report has {len(report)} errors")
#> The global report has 0 errors
print(report.summarize().model_dump_json(indent=4))
"""
{
    "takeoff_format_summary": null,
    "autopilot_format_summary": null,
    "dance_size_summary": null,
    "performance_summary": null,
    "collision_summary": null,
    "physic_parameters": {
        "horizontal_velocity_max": 3.5,
        "acceleration_max": 1.5,
        "velocity_up_max": 3.5,
        "velocity_down_max": 3.5,
        "minimum_distance": 1.5
    },
    "metadata": {
        "loader_version": "0.8.2",
        "lightshow_creator_version": null,
        "blender_version": null
    }
}
"""

dance_path = Path("iostar_json_gcs_collision.json")
iostar_json_gcs = IostarJsonGcs.model_validate_json(dance_path.read_text())
show_user = ShowUser.from_iostar_json_gcs(iostar_json_gcs)
report = GlobalReport.generate(show_user)
print(f"The global report has {len(report)} errors")
#> The global report has 676 errors
print(report.summarize().model_dump_json(indent=4))
"""
{
    "takeoff_format_summary": null,
    "autopilot_format_summary": null,
    "dance_size_summary": null,
    "performance_summary": null,
    "collision_summary": {
        "collision_infractions_summary": {
            "nb_infractions": 676,
            "drone_indices": "0-3",
            "min_collision_infraction": {
                "frame": 1014,
                "drone_index_1": 2,
                "drone_index_2": 3,
                "distance": 1.24
            },
            "max_collision_infraction": {
                "frame": 1014,
                "drone_index_1": 2,
                "drone_index_2": 3,
                "distance": 1.24
            },
            "first_collision_infraction": {
                "frame": 6,
                "drone_index_1": 2,
                "drone_index_2": 3,
                "distance": 1.24
            },
            "last_collision_infraction": {
                "frame": 1014,
                "drone_index_1": 2,
                "drone_index_2": 3,
                "distance": 1.24
            }
        }
    },
    "physic_parameters": {
        "horizontal_velocity_max": 3.5,
        "acceleration_max": 1.5,
        "velocity_up_max": 3.5,
        "velocity_down_max": 3.5,
        "minimum_distance": 1.5
    },
    "metadata": {
        "loader_version": "0.8.2",
        "lightshow_creator_version": null,
        "blender_version": null
    }
}
"""

dance_path = Path("iostar_json_gcs_performance.json")
iostar_json_gcs = IostarJsonGcs.model_validate_json(dance_path.read_text())
show_user = ShowUser.from_iostar_json_gcs(iostar_json_gcs)
report = GlobalReport.generate(show_user)
print(f"The global report has {len(report)} errors")
#> The global report has 4 errors
print(report.summarize().model_dump_json(indent=4))
"""
{
    "takeoff_format_summary": null,
    "autopilot_format_summary": null,
    "dance_size_summary": null,
    "performance_summary": {
        "drone_indices": "0-3",
        "performance_infractions_summary": {
            "acceleration": {
                "nb_infractions": 4,
                "min_performance_infraction": {
                    "performance_name": "acceleration",
                    "drone_index": 3,
                    "frame": 1000,
                    "value": 1.7999999999999998
                },
                "max_performance_infraction": {
                    "performance_name": "acceleration",
                    "drone_index": 3,
                    "frame": 1000,
                    "value": 1.7999999999999998
                },
                "first_performance_infraction": {
                    "performance_name": "acceleration",
                    "drone_index": 3,
                    "frame": 1000,
                    "value": 1.7999999999999998
                },
                "last_performance_infraction": {
                    "performance_name": "acceleration",
                    "drone_index": 3,
                    "frame": 1000,
                    "value": 1.7999999999999998
                }
            }
        }
    },
    "collision_summary": null,
    "physic_parameters": {
        "horizontal_velocity_max": 3.5,
        "acceleration_max": 1.5,
        "velocity_up_max": 3.5,
        "velocity_down_max": 3.5,
        "minimum_distance": 1.5
    },
    "metadata": {
        "loader_version": "0.8.2",
        "lightshow_creator_version": null,
        "blender_version": null
    }
}
"""

dance_path = Path("iostar_json_gcs_dance_size.json")
iostar_json_gcs = IostarJsonGcs.model_validate_json(dance_path.read_text())
show_user = ShowUser.from_iostar_json_gcs(iostar_json_gcs)
report = GlobalReport.generate(show_user)
print(f"The global report has {len(report)} errors")
#> The global report has 1 errors
print(report.summarize().model_dump_json(indent=4))
"""
{
    "takeoff_format_summary": null,
    "autopilot_format_summary": null,
    "dance_size_summary": {
        "dance_size_infractions_summary": {
            "nb_infractions": 1,
            "drone_indices": "0",
            "min_dance_size_infraction": {
                "drone_index": 0,
                "dance_size": 100090,
                "position_percent": 100.02,
                "color_percent": 0.02,
                "fire_percent": 0.01
            },
            "max_dance_size_infraction": {
                "drone_index": 0,
                "dance_size": 100090,
                "position_percent": 100.02,
                "color_percent": 0.02,
                "fire_percent": 0.01
            }
        }
    },
    "performance_summary": null,
    "collision_summary": null,
    "physic_parameters": {
        "horizontal_velocity_max": 3.5,
        "acceleration_max": 1.5,
        "velocity_up_max": 3.5,
        "velocity_down_max": 3.5,
        "minimum_distance": 1.5
    },
    "metadata": {
        "loader_version": "0.8.2",
        "lightshow_creator_version": null,
        "blender_version": null
    }
}
"""
```

### Generate the performance report of the show

```python
from pathlib import Path

from loader.parameters import IostarPhysicParameters
from loader.reports import PerformanceReport
from loader.schemas import IostarJsonGcs, ShowUser

dance_path = Path("iostar_json_gcs_performance.json")
iostar_json_gcs = IostarJsonGcs.model_validate_json(dance_path.read_text())
show_user = ShowUser.from_iostar_json_gcs(iostar_json_gcs)

performance_report = PerformanceReport.generate(show_user)
print(f"The performance report has {len(performance_report)} errors")
#> The performance report has 4 errors
print(performance_report)
"""
performance_infractions = [
    PerformanceInfraction(
        performance_name="acceleration",
        drone_index=0,
        frame=1000,
        value=1.7999999999999998,
    ),
    PerformanceInfraction(
        performance_name="acceleration",
        drone_index=1,
        frame=1000,
        value=1.7999999999999998,
    ),
    PerformanceInfraction(
        performance_name="acceleration",
        drone_index=2,
        frame=1000,
        value=1.7999999999999998,
    ),
    PerformanceInfraction(
        performance_name="acceleration",
        drone_index=3,
        frame=1000,
        value=1.7999999999999998,
    ),
]
"""

show_user.physic_parameters = IostarPhysicParameters(acceleration_max=2)
performance_report = PerformanceReport.generate(show_user)
print(f"The performance report has {len(performance_report)} errors")
#> The performance report has 0 errors
print(performance_report)
#> performance_infractions=[]
```

### Generate the collisions report of the show

```python
from pathlib import Path

from loader.parameters import IostarPhysicParameters
from loader.reports import CollisionReport
from loader.schemas import IostarJsonGcs, ShowUser

dance_path = Path("iostar_json_gcs_collision.json")
iostar_json_gcs = IostarJsonGcs.model_validate_json(dance_path.read_text())
show_user = ShowUser.from_iostar_json_gcs(iostar_json_gcs)

collision_report = CollisionReport.generate(show_user)
print(f"The collision report has {len(collision_report)} errors")
#> The collision report has 676 errors
print(collision_report.collision_infractions[:10])
"""
[
    CollisionInfraction(frame=6, drone_index_1=0, drone_index_2=1, distance=1.24),
    CollisionInfraction(frame=6, drone_index_1=0, drone_index_2=2, distance=1.24),
    CollisionInfraction(frame=6, drone_index_1=1, drone_index_2=3, distance=1.24),
    CollisionInfraction(frame=6, drone_index_1=2, drone_index_2=3, distance=1.24),
    CollisionInfraction(frame=12, drone_index_1=0, drone_index_2=1, distance=1.24),
    CollisionInfraction(frame=12, drone_index_1=0, drone_index_2=2, distance=1.24),
    CollisionInfraction(frame=12, drone_index_1=1, drone_index_2=3, distance=1.24),
    CollisionInfraction(frame=12, drone_index_1=2, drone_index_2=3, distance=1.24),
    CollisionInfraction(frame=18, drone_index_1=0, drone_index_2=1, distance=1.24),
    CollisionInfraction(frame=18, drone_index_1=0, drone_index_2=2, distance=1.24),
]
"""

show_user.physic_parameters = IostarPhysicParameters(minimum_distance=1.0)
collision_report = CollisionReport.generate(show_user)
print(f"The collision report has {len(collision_report)} errors")
#> The collision report has 0 errors
print(collision_report)
#> collision_infractions=[]
```

### Generate the dance size report of the show

```python
from pathlib import Path

from loader.reports import DanceSizeReport
from loader.schemas import DronePx4, IostarJsonGcs, ShowUser

dance_path = Path("iostar_json_gcs_dance_size.json")
iostar_json_gcs = IostarJsonGcs.model_validate_json(dance_path.read_text())
show_user = ShowUser.from_iostar_json_gcs(iostar_json_gcs)
autopilot_format = DronePx4.from_show_user(show_user)

dance_size_report = DanceSizeReport.generate(autopilot_format)
print(f"The dance size report has {len(dance_size_report)} errors")
#> The dance size report has 1 errors
print(dance_size_report)
"""
dance_size_infractions = [
    DanceSizeInfraction(
        drone_index=0,
        dance_size=100090,
        position_percent=100.02,
        color_percent=0.02,
        fire_percent=0.01,
    )
]
"""
```

## Import

To read a show file generated by this loader or Blender, you can use the following code:

<!-- no-print -->

```python
from pathlib import Path

from loader.schemas import IostarJsonGcs, ShowUser

# Import an iostar json gcs file to a show user
dance_path = Path("iostar_json_gcs_valid.json")
show_user = ShowUser.from_iostar_json_gcs(
    IostarJsonGcs.model_validate_json(dance_path.read_text()),
)
# Iterate over the matrix of families
for y_index, row in enumerate(show_user.drones_user_in_matrix):
    # Iterate over the families in the row
    for x_index, family in enumerate(row):
        print(f"Row {y_index}, Column {x_index}:")
        # Iterate over the drones in the family
        for drone in family:
            print(f"Drone {drone.index}:")
            print("\tPositions:")
            for position in drone.position_events:
                print(f"\t\t{position}")
                print("\tColors:")
            for color in drone.color_events:
                print(f"\t\t{color}")
                print("\tFires")
            for fire in drone.fire_events:
                print(f"\t\t{fire}")
```

## Rotate an existing show

To rotate an existing show, you can use the following code:

```python
from pathlib import Path
from sys import exit

import numpy as np
from loader.reports import GlobalReport
from loader.schemas import IostarJsonGcs, ShowUser

# Angle to rotate the show by (in degrees) (counterclockwise)
ANGLE_TO_ROTATE = 20

# Path to the show
dance_path = Path("iostar_json_gcs_valid.json")
dance_report_path = dance_path.with_name(dance_path.stem + "_report.json")
new_dance_path = dance_path.with_name(dance_path.stem + "_rotated.json")

# Import the show
iostar_json_gcs = IostarJsonGcs.model_validate_json(dance_path.read_text())
show_user = ShowUser.from_iostar_json_gcs(iostar_json_gcs)
# Rotate the show
show_user.apply_horizontal_rotation(
    # Convert to radians
    np.deg2rad(ANGLE_TO_ROTATE)
    # Remove the current angle to rotate from angle 0°
    - show_user.angle_takeoff,  # Comment this line to rotate from the current angle
)

# Check the show
global_report = GlobalReport.generate(show_user)
# If there are errors, dump the report and exit
if len(global_report):
    dance_report_path.write_text(global_report.summarize().model_dump_json(indent=2))
    exit(1)

# Export the rotated show
new_iostar_json_gcs = IostarJsonGcs.from_show_user(show_user)
new_iostar_json_gcs.model_dump_json()
new_dance_path.write_text(new_iostar_json_gcs.model_dump_json())
```

## Go further

You explore:

- `loader/schemas/show_user/show_user.py`, for the documentation of the Show User schema
- `loader/schemas/iostar_json_gcs/iostar_json_gcs.py`, for the documentation of the IO Star JSON GCS schema
- `loader/parameters/iostar_physic_parameters.py`, for the documentation of the IO Star physic parameters
