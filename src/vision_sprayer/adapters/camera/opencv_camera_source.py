import cv2

from vision_sprayer.domain.models import Frame


class OpenCVCameraSource:
    """Reads frames from a webcam-like device exposed to OpenCV."""

    def __init__(self, source: int = 0, width: int | None = None, height: int | None = None) -> None:
        self.source = source
        self._sequence = 0
        self._capture = cv2.VideoCapture(source)
        if width is not None:
            self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        if height is not None:
            self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        if not self._capture.isOpened():
            raise RuntimeError(f"Could not open camera source {source}")

    def next_frame(self, now: float) -> Frame:
        ok, image_bgr = self._capture.read()
        if not ok or image_bgr is None:
            raise RuntimeError(f"Could not read frame from camera source {self.source}")

        self._sequence += 1
        height, width = image_bgr.shape[:2]
        return Frame(
            sequence=self._sequence,
            produced_at=now,
            width=width,
            height=height,
            image_bgr=image_bgr,
        )

    def release(self) -> None:
        self._capture.release()


def list_camera_sources(max_sources: int = 8) -> list[int]:
    available_sources = []
    for source in range(max_sources):
        capture = cv2.VideoCapture(source)
        if capture.isOpened():
            available_sources.append(source)
        capture.release()
    return available_sources

