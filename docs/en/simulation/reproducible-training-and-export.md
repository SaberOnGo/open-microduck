# Reproducible Training and ONNX Export

**English** | [简体中文](../../zh-CN/simulation/reproducible-training-and-export.md)

> Primary source: official `pollen-robotics/microduck_rl` repository. This page explains the public workflow; it does not replace upstream instructions.

This page gives a practical map from “I have the official repository” to “I have an exported policy that can be tested in MuJoCo and used by the Microduck runtime.”

The important idea is that deployment is a pipeline, not just a neural-network file:

```text
training environment
      ↓
PPO checkpoint
      ↓
official export script
      ↓
ONNX + baked normalization
      ↓
CPU MuJoCo validation
      ↓
Microduck runtime
```

## Requirements

The official quickstart currently expects:

- a CUDA-capable GPU for local training through MuJoCo Warp;
- `uv` for Python environment/package management;
- the official `pollen-robotics/microduck_rl` repository.

The upstream README also documents Hugging Face Jobs as an alternative when a local GPU is not available.

## 1. Clone the official repository

```bash
git clone https://github.com/pollen-robotics/microduck_rl
cd microduck_rl
```

For reproducible research, record the branch and commit SHA before training. A result from `develop` today may not be identical to a result from `develop` months later.

## 2. Train a walking policy

The official quickstart uses:

```bash
uv run train Mjlab-Velocity-Flat-MicroDuck --env.scene.num-envs 4096
```

The upstream README says that on typical supported GPU hardware, this configuration can produce a usable walking gait in roughly **1–2 hours**. Treat that as an upstream practical estimate, not a guaranteed benchmark: GPU, software version, random seed, and training settings all matter.

## 3. Inspect / play a trained policy

The official workflow can replay a run in the viewer:

```bash
uv run play Mjlab-Velocity-Flat-MicroDuck --wandb-run-path <entity/project/run_id>
```

This step is useful before export because it separates “training failed” from “deployment/export failed.”

## 4. Export with the official exporter

The official command is:

```bash
uv run scripts/export.py Mjlab-Velocity-Flat-MicroDuck --wandb-run-path <...>
```

A critical upstream rule is that the exporter **bakes the observation normalizer into the ONNX graph**.

Therefore a manually converted checkpoint is not automatically equivalent to the official deployment artifact. The same network weights with different input normalization can behave like a different controller.

## 5. Validate the exported ONNX in CPU MuJoCo

The official repository provides `scripts/infer_policy.py`:

```bash
uv run scripts/infer_policy.py --walking output.onnx
```

This is valuable because it tests the actual exported deployment artifact rather than only the training checkpoint.

The script also supports combinations of several policies, for example:

```bash
uv run scripts/infer_policy.py \
  --walking walk.onnx \
  --standing stand.onnx \
  --sitstand sitstand.onnx \
  --roulade roulade.onnx \
  --new-cmd-obs
```

That mirrors the runtime idea of switching among policy files behind a shared interface.

## 6. Preserve the deployment contract

Current official policies use:

```text
61 actor observations
14 policy actions
50 Hz control rate
```

When reproducing an official policy, avoid silently changing:

- observation order;
- normalization;
- joint ordering;
- command padding;
- action scaling;
- runtime filters;
- actuator model assumptions;
- control frequency.

A model can be “the same network” mathematically and still behave differently if one of these surrounding contracts changes.

## Why BAM matters

The official stack does not treat the XL330 servos as ideal torque sources. It uses the Rhoban BAM actuator model and additional randomization to represent effects such as:

- voltage-control behavior;
- back-EMF;
- Coulomb / Stribeck / load-dependent friction;
- battery voltage variation;
- voltage sag under load;
- command delay;
- friction variation.

For a small, lightweight robot, these actuator effects can make up a large part of the sim-to-real gap.

## Why Backlash variants exist

The official project also provides task variants with modeled servo gear play. A passive backlash hinge is inserted in series with each controlled joint while keeping the 61-D / 14-D neural interface unchanged.

This lets researchers ask a useful question: can a policy remain robust when the simulated drivetrain behaves less ideally?

## Domain randomization: what it is for

Domain randomization intentionally varies physical or timing parameters during training so the policy does not overfit one perfect simulated robot.

Current upstream material includes variation in areas such as actuator friction, battery behavior, timing/delay, physical properties, contact, disturbances, and encoder-related effects.

Exact ranges should be read from the active environment configuration rather than copied permanently into a summary page, because they are version-sensitive.

## Recommended reproducibility record

For every public experiment, record at least:

```text
microduck_rl commit
mjlab / dependency lock state
GPU model
training task id
num envs
random seed, if fixed
important CLI overrides
checkpoint identifier
export command
ONNX file checksum
validation command
```

This makes “I trained the same policy” a testable statement instead of a vague claim.

## Common mistakes to avoid

1. **Hand-converting a checkpoint** and forgetting the normalizer.
2. **Changing the observation order** while keeping the same input width.
3. **Adding extra deployment filtering** that was not part of the tested pipeline.
4. **Comparing different model variants** (`robot_walk`, all-collisions, rollers, backlash) as if they were the same physical setup.
5. **Copying domain-randomization numbers into permanent documentation** without recording the source commit.
6. **Treating a successful simulator video as proof of real-hardware performance.** Sim-to-real still needs hardware validation.

## Tests

The official repository provides CPU-side tests:

```bash
uv run --with pytest pytest tests/
```

These include configuration/reward invariants and are useful before changing a training environment.

## Primary official sources

- https://github.com/pollen-robotics/microduck_rl
- https://github.com/pollen-robotics/microduck_rl/blob/develop/README.md
- https://github.com/pollen-robotics/microduck_rl/blob/develop/AGENTS.md
- https://github.com/pollen-robotics/microduck_rl/blob/develop/scripts/export.py
- https://github.com/pollen-robotics/microduck_rl/blob/develop/scripts/infer_policy.py
- https://github.com/Rhoban/bam

## Related pages

- [Simulation and reinforcement learning](model-and-rl.md)
- [Policy catalog and switching](policy-catalog-and-switching.md)
- [Model assets reference](model-assets-reference.md)
- [Upstream version matrix](../upstream/version-matrix.md)
