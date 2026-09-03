# OpenMicroDuck 文档 — 简体中文

[English](../en/README.md) | **简体中文**

OpenMicroDuck 的文档分成两类：

1. 先让普通读者快速看懂 Microduck；
2. 再给需要深入研究的人查参数、源码和逆向资料。

## 第一次看

建议按这个顺序：

1. [官方在线 Sandbox](https://huggingface.co/spaces/pollen-robotics/microduck-simulator) —— 不安装软件，先玩一分钟。
2. [先选路线](getting-started/choose-your-path.md) —— 按电脑、GPU、费用和目标选入口。
3. [小白术语表](getting-started/glossary.md) —— 用普通话分清运行、训练和 sim-to-real。
4. [从这里开始](getting-started/README.md) —— 看懂整台机器人。
5. [第一步先做仿真](getting-started/simulation-first.md) —— 本地运行现成 ONNX。
6. [新手排错](getting-started/troubleshooting.md) —— 按症状判断是哪一层出错。

已经有官方 Microduck 的用户从[官方真机用户入口](getting-started/official-robot-owner.md)开始；制作研究样机再看[公开复现路线图](getting-started/public-reproduction-roadmap.md)和[硬件 Bring-up 与标定](getting-started/hardware-bringup-and-calibration.md)。

## 硬件

- [硬件参数总表](hardware/parameter-reference.md) —— Motor ID、Home Pose、关节范围、质量、IMU、总线、电池。
- [结构与装配地图](hardware/structure-and-assembly-map.md) —— 整机怎么分模块、怎么连接。
- [公开硬件清单与 BOM 状态](hardware/public-bom.md) —— 哪些已经确认，哪些仍然未知。
- [电控、总线、传感器与电源](hardware/electronics-and-buses.md) —— 公开资料能确认的接线和接口。
- [社区 BOM 重建](hardware/community-bom-reconstruction.md) —— 明确标注为第三方推导。
- [公开器件 Datasheet 索引](hardware/component-datasheets.md)
- [机械结构与运动学](hardware/mechanical-structure.md)

## 软件与控制

- [官方真机用户入口](getting-started/official-robot-owner.md) —— 第一次开机、手柄、健康状态、更新和安全边界。
- [Microduck 软件架构：一眼看懂](software/runtime-architecture.md) —— **软件部分最推荐的入口。**
- [控制循环：Microduck 到底怎么动起来](software/control-loop-and-sensor-dataflow.md) —— 50 Hz 运动循环和 61 维 Policy 输入。
- [Autonomous Brain：高层行为怎么决定](software/autonomous-brain.md) —— 感知结果怎样变成“走 / 转 / 看 / 休息”等决定。
- [运动学与里程计](software/kinematics-and-odometry.md) —— 怎么算脚、头、传感器位置，以及怎么估计机器人移动了多远。
- [`robotd` 硬件协议](software/robotd-hardware-protocol.md) —— Bus ID、Timing、读取/写入、Startup Register、IMU Data Block。

## 仿真与训练

- [先选路线：电脑、GPU 与费用](getting-started/choose-your-path.md)
- [小白术语表](getting-started/glossary.md)
- [新手排错](getting-started/troubleshooting.md)
- [第一步先做仿真](getting-started/simulation-first.md)
- [仿真与强化学习](simulation/model-and-rl.md)
- [硬件变体仿真](simulation/hardware-variant-simulation.md) —— **小白入口：保持 Microduck 软件接口不变，只修改 MuJoCo 里的执行器、质量、惯量、几何、摩擦等物理参数。**
- [行为、任务与奖励设计](simulation/behavior-task-and-reward-design.md) —— **要创建一个新动作时从这里开始。**
- [技能、Policy 与运行时切换](simulation/policy-catalog-and-switching.md)
- [可复现训练与 ONNX 导出](simulation/reproducible-training-and-export.md)
- [仿真模型资产参考](simulation/model-assets-reference.md)
- [Sim-to-real 参数总表](simulation/sim-to-real-parameter-reference.md)

## 工具

- [上游参数 Diff 工具](../../tools/upstream-diff/README.md) —— 自动提取部分官方公开参数并比较不同上游版本。

## 来源、未知项和社区研究

- [官方规格基线](product/official-specifications.md)
- [待确认问题与来源冲突](research/open-questions-and-conflicts.md)
- [上游版本基线](upstream/version-matrix.md)
- [资料来源与证据地图](sources.md)
- [逆向分析与社区项目](ecosystem/reverse-engineering-projects.md)
- [更宽范围仓库发现](ecosystem/discovered-repositories.md)
- [研究规范](research-guidelines.md)
- [来源与许可证](legal/provenance-and-licenses.md)
- [公开文档路线图](roadmap.md)

## 本项目统一的写法

每篇文档在进入参数和源码前，应先回答：

```text
这是什么？
它负责什么？
它在整台机器人里的位置是什么？
哪些已经确认，哪些只是推导，哪些还不知道？
```

参数参考页可以保留详细表格，但第一部分必须让普通读者不查术语也能大致看懂。

核心官方来源最近一次核对：**2026-09-03**。社区仓库检索快照仍为 **2026-08-31**。
