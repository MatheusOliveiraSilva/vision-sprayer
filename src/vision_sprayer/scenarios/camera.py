from vision_sprayer.adapters.camera.opencv_camera_source import OpenCVCameraSource
from vision_sprayer.adapters.camera.opencv_camera_source import list_camera_sources
from vision_sprayer.adapters.detection.yolo_detector import YoloBottleDetector
from vision_sprayer.config import RuntimeConfig
from vision_sprayer.pipeline.orchestrator import VisionPipeline
from vision_sprayer.runners.opencv_runner import run_opencv_pipeline
from vision_sprayer.scenarios.components import build_fake_actuator
from vision_sprayer.scenarios.components import build_metrics_collector
from vision_sprayer.scenarios.components import build_targeting_policy
from vision_sprayer.scenarios.components import build_tracker


class CameraScenario:
    def __init__(self, config: RuntimeConfig) -> None:
        self.config = config

    def run(self) -> None:
        if self.config.list_camera_sources:
            sources = list_camera_sources(max_sources=self.config.camera_scan_count)
            print("Available camera sources:", ", ".join(str(source) for source in sources) or "none")
            return

        pipeline = self.build_pipeline()
        run_opencv_pipeline(
            pipeline=pipeline,
            title="Vision Sprayer camera",
            smoke_frames=self.config.smoke_frames,
            display=self.config.display_window,
        )

    def build_pipeline(self) -> VisionPipeline:
        initial_width = self.config.camera_width if self.config.camera_width is not None else 960
        initial_height = self.config.camera_height if self.config.camera_height is not None else 540
        return VisionPipeline(
            frame_source=OpenCVCameraSource(
                source=self.config.camera_source,
                width=self.config.camera_width,
                height=self.config.camera_height,
            ),
            detector=YoloBottleDetector(
                model_name=self.config.model_name,
                target_class_name=self.config.target_class_name,
                confidence_threshold=self.config.confidence_threshold,
                device=self.config.device,
            ),
            tracker=build_tracker(),
            targeting=build_targeting_policy(initial_width=initial_width, initial_height=initial_height),
            actuator=build_fake_actuator(),
            metrics=build_metrics_collector(),
        )
