from vision_sprayer.adapters.actuator.fake_actuator import FakeActuator
from vision_sprayer.adapters.simulation.simulated_detector import SimulatedDetector
from vision_sprayer.adapters.simulation.simulated_frame_source import SimulatedFrameSource
from vision_sprayer.domain.models import Point
from vision_sprayer.observability.metrics import MetricsCollector
from vision_sprayer.pipeline.orchestrator import VisionPipeline
from vision_sprayer.targeting.targeting_policy import TargetingPolicy
from vision_sprayer.tracking.target_tracker import TargetTracker


def create_sim_pipeline(width: int = 960, height: int = 540) -> VisionPipeline:
    return VisionPipeline(
        frame_source=SimulatedFrameSource(width=width, height=height),
        detector=SimulatedDetector(),
        tracker=TargetTracker(),
        targeting=TargetingPolicy(initial_aim=Point(width / 2, height / 2)),
        actuator=FakeActuator(),
        metrics=MetricsCollector(),
    )


def create_camera_pipeline(
    source: int,
    model_name: str,
    target_class_name: str,
    confidence_threshold: float,
    device: str | None,
    width: int | None = None,
    height: int | None = None,
) -> VisionPipeline:
    # Local imports isolate OpenCV/Ultralytics native runtimes from sim-only commands.
    from vision_sprayer.adapters.camera.opencv_camera_source import OpenCVCameraSource
    from vision_sprayer.adapters.detection.yolo_detector import YoloBottleDetector

    initial_width = width if width is not None else 960
    initial_height = height if height is not None else 540
    return VisionPipeline(
        frame_source=OpenCVCameraSource(source=source, width=width, height=height),
        detector=YoloBottleDetector(
            model_name=model_name,
            target_class_name=target_class_name,
            confidence_threshold=confidence_threshold,
            device=device,
        ),
        tracker=TargetTracker(),
        targeting=TargetingPolicy(initial_aim=Point(initial_width / 2, initial_height / 2)),
        actuator=FakeActuator(),
        metrics=MetricsCollector(),
    )
