from __future__ import annotations

from math import sin

from .domain import Frame, Point, Rect


class SimulatedFrameSource:
    """Produces timestamped frames from a small deterministic world simulation."""

    def __init__(self, width: int = 960, height: int = 540) -> None:
        self.width = width
        self.height = height
        self._sequence = 0

    def next_frame(self, now: float) -> Frame:
        self._sequence += 1

        # The target moves continuously while the rest of the system is computing.
        x = self.width * 0.5 + sin(now * 0.9) * self.width * 0.32
        y = self.height * 0.5 + sin(now * 1.4) * self.height * 0.18

        return Frame(
            sequence=self._sequence,
            produced_at=now,
            width=self.width,
            height=self.height,
            target=Rect(center=Point(x, y), width=56, height=120),
        )

