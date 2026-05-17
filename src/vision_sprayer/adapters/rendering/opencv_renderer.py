import cv2

from vision_sprayer.domain.models import RuntimeSnapshot


class OpenCVRenderer:
    def __init__(self, window_name: str) -> None:
        self.window_name = window_name

    def render(self, snapshot: RuntimeSnapshot, display: bool = True) -> None:
        if snapshot.frame.image_bgr is None:
            raise ValueError("OpenCVRenderer requires Frame.image_bgr")

        image = snapshot.frame.image_bgr.copy()
        target = snapshot.detection.bbox if snapshot.detection is not None else None
        if target is not None:
            cv2.rectangle(
                image,
                (int(target.left), int(target.top)),
                (int(target.left + target.width), int(target.top + target.height)),
                (80, 220, 130),
                2,
            )

        if snapshot.track is not None:
            track = snapshot.track.target_center
            cv2.circle(image, (int(track.x), int(track.y)), 7, (255, 90, 60), -1)

        aim = snapshot.command.aim_point
        cv2.drawMarker(
            image,
            (int(aim.x), int(aim.y)),
            (40, 240, 240),
            markerType=cv2.MARKER_CROSS,
            markerSize=34,
            thickness=2,
        )

        if snapshot.actuator_event.fired and target is not None:
            cv2.line(
                image,
                (int(aim.x), int(aim.y)),
                (int(target.center.x), int(target.center.y)),
                (255, 160, 60),
                6,
            )

        self._draw_metrics(image=image, snapshot=snapshot)
        if display:
            cv2.imshow(self.window_name, image)

    def _draw_metrics(self, image, snapshot: RuntimeSnapshot) -> None:
        metrics = snapshot.metrics
        lines = [
            f"FPS {metrics.fps:5.1f}",
            f"frame age {metrics.frame_age_ms:5.1f} ms",
            f"capture {metrics.capture_latency_ms:5.1f} ms",
            f"detect {metrics.detection_latency_ms:5.1f} ms",
            f"track {metrics.track_latency_ms:5.1f} ms",
            f"decision {metrics.decision_latency_ms:5.1f} ms",
            f"render {metrics.render_latency_ms:5.1f} ms",
            f"loop {metrics.loop_latency_ms:5.1f} ms",
            f"distance {snapshot.command.distance_to_target:5.1f} px",
            f"lock {snapshot.track.lock_state if snapshot.track is not None else 'no_target'}",
            f"conf {snapshot.detection.confidence if snapshot.detection is not None else 0.0:4.2f}",
            f"policy {snapshot.command.reason}",
            f"fires {metrics.fired_count}",
        ]
        for index, line in enumerate(lines):
            cv2.putText(
                image,
                line,
                (18, 28 + index * 24),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.62,
                (235, 235, 235),
                2,
                cv2.LINE_AA,
            )
