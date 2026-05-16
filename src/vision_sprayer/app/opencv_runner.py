import time

import cv2

from vision_sprayer.adapters.rendering.opencv_renderer import OpenCVRenderer
from vision_sprayer.pipeline.orchestrator import VisionPipeline


def run_opencv_pipeline(
    pipeline: VisionPipeline,
    title: str,
    smoke_frames: int = 0,
    display: bool = True,
) -> None:
    renderer = OpenCVRenderer(window_name=title)
    previous = time.perf_counter()
    rendered_frames = 0
    running = True

    while running:
        now = time.perf_counter()
        dt = now - previous
        previous = now

        snapshot = pipeline.tick(now=now, dt=dt)
        renderer.render(snapshot=snapshot, display=display)
        rendered_frames += 1
        if smoke_frames and rendered_frames >= smoke_frames:
            running = False
        if display and cv2.waitKey(1) == ord("q"):
            running = False

    cv2.destroyAllWindows()

