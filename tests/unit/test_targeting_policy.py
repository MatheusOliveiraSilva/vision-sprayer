from vision_sprayer.domain.models import Point, TrackState
from vision_sprayer.targeting.targeting_policy import TargetingPolicy


def test_targeting_moves_aim_toward_track_without_overshooting() -> None:
    policy = TargetingPolicy(
        initial_aim=Point(0, 0),
        aim_speed_px_per_second=100,
        fire_threshold_px=1,
    )
    track = TrackState(
        target_center=Point(100, 0),
        confidence=1,
        updated_at=0,
        age_frames=1,
    )

    command = policy.decide(track, dt=0.25, now=0)

    assert command.aim_point == Point(25, 0)
    assert command.fire is False
    assert command.reason == "tracking"


def test_targeting_fires_when_aligned_and_cooldown_ready() -> None:
    policy = TargetingPolicy(
        initial_aim=Point(10, 10),
        fire_threshold_px=2,
        fire_cooldown_s=0.5,
    )
    track = TrackState(
        target_center=Point(10, 10),
        confidence=1,
        updated_at=0,
        age_frames=1,
    )

    command = policy.decide(track, dt=0.016, now=1.0)

    assert command.fire is True
    assert command.reason == "aligned"


def test_targeting_respects_fire_cooldown() -> None:
    policy = TargetingPolicy(
        initial_aim=Point(10, 10),
        fire_threshold_px=2,
        fire_cooldown_s=0.5,
    )
    track = TrackState(
        target_center=Point(10, 10),
        confidence=1,
        updated_at=0,
        age_frames=1,
    )

    first = policy.decide(track, dt=0.016, now=1.0)
    second = policy.decide(track, dt=0.016, now=1.2)

    assert first.fire is True
    assert second.fire is False
    assert second.reason == "cooldown"
