from dataclasses import dataclass


@dataclass(frozen=True)
class FrameParameter:
    position_fps = 4
    color_fps = 24
    fire_fps = 24
    absolute_fps = 24

    def from_position_frame_to_json_frame(self, position_frame: int) -> int:
        return position_frame * int(self.absolute_fps / self.position_fps)

    def from_color_frame_to_json_frame(self, color_frame: int) -> int:
        return color_frame * int(self.absolute_fps / self.color_fps)

    def from_fire_frame_to_json_frame(self, fire_frame: int) -> int:
        return fire_frame * int(self.absolute_fps / self.fire_fps)

    def from_second_to_position_frame(self, second: float) -> int:
        return int(
            int(self.absolute_fps / self.position_fps) * self.absolute_fps * second
        )


FRAME_PARAMETER = FrameParameter()
