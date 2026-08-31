# 可复现训练与 ONNX 导出

[English](../../en/simulation/reproducible-training-and-export.md) | **简体中文**

> 主要来源：官方 `pollen-robotics/microduck_rl` 仓库。这份文档用于解释公开流程，不替代上游 README。

这份文档把“拿到官方 RL 仓库”到“得到可以在 MuJoCo 验证、并可供 Microduck Runtime 使用的 ONNX Policy”这条链路完整串起来。

最重要的是理解：部署不是只有一个神经网络文件，而是一条完整流水线：

```text
训练环境
   ↓
PPO checkpoint
   ↓
官方 export script
   ↓
ONNX + 已写入的 normalization
   ↓
CPU MuJoCo 验证
   ↓
Microduck Runtime
```

## 需要什么

官方 Quickstart 当前主要需要：

- 支持 CUDA 的 GPU，用于通过 MuJoCo Warp 本地训练；
- `uv`，用于 Python environment / package 管理；
- 官方 `pollen-robotics/microduck_rl` 仓库。

如果没有本地 GPU，官方 README 还提供了通过 Hugging Face Jobs 运行训练的方式。

## 1. Clone 官方仓库

```bash
git clone https://github.com/pollen-robotics/microduck_rl
cd microduck_rl
```

如果要做可复现研究，训练前最好先记录 branch 和 commit SHA。

原因很简单：今天的 `develop` 和几个月后的 `develop` 不一定还是同一套模型、reward、randomization 或依赖版本。

## 2. 训练一个 Walking Policy

官方 Quickstart 使用：

```bash
uv run train Mjlab-Velocity-Flat-MicroDuck --env.scene.num-envs 4096
```

官方 README 表示，在其支持的典型 GPU 配置下，4096 environments 的 walking task 大约 **1–2 小时可以得到 usable gait**。

这个数字应该理解为官方给出的实用参考，不是性能保证。GPU、软件版本、random seed、训练参数等都会影响结果。

## 3. 先在 Viewer 里看训练结果

官方流程可以直接播放训练结果：

```bash
uv run play Mjlab-Velocity-Flat-MicroDuck --wandb-run-path <entity/project/run_id>
```

这一步很有用，因为它可以先判断：

- 是训练本身没成功；
- 还是后面的 export / deployment 出了问题。

不要一上来就把所有问题都归因到真实机器人。

## 4. 使用官方 Exporter 导出

官方命令是：

```bash
uv run scripts/export.py Mjlab-Velocity-Flat-MicroDuck --wandb-run-path <...>
```

这里有一个非常重要的上游规则：

**官方 exporter 会把 observation normalizer 写进 ONNX graph。**

因此，不能简单把 training checkpoint 手工转成 ONNX，然后认为它就和官方导出的部署模型完全等价。

网络权重相同，但输入 normalization 不同，实际控制表现也可能完全不同。

## 5. 在 CPU MuJoCo 里验证真正导出的 ONNX

官方提供：

```bash
uv run scripts/infer_policy.py --walking output.onnx
```

这一步验证的是**真正准备部署的 ONNX artifact**，而不仅仅是 training checkpoint。

它还支持一次加载多个 Policy，例如：

```bash
uv run scripts/infer_policy.py \
  --walking walk.onnx \
  --standing stand.onnx \
  --sitstand sitstand.onnx \
  --roulade roulade.onnx \
  --new-cmd-obs
```

这和真实 Runtime 在统一接口后切换多个 Policy 的思路一致。

## 6. 不要破坏 Deployment Contract

当前官方 Policy 共享：

```text
61 actor observations
14 policy actions
50 Hz control rate
```

如果要复现官方 Policy，尽量不要在没有明确记录的情况下改变：

- observation 顺序；
- normalization；
- joint 顺序；
- command padding；
- action scaling；
- Runtime filter；
- actuator model 假设；
- control frequency。

即使神经网络权重完全一样，只要周围接口变化了，真实机器人表现也可能变化。

## 为什么 BAM 很重要

官方训练栈没有把 XL330 当成“理想电机”。它使用 Rhoban 的 BAM actuator model，并配合 randomization 模拟多种非理想因素，例如：

- voltage-control behavior；
- back-EMF；
- Coulomb / Stribeck / load-dependent friction；
- battery voltage variation；
- load 下的 voltage sag；
- command delay；
- friction variation。

对这样一个很轻、使用小型舵机的双足机器人来说，执行器本身的非理想行为可能就是 sim-to-real gap 的重要来源。

## 为什么还有 Backlash Variant

官方项目还提供模拟舵机齿隙的 Backlash task variant。

它不是简单给关节角度加随机噪声，而是在受控舵机关节里串联 passive backlash hinge，同时保持神经网络接口仍然是 61-D observation / 14-D action。

这样就可以研究：当机械传动不再理想时，Policy 是否仍然足够鲁棒。

## Domain Randomization 是干什么的

Domain randomization 会在训练时主动让不同 simulation environment 的物理参数稍有差异，防止 Policy 只适应“一台完美的虚拟机器人”。

当前公开资料涉及的变化范围包括：

- actuator friction；
- battery behavior；
- timing / delay；
- 质量、惯量等物理属性；
- contact / sole friction；
- 外部 disturbance；
- encoder 相关误差等。

但**具体范围不要永久抄死在概述文档里**，因为它们属于版本敏感参数，应从当前 environment config 和对应 commit 中读取。

## 建议记录哪些信息，才能真正叫“可复现”

每次公开实验至少建议记录：

```text
microduck_rl commit
mjlab / dependency lock 状态
GPU 型号
training task id
num envs
random seed（如果固定）
重要 CLI override
checkpoint 标识
export command
ONNX checksum
validation command
```

这样以后别人说“我训练了同一个 Policy”，才有办法判断到底是不是同一套实验条件。

## 常见错误

1. **手工转换 checkpoint**，却忘了 observation normalizer。
2. 输入仍然是 61 维，但**悄悄改变了 observation 顺序**。
3. 部署时额外增加 training 流程里没有验证过的滤波。
4. 把 `robot_walk`、all-collisions、rollers、backlash 等不同模型当成同一个仿真环境比较。
5. 把某个 commit 中的 domain-randomization 数字永久抄到文档里，却不记录来源版本。
6. 看到 simulation 视频跑得很好，就当成真实硬件已经验证成功。**Simulation success 不等于 sim-to-real 已完成。**

## Tests

官方仓库提供 CPU-side tests：

```bash
uv run --with pytest pytest tests/
```

这些测试会检查一些 configuration / reward invariant。在修改 environment 或 reward 前后运行它们，可以避免一些很隐蔽的错误。

## 主要官方来源

- https://github.com/pollen-robotics/microduck_rl
- https://github.com/pollen-robotics/microduck_rl/blob/develop/README.md
- https://github.com/pollen-robotics/microduck_rl/blob/develop/AGENTS.md
- https://github.com/pollen-robotics/microduck_rl/blob/develop/scripts/export.py
- https://github.com/pollen-robotics/microduck_rl/blob/develop/scripts/infer_policy.py
- https://github.com/Rhoban/bam

## 相关页面

- [仿真与强化学习](model-and-rl.md)
- [技能、Policy 与运行时切换](policy-catalog-and-switching.md)
- [仿真模型资产参考](model-assets-reference.md)
- [上游版本基线](../upstream/version-matrix.md)
