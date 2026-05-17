from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeConfig:
    camera_source: int = 0
    model_name: str = "yolo11n.pt"
    target_class_name: str = "bottle"
    confidence_threshold: float = 0.25
    device: str | None = "cpu"
    camera_width: int | None = None
    camera_height: int | None = None
    smoke_frames: int = 0
    display_window: bool = True
    list_camera_sources: bool = False
    camera_scan_count: int = 1


CONFIG = RuntimeConfig()

