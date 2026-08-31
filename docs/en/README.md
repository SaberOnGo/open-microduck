# OpenMicroDuck Documentation — English

**English** | [简体中文](../zh-CN/README.md)

This is the English documentation tree for OpenMicroDuck. It collects public, attributable information about Microduck and the surrounding open-source/community ecosystem.

If you are new to the project, a good reading order is: **official specifications → control/dataflow → policy catalog → simulation/RL → detailed hardware pages**.

## Product baseline

- [Official Microduck specifications](product/official-specifications.md)

## Hardware

- [Public hardware inventory and BOM status](hardware/public-bom.md)
- [Public component datasheet and documentation index](hardware/component-datasheets.md)
- [Community-derived BOM, fasteners, bearings, and assembly reconstruction](hardware/community-bom-reconstruction.md)
- [Mechanical structure and kinematics](hardware/mechanical-structure.md)
- [Electronics, buses, sensors, and power](hardware/electronics-and-buses.md)

## Software and control

- [Onboard runtime architecture](software/runtime-architecture.md)
- [Control loop and sensor dataflow](software/control-loop-and-sensor-dataflow.md)

## Simulation and reinforcement learning

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

## Documentation policy

1. English and Simplified Chinese are maintained as parallel first-class documentation trees.
2. Pages in this English tree should link to English pages by default; language switching belongs at the top of the page or section.
3. Prefer official product documentation and official source code over secondary reporting.
4. Label third-party reconstructions as community-derived rather than official specifications.
5. Record conflicts between sources instead of silently choosing a convenient value.
6. Version-sensitive implementation details should record an upstream commit when practical.
7. Do not publish confidential, leaked, private, unrelated proprietary, or otherwise non-public engineering information.

Last source sweep: **2026-08-31**.
