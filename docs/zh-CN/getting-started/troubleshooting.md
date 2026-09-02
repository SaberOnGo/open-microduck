# 新手排错：先看症状，再找是哪一层

[English](../../en/getting-started/troubleshooting.md) | **简体中文**

> 先运行只读检查，不要一遇到错误就重装系统、改机器人模型或购买硬件。

## 先保存这四项

提问或提交 Issue 前，先保存：

```bash
git rev-parse HEAD
uv --version
uv run list-envs
uv run scripts/infer_policy.py --help
```

如果问题发生在训练阶段，再保存 GPU 型号、完整命令和错误文本。不要上传 Token、私钥、W&B/Hugging Face 凭据或包含它们的截图。

## 按症状排查

| 你看到什么 | 先判断哪一层 | 第一个检查 | 下一步 |
|---|---|---|---|
| `uv` 找不到 | 工具尚未安装或不在 PATH | `uv --version` | 按 [`uv` 官方安装说明](https://docs.astral.sh/uv/getting-started/installation/) 安装，重新打开终端 |
| `uv sync` 下载超时 | 依赖下载，不是 RL 问题 | 重试并保留完整错误 | ARM / CUDA 首次同步可按上游提示设置 `UV_HTTP_TIMEOUT=600` |
| `list-envs` 看不到 Microduck Task | 环境或插件没有正确安装 | `git rev-parse HEAD`、`uv sync` | 确认在 `microduck_rl` 根目录，并使用文档对应 commit |
| 训练提示没有 CUDA / GPU | 训练硬件不满足要求 | `nvidia-smi` | 改用受支持的 NVIDIA CUDA 环境，或先评估付费 HF Jobs |
| Viewer 不显示或黑屏 | 显示/图形环境 | 先跑 `--help` 和 CPU tests | 保留 OS、显示方式、驱动和完整错误；不要先改 Policy |
| W&B 找不到 run | 账号或 run path | 核对 `<entity/project/run_id>` | 确认登录账号和 run 所属 namespace |
| ONNX 无法加载 | 文件路径、导出方式或接口 | 确认文件存在并来自官方 Exporter | 检查输入 `[1,61]`、输出 `[1,14]` 和模型/Policy 版本 |
| 模型能加载，但机器人立刻倒下 | 接口或模型 Variant 不匹配 | 核对 joint order、normalizer、model variant | 不要直接增加 Reward 或随意调 gain |
| `--hf-jobs` 被当成未知参数 | 上游版本早于修复或环境未同步 | `git rev-parse HEAD` | 使用包含 `5946fd9...` 修复的版本并重新 `uv sync` |
| HF Job 已经运行，不知道如何停止 | 云任务与计费 | 查看提交时打印的 Job ID | 使用 HF Jobs 页面或 `hf jobs cancel <job-id>` 取消 |

## 推荐的排错顺序

```text
1. 当前目录和 commit
2. uv / dependency 环境
3. Task registry
4. MJCF 是否能加载
5. ONNX 路径与 61 → 14 接口
6. Model Variant / joint order / normalizer
7. 最后才判断训练或控制效果
```

如果第 2 步还没通过，就不要改 Reward、BAM、摩擦、质量或机械参数。

## 什么叫“成功”？

第一次本地推理至少应满足：

- MJCF 和 ONNX 都成功加载；
- 没有接口 Shape 错误；
- 键盘命令能改变目标速度；
- Robot 不会因为加载错误立即退出；
- 你记录了上游 commit 和实际命令。

动作“看起来不够好”属于后续控制/模型评估，不应和安装失败混成同一个问题。

## 仍需实测的范围

OpenMicroDuck 当前没有完成 Windows 原生、WSL2、不同 Linux 桌面、各代 NVIDIA GPU 和 Apple Silicon 的完整兼容性矩阵。新的平台修复必须附实际命令、版本和错误文本，不能只写“理论上支持”。

## 相关页面

- [先选路线](choose-your-path.md)
- [第一步先做仿真](simulation-first.md)
- [可复现训练与 ONNX 导出](../simulation/reproducible-training-and-export.md)
