# Upstream Version Matrix

**English** | [简体中文](../../zh-CN/upstream/version-matrix.md)

> Purpose: keep OpenMicroDuck research tied to identifiable public upstream revisions instead of a moving `main` / `develop` branch.

Microduck is under active development. A statement that is correct today can become stale after an upstream commit changes a model, task, device path, runtime default, or experimental branch.

This page provides a version baseline for the current OpenMicroDuck documentation sweep.

## Core official-source snapshot — 2026-09-03

| Upstream source | Branch / page | Revision checked | Role in OpenMicroDuck |
|---|---|---|---|
| `pollen-robotics/microduck` | `main` | `2c61dcc1f03440541cdc0729f7a375b2a9ea3005` | onboard runtime, daemons, motor/IMU control, deployment config, hardware bring-up |
| `pollen-robotics/microduck` | `sim-remote-io` | `0cd676d6fbb6e90a762c84aa63abe7a02dbc9495` | **experimental public branch** for `robotd --sim`, `RemoteIo`, and software-in-the-loop simulation; not `main` |
| `pollen-robotics/microduck_rl` | `develop` | `29e887ecfbf5d37144759e5a9f8a176dfb83d547` | MuJoCo/mjlab training, robot models, BAM integration, `duck-body`, ToF simulation, backlash, ONNX export/publishing |
| `Rhoban/bam` | `main` | `620a64fe67c1afe94fca81da73b128c7aed17c5f` | actuator model used by the official RL stack |
| Pollen Robotics Microduck press kit | live page | checked 2026-09-03 | official product-level specifications and provisional-status notices |
| Pollen Robotics Microduck product/store pages | live pages | checked 2026-09-03 | current public product positioning and availability information |

## What changed since the 2026-09-02 OpenMicroDuck snapshot?

### `microduck/main`: `9f7eaad... → 2c61dcc...`

The new main revision primarily improves daemon health reporting for crash-looping services. It does not merge the `robotd --sim` software-in-the-loop path.

That distinction is important: current `main` still does not expose the `--sim` argument found on the separate public `sim-remote-io` branch.

### `microduck_rl/develop`: `5946fd9... → 29e887e...`

This update is significant for simulation research. It includes several merged changes:

1. **Model re-export and collision-family cleanup**
   - the older curated `allcollisions` role was renamed to `groundcontact`;
   - a new true `robot_allcollisions.xml` was added;
   - the upstream PR reports the re-exported existing models remained physics-identical for joint names/order/ranges, masses, inertias, frames, and their intended collision sets, while CAD material colors changed.

2. **`duck-body` MuJoCo body server**
   - `src/mjlab_microduck/sim/body_server.py` serves a simulated Microduck body over TCP;
   - it accepts `--scene`, enabling another MuJoCo scene to be supplied;
   - it maps actuators by Microduck joint name rather than raw object index.

3. **ToF coordinate-convention fix**
   - the simulated ToF columns were reversed left/right relative to the real processing convention;
   - this was fixed before the body-server branch was merged.

4. **BAM in CPU inference path**
   - the CPU MuJoCo inference path was updated to use the BAM `m6` actuator behavior.

5. **Policy publishing support**
   - upstream added a supported publish path for exported ONNX policies and manifests.

These are not small documentation-only changes, so simulation pages should use the 2026-09-03 baseline where current upstream behavior matters.

## Experimental branch status: `sim-remote-io`

The official public `pollen-robotics/microduck` repository currently has a branch named `sim-remote-io`.

At the pinned branch revision, it contains:

```text
robotd --sim HOST:PORT
```

and documents the intended boundary at `duck_control::io::RobotIo`.

The upstream design states that the real 50 Hz loop, ONNX policies, safety, fall detection, odometry, kinematics, IPC, `robotctl`, and related code stay above this boundary; the simulated body replaces the hardware-I/O side below it.

Because this branch is **not merged into `main`**, OpenMicroDuck must label it as:

> Official public upstream experimental branch

not as a stable or released Microduck feature.

## Why record a commit SHA?

A branch name is a moving pointer.

For example:

```text
2026-09-03
microduck_rl/develop → commit A

later
microduck_rl/develop → commit B
```

If a task name, randomization range, model file, collision family, simulator interface, or observation rule changes between A and B, a document that only says “see `develop`” becomes difficult to reproduce.

A commit SHA lets a reader return to the exact public source state used by the document.

## What should be version-pinned most carefully?

The most version-sensitive information includes:

- task registry and task IDs;
- reward functions;
- domain-randomization ranges;
- robot MJCF files;
- model-family meaning (`walk`, `groundcontact`, `allcollisions`, rollers, backlash);
- masses, inertias, collision geometry, and joint limits;
- actuator configuration;
- observation/action contracts;
- export behavior and normalization;
- runtime default gains and filters;
- simulator/runtime protocol boundaries;
- serial device paths and development-board bring-up details;
- provisional product specifications.

High-level facts such as “Microduck has 15 motors” are less likely to move, but should still have an official source.

## Live pages are different from Git commits

Product pages and press kits usually do not expose a Git commit SHA. For those sources, record the **date checked** and, when a value is particularly important, preserve a short source note without copying excessive copyrighted content.

If an official live page changes, OpenMicroDuck should update the current value while keeping important historical conflicts explained where useful.

## How to cite an upstream source in new research

For version-sensitive main/develop work, prefer this style:

```text
Source: pollen-robotics/microduck_rl
Branch: develop
Commit: 29e887ecfbf5d37144759e5a9f8a176dfb83d547
Path: src/mjlab_microduck/...
Checked: 2026-09-03
```

For experimental branch work:

```text
Source: pollen-robotics/microduck
Branch: sim-remote-io
Commit: 0cd676d6fbb6e90a762c84aa63abe7a02dbc9495
Status: official public upstream experimental branch; not main
Checked: 2026-09-03
```

For a live product page:

```text
Source: Pollen Robotics Microduck Press Kit
URL: https://pollen-robotics.com/microduck/press-kit/
Checked: 2026-09-03
Evidence level: Official product spec
```

## Updating this matrix

When a future source sweep finds a new upstream revision:

1. update the revision and checked date;
2. inspect whether version-sensitive OpenMicroDuck pages need changes;
3. separately track experimental branches instead of silently treating them as mainline;
4. do not silently rewrite an unresolved conflict into a new “fact”;
5. keep English and Simplified Chinese pages synchronized.

## Primary sources

- https://github.com/pollen-robotics/microduck
- https://github.com/pollen-robotics/microduck/tree/sim-remote-io
- https://github.com/pollen-robotics/microduck_rl
- https://github.com/Rhoban/bam
- https://pollen-robotics.com/microduck/press-kit/
- https://pollen-robotics.com/microduck/

## Related pages

- [Hardware Variant Simulation](../simulation/hardware-variant-simulation.md)
- [Simulation Model Assets Reference](../simulation/model-assets-reference.md)
- [Sources and evidence map](../sources.md)
- [Open questions and source conflicts](../research/open-questions-and-conflicts.md)
- [Reproducible training and ONNX export](../simulation/reproducible-training-and-export.md)
