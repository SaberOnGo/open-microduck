# Simulation First: The Shortest Path to a Moving Microduck

**English** | [简体中文](../../zh-CN/getting-started/simulation-first.md)

> Goal: see an official Microduck model run an official deployable policy before buying or building any hardware.

## Why this should be the first step

A physical biped mixes many possible failure sources:

```text
mechanics + wiring + servo IDs + IMU orientation + power + Linux + policy + control timing
```

If a new researcher starts with the full robot, a fall does not tell them which layer is wrong.

Simulation removes most of those unknowns. The first milestone should therefore be much smaller:

> **Can the official robot model load, and can an official ONNX policy drive it in MuJoCo?**

If the answer is yes, the researcher has a known-good reference before touching hardware.

## What is already public

Two official repositories are enough for the first experiment:

| Repository | What it provides |
|---|---|
| `pollen-robotics/microduck_rl` | MuJoCo/MJCF robot models, inference script, RL environments, training/export tools |
| `pollen-robotics/microduck` | deployable ONNX policies used by the current runtime |

The runtime policy directory currently documents a common interface:

```text
input:  obs[1, 61]
output: actions[1, 14]
rate:   50 Hz
```

The official runtime repository includes policies for walking, standing, sit/stand, ground pick, kicks, rollers and forward roll.

## Recommended first experiment

### Step 1 — clone both official repositories

```bash
git clone https://github.com/pollen-robotics/microduck_rl
git clone https://github.com/pollen-robotics/microduck
```

For exact reproduction of this documentation snapshot:

```bash
cd microduck_rl
git checkout d424a0c899f6b33cbd3daeb279913134349c0b63
cd ../microduck
git checkout 590b986bd8c0d50ae02cb3ea2f59c463b6828168
```

Using the latest upstream branch is also reasonable for normal exploration, but record the commit when reporting results.

### Step 2 — install the RL repository environment

The official project uses `uv`.

From `microduck_rl`:

```bash
uv sync
```

The upstream README notes that the first dependency sync on some ARM/CUDA machines may need a longer network timeout:

```bash
export UV_HTTP_TIMEOUT=600
uv sync
```

For merely running CPU MuJoCo inference, the main goal is to get the repository dependencies installed successfully. A training GPU is not required for the concept of this first validation step.

### Step 3 — use an already-trained official policy

The important shortcut is: **do not train first.**

The official runtime repository already contains ONNX policy files. That lets a beginner separate “can I run the official controller?” from “can I reproduce the training process?”

A practical multi-policy rehearsal, following the official `infer_policy.py` interface, is:

```bash
cd ../microduck_rl

uv run scripts/infer_policy.py \
  --walking ../microduck/policies/alpha_walking.onnx \
  --standing ../microduck/policies/alpha_stand.onnx \
  --sitstand ../microduck/policies/alpha_sitstand.onnx \
  --roulade ../microduck/policies/roulade.onnx \
  --new-cmd-obs
```

The exact set of available policy files can change upstream, so check `microduck/policies/README.md` when using a different commit.

### Step 4 — verify the important facts, not only the animation

A successful first run should establish:

- the MJCF model loads;
- the ONNX model loads;
- the expected 61-D observation contract is accepted;
- the 14-action joint order is accepted;
- the robot can hold or move without immediately producing a configuration/interface error;
- policy switching in the inference tool behaves plausibly.

Do not judge success only by “the video looks cute.” The purpose is to establish a technical baseline.

## What to inspect next in the model

Once the robot moves, open the model files under:

```text
microduck_rl/
└── src/mjlab_microduck/robot/microduck/
```

The most important files are:

| File | Use |
|---|---|
| `robot_walk.xml` | walking-oriented model with reduced collision scope |
| `robot_allcollisions.xml` | full-body contact model for recovery/tricks/picking |
| `robot_allcollisions_rollers.xml` | roller configuration with passive wheel joints |
| `scene*.xml` | robot + floor + useful keyframes for viewing/inference |
| `add_backlash.py` / `*_backlash.xml` | inserts passive gear-play joints for backlash studies |

A beginner should first learn to identify:

```text
trunk
left leg (5 joints)
neck/head (4 policy joints)
right leg (5 joints)
```

That is the 14-action locomotion tree. The physical runtime has a 15th mouth/beak motor that is controlled separately.

## The easiest training experiment comes second

After inference works, run the official smoke test before any long training job:

```bash
uv run train Mjlab-Velocity-Flat-MicroDuck \
  --env.scene.num-envs 64 \
  --agent.max_iterations 5
```

The official `AGENTS.md` explicitly recommends this small test first. Its purpose is not to learn a useful gait. It checks that the environment builds, steps without NaNs, computes observations/rewards, and can reach the export path.

Only after that should a normal training run be launched, for example the official quickstart:

```bash
uv run train Mjlab-Velocity-Flat-MicroDuck --env.scene.num-envs 4096
```

## A simple milestone checklist

### Milestone A — view / inference

- [ ] repository dependencies install;
- [ ] official MJCF loads;
- [ ] official ONNX loads;
- [ ] robot moves under an existing policy.

### Milestone B — training environment

- [ ] `list-envs` shows Microduck tasks;
- [ ] 64-env / 5-iteration smoke test succeeds;
- [ ] no obvious NaN/configuration failure;
- [ ] observation remains 61-D and action remains 14-D.

### Milestone C — reproduce a walking run

- [ ] train Flat Velocity task;
- [ ] inspect the run in the viewer;
- [ ] export through the official `scripts/export.py`;
- [ ] run the exported ONNX through `infer_policy.py`.

### Milestone D — only then start changing things

Examples:

- actuator parameters;
- backlash;
- mass/CoM;
- IMU error;
- encoder bias;
- command delay;
- terrain;
- collision model;
- robot geometry.

Change one class of assumptions at a time. Otherwise a successful or failed result is difficult to interpret.

## What not to do first

### Do not model a custom robot before understanding the official baseline

The official model already contains a large amount of useful geometry, inertia, collision and joint information. Rebuilding it from zero introduces avoidable error.

### Do not train before confirming inference works

An existing official ONNX policy is a much faster way to verify the deployment-side interface.

### Do not buy all hardware just to discover the software contract

The public repositories already expose most of the information needed to understand the 61/14/50-Hz control contract.

### Do not assume a simulator mesh is a manufacturing CAD package

The released model is extremely useful for simulation and assembly reconstruction, but it does not automatically contain production tolerances, threads, wiring, inserts, materials or final fastener choices.

## If the first run fails

Debug in this order:

```text
1. dependency / Python environment
2. MJCF model load
3. ONNX file path
4. ONNX input/output shape
5. policy/model variant match
6. only then behavior quality
```

This keeps setup failures separate from robotics failures.

## Next pages

After completing this page:

1. [Hardware parameter reference](../hardware/parameter-reference.md)
2. [Structure and assembly map](../hardware/structure-and-assembly-map.md)
3. [Sim-to-real parameter reference](../simulation/sim-to-real-parameter-reference.md)
4. [Public reproduction roadmap](public-reproduction-roadmap.md)

## Primary official sources

- https://github.com/pollen-robotics/microduck_rl
- https://github.com/pollen-robotics/microduck_rl/blob/develop/README.md
- https://github.com/pollen-robotics/microduck_rl/blob/develop/AGENTS.md
- https://github.com/pollen-robotics/microduck_rl/blob/develop/scripts/infer_policy.py
- https://github.com/pollen-robotics/microduck/tree/main/policies
