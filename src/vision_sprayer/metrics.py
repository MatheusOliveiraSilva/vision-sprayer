from __future__ import annotations

from collections import deque

from .domain import Frame, RuntimeSample


class MetricsCollector:
    def __init__(self, window_size: int = 60) -> None:
        self._loop_durations: deque[float] = deque(maxlen=window_size)

    def record(
        self,
        frame: Frame,
        now: float,
        loop_started_at: float,
        detection_started_at: float,
        detection_finished_at: float,
        fired_count: int,
    ) -> RuntimeSample:
        loop_latency = now - loop_started_at
        self._loop_durations.append(loop_latency)

        avg_loop = sum(self._loop_durations) / len(self._loop_durations)
        fps = 1.0 / avg_loop if avg_loop > 0 else 0.0

        return RuntimeSample(
            fps=fps,
            frame_age_ms=(now - frame.produced_at) * 1000,
            loop_latency_ms=loop_latency * 1000,
            detection_latency_ms=(detection_finished_at - detection_started_at) * 1000,
            fired_count=fired_count,
        )

