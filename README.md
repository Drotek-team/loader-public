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
from loader import ShowUser

# Create an empty show user
show_user = ShowUser.create(nb_drones=5)

# Add position events
show_user.drones_user[0].add_position_event(frame=0, xyz=(0.0, 0.0, 0.0))
show_user.drones_user[0].add_position_event(frame=240, xyz=(0.0, 0.0, 10.0))
show_user.drones_user[0].add_position_event(frame=360, xyz=(2.0, 0.0, 10.0))

# Add color events
show_user.drones_user[0].add_color_event(frame=250, rgbw=(1.0, 0.0, 0.0, 0.0))
show_user.drones_user[0].add_color_event(frame=300, rgbw=(0.0, 0.0, 1.0, 0.0))

# Add fire events
show_user.drones_user[0].add_fire_event(frame=210, chanel=0, duration=0)
show_user.drones_user[0].add_fire_event(frame=280, chanel=1, duration=0)
```

### Show Reports

- Generate the global report of the show

  ```python
  from pathlib import Path

  from loader import IostarJsonGcs, ijg_to_su
  from loader.reports import GlobalReport

  iostar_json_gcs = IostarJsonGcs.parse_file(Path("iostar_json_gcs_valid.json"))
  show_user = ijg_to_su(iostar_json_gcs)
  report = GlobalReport.generate(show_user)
  print(report.summary())
  #> takeoff_format=0 autopilot_format=0 performance=0 collision=0

  iostar_json_gcs = IostarJsonGcs.parse_file(Path("iostar_json_gcs_collision.json"))
  show_user = ijg_to_su(iostar_json_gcs)
  report = GlobalReport.generate(show_user)
  print(report.summary())
  #> takeoff_format=0 autopilot_format=0 performance=0 collision=4080

  iostar_json_gcs = IostarJsonGcs.parse_file(Path("iostar_json_gcs_performance.json"))
  show_user = ijg_to_su(iostar_json_gcs)
  report = GlobalReport.generate(show_user)
  print(report.summary())
  #> takeoff_format=0 autopilot_format=0 performance=4 collision=0

  iostar_json_gcs = IostarJsonGcs.parse_file(Path("iostar_json_gcs_dance_size.json"))
  show_user = ijg_to_su(iostar_json_gcs)
  report = GlobalReport.generate(show_user)
  print(report.summary())
  #> takeoff_format=0 autopilot_format=1 performance=0 collision=0
  ```

- Generate the performance report of the show

  ```python
  from pathlib import Path

  from loader import IostarJsonGcs, ijg_to_su
  from loader.parameters import IostarPhysicParameters
  from loader.reports import PerformanceReport

  iostar_json_gcs = IostarJsonGcs.parse_file(Path("iostar_json_gcs_performance.json"))
  show_user = ijg_to_su(iostar_json_gcs)

  performance_report = PerformanceReport.generate(show_user)
  print(performance_report)
  """
  performance_infractions = [
      PerformanceInfraction(
          performance_name="acceleration",
          drone_index=0,
          frame=1000,
          value=1.7999999999999998,
          threshold=1.5,
      ),
      PerformanceInfraction(
          performance_name="acceleration",
          drone_index=1,
          frame=1000,
          value=1.7999999999999998,
          threshold=1.5,
      ),
      PerformanceInfraction(
          performance_name="acceleration",
          drone_index=2,
          frame=1000,
          value=1.7999999999999998,
          threshold=1.5,
      ),
      PerformanceInfraction(
          performance_name="acceleration",
          drone_index=3,
          frame=1000,
          value=1.7999999999999998,
          threshold=1.5,
      ),
  ]
  """

  physic_parameters = IostarPhysicParameters(acceleration_max=2)
  performance_report = PerformanceReport.generate(
      show_user,
      physic_parameters=physic_parameters,
  )
  print(performance_report)
  #> None
  ```

- Generate the collisions report of the show

  ```python
  from pathlib import Path

  from loader import IostarJsonGcs, ijg_to_su
  from loader.parameters import IostarPhysicParameters
  from loader.reports import CollisionReport

  iostar_json_gcs = IostarJsonGcs.parse_file(Path("iostar_json_gcs_collision.json"))
  show_user = ijg_to_su(iostar_json_gcs)

  collision_report = CollisionReport.generate(show_user)
  print(collision_report.collision_infractions[:10])
  """
  [
      CollisionInfraction(
          frame=0, drone_index_1=0, drone_index_2=1, distance=1.24, in_air=True
      ),
      CollisionInfraction(
          frame=0, drone_index_1=0, drone_index_2=2, distance=1.24, in_air=True
      ),
      CollisionInfraction(
          frame=0, drone_index_1=1, drone_index_2=3, distance=1.24, in_air=True
      ),
      CollisionInfraction(
          frame=0, drone_index_1=2, drone_index_2=3, distance=1.24, in_air=True
      ),
      CollisionInfraction(
          frame=1, drone_index_1=0, drone_index_2=1, distance=1.24, in_air=True
      ),
      CollisionInfraction(
          frame=1, drone_index_1=0, drone_index_2=2, distance=1.24, in_air=True
      ),
      CollisionInfraction(
          frame=1, drone_index_1=1, drone_index_2=3, distance=1.24, in_air=True
      ),
      CollisionInfraction(
          frame=1, drone_index_1=2, drone_index_2=3, distance=1.24, in_air=True
      ),
      CollisionInfraction(
          frame=2, drone_index_1=0, drone_index_2=1, distance=1.24, in_air=True
      ),
      CollisionInfraction(
          frame=2, drone_index_1=0, drone_index_2=2, distance=1.24, in_air=True
      ),
  ]
  """

  collision_report = CollisionReport.generate(
      show_user,
      physic_parameters=IostarPhysicParameters(security_distance_in_air=1.0),
  )
  print(collision_report)
  #> None
  ```

- Generate the dance size report of the show
  function

  ```python
  from pathlib import Path

  # TODO(jonathan): improve API
  from loader import IostarJsonGcs, ijg_to_su
  from loader.reports import AutopilotFormatReport

  iostar_json_gcs = IostarJsonGcs.parse_file(Path("iostar_json_gcs_dance_size.json"))
  show_user = ijg_to_su(iostar_json_gcs)

  autopilot_format_report = AutopilotFormatReport.generate(show_user)
  print(autopilot_format_report)
  """
  drone_px4_reports = {
      0: DronePx4Report(
          events_format_report=None,
          dance_size_infraction=DanceSizeInfraction(
              drone_index=0,
              dance_size=100106,
              position_events_size_pct=100,
              color_events_size_pct=0,
              fire_events_size_pct=0,
          ),
      )
  }
  """
  ```

### Import & Export

```python
from pathlib import Path

from loader import IostarJsonGcs, ijg_to_su, su_to_ijg

# Import an iostar json gcs file to a show user
show_user = ijg_to_su(IostarJsonGcs.parse_file(Path("iostar_json_gcs_valid.json")))

# Export the show user to an iostar json gcs string
iostart_json_gcs_string = su_to_ijg(show_user).json()
```
