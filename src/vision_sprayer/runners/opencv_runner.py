import time

import cv2

from vision_sprayer.adapters.rendering.opencv_renderer import OpenCVRenderer
from vision_sprayer.observability.snapshot_metrics import with_render_latency
from vision_sprayer.pipeline.orchestrator import VisionPipeline


def run_opencv_pipeline(
    pipeline: VisionPipeline,
    title: str,
    smoke_frames: int = 0,
    display: bool = True,
) -> None:
    renderer = OpenCVRenderer(window_name=title)
    previous = time.perf_counter()
    previous_render_latency_ms = 0.0
    rendered_frames = 0
    running = True

    while running:
        now = time.perf_counter()
        dt = now - previous
        previous = now

        snapshot = with_render_latency(
            snapshot=pipeline.tick(now=now, dt=dt),
            render_latency_ms=previous_render_latency_ms,
        )
        render_started_at = time.perf_counter()
        renderer.render(snapshot=snapshot, display=display)
        render_finished_at = time.perf_counter()
        previous_render_latency_ms = (render_finished_at - render_started_at) * 1000
        rendered_frames += 1
        if smoke_frames and rendered_frames >= smoke_frames:
            running = False
        if display and cv2.waitKey(1) == ord("q"):
            running = False

    cv2.destroyAllWindows()
