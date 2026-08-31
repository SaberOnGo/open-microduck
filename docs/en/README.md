# OpenMicroDuck Documentation — English

**English** | [简体中文](../zh-CN/README.md)

OpenMicroDuck is organized for two kinds of readers:

1. people who want to understand Microduck quickly;
2. people who need detailed parameters and source-backed reverse-engineering notes.

## First-time reader

Read these in order:

1. [Start Here](getting-started/README.md) — the whole robot in plain language.
2. [How the Microduck Software Fits Together](software/runtime-architecture.md) — sensing, behavior, movement AI and motors.
3. [Simulation First](getting-started/simulation-first.md) — run the virtual robot before touching hardware.
4. [Public Reproduction Roadmap](getting-started/public-reproduction-roadmap.md) — staged research path.

## Hardware

- [Hardware Parameter Reference](hardware/parameter-reference.md) — motor IDs, home pose, joint ranges, masses, IMU, bus, battery.
- [Structure and Assembly Map](hardware/structure-and-assembly-map.md) — how the robot is physically divided and assembled.
- [Public Hardware / BOM Status](hardware/public-bom.md) — what is known and what is still unknown.
- [Electronics, Buses, Sensors, and Power](hardware/electronics-and-buses.md) — wiring and interfaces visible from public sources.
- [Community BOM Reconstruction](hardware/community-bom-reconstruction.md) — clearly labeled third-party reconstruction.
- [Component Datasheet Index](hardware/component-datasheets.md)
- [Mechanical Structure and Kinematics](hardware/mechanical-structure.md)

## Software and control

- [How the Microduck Software Fits Together](software/runtime-architecture.md) — **best software entry page**.
- [Control Loop: How the Robot Moves](software/control-loop-and-sensor-dataflow.md) — 50 Hz movement loop and the 61-D policy input.

## Simulation and learning

- [Simulation First](getting-started/simulation-first.md)
- [Simulation and Reinforcement Learning](simulation/model-and-rl.md)
- [Policy Catalog and Runtime Switching](simulation/policy-catalog-and-switching.md)
- [Reproducible Training and ONNX Export](simulation/reproducible-training-and-export.md)
- [Simulation Model Assets Reference](simulation/model-assets-reference.md)
- [Sim-to-Real Parameter Reference](simulation/sim-to-real-parameter-reference.md)

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

Last source sweep: **2026-08-31**.
