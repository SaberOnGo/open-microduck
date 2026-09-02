# Upstream Version Matrix

**English** | [简体中文](../../zh-CN/upstream/version-matrix.md)

> Purpose: keep OpenMicroDuck research tied to identifiable public upstream revisions instead of a moving `main` / `develop` branch.

Microduck is under active development. A statement that is correct today can become stale after an upstream commit changes a model, task, device path, or runtime default.

This page provides a simple version baseline for the current OpenMicroDuck documentation sweep.

## Core official-source snapshot — 2026-09-02

| Upstream source | Branch / page | Revision checked | Role in OpenMicroDuck |
|---|---|---|---|
| `pollen-robotics/microduck` | `main` | `9f7eaad1008fffd90ef871a33a18aecd066b51a9` | onboard runtime, daemons, motor/IMU control, deployment config, hardware bring-up |
| `pollen-robotics/microduck_rl` | `develop` | `5946fd9cdbc58956424420153e51975af3b30d77` | MuJoCo/mjlab training, task registry, robot models, BAM integration, backlash, ONNX export, HF Jobs |
| `Rhoban/bam` | `main` | `620a64fe67c1afe94fca81da73b128c7aed17c5f` | actuator model used by the official RL stack |
| Pollen Robotics Microduck press kit | live page | checked 2026-09-02 | official product-level specifications and provisional-status notices |
| Pollen Robotics Microduck product page/Sandbox | live pages | checked 2026-09-02 | current product positioning, online simulator entry, and public capabilities |

## Impact of this update

This sweep compared each old snapshot with the new HEAD:

- `microduck` `590b986... → 9f7eaad...`: only the CI workflow and a platform type conversion in `duck-detect` changed; none of the motor, IMU, policy, or deployment parameter files cited here changed.
- `microduck_rl` `d424a0c... → 5946fd9...`: only the HF Jobs entry point, related documentation, and tests changed; robot models, tasks, and sim-to-real parameter files did not.
- `5946fd9...` fixes a case where `train --hf-jobs` could be handled by the wrong CLI entry point, so execution tutorials now use the newer commit.

An existing parameter table may still say “source: `d424a0c...`”. That SHA remains the exact source from which its values were extracted; it does not conflict with using a newer execution baseline in tutorials.

## Why record a commit SHA?

A branch name is a moving pointer.

For example:

```text
2026-09-02
microduck_rl/develop → commit A

later
microduck_rl/develop → commit B
```

If a task name, randomization range, model file, or observation rule changes between A and B, a document that only says “see `develop`” becomes difficult to reproduce.

A commit SHA lets a reader return to the exact public source state used by the document.

## What should be version-pinned most carefully?

The most version-sensitive information includes:

- task registry and task IDs;
- reward functions;
- domain-randomization ranges;
- robot MJCF files;
- masses, inertias, collision geometry, and joint limits;
- actuator configuration;
- observation/action contracts;
- export behavior and normalization;
- runtime default gains and filters;
- serial device paths and development-board bring-up details;
- provisional product specifications.

High-level facts such as “Microduck has 15 motors” are less likely to move, but should still have an official source.

## Live pages are different from Git commits

Product pages and press kits usually do not expose a Git commit SHA. For those sources, record the **date checked** and, when a value is particularly important, preserve the wording in a source note or issue without copying excessive copyrighted content.

If an official live page changes, OpenMicroDuck should update the current value while keeping important historical conflicts explained where useful.

## How to cite an upstream source in new research

For version-sensitive work, prefer this style:

```text
Source: pollen-robotics/microduck_rl
Branch: develop
Commit: 5946fd9cdbc58956424420153e51975af3b30d77
Path: src/mjlab_microduck/...
Checked: 2026-09-02
```

For a live product page:

```text
Source: Pollen Robotics Microduck Press Kit
URL: https://pollen-robotics.com/microduck/press-kit/
Checked: 2026-09-02
Evidence level: Official product spec
```

## Updating this matrix

When a future source sweep finds a new upstream revision:

1. update the revision and checked date;
2. inspect whether version-sensitive OpenMicroDuck pages need changes;
3. do not silently rewrite an unresolved conflict into a new “fact”;
4. keep English and Simplified Chinese pages synchronized.

## Primary sources

- https://github.com/pollen-robotics/microduck
- https://github.com/pollen-robotics/microduck_rl
- https://github.com/Rhoban/bam
- https://pollen-robotics.com/microduck/press-kit/
- https://pollen-robotics.com/microduck/

## Related pages

- [Sources and evidence map](../sources.md)
- [Open questions and source conflicts](../research/open-questions-and-conflicts.md)
- [Reproducible training and ONNX export](../simulation/reproducible-training-and-export.md)
