# Beginner Troubleshooting: Start from the Symptom

**English** | [简体中文](../../zh-CN/getting-started/troubleshooting.md)

> Start with read-only checks. Do not reinstall the operating system, change the robot model, or buy hardware for the first error.

## Save these four facts first

Before asking for help or opening an issue, record:

```bash
git rev-parse HEAD
uv --version
uv run list-envs
uv run scripts/infer_policy.py --help
```

For a training failure, also record the GPU model, complete command, and exact error. Never upload tokens, private keys, W&B/Hugging Face credentials, or screenshots containing them.

## Troubleshoot by symptom

| Symptom | First layer to inspect | First check | Next step |
|---|---|---|---|
| `uv` is not found | Tool missing or absent from PATH | `uv --version` | Follow the [official `uv` installation guide](https://docs.astral.sh/uv/getting-started/installation/) and reopen the terminal |
| `uv sync` times out | Dependency download, not RL | Retry and preserve the complete error | On first ARM/CUDA sync, use upstream's `UV_HTTP_TIMEOUT=600` guidance |
| `list-envs` has no Microduck task | Environment/plugin installation | `git rev-parse HEAD`, then `uv sync` | Confirm that the terminal is in the `microduck_rl` root and uses the documented commit |
| Training reports no CUDA/GPU | Training hardware | `nvidia-smi` | Use a supported NVIDIA CUDA environment or evaluate paid HF Jobs first |
| Viewer is blank or has no window | Display/graphics environment | Run `--help` and CPU tests first | Record OS, display method, driver, and full error; do not edit the policy yet |
| W&B run cannot be found | Account or run path | Recheck `<entity/project/run_id>` | Confirm the logged-in account and run namespace |
| ONNX does not load | File path, exporter, or interface | Confirm the file exists and came from the official exporter | Check `[1,61]` input, `[1,14]` output, and model/policy revision |
| Model loads but the robot immediately falls | Contract or model-variant mismatch | Check joint order, normalizer, and model variant | Do not immediately add rewards or tune gains |
| `--hf-jobs` is an unknown option | Upstream predates the fix or environment is stale | `git rev-parse HEAD` | Use a revision containing `5946fd9...`, then run `uv sync` again |
| A cloud Job is running and you cannot stop it | Cloud task and billing | Find the Job ID printed at submission | Cancel from the Jobs page or run `hf jobs cancel <job-id>` |

## Recommended order

```text
1. working directory and commit
2. uv / dependency environment
3. task registry
4. MJCF loading
5. ONNX path and 61 → 14 interface
6. model variant / joint order / normalizer
7. only then evaluate training or control quality
```

Do not edit rewards, BAM parameters, friction, mass, or geometry while step 2 is still failing.

## What counts as the first success?

A first local inference run should at least show that:

- MJCF and ONNX both load;
- no interface-shape error occurs;
- keyboard input changes the target command;
- the process does not exit immediately because of a load error;
- the upstream commit and actual command are recorded.

“The motion does not look good enough” is a later model/control evaluation, not an installation failure.

## Still unverified across platforms

OpenMicroDuck has not completed a full compatibility matrix for native Windows, WSL2, Linux desktop variants, NVIDIA GPU generations, and Apple Silicon. A new platform claim must include actual commands, versions, and error evidence instead of “it should work.”

## Related pages

- [Choose Your Path](choose-your-path.md)
- [Simulation First](simulation-first.md)
- [Reproducible Training and ONNX Export](../simulation/reproducible-training-and-export.md)
