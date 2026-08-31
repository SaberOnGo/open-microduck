# Control Loop: How the Robot Moves

**English** | [简体中文](../../zh-CN/software/control-loop-and-sensor-dataflow.md)

> This page explains the low-level movement loop in plain language. It is based on the public Microduck runtime and RL repositories.

## The whole loop

Microduck updates its movement **50 times per second**:

```text
read joints + IMU
       ↓
build 61 input values
       ↓
run the selected movement AI
       ↓
get 14 joint actions
       ↓
apply scale / filter / safety / limits
       ↓
send new targets to the servos
       ↓
repeat after 20 ms
```

That is the core low-level control path.

## Why 15 motors but only 14 AI actions?

The current runtime has **15 physical motor IDs**.

The locomotion policies control **14 joints**. The mouth/beak motor is controlled separately, so it is not part of the 14-action policy output.

## What are the 61 input values?

They are mostly information about the robot's own body:

| Input group | Count | Plain meaning |
|---|---:|---|
| Body angular velocity | 3 | how the body is rotating |
| Gravity direction | 3 | which way the body is tilted |
| Joint positions | 14 | where the joints are |
| Joint velocities | 14 | how fast the joints are moving |
| Previous actions | 14 | what the policy commanded last time |
| Movement command | 13 | requested walking, head and body pose |
| **Total** | **61** | |

The 13 command values are:

```text
walk / turn command    3
head target            4
body-pose target       6
```

## Camera and ToF are not in these 61 values

This is an important architectural boundary.

The standard locomotion policy does **not** directly receive:

- camera images;
- raw 8×8 ToF depth frames.

Instead:

```text
Camera / ToF
     ↓
perception and behavior logic
     ↓
movement command
     ↓
61-D locomotion policy
```

So the movement AI focuses on **how to move the body**, while other software decides **where or why to move**.

## What happens after the AI model?

The neural network does not write directly to motors.

The runtime still applies ordinary control code such as:

- action scaling;
- optional low-pass filtering;
- joint travel limits;
- servo gains;
- fall / limp / recovery handling;
- deadman/watchdog behavior;
- bus-error handling.

A useful way to think about the deployed controller is:

```text
movement policy
+ runtime control rules
+ safety
+ real hardware
```

The ONNX file alone is not the complete controller.

## Motor and IMU data path

The current public development path uses a Dynamixel-compatible serial bus:

```text
15 servos + IMU bridge ID 200
            │
            ▼
        1 Mbps UART
            │
            ▼
          robotd
```

The main control IMU and servo state are read through the same control path, helping the runtime use joint and body-orientation data from closely aligned samples.

For exact IDs, register details and sensor formats, see [Hardware Parameter Reference](../hardware/parameter-reference.md) and [Electronics, Buses, Sensors, and Power](../hardware/electronics-and-buses.md).

## Why previous actions are included

The policy sees its previous 14 outputs. This gives it a short memory of what it just asked the body to do without needing a camera stream or a separate recurrent network.

## The main idea to remember

```text
High-level software says: “move this way.”
Locomotion AI says:       “move the joints like this.”
Safety/runtime says:      “only commands that are safe and valid reach the motors.”
```

## Primary public sources

- https://github.com/pollen-robotics/microduck
- https://github.com/pollen-robotics/microduck/blob/main/docs/design/robotd-design.md
- https://github.com/pollen-robotics/microduck/blob/main/deploy/robotd.toml
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/obs.rs
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/model.rs
- https://github.com/pollen-robotics/microduck_rl

## Related pages

- [How the Microduck software fits together](runtime-architecture.md)
- [Policy catalog and runtime switching](../simulation/policy-catalog-and-switching.md)
- [Sim-to-real parameter reference](../simulation/sim-to-real-parameter-reference.md)
