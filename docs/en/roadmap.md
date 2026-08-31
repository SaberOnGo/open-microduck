# OpenMicroDuck Public Documentation Roadmap

**English** | [简体中文](../zh-CN/roadmap.md)

This roadmap tracks the **public research and documentation project**. It is not a product-development plan and does not describe private hardware programs.

## Current priorities

1. Keep a clear official product-specification baseline separate from development-source details and community reconstruction.
2. Maintain the public Microduck hardware inventory without mislabeling it as an official complete BOM.
3. Keep the control-loop/dataflow documentation aligned with the official runtime as `robotd`, sensor services, and deployment behavior evolve.
4. Track the official policy/task catalog and explain policy switching in a way that is understandable without reading the RL source first.
5. Keep the reproducible training → export → ONNX → validation path synchronized with `microduck_rl`.
6. Track MJCF/model variants, asset provenance, and license boundaries.
7. Maintain an explicit list of unresolved questions instead of filling gaps with assumptions.
8. Record upstream commit SHAs for version-sensitive research.
9. Add reproducible public measurements from production hardware when they become available.
10. Keep English and Simplified Chinese documentation aligned topic-by-topic, with full Chinese explanations rather than abbreviated summaries.

## Documentation areas

### Product and evidence

- official product specifications;
- source/evidence hierarchy;
- upstream version baseline;
- unresolved questions and source conflicts.

### Hardware

- public hardware inventory and BOM status;
- manufacturer datasheet/documentation index;
- mechanical structure and kinematics;
- electronics, buses, sensors, audio, power;
- community-derived fastener/bearing/assembly reconstruction.

### Software and control

- onboard runtime architecture;
- control loop and sensor dataflow;
- transport/service boundaries;
- future public runtime topics such as update/recovery and media/remote-control paths when they become useful as standalone guides.

### Simulation and reinforcement learning

- RL overview and sim-to-real concepts;
- policy/task catalog and runtime switching;
- reproducible training and ONNX export;
- MJCF/model asset reference;
- actuator modeling, backlash, and domain randomization.

### Ecosystem and provenance

- reverse-engineering/community project index;
- source and license tracking;
- reproducible public measurements and validation methods.

## Completed in the 2026-08-31 documentation expansion

The current documentation set now includes paired English / Simplified Chinese pages for:

- official specifications;
- policy catalog and switching;
- control loop and sensor dataflow;
- reproducible training and ONNX export;
- upstream version matrix;
- open questions/source conflicts;
- component datasheet index;
- simulation model assets reference.

## Contribution principle

New entries should be publicly attributable and suitable for an open repository. Private, confidential, leaked, unrelated proprietary, or otherwise non-public engineering information is outside the scope of OpenMicroDuck.

When a value cannot be proven from a public source, label it as unresolved rather than guessing.

See the [research guidelines](research-guidelines.md), [sources and evidence map](sources.md), and [open questions](research/open-questions-and-conflicts.md).
