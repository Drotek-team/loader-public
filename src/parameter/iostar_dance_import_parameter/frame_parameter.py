from dataclasses import dataclass


@dataclass(frozen=True)
class FrameParameter:
    _absolute_fps = 24

    def from_second_to_frame(self, time: float) -> int:
        return int(time * self._absolute_fps)

    def from_frame_to_second(self, frame: int) -> float:
        return frame / self._absolute_fps


FRAME_PARAMETER = FrameParameter()
