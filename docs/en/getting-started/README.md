# Start Here: Understanding and Reproducing Microduck from Public Sources

**English** | [简体中文](../../zh-CN/getting-started/README.md)

> This page is the easiest entry point into OpenMicroDuck. It uses only public, attributable information.

Microduck looks complicated because several different subjects are mixed together: mechanics, servos, electronics, Linux, simulation, reinforcement learning, cameras, sensors, and onboard software.

The easiest way to understand it is **not** to study everything at once.

## The whole project in one picture

```text
                    Microduck
                        │
          ┌─────────────┼─────────────┐
          │             │             │
       Hardware      Simulation     Software
          │             │             │
   structure/servos   MuJoCo       robotd/Linux
   IMU/power/sensors  RL/BAM       ONNX/policies
          │             │             │
          └─────────────┼─────────────┘
                        │
                 real robot motion
```

For a public reproduction or reverse-engineering study, the safest order is:

```text
1. Make the official simulated robot move
2. Understand the robot model and joint tree
3. Reproduce one official training task
4. Understand the control bus and sensor dataflow
5. Build small hardware test benches
6. Only then attempt a complete physical research build
```

This order matters because simulation lets a researcher verify the robot model, policy interface, joint order, actuator assumptions, and control rate **before** mechanical or electrical uncertainty is added.

## Choose what you want to do

### “I only want to see Microduck move in simulation”

Start with:

- [Simulation First: the shortest path to a moving Microduck](simulation-first.md)

No robot hardware is required. The official repositories already publish both the MuJoCo models and deployable ONNX policies.

### “I want to understand all important hardware parameters”

Read:

- [Hardware parameter reference](../hardware/parameter-reference.md)
- [Structure and assembly map](../hardware/structure-and-assembly-map.md)
- [Public hardware inventory / BOM status](../hardware/public-bom.md)

These pages distinguish three things that must not be mixed:

1. official product specifications;
2. values visible in official source/simulation assets;
3. community-derived assembly conclusions.

### “I want to make a public research reproduction”

Read:

- [Public reproduction roadmap](public-reproduction-roadmap.md)

It breaks the work into independently testable stages rather than treating “build a Microduck” as one giant task.

### “I want to train or modify the walking policy”

Read:

- [Reproducible training and ONNX export](../simulation/reproducible-training-and-export.md)
- [Sim-to-real parameter reference](../simulation/sim-to-real-parameter-reference.md)
- [Policy catalog and runtime switching](../simulation/policy-catalog-and-switching.md)

### “I want to understand the real control system”

Read:

- [Control loop and sensor dataflow](../software/control-loop-and-sensor-dataflow.md)
- [Onboard runtime architecture](../software/runtime-architecture.md)

The key fact is simple: the locomotion controller is a **50 Hz loop**. On each cycle the runtime reads servo and IMU state, builds the policy observation, evaluates an ONNX policy, processes its 14 actions, and sends new targets to the servos.

## Four numbers to remember first

A beginner can understand much of the architecture by remembering only these:

| Number | Meaning |
|---:|---|
| **15** | physical motor IDs in the current runtime, including the mouth/beak motor |
| **14** | joints controlled by the locomotion RL policies; the mouth is separate |
| **61** | actor observation width shared by the current policy family |
| **50 Hz** | policy/runtime control-loop frequency |

Everything else becomes easier once these four numbers are clear.

## What is known well, and what is still incomplete?

### Relatively well documented publicly

- official MuJoCo kinematic/dynamic models;
- 14 policy-controlled joints and their ordering;
- 15 runtime Dynamixel IDs;
- home pose;
- control-loop rate and serial-bus behavior;
- `imu_to_dxl` data format and LSM6DSV16X processing;
- official RL tasks, domain randomization and BAM actuator model;
- ONNX policy interface and export path;
- many public simulation meshes and assembly transforms.

### Still incomplete as production-hardware information

- complete production electronics schematic and PCB BOM;
- exact final production XL330 sub-variant;
- complete production fastener list and exact screw lengths;
- production wiring harness lengths and connector details;
- exact final camera/lens/FOV and final ToF part if upstream still changes;
- complete manufacturing tolerances, materials, inserts and assembly procedures.

See [Open questions and source conflicts](../research/open-questions-and-conflicts.md) before treating any uncertain value as final.

## Evidence labels used throughout OpenMicroDuck

| Label | Meaning |
|---|---|
| **Official product spec** | stated by Pollen Robotics as a product-level specification |
| **Official source** | directly visible in official source code/docs/models |
| **Official simulation model** | a parameter or geometry from the released simulation assets; not automatically a production measurement |
| **Community reconstruction** | derived by a public third-party project from public evidence |
| **Measured** | reproducible real-hardware measurement with conditions recorded |
| **Unresolved** | not enough public evidence yet |

## A useful rule for reverse engineering

Do not ask only:

> “What part does Microduck use?”

Ask four separate questions:

```text
What does the official product promise?
What does the current official source implementation use?
What does the official simulation model assume?
What has the community inferred but not officially confirmed?
```

Keeping those four answers separate is the difference between a useful public research project and a misleading pseudo-BOM.

## Upstream snapshot used by this documentation sweep

- `pollen-robotics/microduck` main: `590b986bd8c0d50ae02cb3ea2f59c463b6828168`
- `pollen-robotics/microduck_rl` develop: `d424a0c899f6b33cbd3daeb279913134349c0b63`
- `Rhoban/bam` main: `620a64fe67c1afe94fca81da73b128c7aed17c5f`

See [Upstream version matrix](../upstream/version-matrix.md) for why these commits matter.
