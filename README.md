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

- Create your show with `create_empty_show_user`

  ```python
  from loader import create_empty_show_user

  nb_drones = 5
  show_user = create_empty_show_user(nb_drones)
  ```

- Add position events to `drone_user` with `add_position_event`

  ```python
  show_user.drones_user[0].add_position_event(frame=0, xyz=(0.0, 0.0, 0.0))
  show_user.drones_user[0].add_position_event(frame=240, xyz=(0.0, 0.0, 10.0))
  show_user.drones_user[0].add_position_event(frame=360, xyz=(2.0, 0.0, 10.0))
  ```

- Add color events to `drone_user` with `add_color_event`

  ```python
  show_user.drones_user[0].add_color_event(frame=250, rgbw=(1.0, 0.0, 0.0, 0.0))
  show_user.drones_user[0].add_color_event(frame=300, rgbw=(0.0, 0.0, 1.0, 0.0))
  ```

- Add fire events to `drone_user` with `add_fire_event`

  ```python
  show_user.drones_user[0].add_fire_event(frame=210, chanel=0, duration_frame=0)
  show_user.drones_user[0].add_fire_event(frame=280, chanel=1, duration_frame=0)
  ```

### Show Reports

- Generate the global report of the show with `generate_report_from_show_user`

  ```python
  from loader import generate_report_from_show_user

  report = generate_report_from_show_user(show_user)
  print(report.summary())
  ```

- Generate the performance report of the show with `get_performance_infractions` function

  ```python
  from loader import get_performance_infractions, PerformanceKind, PerformanceRange

  performance_infractions = get_performance_infractions(show_user, {})
  print(performance_infractions[0])

  new_performance_configuration = {
      PerformanceKind.HORIZONTAL_VELOCITY: PerformanceRange(3.0)
  }
  performance_infractions = get_performance_infractions(
      show_user, new_performance_configuration
  )
  print(performance_infractions[0])
  ```

- Generate the collisions report of the show with the `get_collision_infractions` function

  ```python
  from loader import get_collision_infractions, create_show_position_frames_from_show_user

  show_position_frames = create_show_position_frames_from_show_user(show_user)
  collision_infractions = get_collision_infractions(show_position_frames)
  print(collision_infractions[0])
  ```

- Generate the dance size report of the show with the `get_dance_size_infractions`
  function

  ```python
  from loader import get_dance_size_infractions

  dance_size_infractions = get_dance_size_infractions(show_user)
  print(dance_size_infractions[0])
  ```

### Import & Export

- Export the show user with the `convert_show_user_to_iostar_json_gcs`

  ```python
  from loader import convert_show_user_to_iostar_json_gcs

  iostart_json_gcs_string = convert_show_user_to_iostar_json_gcs(show_user)
  ```

- Import an iostar json gcs string with `convert_iostar_json_gcs_string_to_show_user`

  ```python
  from loader import convert_iostar_json_gcs_string_to_show_user

  show_user = convert_iostar_json_gcs_string_to_show_user(iostar_json_gcs_string)
  ```
