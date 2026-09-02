# Choose Your Path: Computer, GPU, and Training Requirements

**English** | [简体中文](../../zh-CN/getting-started/choose-your-path.md)

> Pick a goal before installing anything. A first-time reader does not need a training environment or physical hardware.

## Fastest start: play in the browser

Open the [official Pollen Robotics Microduck Sandbox](https://huggingface.co/spaces/pollen-robotics/microduck-simulator).

It runs MuJoCo physics and trained ONNX policies in the browser:

1. move with the arrow keys or `WASD`;
2. press `R` to roll and `Q` / `E` to kick;
3. press `M` to switch between legs and rollers;
4. press `Space` to reset.

This path needs no Python, CUDA, or physical robot. It demonstrates **running an existing policy**. It does not mean that you retrained the model or validated a third-party physical replica.

## Pick a goal

| Goal | Difficulty | What you need | Start here |
|---|---:|---|---|
| See Microduck move | 0 | A modern browser | [Official Sandbox](https://huggingface.co/spaces/pollen-robotics/microduck-simulator) |
| Understand robotics and RL | 1 | No programming required | [Beginner Glossary](glossary.md) |
| Run an existing policy locally | 2 | Git, `uv`, and a terminal; no training GPU required | [Simulation First](simulation-first.md) |
| Train or change a behavior | 3 | NVIDIA CUDA GPU or paid cloud GPU | [Reproducible Training and ONNX Export](../simulation/reproducible-training-and-export.md) |
| Use an official production robot | 2 | An official Microduck | [Official Robot Owner Guide](official-robot-owner.md) |
| Build a public research replica | 5 | Mechanical, electrical, Linux, and safety experience | [Public Reproduction Roadmap](public-reproduction-roadmap.md) |

## Running is not training

```text
Run an existing policy
upstream trained it → you load ONNX → the virtual robot moves

Train a policy
design task and score → GPU practice → checkpoint → export ONNX
```

If you only want to see the robot move, choose the first path. The official local-training quickstart requires a CUDA GPU, while the official `infer_policy.py` tool performs CPU MuJoCo inference.

## Computer and account matrix

| Path | GPU | Accounts | Cost | Evidence boundary |
|---|---|---|---|---|
| Official browser Sandbox | No local GPU requirement | Usually opens directly | The online service is currently accessible | Browser compatibility follows the live Space |
| CPU ONNX inference | No training GPU | No required cloud account | Local compute | Upstream provides CPU inference; project dependencies are still required |
| Official local training | NVIDIA CUDA GPU | W&B for the run paths used by official examples | Local hardware/electricity | The official README explicitly requires CUDA |
| Hugging Face Jobs | Cloud GPU | Hugging Face and usually W&B | **May incur charges** | Billed by selected hardware runtime |
| Apple Silicon community lab | Apple Silicon Mac | Project-dependent | Local compute | Unofficial rapid prototyping, not a replacement for official sim-to-real training |

The official quickstart does not promise native Windows training support. OpenMicroDuck has not completed a full Windows / WSL2 / macOS / Linux compatibility test. `uv` supporting Windows does not prove that the complete CUDA training stack supports native Windows.

## Before using cloud training

Hugging Face Jobs creates cloud compute resources. Hugging Face states that Jobs require a positive credit balance and bill for selected hardware runtime.

Before the first submission:

1. read the [live Hugging Face Jobs pricing](https://huggingface.co/docs/hub/jobs-pricing);
2. use the upstream command's `--dry-run` option;
3. set an explicit `--timeout`;
4. know how to inspect and cancel the Job;
5. never put tokens in Git, screenshots, or logs.

The current OpenMicroDuck tutorial baseline uses `microduck_rl` `5946fd9...`, which includes the `--hf-jobs` entry-point fix. The older `d424a0c...` commit should not be used as the execution baseline for the HF Jobs tutorial.

## Next steps

- New to the vocabulary: [Beginner Glossary](glossary.md)
- Ready for a local run: [Simulation First](simulation-first.md)
- Something failed: [Beginner Troubleshooting](troubleshooting.md)
- You own an official robot: [Official Robot Owner Guide](official-robot-owner.md)

## Primary official sources

- https://pollen-robotics.com/microduck/
- https://huggingface.co/spaces/pollen-robotics/microduck-simulator
- https://github.com/pollen-robotics/microduck_rl
- https://github.com/pollen-robotics/microduck_rl/blob/develop/scripts/hf/README.md
- https://huggingface.co/docs/hub/jobs-pricing
