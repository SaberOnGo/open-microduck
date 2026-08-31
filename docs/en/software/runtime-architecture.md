# How the Microduck Software Fits Together

**English** | [简体中文](../../zh-CN/software/runtime-architecture.md)

> Scope: public information from the official `pollen-robotics/microduck` repository. This page explains the system first and names implementation details second.

## The whole software system in one picture

Microduck does not use one giant AI model for everything. The software is split into layers:

```text
Camera ──► vision AI ──────────────┐
                                   │
ToF ────► distance / obstacle code ├──► high-level behavior
                                   │      “walk there”
Sound / BLE / other inputs ────────┘      “look left”
                                          “kick”
                                              │
                                              ▼
                                     locomotion RL policy
                                      body state + command
                                              │
                                              ▼
                                     14 joint targets
                                              │
                                              ▼
                                   safety / limits / filters
                                              │
                                              ▼
                                          15 motors
```

The important separation is:

- **Perception** finds things around the robot.
- **High-level behavior** decides what the robot should try to do.
- **Locomotion AI** decides how the body should move to follow that command.
- **Safety and motor code** turn the result into physical servo commands.

## Which parts use AI?

| Part | Main method in the current public stack |
|---|---|
| Camera object detection | AI model (`duck_detect.onnx` / `duck_detect.rknn`) |
| ToF depth processing | Normal geometry and filtering code |
| High-level autonomous behavior | Mainly state-machine / rule logic in the older runtime; not yet fully ported to the new daemon architecture |
| Walking, standing and movement skills | Reinforcement-learning policies exported to ONNX |
| Safety, limits, bus I/O, updates, networking | Normal software |

So “AI robot” does not mean every sensor is fed directly into one neural network.

## What are the strangely named programs?

The official software is mostly Rust. It runs several small background programs on Linux. A background program that stays running is often called a **daemon**.

The names are easier to remember by their jobs:

| Code name | Plain-language job |
|---|---|
| `robotd` | **Body controller.** Runs the 50 Hz movement loop, movement policies and safety logic. |
| `mediad` | **Camera and remote video.** Captures camera frames, runs the current vision detector and streams video. |
| `tofd` | **Depth sensor.** Reads the 8×8 ToF sensor and publishes depth frames. |
| `padd` | **Gamepad reader.** Turns stick/button input into robot commands. |
| `btd` | **Bluetooth bridge.** Carries supported commands over Bluetooth. |
| `configd` | **Settings.** Handles Wi-Fi, identity and system configuration. |
| `updaterd` | **Software updater.** Installs signed releases and can roll back a bad update. |
| `robotctl` | **Developer/operator tool.** A command-line way to inspect and control the robot. |

The split is useful because one failure does not need to stop everything. For example, a camera problem should not kill the motor-control loop.

## How movement works

The low-level movement loop runs at **50 Hz**, once every **20 ms**:

```text
read joints + IMU
       ↓
build 61-number observation
       ↓
run selected ONNX movement policy
       ↓
14 actions
       ↓
scale / filter / safety / limits
       ↓
write new servo targets
       ↓
repeat
```

There are **15 physical motor IDs** in the current runtime. The locomotion policy controls **14 joints**; the mouth/beak motor is handled separately.

The 61-number movement input is mainly the robot's own body state plus a command. Camera images and the raw 8×8 ToF frame are **not** part of this standard 61-D locomotion input.

See [Control loop and sensor dataflow](control-loop-and-sensor-dataflow.md) for the exact 61-D layout.

## Where Camera and ToF fit

### Camera

The current public path is roughly:

```text
camera
  ↓
mediad
  ├──► video / WebRTC
  └──► duck-detect
          ↓
      detected object positions
```

The detector can use the RK3566 NPU through an RKNN model or use the CPU with an ONNX model.

### ToF

The current public path is roughly:

```text
8×8 ToF
   ↓
 tofd
   ↓
64 distance values
   ↓
kinematics + geometry code
   ↓
floor / empty space / obstacle points
```

This processing is ordinary geometry/filtering code rather than a neural network.

## What decides the robot's behavior?

This is the layer between perception and the movement policies:

```text
“I see something ahead”
        ↓
behavior logic
        ↓
“turn left and walk slowly”
        ↓
locomotion policy
```

The older Microduck runtime had an autonomous behavior system built mainly as a state machine with rules, mood/energy state, exploration memory, ToF avoidance and behaviors such as wandering, looking around, playing and sleeping.

The official new daemon-based software has not yet fully ported that complete autonomous brain. The current official roadmap lists it as a remaining major area of work. This is a **software migration gap**, not evidence that Camera or ToF support is closed-source.

## How the programs talk to each other

Most local control/status traffic uses **JSON-RPC over Unix sockets**. In simple terms:

> one background program sends a small structured message to another background program on the same Linux computer.

This lets the gamepad, Bluetooth path, command-line tools and other clients reuse the same robot commands instead of each inventing a separate motor-control protocol.

## Why this architecture is useful for reproduction

A compatible research build does not need to rewrite every layer at once. The public software already separates useful boundaries:

```text
sensor input
   ↓
perception
   ↓
behavior command
   ↓
movement policy
   ↓
motor interface
```

If hardware changes, the hardware-facing layer can change while the higher-level logic stays similar. If behavior requirements change, the behavior layer can change without retraining every walking policy.

## Primary public sources

- https://github.com/pollen-robotics/microduck
- https://github.com/pollen-robotics/microduck/blob/main/docs/design/architecture.md
- https://github.com/pollen-robotics/microduck/blob/main/docs/project/roadmap.md
- https://github.com/pollen-robotics/microduck/tree/main/mediad
- https://github.com/pollen-robotics/microduck/tree/main/tof
- https://github.com/pollen-robotics/microduck/tree/main/duck-detect
- https://github.com/pollen-robotics/microduck/tree/main/kinematics
- https://github.com/pollen-robotics/microduck_rl
