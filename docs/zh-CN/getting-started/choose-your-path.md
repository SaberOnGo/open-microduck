# 先选路线：我需要什么电脑，要不要训练？

[English](../../en/getting-started/choose-your-path.md) | **简体中文**

> 这页先帮你选路。第一次接触 Microduck，不需要立刻安装训练环境，也不需要先买硬件。

## 最快入口：浏览器里直接玩

打开 [Pollen Robotics 官方 Microduck Sandbox](https://huggingface.co/spaces/pollen-robotics/microduck-simulator)。

它在浏览器里运行 MuJoCo 物理仿真和已经训练好的 ONNX Policy：

1. 用方向键或 `WASD` 控制移动；
2. 按 `R` 触发翻滚，按 `Q` / `E` 踢球；
3. 按 `M` 切换腿和轮滑模式；
4. 按 `Space` 重置。

这一步不需要 Python、CUDA 或实体机器人。它能帮助你理解“运行现成 Policy”，但不等于你已经重新训练了模型，也不证明第三方实体复刻已经完成真机验证。

## 按目标选路线

| 你的目标 | 难度 | 需要什么 | 从哪里开始 |
|---|---:|---|---|
| 看看 Microduck 怎么动 | 0 | 现代浏览器 | [官方在线 Sandbox](https://huggingface.co/spaces/pollen-robotics/microduck-simulator) |
| 看懂机器人和强化学习 | 1 | 不需要编程 | [小白术语表](glossary.md) |
| 在本地运行现成 Policy | 2 | Git、`uv`、命令行；训练 GPU 不是必需 | [第一步先做仿真](simulation-first.md) |
| 训练或修改一个动作 | 3 | NVIDIA CUDA GPU，或付费云 GPU | [可复现训练与 ONNX 导出](../simulation/reproducible-training-and-export.md) |
| 使用购买的官方真机 | 2 | 官方 Microduck | [官方真机用户入口](official-robot-owner.md) |
| 制作公开研究样机 | 5 | 机械、电气、Linux 和安全经验 | [公开复现路线图](public-reproduction-roadmap.md) |

## “运行”和“训练”不是一回事

```text
运行现成 Policy
官方已经训练好 → 你加载 ONNX → 虚拟机器人运动

重新训练 Policy
设计任务和评分 → GPU 反复练习 → 得到 checkpoint → 导出 ONNX
```

只想先看到机器人运动，应选择第一条。官方本地训练 Quickstart 需要 CUDA GPU，但官方 `infer_policy.py` 是 CPU MuJoCo 推理工具。

## 电脑和账号速查

| 路线 | GPU | 账号 | 费用 | 当前证据边界 |
|---|---|---|---|---|
| 官方在线 Sandbox | 不要求本地 GPU | 通常可直接打开 | 在线服务本身当前可访问 | 浏览器兼容性以 Space 当前页面为准 |
| CPU 运行现成 ONNX | 不要求训练 GPU | 无强制云账号 | 本地计算 | 上游提供 CPU inference；仍需安装项目依赖 |
| 官方本地训练 | NVIDIA CUDA GPU | W&B 用于官方示例中的 run 路径 | 本地硬件/电力 | 官方 README 明确要求 CUDA GPU |
| Hugging Face Jobs | 云端 GPU | Hugging Face；通常还需 W&B | **可能收费** | 按硬件运行时间计费 |
| Apple Silicon 社区实验 | Apple Silicon Mac | 视社区项目而定 | 本地计算 | 非官方快速原型，不能代替官方 sim-to-real 训练 |

官方 Quickstart 没有明确承诺 Windows 原生训练支持。本项目目前也没有完成 Windows / WSL2 / macOS / Linux 的全平台实测，因此不要因为 `uv` 能在 Windows 安装，就推断整套 CUDA 训练栈一定能在 Windows 原生运行。

## 使用云训练前先看

Hugging Face Jobs 会创建云端计算任务。Hugging Face 官方说明，Jobs 需要正的账户余额，并按所选硬件的运行时间计费。

第一次使用应先：

1. 查看 [Hugging Face Jobs 实时定价](https://huggingface.co/docs/hub/jobs-pricing)；
2. 使用官方训练命令的 `--dry-run` 检查提交内容；
3. 设置明确的 `--timeout`；
4. 知道如何查看和取消 Job；
5. 不把 Token 写入 Git、截图或日志。

当前 OpenMicroDuck 教程基线使用 `microduck_rl` `5946fd9...`，它包含 `--hf-jobs` 命令入口修复。更早的 `d424a0c...` 不应作为 HF Jobs 教程的执行基线。

## 下一步

- 完全不懂术语：[小白术语表](glossary.md)
- 准备本地运行：[第一步先做仿真](simulation-first.md)
- 已经遇到错误：[新手排错](troubleshooting.md)
- 已经有官方真机：[官方真机用户入口](official-robot-owner.md)

## 主要官方来源

- https://pollen-robotics.com/microduck/
- https://huggingface.co/spaces/pollen-robotics/microduck-simulator
- https://github.com/pollen-robotics/microduck_rl
- https://github.com/pollen-robotics/microduck_rl/blob/develop/scripts/hf/README.md
- https://huggingface.co/docs/hub/jobs-pricing
