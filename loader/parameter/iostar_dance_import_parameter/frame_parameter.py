from dataclasses import dataclass


@dataclass(frozen=True)
class FrameParameter:
    _fps = 24

    def from_second_to_frame(self, time: float) -> int:
        return round(time * self._fps)

    def from_frame_to_second(self, frame: int) -> float:
        return frame / self._fps


FRAME_PARAMETER = FrameParameter()
