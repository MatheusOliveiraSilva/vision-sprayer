# Pet Bottle Sprayer Sim

V0 simulation for a perception -> decision -> fake actuation loop.

The first goal is not visual realism. The first goal is to see the runtime loop alive and keep the core behavior testable.

## Architecture

```text
SimulatedFrameSource
  -> SimulatedDetector
  -> TargetTracker
  -> TargetingPolicy
  -> FakeActuator
  -> MetricsCollector
  -> PygameRenderer
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

## Run

```bash
uv sync --extra dev --no-editable
source .venv/bin/activate
PYTHONPATH=src python -m sprayer_sim.app
```

Or without activating the environment:

```bash
PYTHONPATH=src uv run python -m sprayer_sim.app
```

## Test

```bash
uv run pytest
```

## Smoke

```bash
PYTHONPATH=src SDL_VIDEODRIVER=dummy uv run python -m sprayer_sim.app --smoke-frames 5
```

## Troubleshooting

If `python -m sprayer_sim.app` says `No module named 'sprayer_sim'`, run it with the source path:

```bash
PYTHONPATH=src python -m sprayer_sim.app
```
