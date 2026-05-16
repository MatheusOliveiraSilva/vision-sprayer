from __future__ import annotations

from .domain import ActuatorEvent, AimCommand


class FakeActuator:
    """Fake physical boundary for V0.

    Later this is where a SerialActuator can send commands to ESP32 firmware.
    """

    def __init__(self) -> None:
        self.fired_count = 0
        self.last_event: ActuatorEvent | None = None

    def apply(self, command: AimCommand, now: float) -> ActuatorEvent:
        if command.fire:
            self.fired_count += 1

        event = ActuatorEvent(
            fired=command.fire,
            fired_at=now if command.fire else 0.0,
            aim_point=command.aim_point,
        )
        self.last_event = event
        return event

