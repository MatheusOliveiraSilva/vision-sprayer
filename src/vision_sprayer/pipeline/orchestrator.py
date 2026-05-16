import time

from vision_sprayer.domain.models import RuntimeSnapshot
from vision_sprayer.observability.metrics import MetricsCollector
from vision_sprayer.ports.actuator import Actuator
from vision_sprayer.ports.detector import Detector
from vision_sprayer.ports.frame_source import FrameSource
from vision_sprayer.targeting.targeting_policy import TargetingPolicy
from vision_sprayer.tracking.target_tracker import TargetTracker


class VisionPipeline:
    """Owns the runtime lifecycle for one perception -> action tick."""

    def __init__(
        self,
        frame_source: FrameSource,
        detector: Detector,
        tracker: TargetTracker,
        targeting: TargetingPolicy,
        actuator: Actuator,
        metrics: MetricsCollector,
    ) -> None:
        self.frame_source = frame_source
        self.detector = detector
        self.tracker = tracker
        self.targeting = targeting
        self.actuator = actuator
        self.metrics = metrics

    def tick(self, now: float, dt: float) -> RuntimeSnapshot:
        loop_started_at = time.perf_counter()

        frame = self.frame_source.next_frame(now)
        capture_finished_at = time.perf_counter()

        detection_started_at = time.perf_counter()
        detection = self.detector.detect(frame, now)
        detection_finished_at = time.perf_counter()

        track = self.tracker.update(detection)
        command = self.targeting.decide(track, dt=dt, now=now)
        actuator_event = self.actuator.apply(command, now=now)
        loop_finished_at = time.perf_counter()
        metrics = self.metrics.record(
            frame=frame,
            now=loop_finished_at,
            loop_started_at=loop_started_at,
            capture_finished_at=capture_finished_at,
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
