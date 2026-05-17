from vision_sprayer.domain.models import ActuatorEvent
from vision_sprayer.domain.models import AimCommand
from vision_sprayer.domain.models import Detection
from vision_sprayer.domain.models import Frame
from vision_sprayer.domain.models import RuntimeSample
from vision_sprayer.domain.models import RuntimeSnapshot
from vision_sprayer.domain.models import TrackState
from vision_sprayer.observability.metrics import MetricsCollector
from vision_sprayer.observability.timing import StepTimings
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
        timings = StepTimings()

        frame = timings.measure_capture(lambda: self.capture_frame(now))
        detection = timings.measure_detection(lambda: self.detect_target(frame, now))
        track = timings.measure_tracking(lambda: self.update_track(detection))
        command = timings.measure_decision(lambda: self.decide_action(track, dt, now))
        actuator_event = self.apply_action(command, now)
        timings.finish_loop()
        metrics = self.collect_metrics(frame, timings)

        return self.build_snapshot(frame, detection, track, command, actuator_event, metrics)

    def capture_frame(self, now: float) -> Frame:
        return self.frame_source.next_frame(now)

    def detect_target(self, frame: Frame, now: float) -> Detection | None:
        return self.detector.detect(frame, now)

    def update_track(self, detection: Detection | None) -> TrackState | None:
        return self.tracker.update(detection)

    def decide_action(self, track: TrackState | None, dt: float, now: float) -> AimCommand:
        return self.targeting.decide(track, dt=dt, now=now)

    def apply_action(self, command: AimCommand, now: float) -> ActuatorEvent:
        return self.actuator.apply(command, now=now)

    def collect_metrics(self, frame: Frame, timings: StepTimings) -> RuntimeSample:
        return self.metrics.record(
            frame=frame,
            timings=timings,
            fired_count=self.actuator.fired_count,
        )

    def build_snapshot(
        self,
        frame: Frame,
        detection: Detection | None,
        track: TrackState | None,
        command: AimCommand,
        actuator_event: ActuatorEvent,
        metrics: RuntimeSample,
    ) -> RuntimeSnapshot:
        return RuntimeSnapshot(
            frame=frame,
            detection=detection,
            track=track,
            command=command,
            actuator_event=actuator_event,
            metrics=metrics,
        )
