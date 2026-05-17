import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import ParamSpec
from typing import TypeVar


P = ParamSpec("P")
T = TypeVar("T")


@dataclass
class StepTimings:
    loop_started_at: float = field(default_factory=time.perf_counter)
    loop_finished_at: float = 0.0
    capture_latency_s: float = 0.0
    detection_latency_s: float = 0.0
    tracking_latency_s: float = 0.0
    decision_latency_s: float = 0.0

    def measure_capture(self, action: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
        return self._measure("capture_latency_s", action, *args, **kwargs)

    def measure_detection(self, action: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
        return self._measure("detection_latency_s", action, *args, **kwargs)

    def measure_tracking(self, action: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
        return self._measure("tracking_latency_s", action, *args, **kwargs)

    def measure_decision(self, action: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
        return self._measure("decision_latency_s", action, *args, **kwargs)

    def finish_loop(self) -> None:
        self.loop_finished_at = time.perf_counter()

    def _measure(self, field_name: str, action: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
        started_at = time.perf_counter()
        result = action(*args, **kwargs)
        finished_at = time.perf_counter()
        setattr(self, field_name, finished_at - started_at)
        return result
