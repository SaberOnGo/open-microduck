# Control Loop and Sensor Dataflow

**English** | [简体中文](../../zh-CN/software/control-loop-and-sensor-dataflow.md)

> Primary source: official Microduck runtime and RL repositories.

This page explains, in plain language, how data moves through the low-level control system: from servos and IMU, into the policy, and back to motor commands.

The key idea is that the physical robot executes a **closed loop at 50 Hz**. Every 20 ms, the runtime reads state, builds the policy input, runs the neural network, processes the output, and sends new joint targets.

## The short version

```text
14 controlled servos + control IMU
              │
              ▼
       synchronized state read
              │
              ▼
   joint position / velocity
   body orientation / angular data
              │
              ▼
      observation builder
           61 values
              │
              ▼
          ONNX policy
          14 actions
              │
              ▼
 scale / filter / limits / safety
              │
              ▼
       servo target write
              │
              └────── repeats at 50 Hz
```

Microduck has 15 motors in total, but the articulated beak/mouth motor is outside the 14-action locomotion policy and is handled separately.

## What happens during one control tick

A simplified control tick is:

1. **Read the robot state.** The runtime obtains joint state and IMU-related data through the motor/control bus.
2. **Build the observation.** The runtime converts raw robot state into the 61-value interface expected by the policy.
3. **Run the ONNX network.** The selected policy produces 14 action values.
4. **Post-process the actions.** Runtime-side scaling, filters, limits, gains, safety logic, and other actuator-facing rules are applied.
5. **Write new joint targets.** Commands are sent back to the controlled servos.
6. **Repeat at 50 Hz.**

The neural network is therefore only one part of the controller. The deployed behavior is better described as:

```text
policy + observation construction + filters + actuator rules + safety + hardware
```

## Motor and IMU path

The current official runtime exposes a Dynamixel-style bus containing the servo devices and an `imu_to_dxl` device used for the control IMU.

Public source identifies:

- 15 motor IDs;
- `imu_to_dxl` device ID **200**;
- current development serial rate **1 Mbps**;
- the beak motor as separate from the 14-action locomotion vector.

Reading servo state and control-IMU data through the same control path helps keep joint and orientation data aligned in time.

## What is inside the 61-D observation

The official RL project defines the shared actor observation as:

```text
base angular velocity      3
projected gravity          3
joint position            14
joint velocity            14
previous actions          14
----------------------------
proprioception            48

twist command              3
head-pose command           4
body-pose command           6
----------------------------
command block              13

total                     61
```

This is primarily **proprioception**: information about the robot's own body and the command it is currently trying to follow.

## Does the walking policy directly use the camera or ToF image?

Based on the currently published 61-D actor contract, **the standard low-level locomotion policy does not take a camera image or 8×8 ToF frame as part of those 61 values**.

That does not mean the camera or ToF sensor is unimportant. They can serve other parts of the robot stack, such as perception, remote operation, application logic, object-related behavior, or future policies.

The important distinction is:

```text
low-level locomotion policy
    mainly body state + commands

camera / ToF services
    environmental perception for other software paths
```

Do not assume that every onboard sensor is automatically an input to every neural policy.

## Why “previous actions” are part of the input

The 61-D contract includes the previous 14 actions. This gives the policy information about what it commanded on the previous control step.

For a fast physical controller, this helps the network reason about short-term command history without needing an image stream or a long external history buffer.

## Runtime-side filtering matters

The official runtime includes actuator-facing processing such as action scaling, low-pass filtering for selected joints, position gains, joint travel handling, fall/limp/recovery state, watchdog behavior, and bus-error handling.

These details matter for sim-to-real because a policy trained with one action path can behave differently if deployment silently adds or removes filters.

A useful rule is: **the ONNX file alone is not the whole controller**.

## Where camera and ToF live in the software architecture

The official runtime separates major hardware responsibilities into services. In the current source tree:

- `mediad` handles the camera/media path;
- `tofd` owns the multi-zone ToF sensor;
- `robotd` owns the real-time robot control loop and policy execution.

This service separation avoids letting every application talk directly to low-level hardware.

## Timing and failures

A 50 Hz loop means the target period is about **20 ms**. The runtime also tracks whether the loop is actually achieving its expected rate and whether bus transactions are failing.

This matters because “Linux is still running” is not enough for a walking robot. A control daemon that is alive but missing motor deadlines can still be unsafe or unusable.

## Primary official sources

- https://github.com/pollen-robotics/microduck
- https://github.com/pollen-robotics/microduck/blob/main/docs/design/robotd-design.md
- https://github.com/pollen-robotics/microduck/blob/main/deploy/robotd.toml
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/model.rs
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/imu.rs
- https://github.com/pollen-robotics/microduck_rl/blob/develop/README.md

## Related pages

- [Onboard runtime architecture](runtime-architecture.md)
- [Policy catalog and switching](../simulation/policy-catalog-and-switching.md)
- [Simulation and reinforcement learning](../simulation/model-and-rl.md)
- [Electronics, buses, sensors, and power](../hardware/electronics-and-buses.md)
