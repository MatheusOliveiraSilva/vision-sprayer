# Vision Sprayer

Realtime perception -> decision -> fake actuation loop.

The first goal is to see the runtime loop alive and keep the core behavior testable.

## Architecture

```text
src/vision_sprayer/
  main.py          default camera scenario entrypoint
  config.py        runtime settings
  scenarios/       camera and simulation composition
  runners/         visual loop runners
  domain/          value objects shared by the pipeline
  adapters/        camera, model, simulation, rendering, actuator
  pipeline/        orchestration and frame lifecycle
  tracking/        target state across frames
  targeting/       aim/fire decision logic
  observability/   FPS and latency metrics
```

Runtime flow:

```text
SimulatedFrameSource -> SimulatedDetector -> TargetTracker
  -> TargetingPolicy -> FakeActuator -> MetricsCollector -> PygameRenderer

OpenCVCameraSource -> YoloBottleDetector -> TargetTracker
  -> TargetingPolicy -> FakeActuator -> MetricsCollector -> OpenCVRenderer
```

The visual overlay separates three different runtime states:

```text
raw detection box  -> where the model thinks the target is now
tracker point      -> smoothed target state across frames
aim crosshair      -> where the actuator can currently point
```

Tracker lifecycle:

```text
NO_TARGET -> ACQUIRING -> LOCKED -> LOST
```

## Responsibility boundaries

- `FrameSource`: owns simulated world state and produces timestamped frames.
- `Detector`: converts a frame into target observations.
- `Tracker`: owns smoothed target state across frames.
- `TargetingPolicy`: pure decision logic for aim movement and fire intent.
- `Actuator`: receives commands; V0 uses a fake actuator.
- `MetricsCollector`: records loop timing and observable runtime signals.
- `Renderer`: draws state and metrics; no decision logic belongs here.
- `Orchestrator`: wires components and owns the frame lifecycle.

## How to read the codebase

Start with the runtime path, not implementation details:

```text
main.py
  -> runs the configured camera scenario

config.py
  -> contains runtime settings

scenarios/camera.py
  -> wires camera/model/rendering adapters

scenarios/simulation.py
  -> wires simulation adapters for tests/smoke

pipeline/orchestrator.py
  -> describes one frame lifecycle:
     capture frame
     detect target
     update track
     decide action
     apply action
     collect metrics
     build snapshot

targeting/targeting_policy.py
  -> explains when the aim moves and when fire is allowed

tracking/target_tracker.py
  -> explains target lock lifecycle across frames
```

Adapters are implementation edges. Read them after the pipeline is clear.

## Setup

```bash
uv sync --extra dev --no-editable
```

## Simulation

```bash
PYTHONPATH=src SDL_VIDEODRIVER=dummy uv run python - <<'PY'
from vision_sprayer.scenarios.simulation import SimulationScenario

SimulationScenario(smoke_frames=5).run()
PY
```

## Camera Sources

```bash
PYTHONPATH=src uv run python - <<'PY'
from vision_sprayer.config import RuntimeConfig
from vision_sprayer.scenarios.camera import CameraScenario

CameraScenario(RuntimeConfig(list_camera_sources=True)).run()
PY
```

On macOS with iPhone, connect the iPhone with USB, trust the Mac if prompted, and select/enable Continuity Camera if macOS asks. The camera source is usually `0`, but confirm with the camera-source listing snippet above.

## Camera + YOLO Bottle Detection

```bash
PYTHONPATH=src uv run python -m vision_sprayer
```

Edit `src/vision_sprayer/config.py` to change:

```python
camera_source = 0
model_name = "yolo11n.pt"
target_class_name = "bottle"
confidence_threshold = 0.25
device = "cpu"
```

The overlay shows capture, detection, tracking, decision, render, and loop latency.

## Test

```bash
uv run pytest
```

## Smoke

```bash
PYTHONPATH=src SDL_VIDEODRIVER=dummy uv run python - <<'PY'
from vision_sprayer.scenarios.simulation import SimulationScenario

SimulationScenario(smoke_frames=5).run()
PY

PYTHONPATH=src uv run python - <<'PY'
from vision_sprayer.config import RuntimeConfig
from vision_sprayer.scenarios.camera import CameraScenario

CameraScenario(RuntimeConfig(smoke_frames=1, display_window=False)).run()
PY
```
