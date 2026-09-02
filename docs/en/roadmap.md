# OpenMicroDuck Public Documentation Roadmap

**English** | [简体中文](../zh-CN/roadmap.md)

This roadmap tracks the **public research and documentation project**. It is not a product-development plan and does not describe private hardware programs.

## Current priorities

1. Keep the documentation understandable to a reader who has never built a robot before: start with a project map and staged reproduction path, then expose detailed parameters.
2. Keep a clear official product-specification baseline separate from development-source details, official simulation-model values, and community reconstruction.
3. Maintain a detailed public hardware/control parameter reference without mislabeling it as an official complete production BOM.
4. Turn public MJCF/mesh information into an understandable structure and assembly map while preserving the simulation-model-versus-manufacturing boundary.
5. Keep the control-loop/dataflow documentation aligned with the official runtime as `robotd`, sensor services, policies and deployment behavior evolve.
6. Track the official policy/task catalog and preserve training/runtime compatibility details such as observation order, action order, filtering, gains and control rate.
7. Keep the reproducible simulation → training → export → ONNX → validation path synchronized with `microduck_rl`.
8. Maintain an explicit sim-to-real parameter reference for BAM, backlash, voltage, delay, friction, mass/CoM/inertia, IMU/encoder errors, contact and terrain.
9. Maintain an explicit list of unresolved questions instead of filling hardware gaps with assumptions.
10. Record upstream commit SHAs for version-sensitive research and add reproducible public hardware measurements when available.
11. Keep English and Simplified Chinese documentation aligned topic-by-topic, with full Chinese explanations rather than abbreviated summaries.

## Recommended reader path

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
Detailed runtime / RL / provenance pages
```

The public reproduction workflow is deliberately staged so a researcher can validate software, simulation, bus timing, sensor conventions and mechanical subassemblies separately before combining them.

## Documentation areas

### Getting started and reproduction

- beginner-friendly project map;
- simulation-first quickstart using official MJCF + existing official ONNX policies;
- staged public reproduction roadmap from software baseline to hardware validation.

### Product and evidence

- official product specifications;
- source/evidence hierarchy;
- upstream version baseline;
- unresolved questions and source conflicts.

### Hardware

- public hardware inventory and BOM status;
- detailed hardware/control parameter reference;
- manufacturer datasheet/documentation index;
- structure and assembly map;
- mechanical structure and kinematics;
- electronics, buses, sensors, audio and power;
- community-derived fastener/bearing/assembly reconstruction.

### Software and control

- onboard runtime architecture;
- 50 Hz control loop and sensor dataflow;
- servo IDs, home pose, bus timing and IMU conventions;
- transport/service boundaries;
- future public runtime topics such as update/recovery and media/remote-control paths when useful as standalone guides.

### Simulation and reinforcement learning

- RL overview and sim-to-real concepts;
- policy/task catalog and runtime switching;
- reproducible training and ONNX export;
- MJCF/model asset reference;
- detailed sim-to-real parameter map covering BAM, backlash, domain randomization, contact and terrain;
- explicit version conflicts such as policy-lineage-dependent runtime filtering.

### Ecosystem and provenance

- reverse-engineering/community project index;
- source and license tracking;
- reproducible public measurements and validation methods.

## Completed documentation expansions on 2026-08-31

The current documentation set includes paired English / Simplified Chinese pages for:

### Foundation set

- official specifications;
- policy catalog and switching;
- control loop and sensor dataflow;
- reproducible training and ONNX export;
- upstream version matrix;
- open questions/source conflicts;
- component datasheet index;
- simulation model assets reference.

### Reverse-engineering / reproduction set

- Start Here beginner guide;
- Simulation First quickstart;
- public reproduction roadmap;
- detailed hardware parameter reference;
- structure and assembly map;
- sim-to-real parameter reference.

## Beginner usability additions completed on 2026-09-02

- added the no-install official browser Sandbox to the landing page;
- added Choose Your Path, a beginner glossary, and symptom-based troubleshooting;
- separated the official-robot owner route from the research-replica route;
- added prerequisites, cloud-cost, `--dry-run`, job-cancellation, and credential-safety guidance;
- updated the reviewed upstream execution baseline while preserving the original evidence revisions on parameter-extraction pages;
- added Issue Forms for documentation errors, reproduction failures, and new sources.

## Next useful public research topics

Good future additions, when public evidence is sufficient, include:

- reproducible scripts/tables that automatically extract joint limits, inertial masses, sites and mesh-instance counts from pinned MJCF files;
- public measurement protocols for servo latency, backlash, voltage sag, IMU orientation and sole friction;
- revision-to-revision parameter diffs as upstream Microduck evolves;
- clearer public wiring/interface diagrams where official source evidence supports them;
- additional community assembly validation, always separated from official production facts.

## Contribution principle

New entries should be publicly attributable and suitable for an open repository. Private, confidential, leaked, unrelated proprietary, or otherwise non-public engineering information is outside the scope of OpenMicroDuck.

When a value cannot be proven from a public source, label it as unresolved rather than guessing.

See the [Start Here guide](getting-started/README.md), [research guidelines](research-guidelines.md), [sources and evidence map](sources.md), and [open questions](research/open-questions-and-conflicts.md).
