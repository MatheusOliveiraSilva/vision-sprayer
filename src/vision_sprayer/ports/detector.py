from typing import Protocol

from vision_sprayer.domain.models import Detection, Frame


class Detector(Protocol):
    def detect(self, frame: Frame, now: float) -> Detection | None:
        pass

