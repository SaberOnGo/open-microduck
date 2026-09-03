# OpenMicroDuck Documentation — English

**English** | [简体中文](../zh-CN/README.md)

OpenMicroDuck is organized for two kinds of readers:

1. people who want to understand Microduck quickly;
2. people who need detailed parameters and source-backed reverse-engineering notes.

## First-time reader

Read these in order:

1. [Official browser Sandbox](https://huggingface.co/spaces/pollen-robotics/microduck-simulator) — play for a minute without installing software.
2. [Choose Your Path](getting-started/choose-your-path.md) — pick an entry by goal, computer, GPU, and cost.
3. [Beginner Glossary](getting-started/glossary.md) — separate running, training, and sim-to-real.
4. [Start Here](getting-started/README.md) — understand the whole robot.
5. [Simulation First](getting-started/simulation-first.md) — run an existing ONNX policy locally.
6. [Beginner Troubleshooting](getting-started/troubleshooting.md) — diagnose by symptom and layer.

Owners of an official Microduck should start at the [Official Robot Owner Guide](getting-started/official-robot-owner.md). Research-replica builders should continue to the [Public Reproduction Roadmap](getting-started/public-reproduction-roadmap.md) and [Hardware Bring-up and Calibration](getting-started/hardware-bringup-and-calibration.md).

## Hardware

- [Hardware Parameter Reference](hardware/parameter-reference.md) — motor IDs, home pose, joint ranges, masses, IMU, bus, battery.
- [Structure and Assembly Map](hardware/structure-and-assembly-map.md) — how the robot is physically divided and assembled.
- [Public Hardware / BOM Status](hardware/public-bom.md) — what is known and what is still unknown.
- [Electronics, Buses, Sensors, and Power](hardware/electronics-and-buses.md) — wiring and interfaces visible from public sources.
- [Community BOM Reconstruction](hardware/community-bom-reconstruction.md) — clearly labeled third-party reconstruction.
- [Component Datasheet Index](hardware/component-datasheets.md)
- [Mechanical Structure and Kinematics](hardware/mechanical-structure.md)

## Software and control

- [Official Robot Owner Guide](getting-started/official-robot-owner.md) — first boot, gamepad, health checks, updates, and safety boundaries.
- [How the Microduck Software Fits Together](software/runtime-architecture.md) — **best software entry page**.
- [Control Loop: How the Robot Moves](software/control-loop-and-sensor-dataflow.md) — 50 Hz movement loop and the 61-D policy input.
- [Autonomous Brain and High-Level Behavior](software/autonomous-brain.md) — how perception becomes “walk / turn / look / rest” decisions.
- [Kinematics and Odometry](software/kinematics-and-odometry.md) — how the robot computes feet/head/sensor positions and estimates movement.
- [`robotd` Hardware Protocol](software/robotd-hardware-protocol.md) — bus IDs, timing, reads/writes, startup registers and IMU block.

## Simulation and learning

- [Choose Your Path: Computer, GPU, and Cost](getting-started/choose-your-path.md)
- [Beginner Glossary](getting-started/glossary.md)
- [Beginner Troubleshooting](getting-started/troubleshooting.md)
- [Simulation First](getting-started/simulation-first.md)
- [Simulation and Reinforcement Learning](simulation/model-and-rl.md)
- [Hardware Variant Simulation](simulation/hardware-variant-simulation.md) — **beginner guide to keeping the Microduck software contract while changing actuator, mass, inertia, geometry, friction, and related physical parameters in MuJoCo.**
- [Behavior, Task, and Reward Design](simulation/behavior-task-and-reward-design.md) — **start here when creating a new action**.
- [Policy Catalog and Runtime Switching](simulation/policy-catalog-and-switching.md)
- [Reproducible Training and ONNX Export](simulation/reproducible-training-and-export.md)
- [Simulation Model Assets Reference](simulation/model-assets-reference.md)
- [Sim-to-Real Parameter Reference](simulation/sim-to-real-parameter-reference.md)

## Tools

- [Upstream Parameter Diff Tool](../../tools/upstream-diff/README.md) — extract selected public source parameters into JSON and compare upstream revisions.

## Sources, uncertainty and community research

- [Official Specification Baseline](product/official-specifications.md)
- [Open Questions and Source Conflicts](research/open-questions-and-conflicts.md)
- [Upstream Version Matrix](upstream/version-matrix.md)
- [Sources and Evidence Map](sources.md)
- [Reverse-Engineering and Community Projects](ecosystem/reverse-engineering-projects.md)
- [Broader Repository Discovery](ecosystem/discovered-repositories.md)
- [Research Guidelines](research-guidelines.md)
- [Provenance and Licensing](legal/provenance-and-licenses.md)
- [Documentation Roadmap](roadmap.md)

## Reading rule used by this project

Every page should answer these questions before going deep into parameters:

```text
What is this part?
What does it do?
Where does it sit in the whole robot?
Which facts are confirmed, inferred or still unknown?
```

Detailed reference pages may still contain dense tables, but the first section should explain the subject without requiring specialist vocabulary.

Core official sources last checked: **2026-09-03**. The broader community-repository discovery snapshot remains **2026-08-31**.
