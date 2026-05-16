from typing import Protocol

from vision_sprayer.domain.models import ActuatorEvent, AimCommand


class Actuator(Protocol):
    fired_count: int

    def apply(self, command: AimCommand, now: float) -> ActuatorEvent:
        pass

