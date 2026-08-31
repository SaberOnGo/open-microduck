# Reverse-Engineering and Community Project Index

> Last reviewed: 2026-08-31. Inclusion means “relevant public project”, not endorsement. Verify each project's current code, provenance, and license before reuse.

The Microduck ecosystem is already branching into hardware reconstruction, mesh/CAD processing, alternative simulators, training-framework ports, language ports, and interaction experiments. This page records projects that were inspected during the current source sweep.

## Mechanical / hardware reconstruction

### `fanhao375/microduck-replica`

Repository: https://github.com/fanhao375/microduck-replica

**Focus:** third-party reconstruction from public Pollen Robotics MJCF/STL/source assets.

Public outputs described by the project include:

- assembled and exploded views reconstructed from MJCF transforms;
- world-transformed STL assemblies for CAD/mesh inspection;
- rigid-body hierarchy and model-derived dimensions/mass summaries;
- joint-limit extraction;
- hole-feature scanning and an inferred M2-dominant fastener system;
- bearing geometry inferred from public meshes;
- source-code-based electronics/bus notes;
- scripts that fetch upstream assets and regenerate analysis outputs.

**Evidence status:** community reconstruction. Several facts can be cross-checked directly against official source, while fastener quantities, assembly assumptions, and manufacturing conclusions remain third-party derivations.

**License note:** the repository states Apache-2.0 for its scripts and CC BY-SA-NC 4.0 for CAD/assembly outputs derived from upstream 3D assets. Check its `LICENSE`/`NOTICE` and upstream asset licensing before reuse.

This is currently the most directly relevant public repository found for Microduck mechanical/hardware reverse-engineering work.

### `boris721/microduck-3d`

Repository: https://github.com/boris721/microduck-3d

**Focus:** cataloging and transforming public Microduck 3D/simulation assets.

The README documents:

- walking and roller MJCF variants;
- kinematic trees;
- grouped STL assets for body/head/legs/electronics/rollers/motors/bearings;
- scripts for assembling meshes into combined models;
- links back to public upstream simulator/CAD sources.

**Evidence status:** community packaging/interpretation of public model assets. File names and counts depend on the upstream snapshot.

## Browser simulator / visualization

### `IronSpiderMan/MicroDuckModels`

Repository: https://github.com/IronSpiderMan/MicroDuckModels

**Focus:** browser-based Microduck simulator.

The project uses Three.js / React Three Fiber for rendering, MuJoCo WebAssembly for physics, and ONNX Runtime Web for policy inference. Its README documents walking, sit/stand, recovery, rolling, kicking, ground-pick, and roller behaviors and notes a 50 Hz policy loop.

**Evidence status:** independent simulator built from public Microduck simulator/model assets. Check upstream asset licenses before redistribution.

## Training-framework ports

### `kabilankb/isaaclab-microduck`

Repository: https://github.com/kabilankb/isaaclab-microduck

**Focus:** Isaac Lab 3.0 / Newton MJWarp port of the Microduck RL stack.

The project preserves the current 61-D observation / 14-action deployment contract and compares ported behavior against the official mjlab baseline.

**Important status caveat:** its current README says several task experiments exist, but locomotion is not yet working as a deployable equivalent and actuator/delay/bias parity is still incomplete. Treat it as a research port, not as a drop-in replacement for the official sim-to-real stack.

### `Macmachi/microduck-rl-genesis`

Repository: https://github.com/Macmachi/microduck-rl-genesis

**Focus:** Genesis port aimed in particular at AMD/ROCm GPU training.

The project states that it preserves the upstream 61-D deployment contract and ports the Microduck walking recipe, BAM actuator behavior, randomization, ONNX export, and backlash variants into Genesis. Its documentation includes numerical comparison tests against MuJoCo/BAM references.

**Evidence status:** independent port with its own validation suite. Claims of parity should be evaluated against the current upstream commit and the project's tests.

### `APX103/mjx_microduck`

Repository: https://github.com/APX103/mjx_microduck

**Focus:** from-scratch MJX/JAX/Brax implementation of Microduck RL tasks.

The current README lists velocity, stand-up, ground-pick, and imitation tasks, with MJX physics and Brax PPO.

**Important compatibility caveat:** the README currently documents **51-D** observations for several tasks, whereas the current official alpha runtime uses a **61-D** observation contract. This is therefore an independent/legacy-compatible research implementation, not automatically a current runtime-compatible policy pipeline.

### `nickoenig37/mjlab_microduck_waddle`

Repository: https://github.com/nickoenig37/mjlab_microduck_waddle

Found in the Microduck GitHub ecosystem as a mjlab-related walking project. It should be reviewed at the code/config level before any technical result from it is promoted into OpenMicroDuck documentation.

## Runtime / language ports

### `craigm26/duckkit`

Repository: https://github.com/craigm26/duckkit

**Focus:** pure Swift model/policy/protocol implementation.

Its README describes:

- Microduck joint model and kinematics;
- the 61-float observation contract;
- policy loading/inference;
- gait/action processing;
- JSON-RPC data structures;
- ToF/state handling;
- voice/performance helpers;
- Linux/macOS testing.

The project states Apache-2.0 and explicitly says it is not affiliated with Pollen Robotics.

**Evidence status:** independent language port. Upstream-derived fixtures and behavior should be traced to the stated official sources when used as evidence.

## Interaction / control experiments

### `kgediya/specs-microduck`

Repository: https://github.com/kgediya/specs-microduck

**Focus:** Snap Spectacles / AR gesture teleoperation for the Microduck simulator.

It demonstrates a community control layer around the simulator using hand tracking and WebSocket relay logic. This is not a hardware reverse-engineering source but is useful evidence of the rapidly growing control/interface ecosystem.

## Official repositories that community projects commonly build on

These are upstream, not third-party reverse-engineering projects:

- https://github.com/pollen-robotics/microduck — onboard runtime and system software;
- https://github.com/pollen-robotics/microduck_rl — official RL/simulation stack;
- https://github.com/pollen-robotics/microduck-gst-plugins — media plugin build artifacts/workflow;
- https://github.com/Rhoban/bam — actuator modeling used by the RL stack.

## Other repositories found but not yet promoted as technical sources

GitHub searches also returned projects with names such as `microduck-simulator`, `microduck-courier`, `microduck-parkour`, `awesome-microduck`, and other forks/experiments. OpenMicroDuck should avoid automatically treating search results as evidence. A project should be inspected for provenance, actual implementation, current status, and licensing before being summarized as a technical source.

## How OpenMicroDuck uses community sources

Community repositories are valuable for discovering:

- transformations that can be reproduced from upstream assets;
- alternative simulator/toolchain implementations;
- possible hardware interpretations to verify;
- useful scripts and visualization methods;
- inconsistencies or undocumented assumptions worth checking upstream.

They do **not** automatically override official specifications. When a community source and an official product/source statement conflict, OpenMicroDuck records the conflict and prioritizes the authoritative source for claims about Microduck itself.

See [../sources.md](../sources.md) for the evidence hierarchy and [../legal/provenance-and-licenses.md](../legal/provenance-and-licenses.md) for reuse cautions.
