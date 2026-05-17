# Vision Sprayer

Realtime perception -> decision -> fake actuation loop.

The first goal is to see the runtime loop alive and keep the core behavior testable.

## Architecture

```text
src/vision_sprayer/
  app/             CLI and runnable app entrypoints
  domain/          value objects shared by the pipeline
  adapters/        simulation, rendering, actuator, camera/model later
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

## Setup

```bash
uv sync --extra dev --no-editable
```

## Simulation

```bash
PYTHONPATH=src uv run python -m vision_sprayer.app sim
```

## Camera Sources

```bash
PYTHONPATH=src uv run python -m vision_sprayer.app cameras
```

On macOS with iPhone, connect the iPhone with USB, trust the Mac if prompted, and select/enable Continuity Camera if macOS asks. The camera source is usually `0`, but confirm with the `cameras` command.

## Camera + YOLO Bottle Detection

```bash
PYTHONPATH=src uv run python -m vision_sprayer.app camera --source 0 --device cpu
```

Useful options:

```bash
--model yolo11n.pt
--target bottle
--confidence 0.25
--device cpu
--device mps
--no-window
```

The overlay shows capture, detection, tracking, decision, render, and loop latency.

## Test

```bash
uv run pytest
```

## Smoke

```bash
PYTHONPATH=src SDL_VIDEODRIVER=dummy uv run python -m vision_sprayer.app sim --smoke-frames 5
PYTHONPATH=src uv run python -m vision_sprayer.app camera --source 0 --device cpu --smoke-frames 1 --no-window
```
