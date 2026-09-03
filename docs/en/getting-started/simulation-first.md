# Simulation First: The Shortest Path to a Moving Microduck

**English** | [简体中文](../../zh-CN/getting-started/simulation-first.md)

> Goal: see an official Microduck model run an official deployable policy before buying or building any hardware.
>
> Upstream baseline checked: **2026-09-03**.

## Do not want to install anything yet?

Open the [official Microduck Sandbox](https://huggingface.co/spaces/pollen-robotics/microduck-simulator) to run official policies directly in a browser. That is the true step zero for a first-time reader.

This page continues with a local run. Read [Computer, GPU, and Cost Requirements](choose-your-path.md) first if you are unsure which path fits your machine.

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

The runtime policy family uses a common interface:

```text
input:  obs[1, 61]
output: actions[1, 14]
rate:   50 Hz
```

## Recommended first experiment

### What you need before starting

| Item | Requirement for this step |
|---|---|
| Git | Clones and pins the two official repositories |
| `uv` | Installs and runs the Python project; see the [official `uv` installation guide](https://docs.astral.sh/uv/getting-started/installation/) |
| GPU | Running an existing ONNX does not require a training GPU; official local training uses CUDA |
| Disk and network | The first sync downloads substantial dependencies; exact size varies by upstream version and platform |
| Operating system | This project has not completed a native Windows / WSL2 / Linux / macOS compatibility matrix and makes no unverified promise |

### Step 1 — clone both official repositories

```bash
git clone https://github.com/pollen-robotics/microduck_rl
git clone https://github.com/pollen-robotics/microduck
```

For exact reproduction of the current OpenMicroDuck upstream snapshot:

```bash
cd microduck_rl
git checkout 29e887ecfbf5d37144759e5a9f8a176dfb83d547
cd ../microduck
git checkout 2c61dcc1f03440541cdc0729f7a375b2a9ea3005
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

If `uv`, the task registry, the viewer, ONNX, or CUDA fails, do not edit model parameters first. Work through [Beginner Troubleshooting](troubleshooting.md) by layer.

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

At the current RL snapshot, CPU inference also uses the BAM M6 XL330 actuator path by default; `--no-bam` falls back to the XML PD actuators. That makes the inference path more useful for sim-to-real comparison than a purely ideal position actuator.

The exact set of available policy files can change upstream, so check the active runtime repository when using a different commit.

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

The main model families at the current snapshot are:

| File | Use |
|---|---|
| `robot_walk.xml` | walking-oriented model with reduced collision scope |
| `robot_groundcontact.xml` | curated body-contact model for recovery / ground tasks |
| `robot_groundcontact_rollers.xml` | roller configuration with passive wheel mechanics |
| `robot_allcollisions.xml` | true full-part collision model; currently an inspection/experimental model rather than the task default |
| `scene*.xml` | robot + floor/environment + useful keyframes |
| `add_backlash.py` / `*_backlash.xml` | inserts passive gear-play joints for backlash studies |

The `groundcontact` name is newer. Upstream renamed the older curated `allcollisions` role because it did not actually contain collision geometry for every part.

A beginner should first learn to identify:

```text
trunk
left leg (5 joints)
neck/head (4 policy joints)
right leg (5 joints)
```

That is the 14-action locomotion tree. The physical runtime has a 15th mouth/beak motor that is controlled separately.

## Optional next step: run the real control stack against a MuJoCo body

The current `microduck_rl/develop` snapshot also contains `duck-body`, a TCP-served MuJoCo body that accepts a custom scene:

```bash
uv run duck-body --scene path/to/scene.xml
```

The matching `robotd --sim HOST:PORT` implementation is currently on the official public `pollen-robotics/microduck` branch `sim-remote-io`, **not on `main` as of 2026-09-03**.

This is an upstream experimental path rather than a stable release feature. It is especially useful when the research question is “keep the Microduck software contract but change physical-model parameters.” See [Hardware Variant Simulation](../simulation/hardware-variant-simulation.md).

## The easiest training experiment comes second

After inference works, run a small smoke test before any long training job:

```bash
uv run train Mjlab-Velocity-Flat-MicroDuck \
  --env.scene.num-envs 64 \
  --agent.max-iterations 5
```

The purpose is not to learn a useful gait. It checks that the environment builds, steps without NaNs, computes observations/rewards, and reaches the training path.

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
- mass/CoM/inertia;
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

1. [Hardware Variant Simulation](../simulation/hardware-variant-simulation.md)
2. [Hardware parameter reference](../hardware/parameter-reference.md)
3. [Structure and assembly map](../hardware/structure-and-assembly-map.md)
4. [Sim-to-real parameter reference](../simulation/sim-to-real-parameter-reference.md)
5. [Public reproduction roadmap](public-reproduction-roadmap.md)

## Primary official sources

- https://github.com/pollen-robotics/microduck_rl
- https://github.com/pollen-robotics/microduck_rl/blob/develop/README.md
- https://github.com/pollen-robotics/microduck_rl/blob/develop/AGENTS.md
- https://github.com/pollen-robotics/microduck_rl/blob/develop/scripts/infer_policy.py
- https://github.com/pollen-robotics/microduck
- https://github.com/pollen-robotics/microduck/tree/sim-remote-io
