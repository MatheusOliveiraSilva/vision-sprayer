from vision_sprayer.domain.models import Detection, Point, TrackState


class TargetTracker:
    """Smooths target detections into state that can survive across frames."""

    def __init__(self, smoothing: float = 0.28) -> None:
        if not 0 < smoothing <= 1:
            raise ValueError("smoothing must be in (0, 1]")
        self.smoothing = smoothing
        self._state: TrackState | None = None

    @property
    def state(self) -> TrackState | None:
        return self._state

    def update(self, detection: Detection) -> TrackState:
        observed = detection.bbox.center

        if self._state is None:
            self._state = TrackState(
                target_center=observed,
                confidence=detection.confidence,
                updated_at=detection.observed_at,
                age_frames=1,
            )
            return self._state

        previous = self._state.target_center
        alpha = self.smoothing
        smoothed = Point(
            x=previous.x + (observed.x - previous.x) * alpha,
            y=previous.y + (observed.y - previous.y) * alpha,
        )

        self._state = TrackState(
            target_center=smoothed,
            confidence=detection.confidence,
            updated_at=detection.observed_at,
            age_frames=self._state.age_frames + 1,
        )
        return self._state
