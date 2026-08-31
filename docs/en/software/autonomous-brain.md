# Autonomous Brain and High-Level Behavior

**English** | [简体中文](../../zh-CN/software/autonomous-brain.md)

> Scope: public information from the official Microduck repositories. The current daemon architecture has not yet fully ported the earlier autonomous brain, so this page separates **confirmed current code** from **documented legacy behavior**.

## The whole idea in one picture

Microduck does not use one giant AI model for everything.

```text
Camera ──> visual detection ──┐
ToF ─────> obstacle geometry ─┼─> high-level behavior logic
Audio/BLE/other events ───────┘          │
                                         ▼
                              choose an intention
                              walk / turn / look / kick / rest
                                         │
                                         ▼
                              locomotion / skill policy
                                         │
                                         ▼
                                    joint targets
```

The **high-level behavior logic** answers questions such as:

- should the robot wander or stay still?
- should it turn away from an obstacle?
- should it look toward something it detected?
- should it enter a ball-play, dance, nap, or reaction behavior?

It does **not** directly calculate every servo angle. The locomotion and skill policies do that lower-level job.

## Is the Autonomous Brain another AI model?

Based on the public design notes, the earlier autonomous brain is primarily **ordinary program logic**: a state machine, timers, memory and rules.

The official current roadmap describes the earlier runtime as roughly:

```text
energy / mood
     │
     ▼
choose one behavior state
     │
     ├─ Chill
     ├─ LookAround
     ├─ Wander
     ├─ TurnInPlace
     ├─ Zoomies
     ├─ Startle
     ├─ Stretch
     ├─ Ruffle
     ├─ Preen
     ├─ Sneeze
     ├─ Dance
     ├─ GroundPick
     ├─ Nap
     ├─ BallPlay
     ├─ Petted
     └─ Held
```

That is a very different role from `duck_detect.onnx` or the walking ONNX policy:

| Layer | Main job | AI model? |
|---|---|---|
| Camera detector | find a visual target in an image | yes, ONNX/RKNN |
| ToF processing | turn 8×8 ranges into usable geometry | no, normal geometry/rules |
| Autonomous Brain | decide what the robot should do next | mainly normal state-machine/rule logic in the documented earlier design |
| Locomotion policy | turn body state + command into 14 joint actions | yes, RL policy |

## What inputs does the brain use?

Public official design notes describe inputs such as:

- ToF obstacle information;
- ambient sound / voice events;
- camera detections;
- petting / held-type events;
- nearby Microduck presence through BLE;
- motion state and other robot state;
- internal energy/mood state;
- short-term exploration memory.

Not every input has to be used by every behavior.

## What does the brain output?

The output is best understood as **intent**, not raw motor commands.

Examples:

```text
move forward slowly
turn left
look toward this direction
stop
start kick-left skill
start dance behavior
sit / rest
```

Those intentions are then handled by `robotd` and the appropriate locomotion or skill policy.

## Current status in the new Rust daemon architecture

The current official `microduck` repository already contains many pieces that the autonomous brain needs:

- `mediad` and `duck-detect` for camera perception;
- `tofd` for the 8×8 ToF stream;
- `kinematics` for converting sensor/joint geometry into robot-frame geometry;
- `odometry` for position estimation;
- audio, BLE/social and other event sources;
- `robotd` intents and skills.

However, the official roadmap still lists **M9 — The autonomous brain** as an unfinished major migration. The documented earlier `autonomous.rs` behavior set is therefore useful as a public architecture reference, but it should not be presented as already fully present in the current daemon code.

## What is reusable for third-party research?

The architecture is highly reusable:

```text
sensor results
    ↓
behavior state machine
    ↓
intent API
    ↓
movement / skill policies
```

A compatible research robot can keep the same structure and only change behaviors when its goals differ. The main adaptation points are normally:

1. which perception events exist;
2. how those events are represented;
3. which behaviors are available;
4. which movement/skill commands the lower layer accepts.

There is usually no reason to rebuild the whole concept from zero just because a motor, camera, or compute board changes.

## Primary public sources

- https://github.com/pollen-robotics/microduck/blob/main/docs/ideas/autonomous_behavior.md
- https://github.com/pollen-robotics/microduck/blob/main/docs/project/roadmap.md
- https://github.com/pollen-robotics/microduck/blob/main/docs/design/architecture.md
- https://github.com/pollen-robotics/microduck

See also:

- [Onboard runtime architecture](runtime-architecture.md)
- [Control loop and sensor dataflow](control-loop-and-sensor-dataflow.md)
- [Policy catalog and switching](../simulation/policy-catalog-and-switching.md)
