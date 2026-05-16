from dataclasses import dataclass
from math import hypot
from typing import Any
from typing import Self


@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def distance_to(self, other: Self) -> float:
        return hypot(self.x - other.x, self.y - other.y)

    def move_toward(self, target: Self, max_distance: float) -> Self:
        distance = self.distance_to(target)
        if distance == 0 or distance <= max_distance:
            return target

        ratio = max_distance / distance
        return Point(
            x=self.x + (target.x - self.x) * ratio,
            y=self.y + (target.y - self.y) * ratio,
        )


@dataclass(frozen=True)
class Rect:
    center: Point
    width: float
    height: float

    @property
    def left(self) -> float:
        return self.center.x - self.width / 2

    @property
    def top(self) -> float:
        return self.center.y - self.height / 2


@dataclass(frozen=True)
class Frame:
    sequence: int
    produced_at: float
    width: int
    height: int
    target: Rect | None = None
    image_bgr: Any | None = None


@dataclass(frozen=True)
class Detection:
    frame_sequence: int
    observed_at: float
    bbox: Rect
    confidence: float


@dataclass(frozen=True)
class TrackState:
    target_center: Point
    confidence: float
    updated_at: float
    age_frames: int


@dataclass(frozen=True)
class AimCommand:
    aim_point: Point
    fire: bool
    distance_to_target: float
    reason: str


@dataclass(frozen=True)
class ActuatorEvent:
    fired: bool
    fired_at: float
    aim_point: Point


@dataclass(frozen=True)
class RuntimeSample:
    fps: float
    frame_age_ms: float
    loop_latency_ms: float
    detection_latency_ms: float
    capture_latency_ms: float
    fired_count: int


@dataclass(frozen=True)
class RuntimeSnapshot:
    frame: Frame
    detection: Detection | None
    track: TrackState | None
    command: AimCommand
    actuator_event: ActuatorEvent
    metrics: RuntimeSample
