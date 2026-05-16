from vision_sprayer.domain.models import Detection, Frame


class SimulatedDetector:
    """Detection adapter for V0.

    V0 has no pixels or neural network yet. This adapter preserves the same
    boundary a future OpenCV/YOLO detector will use: Frame in, Detection out.
    """

    def __init__(self, confidence: float = 0.98) -> None:
        self.confidence = confidence

    def detect(self, frame: Frame, now: float) -> Detection:
        return Detection(
            frame_sequence=frame.sequence,
            observed_at=now,
            bbox=frame.target,
            confidence=self.confidence,
        )
