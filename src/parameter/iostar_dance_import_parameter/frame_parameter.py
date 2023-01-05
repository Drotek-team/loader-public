from dataclasses import dataclass


@dataclass(frozen=True)
class FrameParameter:
    position_fps = 4
    color_fps = 24
    fire_fps = 24
    absolute_fps = 24

    # TO DO: test this
    def from_position_frame_to_json_frame(self, position_frame: int) -> int:
        return position_frame * int(self.absolute_fps / self.position_fps)

    # TO DO: test this
    def from_color_frame_to_json_frame(self, color_frame: int) -> int:
        return color_frame * int(self.absolute_fps / self.color_fps)

    # TO DO: test this
    def from_fire_frame_to_json_frame(self, fire_frame: int) -> int:
        return fire_frame * int(self.absolute_fps / self.fire_fps)

    # TO DO: test this
    def from_second_to_position_frame(self, second: float) -> int:
        return int(self.position_fps * second)


FRAME_PARAMETER = FrameParameter()
