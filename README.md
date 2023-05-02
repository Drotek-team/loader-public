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
from loader import create_empty_show_user

# Create an empty show user with `create_empty_show_user`
show_user = create_empty_show_user(nb_drones=5)

# Add position events to `drone_user` with `add_position_event`
show_user.drones_user[0].add_position_event(frame=0, xyz=(0.0, 0.0, 0.0))
show_user.drones_user[0].add_position_event(frame=240, xyz=(0.0, 0.0, 10.0))
show_user.drones_user[0].add_position_event(frame=360, xyz=(2.0, 0.0, 10.0))

# Add color events to `drone_user` with `add_color_event`
show_user.drones_user[0].add_color_event(frame=250, rgbw=(1.0, 0.0, 0.0, 0.0))
show_user.drones_user[0].add_color_event(frame=300, rgbw=(0.0, 0.0, 1.0, 0.0))

# Add fire events to `drone_user` with `add_fire_event`
show_user.drones_user[0].add_fire_event(frame=210, chanel=0, duration_frame=0)
show_user.drones_user[0].add_fire_event(frame=280, chanel=1, duration_frame=0)
```

### Show Reports

- Generate the global report of the show with `generate_report_from_show_user`

  ```python
  from pathlib import Path

  from loader import generate_report_from_iostar_json_gcs_string

  report = generate_report_from_iostar_json_gcs_string(
      Path("iostar_json_gcs_valid.json").read_text(),
  )
  print(report.summary())
  #> takeoff_format=0 autopilot_format=0 performance=0 collision=0

  report = generate_report_from_iostar_json_gcs_string(
      Path("iostar_json_gcs_collision.json").read_text(),
  )
  print(report.summary())
  #> takeoff_format=0 autopilot_format=0 performance=0 collision=4080

  report = generate_report_from_iostar_json_gcs_string(
      Path("iostar_json_gcs_performance.json").read_text(),
  )
  print(report.summary())
  #> takeoff_format=0 autopilot_format=0 performance=4 collision=0

  report = generate_report_from_iostar_json_gcs_string(
      Path("iostar_json_gcs_dance_size.json").read_text(),
  )
  print(report.summary())
  #> takeoff_format=0 autopilot_format=1 performance=0 collision=0
  ```

- Generate the performance report of the show with `get_performance_infractions` function

  ```python
  from pathlib import Path

  from loader import (
      IostarPhysicParameter,
      convert_iostar_json_gcs_string_to_show_user,
      get_performance_infractions,
  )

  show_user = convert_iostar_json_gcs_string_to_show_user(
      Path("iostar_json_gcs_performance.json").read_text(),
  )

  performance_infractions = get_performance_infractions(show_user)
  print(performance_infractions)
  """
  [
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

  physic_parameter = IostarPhysicParameter(acceleration_max=2)
  performance_infractions = get_performance_infractions(
      show_user,
      physic_parameter=physic_parameter,
  )
  print(performance_infractions)
  #> []
  ```

- Generate the collisions report of the show with the `get_collision_infractions` function

  ```python
  from pathlib import Path

  from loader import (
      convert_iostar_json_gcs_string_to_show_user,
      create_show_position_frames_from_show_user,
      get_collision_infractions,
  )

  show_user = convert_iostar_json_gcs_string_to_show_user(
      Path("iostar_json_gcs_collision.json").read_text(),
  )

  show_position_frames = create_show_position_frames_from_show_user(show_user)
  collision_infractions = get_collision_infractions(show_position_frames)
  print(collision_infractions[:10])
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

  collision_infractions = get_collision_infractions(
      show_position_frames,
      collision_distance=1.0,
  )
  print(collision_infractions)
  #> []
  ```

- Generate the dance size report of the show with the `get_dance_size_infractions`
  function

  ```python
  from pathlib import Path

  from loader import (
      convert_iostar_json_gcs_string_to_show_user,
      get_dance_size_infractions,
  )

  show_user = convert_iostar_json_gcs_string_to_show_user(
      Path("iostar_json_gcs_dance_size.json").read_text(),
  )

  dance_size_infractions = get_dance_size_infractions(show_user)
  print(dance_size_infractions)
  """
  [
      DanceSizeInfraction(
          drone_index=0,
          dance_size=100106,
          position_events_size_pct=100,
          color_events_size_pct=0,
          fire_events_size_pct=0,
      )
  ]
  """
  ```

### Import & Export

```python
from pathlib import Path

from loader import (
    convert_iostar_json_gcs_string_to_show_user,
    convert_show_user_to_iostar_json_gcs,
)

# Import an iostar json gcs string with `convert_iostar_json_gcs_string_to_show_user`
show_user = convert_iostar_json_gcs_string_to_show_user(
    Path("iostar_json_gcs_valid.json").read_text(),
)

# Export the show user with `convert_show_user_to_iostar_json_gcs`
iostart_json_gcs_string = convert_show_user_to_iostar_json_gcs(show_user)
```
