from vision_sprayer.domain.models import AimCommand, LockState, Point, TrackState


class TargetingPolicy:
    """Pure aiming/fire decision logic.

    It does not know about rendering, hardware, serial ports, or Pygame.
    """

    def __init__(
        self,
        initial_aim: Point,
        aim_speed_px_per_second: float = 650.0,
        fire_threshold_px: float = 18.0,
        fire_cooldown_s: float = 0.35,
    ) -> None:
        self.aim_point = initial_aim
        self.aim_speed_px_per_second = aim_speed_px_per_second
        self.fire_threshold_px = fire_threshold_px
        self.fire_cooldown_s = fire_cooldown_s
        self._last_fire_at = -9999.0

    def decide(self, track: TrackState | None, dt: float, now: float) -> AimCommand:
        if self.has_no_target(track):
            return self.hold_aim(reason="no_target")

        track = self.require_track(track)
        if self.target_is_lost(track):
            return self.hold_aim(reason="lost", track=track)

        self.move_aim_toward_track(track, dt)
        distance = self.distance_to_track(track)
        should_fire = self.should_fire(track=track, distance=distance, now=now)

        if should_fire:
            self._last_fire_at = now

        return AimCommand(
            aim_point=self.aim_point,
            fire=should_fire,
            distance_to_target=distance,
            reason=self.decision_reason(track=track, distance=distance, should_fire=should_fire, now=now),
        )

    def has_no_target(self, track: TrackState | None) -> bool:
        return track is None

    def require_track(self, track: TrackState | None) -> TrackState:
        if track is None:
            raise ValueError("track is required")
        return track

    def target_is_lost(self, track: TrackState) -> bool:
        return track.lock_state == LockState.LOST

    def hold_aim(self, reason: str, track: TrackState | None = None) -> AimCommand:
        distance = float("inf")
        if track is not None:
            distance = self.aim_point.distance_to(track.target_center)
        return AimCommand(
            aim_point=self.aim_point,
            fire=False,
            distance_to_target=distance,
            reason=reason,
        )

    def move_aim_toward_track(self, track: TrackState, dt: float) -> None:
        max_step = self.aim_speed_px_per_second * dt
        self.aim_point = self.aim_point.move_toward(track.target_center, max_step)

    def distance_to_track(self, track: TrackState) -> float:
        return self.aim_point.distance_to(track.target_center)

    def should_fire(self, track: TrackState, distance: float, now: float) -> bool:
        return self.is_aligned(distance) and self.has_lock(track) and self.cooldown_ready(now)

    def is_aligned(self, distance: float) -> bool:
        return distance <= self.fire_threshold_px

    def has_lock(self, track: TrackState) -> bool:
        return track.lock_state == LockState.LOCKED

    def cooldown_ready(self, now: float) -> bool:
        return now - self._last_fire_at >= self.fire_cooldown_s

    def decision_reason(self, track: TrackState, distance: float, should_fire: bool, now: float) -> str:
        if should_fire:
            return "aligned"
        if not self.has_lock(track):
            return track.lock_state.value
        if self.is_aligned(distance) and not self.cooldown_ready(now):
            return "cooldown"
        return "tracking"
