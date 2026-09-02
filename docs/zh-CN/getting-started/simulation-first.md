# 第一步先做仿真：最快让 Microduck 动起来

[English](../../en/getting-started/simulation-first.md) | **简体中文**

> 目标：在购买或制作任何硬件之前，先让官方 Microduck 模型跑起官方可部署 ONNX Policy。

## 不想安装？先用官方在线版

如果你只是想先看看 Microduck 怎样运动，打开 [官方 Microduck Sandbox](https://huggingface.co/spaces/pollen-robotics/microduck-simulator)。浏览器里可以直接运行官方 Policy；这比本地安装更适合作为真正的第 0 步。

本页继续讲本地运行。开始前建议先看[路线、电脑与费用要求](choose-your-path.md)。

## 为什么第一步应该是仿真？

一台真实双足机器人会把很多问题同时混在一起：

```text
机械结构
+ 接线
+ 舵机 ID
+ IMU 方向
+ 电源
+ Linux
+ Policy
+ 控制时序
```

如果一上来就做完整实体机器人，它一摔倒，你很难判断究竟是哪一层错了。

仿真可以先拿掉大量不确定因素。

所以第一个目标应该非常简单：

> **官方机器人模型能不能正常加载？官方 ONNX Policy 能不能在 MuJoCo 里控制它？**

只要这一步成功，后面做硬件时就已经有了一条“已知正确”的参考链路。

## 官方现在已经公开了什么？

第一步只需要两个官方仓库：

| 仓库 | 提供什么 |
|---|---|
| `pollen-robotics/microduck_rl` | MuJoCo / MJCF 模型、推理脚本、RL 环境、训练与导出工具 |
| `pollen-robotics/microduck` | 当前 Runtime 使用的可部署 ONNX Policy |

当前 Runtime 的 Policy 目录明确记录了一套共同接口：

```text
输入：  obs[1, 61]
输出：  actions[1, 14]
频率：  50 Hz
```

官方 Runtime 仓库中已经有 Walking、Standing、Sit/Stand、Ground Pick、Kick、Roller、Roulade 等 Policy。

## 推荐的第一个实验

### 开始前需要什么

| 项目 | 这一步的要求 |
|---|---|
| Git | 用来下载和固定两个官方仓库版本 |
| `uv` | 用来安装和运行 Python 项目；未安装时看 [`uv` 官方说明](https://docs.astral.sh/uv/getting-started/installation/) |
| GPU | 运行现成 ONNX 不要求训练 GPU；官方本地训练才明确需要 CUDA GPU |
| 磁盘和网络 | 第一次同步会下载较多依赖；具体大小随上游版本和平台变化 |
| 系统 | 本轮没有完成 Windows 原生 / WSL2 / Linux / macOS 全平台实测，不做未经验证的兼容承诺 |

### 第 1 步：Clone 两个官方仓库

```bash
git clone https://github.com/pollen-robotics/microduck_rl
git clone https://github.com/pollen-robotics/microduck
```

如果希望和本轮 OpenMicroDuck 文档使用完全相同的版本：

```bash
cd microduck_rl
git checkout 5946fd9cdbc58956424420153e51975af3b30d77
cd ../microduck
git checkout 9f7eaad1008fffd90ef871a33a18aecd066b51a9
```

平时探索也可以直接使用上游最新 branch，但如果要发表结果或比较实验，一定要记下 commit。

### 第 2 步：安装 RL 仓库运行环境

官方项目使用 `uv`。

在 `microduck_rl` 目录中：

```bash
uv sync
```

官方 README 还提醒：某些 ARM / CUDA 机器第一次下载依赖时，网络超时可能需要调大：

```bash
export UV_HTTP_TIMEOUT=600
uv sync
```

第一阶段只是跑 CPU MuJoCo inference，并不需要先拥有一块适合大规模训练的 GPU。这里的重点只是：**先把官方模型和 Policy 跑起来。**

如果 `uv`、Task、Viewer、ONNX 或 CUDA 报错，不要直接修改模型参数，先按[新手排错](troubleshooting.md)逐层检查。

### 第 3 步：先用官方已经训练好的 Policy

这里有一个非常重要的捷径：

**不要第一天就重新训练。**

官方 Runtime 仓库已经带了 ONNX Policy，所以可以先把两个问题拆开：

```text
问题 A：我能不能正确运行官方控制器？
问题 B：我能不能重新训练出类似控制器？
```

先解决 A，会简单很多。

按照官方 `infer_policy.py` 的接口，可以做一个多 Policy 仿真：

```bash
cd ../microduck_rl

uv run scripts/infer_policy.py \
  --walking ../microduck/policies/alpha_walking.onnx \
  --standing ../microduck/policies/alpha_stand.onnx \
  --sitstand ../microduck/policies/alpha_sitstand.onnx \
  --roulade ../microduck/policies/roulade.onnx \
  --new-cmd-obs
```

如果使用其它 commit，Policy 文件可能变化，应先查看：

`microduck/policies/README.md`

### 第 4 步：不要只看“动画有没有动”

第一次仿真成功，应该确认的是：

- MJCF 模型能加载；
- ONNX 能加载；
- 61-D Observation 接口被正确接受；
- 14-Action 关节顺序没有错；
- Robot 能保持姿态或运动，不是立刻因为接口错误崩掉；
- `infer_policy.py` 中不同 Policy 的切换逻辑基本合理。

不要只用“看起来挺可爱、会走了”作为技术验收标准。

## 下一步应该看模型里的什么？

机器人跑起来以后，再打开：

```text
microduck_rl/
└── src/mjlab_microduck/robot/microduck/
```

最重要的模型文件：

| 文件 | 用途 |
|---|---|
| `robot_walk.xml` | Walking 使用的模型，减少了一些不需要的身体碰撞 |
| `robot_allcollisions.xml` | Recovery、Trick、Ground Pick 等需要全身接触的模型 |
| `robot_allcollisions_rollers.xml` | 带被动轮子的 Roller 模型 |
| `scene*.xml` | Robot + 地面 + 常用 Keyframe，方便查看和 inference |
| `add_backlash.py` / `*_backlash.xml` | 为各舵机关节插入被动齿隙关节 |

第一次看结构，只要先认清：

```text
Trunk / 躯干
├─ 左腿：5 个关节
├─ Neck + Head：4 个 Policy 关节
└─ 右腿：5 个关节
```

这就是 14-Action 的运动控制树。

真实 Runtime 还有第 15 个嘴/喙电机，但它不进入 14 维 Locomotion Action。

## 第二个实验才是“训练”

Inference 正常以后，先跑官方推荐的 Smoke Test：

```bash
uv run train Mjlab-Velocity-Flat-MicroDuck \
  --env.scene.num-envs 64 \
  --agent.max_iterations 5
```

官方 `AGENTS.md` 明确建议长时间训练之前先跑这个小测试。

它不是为了学会走路，而是检查：

- Environment 能不能构建；
- Simulation 能不能正常 step；
- 有没有 NaN；
- Observation / Reward 是否正常；
- Export 路径是否基本可用。

通过之后，再跑官方 Quickstart 的正常训练，例如：

```bash
uv run train Mjlab-Velocity-Flat-MicroDuck --env.scene.num-envs 4096
```

## 推荐的阶段验收表

### A. 先让现成 Policy 跑起来

- [ ] 依赖安装成功；
- [ ] 官方 MJCF 能加载；
- [ ] 官方 ONNX 能加载；
- [ ] Robot 能在官方 Policy 下运动。

### B. 再确认训练环境

- [ ] `list-envs` 能看到 Microduck Task；
- [ ] 64 env / 5 iteration Smoke Test 成功；
- [ ] 没有明显 NaN / configuration error；
- [ ] Actor Observation 仍然是 61-D，Action 仍然是 14-D。

### C. 再复现 Walking Training

- [ ] 训练 Flat Velocity Task；
- [ ] 在 Viewer 里看训练结果；
- [ ] 通过官方 `scripts/export.py` 导出；
- [ ] 再用 `infer_policy.py` 跑真正导出的 ONNX。

### D. 最后才开始改参数

例如：

- Actuator 参数；
- Backlash；
- Mass / CoM；
- IMU 误差；
- Encoder Bias；
- Command Delay；
- Terrain；
- Collision Model；
- Robot Geometry。

**每次最好只改一类假设。**

否则“结果变好了 / 变差了”也不知道究竟是哪一个因素造成的。

## 第一步不建议做什么？

### 不要先自己从零画一个 Robot Model

官方模型已经公开了大量 Geometry、Mass、Inertia、Collision 和 Joint 信息。没看懂官方基线之前就从零重建，会白白增加误差。

### 不要没跑现成 Policy 就先开始训练

已经训练好的官方 ONNX 是验证 Deployment Interface 最快的办法。

### 不要为了搞懂软件接口就一次把所有硬件买齐

61 / 14 / 50 Hz 这套关键控制合同，大部分已经可以从公开源码搞清楚。

### 不要把 Simulation Mesh 当成量产 CAD

官方模型对仿真和装配逆向极有价值，但它并不自动包含：制造公差、真实螺纹、最终线束、材料、嵌件和量产紧固件选择。

## 如果第一步跑不起来，按这个顺序排查

```text
1. Python / dependency 环境
2. MJCF 能否单独加载
3. ONNX 文件路径
4. ONNX 输入输出 Shape
5. Policy 与 Model Variant 是否匹配
6. 最后才判断“控制效果好不好”
```

这样可以把“环境安装错误”和“机器人学问题”分开。

## 完成后继续看

1. [硬件参数总表](../hardware/parameter-reference.md)
2. [结构与装配地图](../hardware/structure-and-assembly-map.md)
3. [Sim-to-real 参数总表](../simulation/sim-to-real-parameter-reference.md)
4. [公开复现路线图](public-reproduction-roadmap.md)

## 主要官方来源

- https://github.com/pollen-robotics/microduck_rl
- https://github.com/pollen-robotics/microduck_rl/blob/develop/README.md
- https://github.com/pollen-robotics/microduck_rl/blob/develop/AGENTS.md
- https://github.com/pollen-robotics/microduck_rl/blob/develop/scripts/infer_policy.py
- https://github.com/pollen-robotics/microduck/tree/main/policies
