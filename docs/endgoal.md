# Vision Sprayer End Goal

## Product goal

Build a short-range, low-pressure, supervised spray system for a fixed indoor context, initially aimed at detecting a specific door-barking situation and triggering a brief corrective water spray.

The long-term device should run without a notebook:

```text
camera
  -> edge computer
  -> realtime vision model
  -> targeting decision
  -> ESP32 actuator controller
  -> servo / pump
  -> short water spray
```

## Runtime goal

The system should become a complete embodied AI loop:

```text
perception -> tracking -> decision -> physical action -> observation -> correction
```

The learning value is not only the final spray. The project exists to build practical intuition for:

- realtime camera pipelines
- model latency
- target tracking
- actuator timing
- hardware/software boundaries
- safety gates
- edge deployment
- observability

## Standalone deployment goal

The notebook should eventually be replaced by an always-on edge computer connected to wall power:

```text
wall power
  -> edge computer runs camera + model + Python pipeline
  -> ESP32 handles electrical IO
  -> separate power rail drives servo/pump
```

The ESP32 should not own perception. It should receive simple action commands and translate them into electrical signals.

## Safety constraints

Before water is introduced, the system must work with dry actuator tests.

Required safety boundaries:

- manual arming switch before any spray is possible
- emergency stop
- short maximum spray duration
- cooldown between sprays
- low-pressure output only
- no aiming at face, eyes, or ears
- first tests must use bottles or inanimate targets
- human supervision during animal-facing use

The system should be treated as a training aid, not an autonomous punishment machine.

## Current milestone ladder

1. Camera + model detects a target and moves an on-screen aim point.
2. Fake actuator emits observable action events.
3. Serial actuator translates action intent into a testable microcontroller command.
4. ESP32 receives command and moves a servo, no water.
5. Servo motion is calibrated against camera coordinates.
6. Pump trigger is added with timeout, cooldown, and manual arming.
7. Notebook is replaced by an edge computer.
8. Device becomes a wall-powered standalone prototype.
