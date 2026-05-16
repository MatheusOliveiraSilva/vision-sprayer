from sprayer_sim.domain import Detection, Point, Rect
from sprayer_sim.tracker import TargetTracker


def test_tracker_initializes_from_first_detection() -> None:
    tracker = TargetTracker(smoothing=0.5)
    detection = Detection(
        frame_sequence=1,
        observed_at=10,
        bbox=Rect(center=Point(20, 30), width=10, height=10),
        confidence=0.9,
    )

    state = tracker.update(detection)

    assert state.target_center == Point(20, 30)
    assert state.confidence == 0.9
    assert state.age_frames == 1


def test_tracker_smooths_subsequent_detections() -> None:
    tracker = TargetTracker(smoothing=0.5)
    tracker.update(
        Detection(
            frame_sequence=1,
            observed_at=10,
            bbox=Rect(center=Point(0, 0), width=10, height=10),
            confidence=1,
        )
    )

    state = tracker.update(
        Detection(
            frame_sequence=2,
            observed_at=11,
            bbox=Rect(center=Point(100, 50), width=10, height=10),
            confidence=1,
        )
    )

    assert state.target_center == Point(50, 25)
    assert state.age_frames == 2

