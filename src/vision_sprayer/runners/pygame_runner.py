import time

import pygame

from vision_sprayer.observability.snapshot_metrics import with_render_latency
from vision_sprayer.adapters.rendering.pygame_renderer import PygameRenderer
from vision_sprayer.pipeline.orchestrator import VisionPipeline


def run_pygame_pipeline(pipeline: VisionPipeline, title: str, smoke_frames: int = 0) -> None:
    pygame.init()
    screen = pygame.display.set_mode((960, 540))
    pygame.display.set_caption(title)
    clock = pygame.time.Clock()

    renderer = PygameRenderer(screen, pygame)
    previous = time.perf_counter()
    previous_render_latency_ms = 0.0
    running = True
    rendered_frames = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        now = time.perf_counter()
        dt = now - previous
        previous = now

        snapshot = with_render_latency(
            snapshot=pipeline.tick(now=now, dt=dt),
            render_latency_ms=previous_render_latency_ms,
        )
        render_started_at = time.perf_counter()
        renderer.render(snapshot)
        render_finished_at = time.perf_counter()
        previous_render_latency_ms = (render_finished_at - render_started_at) * 1000
        pygame.display.flip()
        rendered_frames += 1
        if smoke_frames and rendered_frames >= smoke_frames:
            running = False
        clock.tick(60)

    pygame.quit()
