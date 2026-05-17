from dataclasses import dataclass
from typing import Protocol

from vision_sprayer.domain.models import ActuatorEvent
from vision_sprayer.domain.models import AimCommand
from vision_sprayer.domain.models import Point


class LineTransport(Protocol):
    def write_line(self, line: str) -> None:
        pass


@dataclass(frozen=True)
class ServoCalibration:
    frame_width: int
    frame_height: int
    min_pan_degrees: float = 30.0
    max_pan_degrees: float = 150.0
    min_tilt_degrees: float = 60.0
    max_tilt_degrees: float = 120.0


@dataclass(frozen=True)
class ServoAngles:
    pan_degrees: float
    tilt_degrees: float


class ServoAimMapper:
    def __init__(self, calibration: ServoCalibration) -> None:
        self.calibration = calibration

    def map_point(self, point: Point) -> ServoAngles:
        return ServoAngles(
            pan_degrees=self.map_axis(
                value=point.x,
                source_max=self.calibration.frame_width,
                target_min=self.calibration.min_pan_degrees,
                target_max=self.calibration.max_pan_degrees,
            ),
            tilt_degrees=self.map_axis(
                value=point.y,
                source_max=self.calibration.frame_height,
                target_min=self.calibration.min_tilt_degrees,
                target_max=self.calibration.max_tilt_degrees,
            ),
        )

    def map_axis(self, value: float, source_max: float, target_min: float, target_max: float) -> float:
        normalized = self.clamp(value / source_max, minimum=0.0, maximum=1.0)
        return target_min + (target_max - target_min) * normalized

    def clamp(self, value: float, minimum: float, maximum: float) -> float:
        return max(minimum, min(maximum, value))


class SerialActuator:
    def __init__(self, transport: LineTransport, mapper: ServoAimMapper) -> None:
        self.transport = transport
        self.mapper = mapper
        self.fired_count = 0
        self.last_event: ActuatorEvent | None = None

    def apply(self, command: AimCommand, now: float) -> ActuatorEvent:
        angles = self.mapper.map_point(command.aim_point)
        self.transport.write_line(self.encode_command(command=command, angles=angles))

        if command.fire:
            self.fired_count += 1

        event = ActuatorEvent(
            fired=command.fire,
            fired_at=now if command.fire else 0.0,
            aim_point=command.aim_point,
        )
        self.last_event = event
        return event

    def encode_command(self, command: AimCommand, angles: ServoAngles) -> str:
        fire = 1 if command.fire else 0
        return f"AIM pan={angles.pan_degrees:.2f} tilt={angles.tilt_degrees:.2f} fire={fire}"
