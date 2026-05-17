from collections import deque

from vision_sprayer.domain.models import Frame, RuntimeSample
from vision_sprayer.observability.timing import StepTimings


class MetricsCollector:
    def __init__(self, window_size: int = 60) -> None:
        self._loop_durations: deque[float] = deque(maxlen=window_size)

    def record(
        self,
        frame: Frame,
        timings: StepTimings,
        fired_count: int,
    ) -> RuntimeSample:
        loop_latency = timings.loop_finished_at - timings.loop_started_at
        self._loop_durations.append(loop_latency)

        avg_loop = sum(self._loop_durations) / len(self._loop_durations)
        fps = 1.0 / avg_loop if avg_loop > 0 else 0.0

        return RuntimeSample(
            fps=fps,
            frame_age_ms=(timings.loop_finished_at - frame.produced_at) * 1000,
            loop_latency_ms=loop_latency * 1000,
            capture_latency_ms=timings.capture_latency_s * 1000,
            detection_latency_ms=timings.detection_latency_s * 1000,
            track_latency_ms=timings.tracking_latency_s * 1000,
            decision_latency_ms=timings.decision_latency_s * 1000,
            render_latency_ms=0.0,
            fired_count=fired_count,
        )
