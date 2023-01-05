from dataclasses import dataclass


@dataclass(frozen=True)
class FrameParameter:
    position_fps = 4
    color_fps = 24
    fire_fps = 24
    absolute_fps = 24

    # TO DO: test this
    def from_position_frame_to_absolute_frame(self, position_frame: int) -> int:
        return position_frame * int(self.absolute_fps / self.color_fps)

    # TO DO: test this
    def from_position_frame_to_absolute_time(self, position_frame: int) -> float:
        return position_frame / self.position_fps

    # TO DO: test this
    def from_absolute_time_to_position_frame(self, second: float) -> int:
        return int(self.position_fps * second)

    # TO DO: test this
    def from_color_frame_to_absolute_frame(self, color_frame: int) -> int:
        return color_frame * int(self.absolute_fps / self.color_fps)

    # TO DO: test this
    def from_color_frame_to_absolute_time(self, color_frame: int) -> float:
        return color_frame / self.color_fps

    # TO DO: test this
    def from_absolute_time_to_color_frame(self, second: float) -> int:
        return int(self.color_fps * second)

    # TO DO: test this
    def from_fire_frame_to_absolute_frame(self, fire_frame: int) -> int:
        return fire_frame * int(self.absolute_fps / self.color_fps)

    # TO DO: test this
    def from_fire_frame_to_absolute_time(self, fire_frame: int) -> float:
        return fire_frame / self.fire_fps

    # TO DO: test this
    def from_absolute_time_to_fire_frame(self, second: float) -> int:
        return int(self.fire_fps * second)


FRAME_PARAMETER = FrameParameter()
