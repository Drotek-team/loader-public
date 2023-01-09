from dataclasses import dataclass


# TODO: make the missing test
@dataclass(frozen=True)
class FrameParameter:
    absolute_fps = 24

    def from_absolute_time_to_absolute_frame(self, absolute_time: float) -> int:
        return int(absolute_time * self.absolute_fps)

    def from_absolute_frame_to_absolute_time(self, absolute_frame: int) -> float:
        return absolute_frame / self.absolute_fps


FRAME_PARAMETER = FrameParameter()
