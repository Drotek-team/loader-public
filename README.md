# Loader

This project provides standard tools for the creation and verification of Drotek dance file.

## Installation

### Installation of the module in your project

1. Copy the `loader` in your project

1. Minimal python version: Python 3.8

1. Run this command with the python interpreter of your project

   ```console
   python3 -m pip install path/to/loader
   ```

## Use the loader in your project

### Show Creation

```python
from loader.schemas import ShowUser

# Create an empty show user
show_user = ShowUser.create(nb_drones=5, angle_takeoff=0.0, step=2)

# Add position events
show_user.drones_user[0].add_position_event(frame=0, xyz=(0.0, 0.0, 0.0))
show_user.drones_user[0].add_position_event(frame=240, xyz=(0.0, 0.0, 10.0))
show_user.drones_user[0].add_position_event(frame=360, xyz=(2.0, 0.0, 10.0))

# Add color events
show_user.drones_user[0].add_color_event(frame=250, rgbw=(1.0, 0.0, 0.0, 0.0))
show_user.drones_user[0].add_color_event(frame=300, rgbw=(0.0, 0.0, 1.0, 0.0))

# Add fire events
show_user.drones_user[0].add_fire_event(frame=210, channel=0, duration=0)
show_user.drones_user[0].add_fire_event(frame=280, channel=1, duration=0)
```

### Show Reports

- Generate the global report of the show

  ```python
  from pathlib import Path

  from loader.reports import GlobalReport
  from loader.schemas import IostarJsonGcs, ShowUser

  dance_path = Path("iostar_json_gcs_valid.json")
  iostar_json_gcs = IostarJsonGcs.model_validate_json(dance_path.read_text())
  show_user = ShowUser.from_iostar_json_gcs(iostar_json_gcs)
  report = GlobalReport.generate(show_user)
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
          "loader_version": "0.6.0a6",
          "lightshow_creator_version": null,
          "blender_version": null
      }
  }
  """

  dance_path = Path("iostar_json_gcs_collision.json")
  iostar_json_gcs = IostarJsonGcs.model_validate_json(dance_path.read_text())
  show_user = ShowUser.from_iostar_json_gcs(iostar_json_gcs)
  report = GlobalReport.generate(show_user)
  print(report.summarize().model_dump_json(indent=4))
  """
  {
      "takeoff_format_summary": null,
      "autopilot_format_summary": null,
      "dance_size_summary": null,
      "performance_summary": null,
      "collision_summary": {
          "collision_infractions_summary": {
              "nb_infractions": 680,
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
                  "frame": 0,
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
          "loader_version": "0.6.0a6",
          "lightshow_creator_version": null,
          "blender_version": null
      }
  }
  """

  dance_path = Path("iostar_json_gcs_performance.json")
  iostar_json_gcs = IostarJsonGcs.model_validate_json(dance_path.read_text())
  show_user = ShowUser.from_iostar_json_gcs(iostar_json_gcs)
  report = GlobalReport.generate(show_user)
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
          "loader_version": "0.6.0a6",
          "lightshow_creator_version": null,
          "blender_version": null
      }
  }
  """

  dance_path = Path("iostar_json_gcs_dance_size.json")
  iostar_json_gcs = IostarJsonGcs.model_validate_json(dance_path.read_text())
  show_user = ShowUser.from_iostar_json_gcs(iostar_json_gcs)
  report = GlobalReport.generate(show_user)
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
                  "dance_size": 100106,
                  "position_percent": 100.03,
                  "color_percent": 0.02,
                  "fire_percent": 0.02
              },
              "max_dance_size_infraction": {
                  "drone_index": 0,
                  "dance_size": 100106,
                  "position_percent": 100.03,
                  "color_percent": 0.02,
                  "fire_percent": 0.02
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
          "loader_version": "0.6.0a6",
          "lightshow_creator_version": null,
          "blender_version": null
      }
  }
  """
  ```

- Generate the performance report of the show

  ```python
  from pathlib import Path

  from loader.parameters import IostarPhysicParameters
  from loader.reports import PerformanceReport
  from loader.schemas import IostarJsonGcs, ShowUser

  dance_path = Path("iostar_json_gcs_performance.json")
  iostar_json_gcs = IostarJsonGcs.model_validate_json(dance_path.read_text())
  show_user = ShowUser.from_iostar_json_gcs(iostar_json_gcs)

  performance_report = PerformanceReport.generate(show_user)
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
  print(performance_report)
  #> performance_infractions=[]
  ```

- Generate the collisions report of the show

  ```python
  from pathlib import Path

  from loader.parameters import IostarPhysicParameters
  from loader.reports import CollisionReport
  from loader.schemas import IostarJsonGcs, ShowUser

  dance_path = Path("iostar_json_gcs_collision.json")
  iostar_json_gcs = IostarJsonGcs.model_validate_json(dance_path.read_text())
  show_user = ShowUser.from_iostar_json_gcs(iostar_json_gcs)

  collision_report = CollisionReport.generate(show_user)
  print(collision_report.collision_infractions[:10])
  """
  [
      CollisionInfraction(frame=0, drone_index_1=0, drone_index_2=1, distance=1.24),
      CollisionInfraction(frame=0, drone_index_1=0, drone_index_2=2, distance=1.24),
      CollisionInfraction(frame=0, drone_index_1=1, drone_index_2=3, distance=1.24),
      CollisionInfraction(frame=0, drone_index_1=2, drone_index_2=3, distance=1.24),
      CollisionInfraction(frame=6, drone_index_1=0, drone_index_2=1, distance=1.24),
      CollisionInfraction(frame=6, drone_index_1=0, drone_index_2=2, distance=1.24),
      CollisionInfraction(frame=6, drone_index_1=1, drone_index_2=3, distance=1.24),
      CollisionInfraction(frame=6, drone_index_1=2, drone_index_2=3, distance=1.24),
      CollisionInfraction(frame=12, drone_index_1=0, drone_index_2=1, distance=1.24),
      CollisionInfraction(frame=12, drone_index_1=0, drone_index_2=2, distance=1.24),
  ]
  """

  show_user.physic_parameters = IostarPhysicParameters(minimum_distance=1.0)
  collision_report = CollisionReport.generate(show_user)
  print(collision_report)
  #> collision_infractions=[]
  ```

- Generate the dance size report of the show
  function

  ```python
  from pathlib import Path

  from loader.reports import DanceSizeReport
  from loader.schemas import DronePx4, IostarJsonGcs, ShowUser

  dance_path = Path("iostar_json_gcs_dance_size.json")
  iostar_json_gcs = IostarJsonGcs.model_validate_json(dance_path.read_text())
  show_user = ShowUser.from_iostar_json_gcs(iostar_json_gcs)
  autopilot_format = DronePx4.from_show_user(show_user)

  dance_size_report = DanceSizeReport.generate(autopilot_format)
  print(dance_size_report)
  """
  dance_size_infractions = [
      DanceSizeInfraction(
          drone_index=0,
          dance_size=100106,
          position_percent=100.03,
          color_percent=0.02,
          fire_percent=0.02,
      )
  ]
  """
  ```

### Import & Export

```python
from pathlib import Path

from loader.schemas import IostarJsonGcs, ShowUser

# Import an iostar json gcs file to a show user
dance_path = Path("iostar_json_gcs_valid.json")
show_user = ShowUser.from_iostar_json_gcs(
    IostarJsonGcs.model_validate_json(dance_path.read_text()),
)

# Export the show user to an iostar json gcs string
iostart_json_gcs_string = IostarJsonGcs.from_show_user(show_user).model_dump_json()
```
