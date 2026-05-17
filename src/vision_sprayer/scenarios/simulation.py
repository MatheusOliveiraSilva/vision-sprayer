from vision_sprayer.adapters.simulation.simulated_detector import SimulatedDetector
from vision_sprayer.adapters.simulation.simulated_frame_source import SimulatedFrameSource
from vision_sprayer.pipeline.orchestrator import VisionPipeline
from vision_sprayer.runners.pygame_runner import run_pygame_pipeline
from vision_sprayer.scenarios.components import build_fake_actuator
from vision_sprayer.scenarios.components import build_metrics_collector
from vision_sprayer.scenarios.components import build_targeting_policy
from vision_sprayer.scenarios.components import build_tracker


class SimulationScenario:
    def __init__(self, width: int = 960, height: int = 540, smoke_frames: int = 0) -> None:
        self.width = width
        self.height = height
        self.smoke_frames = smoke_frames

    def run(self) -> None:
        pipeline = self.build_pipeline()
        run_pygame_pipeline(
            pipeline=pipeline,
            title="Vision Sprayer sim",
            smoke_frames=self.smoke_frames,
        )

    def build_pipeline(self) -> VisionPipeline:
        return VisionPipeline(
            frame_source=SimulatedFrameSource(width=self.width, height=self.height),
            detector=SimulatedDetector(),
            tracker=build_tracker(),
            targeting=build_targeting_policy(initial_width=self.width, initial_height=self.height),
            actuator=build_fake_actuator(),
            metrics=build_metrics_collector(),
        )
