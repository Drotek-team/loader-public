# Changelog

## v0.7.1 (2023-09-27)

### Perf

- use list(dance_binary) instead of list(map(int, dance_binary))
- remove in_air flag
- improve in_dance_flight_simulation() numpy use
- use np.arange instead of np.array(list(range()))
- use scipy.spatial.distance.cdist

## v0.7.0 (2023-09-14)

### Feat

- implement the new color interpolation
- implement the new time format
- add MagicNumber to select the binary schema version

### Refactor

- use new binary format by default
- replace Event.timecode by Event.frame
- remove duplicate logic
- improve Events typing
- **drone_px4**: pass frame instead of timecode

## v0.6.0 (2023-09-11)

### Fix

- use the barycenter of the family drones as family position

## v0.6.0a7 (2023-07-31)

### Fix

- add physic_parameters to reports

## v0.6.0a6 (2023-07-31)

### Fix

- increase performance tolerance for import checks

## v0.6.0a5 (2023-07-28)

### Feat

- keep physic parameters when converting from IostarJsonGcs to ShowUser

## v0.6.0a4 (2023-07-28)

### Feat

- add physic_parameters to GlobalReport and summary

### Fix

- retro-compatibility with old dance

## v0.6.0a3 (2023-07-27)

### Feat

- add metadata to GlobalReport and summary

### Refactor

- use metadata in ShowUser.create()
- group metadata

## v0.6.0a2 (2023-07-27)

### Refactor

- add blender and lightshow creator version to dance schemas
- add loader version to dance schemas
- add physic parameters to IostarJsonGcs
- add physic parameters to show user

## v0.6.0a1 (2023-07-27)

### Perf

- check collisions at 4 FPS instead of 24

## v0.6.0a0 (2023-07-26)

### Refactor

- upgrade pydantic to v2

## v0.5.0 (2023-07-25)

### Feat

- add .summarize() on infractions and reports
- rework report structure
- add progress bars

### Refactor

- display drone_indices with ranges
- rework base reports, infractions, summaries inheritance
- use drone_indices in all summaries
- rework BoundaryInfraction.generate()
- add IntegerBoundaryInfraction.generate()
- extract DanceSizeReport from AutopilotFormatReport

## v0.4.2 (2023-06-05)

### Fix

- add tolerance for import and export checks

## v0.4.1 (2023-06-01)

### Fix

- invert nb_x and nb_y in IostarJsonGcs

## v0.4.0 (2023-05-31)

### Feat

- allow empty families
- allow different number of drones in families
- support is_partial for collision check

### Fix

- compatibility with numpy 1.17
- IostarJsonGcs.nb_drones_per_family
- inverse nb_x and nb_y in IostarJsonGcs
- include angle_takeoff in ShowUser.\_\_eq\_\_()
- **ShowPositionFrame**: set in_air to false on ground
- use len() instead of comparing to None
- ShowPositionFrames.create_from_show_user()
- **land_parameter**: always return floats

### Refactor

- add nb_x, nb_y, nb_drones_per_family to ShowUser
- invert matrix indices
- add GridInfos
- add Family.from_drone_px4()
- remove ShowConfigurationGcs
- remove GridConfiguration
- round instead of troncating
- use matrix in get_valid_show_user()
- calculate matrix directly in GridConfiguration
- use matrix to init the grid configuration
- add matrix to grid configurations
- remove ShowConfigurationGcs.from_show_configuration
- **show_user**: use radians
- merge ShowConfiguration
- require step in ShowUser.create()
- require takeoff_angle in ShowUser.create()
- add DroneUser.from_drone_px4
- add \_\_eq\_\_ to ShowUser
- remove possible GridConfiguration cycle
- get_valid_show_user() to use API
- remove \_\_future\_\_ annotations
- add drone_index to TakeoffFormatReport
- drop dict support in reports
- rework AutopilotFormatReport
- allow drone_index field in reports
- remove get_report_validation()
- change DanceSizeInfraction to a report
- use \_\_len\_\_() instead of get_nb_errors()
- rework report generation
- rename shows to schemas
- remove performance/collision types from API
- move ShowPositionFrame/DroneTrajectoryPerformance
- rework shows access
- rework grid configurations
- rework Grid
- rework IostarJsonGcs migrations
- rework DronePx4 to ShowUser migration
- rework ShowUser to DronePx4 migration
- rework DronePx4 migrations
- rework show configurations migrations
- regroup migrations
- rename report to reports
- rework parameters access
- rework report access
- rename report files
- remove su_to_stp
- rename show_env to shows
- add s to parameter
- move simulation
- use ShowPositionFrame.from_show_user
- reorganize migration_dp_binary
- rename iostar_json(\_gcs)
- remove autopilot_format folder
- move all migrations in show_env
- remove ShowPositionFrames
- remove ShowTrajectoryPerformance
- remove IostarJson
- rework public API
- remove ShowCollisionTrajectory use
- use milliseconds for fire duration

## v0.3.0 (2023-05-03)

### Feat

- add configuration to generate a report
- add recommended physic parameters
- **report**: add conf for physic_parameter
- generate report without TakeoffFormatReport

### Fix

- add types to dataclasses attributes
- remove try except ImportError, ModuleNotFoundError

## v0.2.3 (2023-04-27)

### Fix

- round second to frame conversion

## v0.2.2 (2023-04-21)

### Fix

- nb_x and nb_y from get_nb_x_nb_y_from_grid()

## v0.2.1 (2023-04-17)

### Fix

- ignore takeoff in PerformanceInfraction

## v0.2.0 (2023-04-14)

### Feat

- add collision_distance as parameter

## v0.1.7 (2023-04-05)

### Fix

- recalculate convex-hull after rounding

## v0.1.6 (2023-04-05)

### Fix

- use all positions to calculate the hull

## v0.1.5 (2023-03-17)

### Fix

- calculate_convex_hull

## v0.1.4 (2023-03-13)

### Fix

- change angle_takeoff direction

## v0.1.3 (2023-03-09)

### Feat

- add get_dance_size_information function

### Fix

- velocity and acceleration evaluation

### Refactor

- fuse dance_size and dance_size_info
- **\_\_init\_\_.py**: use contextlib.suppress

## v0.1.2 (2023-02-27)

### Feat

- **ci**: run commitizen in CI

### Fix

- **ci**: do not run commitizen on (dev-)master
- improve decimal_number_tolerance

## v0.1.1 (2023-02-24)

## v0.1.0 (2023-02-24)
