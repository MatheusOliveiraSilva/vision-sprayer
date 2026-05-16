from __future__ import annotations

import argparse
import time

from .orchestrator import SprayerOrchestrator
from .renderer import PygameRenderer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the pet bottle sprayer V0 simulation.")
    parser.add_argument(
        "--smoke-frames",
        type=int,
        default=0,
        help="Exit after rendering this many frames. Useful for automated smoke checks.",
    )
    return parser.parse_args()


def main() -> None:
    import pygame

    args = parse_args()
    pygame.init()
    width, height = 960, 540
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pet Bottle Sprayer Sim V0")
    clock = pygame.time.Clock()

    orchestrator = SprayerOrchestrator.default(width=width, height=height)
    renderer = PygameRenderer(screen, pygame)
    previous = time.perf_counter()
    running = True
    rendered_frames = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        now = time.perf_counter()
        dt = now - previous
        previous = now

        snapshot = orchestrator.tick(now=now, dt=dt)
        renderer.render(snapshot)
        pygame.display.flip()
        rendered_frames += 1
        if args.smoke_frames and rendered_frames >= args.smoke_frames:
            running = False
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
