from dataclasses import dataclass


# TODO: make the missing test
@dataclass(frozen=True)
class FrameParameter:
    position_fps = 4
    color_fps = 24
    fire_fps = 24
    absolute_fps = 24

    @property
    def position_frame(self):
        return self.from_position_frame_to_absolute_frame(1)

    @property
    def color_frame(self):
        return self.from_color_frame_to_absolute_frame(1)

    @property
    def fire_frame(self):
        return self.from_fire_frame_to_absolute_frame(1)

    def from_position_frame_to_absolute_frame(self, position_frame: int) -> int:
        return position_frame * int(self.absolute_fps / self.position_fps)

    def from_absolute_frame_to_position_frame(self, absolute_frame: int) -> int:
        return int(absolute_frame * self.position_fps / self.absolute_fps)

    def from_position_frame_to_absolute_time(self, position_frame: int) -> float:
        return position_frame / self.position_fps

    def from_absolute_time_to_position_frame(self, second: float) -> int:
        return int(self.position_fps * second)

    def from_color_frame_to_absolute_frame(self, color_frame: int) -> int:
        return color_frame * int(self.absolute_fps / self.color_fps)

    def from_absolute_frame_to_color_frame(self, absolute_frame: int) -> float:
        return absolute_frame * self.color_fps / self.absolute_fps

    def from_color_frame_to_absolute_time(self, color_frame: int) -> float:
        return color_frame / self.color_fps

    def from_absolute_time_to_color_frame(self, second: float) -> int:
        return int(self.color_fps * second)

    def from_fire_frame_to_absolute_frame(self, fire_frame: int) -> int:
        return fire_frame * int(self.absolute_fps / self.color_fps)

    def from_absolute_frame_to_fire_frame(self, absolute_frame: int) -> float:
        return absolute_frame * self.fire_fps / self.absolute_fps

    def from_fire_frame_to_absolute_time(self, fire_frame: int) -> float:
        return fire_frame / self.fire_fps

    def from_absolute_time_to_fire_frame(self, second: float) -> int:
        return int(self.fire_fps * second)

    def from_absolute_frame_to_absolute_time(self, absolute_frame: int) -> float:
        return absolute_frame / self.absolute_fps

    def from_absolute_time_to_absolute_frame(self, absolute_time: float) -> int:
        return int(absolute_time * self.absolute_fps)


FRAME_PARAMETER = FrameParameter()
