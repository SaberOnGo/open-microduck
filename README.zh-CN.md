# OpenMicroDuck

<p align="center"><strong>🌐 Language / 语言</strong></p>
<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/ENGLISH-1f6feb?style=for-the-badge" alt="English" height="44"></a>&nbsp;&nbsp;
  <a href="README.zh-CN.md"><img src="https://img.shields.io/badge/%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-d73a49?style=for-the-badge" alt="简体中文" height="44"></a>
</p>

**独立、非官方的 Microduck 研究、逆向分析、仿真与技术资料整理项目。**

OpenMicroDuck 把已经公开的 Microduck 资料整理成能真正使用的参考：机器人由什么组成、软件怎么配合、运动 AI 怎么训练和部署、哪些细节已经确认、哪些仍然未知。

> OpenMicroDuck 与 Pollen Robotics、Hugging Face 不存在官方隶属或授权关系。本项目不声称 Microduck 是开源硬件。公开资料表明其软件栈开放，但完整量产机械和电子设计文件并未作为开源硬件发布。

## 20 秒看懂 Microduck

```text
Camera ──► 视觉 AI ──────────────┐
ToF ────► 障碍物几何算法 ────────┼──► 高层行为判断
其它传感器 ───────────────────────┘      “走 / 看 / 踢”
                                           │
                                           ▼
                                        运动 RL
                                  61 个输入 → 14 个动作
                                           │
                                           ▼
                                     安全 + 电机控制
                                           │
                                           ▼
                                        15 个电机
```

标准 Walking Policy **不会直接读取 Camera 图像或原始 8×8 ToF 深度图**。视觉、ToF、高层行为、运动 AI 和电机控制是分开的几层。

## 第一次看，从这里开始

| 你想做什么 | 先看这一页 |
|---|---|
| 看懂整台机器人 | [从这里开始](docs/zh-CN/getting-started/README.md) |
| 看懂软件架构 | [Microduck 软件架构：一眼看懂](docs/zh-CN/software/runtime-architecture.md) |
| 先跑虚拟机器人 | [第一步先做仿真](docs/zh-CN/getting-started/simulation-first.md) |
| 按步骤做公开复现 | [公开复现路线图](docs/zh-CN/getting-started/public-reproduction-roadmap.md) |
| 第一次上真机 | [硬件 Bring-up 与标定](docs/zh-CN/getting-started/hardware-bringup-and-calibration.md) |
| 看懂高层行为怎么决定 | [Autonomous Brain](docs/zh-CN/software/autonomous-brain.md) |
| 看懂脚/头位置和里程计 | [运动学与里程计](docs/zh-CN/software/kinematics-and-odometry.md) |
| 查真机总线细节 | [`robotd` 硬件协议](docs/zh-CN/software/robotd-hardware-protocol.md) |
| 查硬件参数 | [硬件参数总表](docs/zh-CN/hardware/parameter-reference.md) |
| 看懂结构怎么装 | [结构与装配地图](docs/zh-CN/hardware/structure-and-assembly-map.md) |
| 查 Sim-to-real 参数 | [Sim-to-real 参数总表](docs/zh-CN/simulation/sim-to-real-parameter-reference.md) |

## 先记住 4 个数字

| 数字 | 含义 |
|---:|---|
| **15** | 当前 Runtime 中的物理电机 ID 数量 |
| **14** | 运动 Policy 控制的关节数量 |
| **61** | 标准运动 Policy 输入宽度 |
| **50 Hz** | 运动控制频率 |

## 文档入口

### 硬件

- [硬件参数总表](docs/zh-CN/hardware/parameter-reference.md)
- [结构与装配地图](docs/zh-CN/hardware/structure-and-assembly-map.md)
- [公开硬件清单与 BOM 状态](docs/zh-CN/hardware/public-bom.md)
- [电控、总线、传感器与电源](docs/zh-CN/hardware/electronics-and-buses.md)
- [社区 BOM 重建](docs/zh-CN/hardware/community-bom-reconstruction.md)

### 软件

- [Microduck 软件架构：一眼看懂](docs/zh-CN/software/runtime-architecture.md)
- [控制循环：Microduck 到底怎么动起来](docs/zh-CN/software/control-loop-and-sensor-dataflow.md)
- [Autonomous Brain：高层行为怎么决定](docs/zh-CN/software/autonomous-brain.md)
- [运动学与里程计](docs/zh-CN/software/kinematics-and-odometry.md)
- [`robotd` 硬件协议](docs/zh-CN/software/robotd-hardware-protocol.md)
- [硬件 Bring-up 与标定](docs/zh-CN/getting-started/hardware-bringup-and-calibration.md)

### 仿真与训练

- [仿真与强化学习](docs/zh-CN/simulation/model-and-rl.md)
- [技能、Policy 与运行时切换](docs/zh-CN/simulation/policy-catalog-and-switching.md)
- [可复现训练与 ONNX 导出](docs/zh-CN/simulation/reproducible-training-and-export.md)
- [Sim-to-real 参数总表](docs/zh-CN/simulation/sim-to-real-parameter-reference.md)

### 工具

- [上游参数 Diff 工具](tools/upstream-diff/README.md)

### 来源与研究状态

- [官方规格基线](docs/zh-CN/product/official-specifications.md)
- [待确认问题与来源冲突](docs/zh-CN/research/open-questions-and-conflicts.md)
- [上游版本基线](docs/zh-CN/upstream/version-matrix.md)
- [资料来源与证据地图](docs/zh-CN/sources.md)
- [完整中文文档索引](docs/zh-CN/README.md)

## 证据标签

OpenMicroDuck 会区分：

- **官方产品规格**：公开的产品级事实；
- **官方源码**：官方代码或文档中可直接验证；
- **官方仿真模型**：来自公开 Simulation Asset；
- **社区重建**：第三方根据公开资料推导；
- **Measured / 实测**：可复现的真实硬件测量；
- **Unresolved / 待确认**：公开证据不足。

没有证据的地方继续写“未知”，不靠猜测补齐。

## 仅公开资料原则

不得提交保密、泄露、私有或其它未公开工程信息。第三方资产必须具备可兼容的权利和来源说明。

详见：[研究规范](docs/zh-CN/research-guidelines.md)、[贡献指南](CONTRIBUTING.zh-CN.md)、[来源与许可证](docs/zh-CN/legal/provenance-and-licenses.md)。

## 主要上游资料

- https://github.com/pollen-robotics/microduck
- https://github.com/pollen-robotics/microduck_rl
- https://pollen-robotics.com/microduck/
- https://pollen-robotics.com/microduck/press-kit/
