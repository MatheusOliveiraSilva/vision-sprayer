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
        if track is None:
            return AimCommand(
                aim_point=self.aim_point,
                fire=False,
                distance_to_target=float("inf"),
                reason="no_target",
            )
        if track.lock_state == LockState.LOST:
            return AimCommand(
                aim_point=self.aim_point,
                fire=False,
                distance_to_target=self.aim_point.distance_to(track.target_center),
                reason="lost",
            )

        max_step = self.aim_speed_px_per_second * dt
        self.aim_point = self.aim_point.move_toward(track.target_center, max_step)
        distance = self.aim_point.distance_to(track.target_center)

        cooldown_ready = now - self._last_fire_at >= self.fire_cooldown_s
        has_lock = track.lock_state == LockState.LOCKED
        should_fire = distance <= self.fire_threshold_px and cooldown_ready and has_lock

        if should_fire:
            self._last_fire_at = now

        reason = "aligned" if should_fire else "tracking"
        if track.lock_state != LockState.LOCKED:
            reason = track.lock_state.value
        if distance <= self.fire_threshold_px and has_lock and not cooldown_ready:
            reason = "cooldown"

        return AimCommand(
            aim_point=self.aim_point,
            fire=should_fire,
            distance_to_target=distance,
            reason=reason,
        )
