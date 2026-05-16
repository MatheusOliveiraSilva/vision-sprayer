from ultralytics import YOLO

from vision_sprayer.domain.models import Detection, Frame, Point, Rect


class YoloBottleDetector:
    """YOLO adapter that emits the highest-confidence bottle detection."""

    def __init__(
        self,
        model_name: str = "yolo11n.pt",
        target_class_name: str = "bottle",
        confidence_threshold: float = 0.25,
        device: str | None = None,
    ) -> None:
        self.model = YOLO(model_name)
        self.target_class_name = target_class_name
        self.confidence_threshold = confidence_threshold
        self.device = device

    def detect(self, frame: Frame, now: float) -> Detection | None:
        if frame.image_bgr is None:
            raise ValueError("YoloBottleDetector requires Frame.image_bgr")

        results = self.model.predict(
            source=frame.image_bgr,
            verbose=False,
            device=self.device,
        )
        result = results[0]
        best_detection = None

        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = self.model.names[class_id]
            confidence = float(box.conf[0])
            if class_name != self.target_class_name:
                continue
            if confidence < self.confidence_threshold:
                continue

            x1, y1, x2, y2 = [float(value) for value in box.xyxy[0]]
            detection = Detection(
                frame_sequence=frame.sequence,
                observed_at=now,
                bbox=Rect(
                    center=Point(x=(x1 + x2) / 2, y=(y1 + y2) / 2),
                    width=x2 - x1,
                    height=y2 - y1,
                ),
                confidence=confidence,
            )
            if best_detection is None or detection.confidence > best_detection.confidence:
                best_detection = detection

        return best_detection

