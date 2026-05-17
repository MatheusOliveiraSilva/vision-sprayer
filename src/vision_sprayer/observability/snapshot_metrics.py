from vision_sprayer.domain.models import RuntimeSample, RuntimeSnapshot


def with_render_latency(snapshot: RuntimeSnapshot, render_latency_ms: float) -> RuntimeSnapshot:
    return RuntimeSnapshot(
        frame=snapshot.frame,
        detection=snapshot.detection,
        track=snapshot.track,
        command=snapshot.command,
        actuator_event=snapshot.actuator_event,
        metrics=RuntimeSample(
            fps=snapshot.metrics.fps,
            frame_age_ms=snapshot.metrics.frame_age_ms,
            loop_latency_ms=snapshot.metrics.loop_latency_ms,
            detection_latency_ms=snapshot.metrics.detection_latency_ms,
            capture_latency_ms=snapshot.metrics.capture_latency_ms,
            track_latency_ms=snapshot.metrics.track_latency_ms,
            decision_latency_ms=snapshot.metrics.decision_latency_ms,
            render_latency_ms=render_latency_ms,
            fired_count=snapshot.metrics.fired_count,
        ),
    )
