from __future__ import annotations

from .actuator import FakeActuator
from .detector import SimulatedDetector
from .domain import Point, RuntimeSnapshot
from .frame_source import SimulatedFrameSource
from .metrics import MetricsCollector
from .targeting import TargetingPolicy
from .tracker import TargetTracker


class SprayerOrchestrator:
    """Owns the runtime lifecycle for one perception -> action tick."""

    def __init__(
        self,
        frame_source: SimulatedFrameSource,
        detector: SimulatedDetector,
        tracker: TargetTracker,
        targeting: TargetingPolicy,
        actuator: FakeActuator,
        metrics: MetricsCollector,
    ) -> None:
        self.frame_source = frame_source
        self.detector = detector
        self.tracker = tracker
        self.targeting = targeting
        self.actuator = actuator
        self.metrics = metrics

    @classmethod
    def default(cls, width: int = 960, height: int = 540) -> "SprayerOrchestrator":
        return cls(
            frame_source=SimulatedFrameSource(width=width, height=height),
            detector=SimulatedDetector(),
            tracker=TargetTracker(),
            targeting=TargetingPolicy(initial_aim=Point(width / 2, height / 2)),
            actuator=FakeActuator(),
            metrics=MetricsCollector(),
        )

    def tick(self, now: float, dt: float) -> RuntimeSnapshot:
        loop_started_at = now

        frame = self.frame_source.next_frame(now)

        detection_started_at = now
        detection = self.detector.detect(frame, now)
        detection_finished_at = now

        track = self.tracker.update(detection)
        command = self.targeting.decide(track, dt=dt, now=now)
        actuator_event = self.actuator.apply(command, now=now)
        metrics = self.metrics.record(
            frame=frame,
            now=now,
            loop_started_at=loop_started_at,
            detection_started_at=detection_started_at,
            detection_finished_at=detection_finished_at,
            fired_count=self.actuator.fired_count,
        )

        return RuntimeSnapshot(
            frame=frame,
            detection=detection,
            track=track,
            command=command,
            actuator_event=actuator_event,
            metrics=metrics,
        )

