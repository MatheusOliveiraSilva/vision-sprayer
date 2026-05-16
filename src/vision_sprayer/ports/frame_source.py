from typing import Protocol

from vision_sprayer.domain.models import Frame


class FrameSource(Protocol):
    def next_frame(self, now: float) -> Frame:
        pass

