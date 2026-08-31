# OpenMicroDuck Documentation — English

**English** | [简体中文](../zh-CN/README.md)

OpenMicroDuck is a public, source-driven technical reference for understanding Microduck, reproducing its public simulation stack, and studying its hardware/software architecture without turning guesses into “official specifications.”

## Start here

If this is your first visit, do **not** begin by reading every hardware page. Use the path that matches your goal:

| Goal | Read this first |
|---|---|
| Understand the whole project in a few minutes | [Start Here](getting-started/README.md) |
| See Microduck move before buying hardware | [Simulation First](getting-started/simulation-first.md) |
| Plan a public research reproduction step by step | [Public Reproduction Roadmap](getting-started/public-reproduction-roadmap.md) |
| Look up concrete hardware/control parameters | [Hardware Parameter Reference](hardware/parameter-reference.md) |
| Understand how the parts fit together | [Structure and Assembly Map](hardware/structure-and-assembly-map.md) |
| Look up sim-to-real/randomization values | [Sim-to-Real Parameter Reference](simulation/sim-to-real-parameter-reference.md) |

A useful beginner sequence is:

```text
Start Here
   ↓
Simulation First
   ↓
Hardware Parameter Reference
   ↓
Structure and Assembly Map
   ↓
Sim-to-Real Parameter Reference
   ↓
Detailed software / RL / provenance pages
```

## Product baseline

- [Official Microduck specifications](product/official-specifications.md)

## Hardware

### Best entry pages

- [Hardware parameter reference](hardware/parameter-reference.md) — motor IDs, home pose, joint limits, masses, bus timing, IMU format, battery, HAT/I2C/audio and evidence levels.
- [Structure and assembly map](hardware/structure-and-assembly-map.md) — the robot as understandable modules instead of a pile of STL names.

### Detailed references

- [Public hardware inventory and BOM status](hardware/public-bom.md)
- [Public component datasheet and documentation index](hardware/component-datasheets.md)
- [Community-derived BOM, fasteners, bearings, and assembly reconstruction](hardware/community-bom-reconstruction.md)
- [Mechanical structure and kinematics](hardware/mechanical-structure.md)
- [Electronics, buses, sensors, and power](hardware/electronics-and-buses.md)

## Software and control

- [Control loop and sensor dataflow](software/control-loop-and-sensor-dataflow.md) — the easiest way to understand the 50 Hz servo/IMU → observation → ONNX → action path.
- [Onboard runtime architecture](software/runtime-architecture.md) — `robotd`, services, Linux daemon boundaries and deployment structure.

## Simulation and reinforcement learning

### Start with these

- [Simulation First](getting-started/simulation-first.md)
- [Sim-to-real parameter reference](simulation/sim-to-real-parameter-reference.md)

### Deeper references

- [Simulation and reinforcement learning overview](simulation/model-and-rl.md)
- [Policy catalog and runtime switching](simulation/policy-catalog-and-switching.md)
- [Reproducible training and ONNX export](simulation/reproducible-training-and-export.md)
- [Simulation model assets reference](simulation/model-assets-reference.md)

## Research status and reproducibility

- [Open questions and source conflicts](research/open-questions-and-conflicts.md)
- [Upstream version matrix](upstream/version-matrix.md)
- [Sources and evidence map](sources.md)
- [Research guidelines](research-guidelines.md)
- [Provenance and licensing](legal/provenance-and-licenses.md)

## Ecosystem and project docs

- [Public documentation roadmap](roadmap.md)
- [Reviewed reverse-engineering and community projects](ecosystem/reverse-engineering-projects.md)
- [Broader GitHub repository discovery snapshot](ecosystem/discovered-repositories.md)

## Evidence labels

OpenMicroDuck deliberately separates:

- **Official product spec** — product/press/store statements from Pollen Robotics;
- **Official source** — values directly visible in official source code or design documents;
- **Official simulation model** — geometry/dynamics from released simulation assets, not automatically a production measurement;
- **Community reconstruction** — third-party conclusions derived from public evidence;
- **Measured** — reproducible real-hardware measurement with test conditions;
- **Unresolved / provisional** — not established well enough to present as final fact.

This separation is especially important for BOM, fasteners, PCB details, model filenames and simulation parameters.

## Documentation policy

1. English and Simplified Chinese are maintained as parallel first-class documentation trees.
2. Pages in this English tree should link to English pages by default; language switching belongs at the top of a page.
3. Prefer official product documentation and official source code over secondary reporting.
4. Label third-party reconstructions as community-derived rather than official specifications.
5. Record conflicts between sources instead of silently choosing a convenient value.
6. Version-sensitive implementation details should record an upstream commit when practical.
7. Keep explanations readable: introduce the system first, then show detailed parameters and source paths.
8. Do not publish confidential, leaked, private, unrelated proprietary, or otherwise non-public engineering information.

Last source sweep: **2026-08-31**.
