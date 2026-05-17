from vision_sprayer.domain.models import Detection, LockState, Point, TrackState


class TargetTracker:
    """Smooths target detections into state that can survive across frames."""

    def __init__(
        self,
        smoothing: float = 0.28,
        locked_after_frames: int = 3,
        lost_after_missed_frames: int = 3,
    ) -> None:
        if not 0 < smoothing <= 1:
            raise ValueError("smoothing must be in (0, 1]")
        if locked_after_frames < 1:
            raise ValueError("locked_after_frames must be >= 1")
        if lost_after_missed_frames < 1:
            raise ValueError("lost_after_missed_frames must be >= 1")
        self.smoothing = smoothing
        self.locked_after_frames = locked_after_frames
        self.lost_after_missed_frames = lost_after_missed_frames
        self._state: TrackState | None = None

    @property
    def state(self) -> TrackState | None:
        return self._state

    def update(self, detection: Detection | None) -> TrackState | None:
        if detection is None:
            self._state = self._mark_missing_detection()
            return self._state

        observed = detection.bbox.center

        if self._state is None:
            self._state = TrackState(
                target_center=observed,
                confidence=detection.confidence,
                updated_at=detection.observed_at,
                age_frames=1,
                lock_state=self._lock_state_for_age(age_frames=1),
                missed_frames=0,
                raw_center=observed,
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
            lock_state=self._lock_state_for_age(age_frames=self._state.age_frames + 1),
            missed_frames=0,
            raw_center=observed,
        )
        return self._state

    def _mark_missing_detection(self) -> TrackState | None:
        if self._state is None:
            return None

        missed_frames = self._state.missed_frames + 1
        if missed_frames >= self.lost_after_missed_frames:
            return TrackState(
                target_center=self._state.target_center,
                confidence=self._state.confidence,
                updated_at=self._state.updated_at,
                age_frames=self._state.age_frames,
                lock_state=LockState.LOST,
                missed_frames=missed_frames,
                raw_center=None,
            )

        return TrackState(
            target_center=self._state.target_center,
            confidence=self._state.confidence,
            updated_at=self._state.updated_at,
            age_frames=self._state.age_frames,
            lock_state=LockState.LOCKED if self._state.lock_state == LockState.LOCKED else LockState.ACQUIRING,
            missed_frames=missed_frames,
            raw_center=None,
        )

    def _lock_state_for_age(self, age_frames: int) -> LockState:
        if age_frames >= self.locked_after_frames:
            return LockState.LOCKED
        return LockState.ACQUIRING
