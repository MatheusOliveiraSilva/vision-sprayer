from vision_sprayer.adapters.actuator.serial_actuator import SerialActuator
from vision_sprayer.adapters.actuator.serial_actuator import ServoAimMapper
from vision_sprayer.adapters.actuator.serial_actuator import ServoCalibration
from vision_sprayer.domain.models import AimCommand
from vision_sprayer.domain.models import Point


class RecordingTransport:
    def __init__(self) -> None:
        self.lines: list[str] = []

    def write_line(self, line: str) -> None:
        self.lines.append(line)


def test_serial_actuator_maps_center_point_to_center_servo_angles() -> None:
    transport = RecordingTransport()
    actuator = SerialActuator(
        transport=transport,
        mapper=ServoAimMapper(ServoCalibration(frame_width=100, frame_height=100)),
    )

    event = actuator.apply(
        command=AimCommand(
            aim_point=Point(50, 50),
            fire=False,
            distance_to_target=0,
            reason="tracking",
        ),
        now=1.0,
    )

    assert transport.lines == ["AIM pan=90.00 tilt=90.00 fire=0"]
    assert event.fired is False
    assert actuator.fired_count == 0


def test_serial_actuator_clamps_point_to_servo_limits_and_counts_fire() -> None:
    transport = RecordingTransport()
    actuator = SerialActuator(
        transport=transport,
        mapper=ServoAimMapper(ServoCalibration(frame_width=100, frame_height=100)),
    )

    event = actuator.apply(
        command=AimCommand(
            aim_point=Point(200, -50),
            fire=True,
            distance_to_target=0,
            reason="aligned",
        ),
        now=2.0,
    )

    assert transport.lines == ["AIM pan=150.00 tilt=60.00 fire=1"]
    assert event.fired is True
    assert event.fired_at == 2.0
    assert actuator.fired_count == 1
