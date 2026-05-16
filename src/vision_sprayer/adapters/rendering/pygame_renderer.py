import numpy as np

from vision_sprayer.domain.models import RuntimeSnapshot


class PygameRenderer:
    def __init__(self, screen, pygame_module) -> None:
        self.screen = screen
        self.pygame = pygame_module
        self.font = pygame_module.font.SysFont("Menlo", 18)

    def render(self, snapshot: RuntimeSnapshot) -> None:
        pg = self.pygame
        self._draw_frame(snapshot)

        target = snapshot.detection.bbox if snapshot.detection is not None else snapshot.frame.target
        if target is not None:
            target_rect = pg.Rect(target.left, target.top, target.width, target.height)
            pg.draw.rect(self.screen, (45, 170, 120), target_rect, width=3, border_radius=10)

        aim = snapshot.command.aim_point
        pg.draw.circle(self.screen, (240, 235, 90), (int(aim.x), int(aim.y)), 24, width=2)
        pg.draw.line(self.screen, (240, 235, 90), (aim.x - 34, aim.y), (aim.x + 34, aim.y), 2)
        pg.draw.line(self.screen, (240, 235, 90), (aim.x, aim.y - 34), (aim.x, aim.y + 34), 2)

        if snapshot.actuator_event.fired and target is not None:
            pg.draw.line(
                self.screen,
                (80, 170, 255),
                (int(aim.x), int(aim.y)),
                (int(target.center.x), int(target.center.y)),
                8,
            )

        self._draw_metrics(snapshot)

    def _draw_frame(self, snapshot: RuntimeSnapshot) -> None:
        if snapshot.frame.image_bgr is None:
            self.screen.fill((15, 18, 22))
            if snapshot.frame.target is not None:
                target = snapshot.frame.target
                target_rect = self.pygame.Rect(target.left, target.top, target.width, target.height)
                self.pygame.draw.rect(self.screen, (45, 170, 120), target_rect, border_radius=10)
                self.pygame.draw.rect(self.screen, (210, 240, 225), target_rect, width=2, border_radius=10)
            return

        image_rgb = snapshot.frame.image_bgr[:, :, ::-1]
        image_rgb = np.rot90(image_rgb)
        surface = self.pygame.surfarray.make_surface(image_rgb)
        surface = self.pygame.transform.scale(surface, self.screen.get_size())
        self.screen.blit(surface, (0, 0))

    def _draw_metrics(self, snapshot: RuntimeSnapshot) -> None:
        metrics = snapshot.metrics
        lines = [
            f"FPS {metrics.fps:5.1f}",
            f"frame age {metrics.frame_age_ms:5.1f} ms",
            f"capture {metrics.capture_latency_ms:5.1f} ms",
            f"loop {metrics.loop_latency_ms:5.1f} ms",
            f"detect {metrics.detection_latency_ms:5.1f} ms",
            f"distance {snapshot.command.distance_to_target:5.1f} px",
            f"state {snapshot.command.reason}",
            f"fires {metrics.fired_count}",
        ]

        for index, line in enumerate(lines):
            surface = self.font.render(line, True, (225, 230, 235))
            self.screen.blit(surface, (18, 16 + index * 24))
