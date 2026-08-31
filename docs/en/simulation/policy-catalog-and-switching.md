# Policy Catalog and Runtime Switching

**English** | [简体中文](../../zh-CN/simulation/policy-catalog-and-switching.md)

> Primary source: official `pollen-robotics/microduck_rl` and `pollen-robotics/microduck` repositories.

Microduck does not rely on one giant neural network for every visible behavior. The public RL stack contains **multiple policy/task families**, while the runtime gives them a shared interface so it can switch between them without changing the whole robot software stack.

That design is easier to understand as:

```text
high-level command / selected skill
               │
               ▼
        policy selection
               │
    ┌──────────┼───────────┐
    ▼          ▼           ▼
  walking   stand-up    sit/stand ...
   ONNX       ONNX         ONNX
    └──────────┼───────────┘
               ▼
       shared 61-D input
       shared 14-D output
               │
               ▼
          robotd @ 50 Hz
```

## Why several policies can share one runtime

The official RL project keeps a common actor interface across the current policy family:

```text
actor observation: 61 values
policy action:      14 values
control rate:       50 Hz
```

The observation is:

```text
48 proprioception
+ 13 command values
= 61 total
```

The 13 command values are arranged as:

- twist command: 3;
- head pose command: 4;
- body pose command: 6.

A task that does not need one of those command fields normally keeps the same interface and zero-pads the unused part. This avoids changing the neural-network input size for every skill.

## Current public task families

The live upstream registry is the authoritative source, because task names can evolve. At the 2026-08-31 source snapshot, the official RL README lists these important families:

| Task family | Plain-language purpose |
|---|---|
| `Velocity` | Main walking policy with velocity and head-pose commands |
| `VelStand` | Walking plus fall recovery inside one policy |
| `StandUp` | Get up from several lying/sitting poses, then hold standing |
| `SitStand` | Controlled sit ↔ stand motion |
| `GroundPick` | Lower the body, touch/reach the ground with the beak, return to stand |
| `BallKick` | Kick a small ball forward |
| `Roulade` | Forward roll and return to the feet |
| `Velocity ... Rollers` | Velocity tracking while using passive roller attachments |
| `Swizzle` | Symmetric roller-skating motion |
| `RollerCrouch` | Crouch while gliding |
| `RollerSlope` | Glide down a slope on rollers |
| `RollerStandUp` | Stand up while using roller attachments |
| `Spin` | Fast in-place spin on rollers |

Flat/Rough variants exist for several families, and the upstream project also registers backlash variants.

## Does each skill require loading a new firmware image?

No.

The runtime can **hot-swap policies** behind the same 61-input / 14-output interface. In other words, switching from one locomotion skill to another is closer to selecting a different controller model than replacing the entire onboard software.

The official `scripts/infer_policy.py` can rehearse this pattern in simulation by loading multiple exported ONNX files at once, for example walking, standing, sit/stand, and roulade policies.

## One policy can still contain more than one behavior

“Multiple policies” does not mean every tiny motion must have its own network.

For example:

- `VelStand` combines walking and fall recovery in one policy;
- `SitStand` handles both directions of the sit/stand transition;
- `StandUp` can recover from more than one initial body pose.

So the design is a mix:

- some related behaviors are trained together inside one policy;
- larger or very different behaviors may use separate policies;
- the runtime keeps the interface stable so they can coexist.

## The 15th motor: the beak

Microduck has **15 motors**, but the locomotion policy action vector has **14 values**.

The 14 RL-controlled joints cover the two legs plus neck/head joints. The articulated mouth/beak motor is handled separately by the runtime rather than being part of the 14-action locomotion policy output.

That distinction is why “15 motors” and “14 policy actions” are both correct.

## Backlash policy variants

The official RL project provides Backlash variants for the main tasks. These variants insert a passive hinge that represents gear play in series with each of the 14 controlled servo joints.

The important design point is that the **network interface remains 61 observations / 14 actions**. The mechanical model becomes more realistic, but the deployed policy contract does not need to change.

## What higher-level AI would do

The public low-level policies answer questions such as:

- how should the joints move to walk forward?
- how should the robot stand up from the floor?
- how should it execute a roll or sit-down motion?

A higher-level application or agent can instead answer:

- which skill should run now?
- what velocity or pose command should be sent?
- when should the robot stop one skill and start another?

This separation is common in robotics because high-level reasoning and fast, stable motor control have very different timing and safety requirements.

## Primary sources

- https://github.com/pollen-robotics/microduck_rl/blob/develop/README.md
- https://github.com/pollen-robotics/microduck_rl/tree/develop/src/mjlab_microduck/tasks
- https://github.com/pollen-robotics/microduck_rl/blob/develop/scripts/infer_policy.py
- https://github.com/pollen-robotics/microduck

## Related pages

- [Simulation and reinforcement learning](model-and-rl.md)
- [Control loop and sensor dataflow](../software/control-loop-and-sensor-dataflow.md)
- [Model assets reference](model-assets-reference.md)
