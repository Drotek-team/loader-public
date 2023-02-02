# Loader

This project goal is to help the creation and verification of Drotek dance file.

## Installation

### Installation of the python tools

- Install pyenv and poetry [pyenv & poetry](https://drotek.atlassian.net/wiki/spaces/DRONE/pages/36143105/Python+Tools+Tutorial)

### Installation of the module in your project

1. Copy the _loader_ in your project

1. Open the _loader_ with _Visual Studio Code_

1. Use Python 3.8.2

   ```shell
   pyenv shell 3.8.2
   ```

1. Initialize the _poetry_ environment

   ```shell
   poetry shell
   ```

1. Install the dependencies of the project

   ```shell
   poetry install
   ```

## Use the loader in your project

### Show Creation

1. Create your show with the `create_empty_show_user` function

   ```shell
   from loader.src.editor import create_empty_show_user

   nb_drones = 1
   show_user = create_empty_show_user(nb_drones)
   ```

1. Add position events to the `drone_user` with the `add_position_event` method

   ```shell
   show_user.drones_user[0].add_position_event(frame=0,xyz=(0.0,0.0,0.0))
   show_user.drones_user[0].add_position_event(frame=240,xyz=(0.0,0.0,10.0))
   show_user.drones_user[0].add_position_event(frame=360,xyz=(2.0,0.0,10.0))
   ```

1. Add color events to the `drone_user` with the `add_color_event` method

   ```shell
   show_user.drones_user[0].add_color_event(frame=250,rgbw=(1.0,0.0,0.0,0.0))
   show_user.drones_user[0].add_color_event(frame=300,rgbw=(0.0,0.0,1.0,0.0))
   ```

1. Add fire events to the `drone_user` with the `add_fire_event` method

   ```shell
   show_user.drones_user[0].add_fire_event(frame=210,chanel=0,duration_frame=0)
   show_user.drones_user[0].add_fire_event(frame=280,chanel=1,duration_frame=0)
   ```

### Show Check

1. Check the show validity with the `global_check_show_user`

   ```shell
   report_string = global_check_show_user(show_user)
   print(report_string)
   ```

1. Check the performance of the show with the `get_performance_infractions` function

   ```shell
   from loader.src.editor import get_performance_infractions,Metric,MetricRange

   performance_infractions = get_performance_infractions(show_user,{})
   print(performance_infractions.display_message())

   new_performance_configuration = {Metric.HORIZONTAL_VELOCITY:MetricRange(3.0)}
   performance_infractions = get_performance_infractions(show_user,new_performance_configuration)
   print(performance_infractions.display_message())
   ```

1. Check the collisions of the show with the `get_collision_infractions` function

   ```shell
   from loader.src.editor import get_collision_infractions, su_to_ss

   collision_infractions = get_collision_infractions(su_to_ss(show_user))
   print(collision_infractions.display_message())
   ```

1. Check the dance size infractions of the show with the `get_dance_size_infractions`
   function

   ```shell
   from loader.src.editor import get_dance_size_infractions, su_to_ss

   dance_size_infractions = get_dance_size_infractions(show_user)
   print(dance_size_infractions.display_message())
   ```

### Import & Export

1. Export the show user with the `export_show_user_to_iostar_json_gcs_string`

   ```shell
   from loader.src.editor import export_show_user_to_iostar_json_gcs_string

   iostart_json_gcs_string = export_show_user_to_iostar_json_gcs_string(show_user)
   ```

1. Import an iostar json gcs string with `import_iostar_json_gcs_string_to_show_user`

   ```shell
   from loader.src.editor import import_iostar_json_gcs_string_to_show_user

   show_user = import_iostar_json_gcs_string_to_show_user(iostar_json_gcs_string)
   ```

1. Get an iostar json gcs with verified metadata with `get_verified_iostar_json_gcs`

   ```shell
   from loader.src.editor import import_iostar_json_gcs_string_to_show_user

   verified_iostar_json_gcs = get_verified_iostar_json_gcs(iostar_json_gcs_string)
   ```
