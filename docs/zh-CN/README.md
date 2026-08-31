# OpenMicroDuck 文档 — 简体中文

[English](../en/README.md) | **简体中文**

OpenMicroDuck 是一个面向公众的、以来源可追溯为基础的 Microduck 技术资料库。目标不是把所有资料堆在一起，而是让普通读者也能逐步看懂：Microduck 怎么组成、怎么在仿真里运行、真实机器人怎样控制、哪些硬件参数已经公开、哪些仍然不能确认。

## 第一次看，从这里开始

不要一上来把所有 Hardware / RL 页面全看一遍。先按自己的目的选入口：

| 你想做什么 | 第一篇先看 |
|---|---|
| 几分钟看懂整个项目 | [从这里开始](getting-started/README.md) |
| 不买硬件，先让 Microduck 在电脑里动起来 | [第一步先做仿真](getting-started/simulation-first.md) |
| 按阶段做公开研究复现 | [公开复现路线图](getting-started/public-reproduction-roadmap.md) |
| 查具体硬件 / 控制参数 | [硬件参数总表](hardware/parameter-reference.md) |
| 看懂各个零件怎么连接、怎么装 | [结构与装配地图](hardware/structure-and-assembly-map.md) |
| 查 Domain Randomization / Backlash / Voltage 等数值 | [Sim-to-real 参数总表](simulation/sim-to-real-parameter-reference.md) |

第一次阅读推荐顺序：

```text
从这里开始
   ↓
第一步先做仿真
   ↓
硬件参数总表
   ↓
结构与装配地图
   ↓
Sim-to-real 参数总表
   ↓
再进入软件 / RL / 来源与许可证等详细页面
```

## 产品规格基线

- [Microduck 官方规格基线](product/official-specifications.md)

## 硬件

### 建议先看的两页

- [硬件参数总表](hardware/parameter-reference.md) —— Motor ID、Home Pose、Joint Limit、Mass、Bus Timing、IMU Data Format、Battery、HAT / I2C / Audio 等重要参数集中查阅。
- [结构与装配地图](hardware/structure-and-assembly-map.md) —— 先把整机看成 Trunk、两条腿、Head、Feet，而不是面对一堆看不懂的 STL 名称。

### 详细参考

- [公开硬件清单与 BOM 状态](hardware/public-bom.md)
- [公开器件 Datasheet 与官方资料索引](hardware/component-datasheets.md)
- [社区推导 BOM、紧固件、轴承与装配重建](hardware/community-bom-reconstruction.md)
- [机械结构与运动学](hardware/mechanical-structure.md)
- [电控、总线、传感器与电源](hardware/electronics-and-buses.md)

## 软件与控制

- [控制循环与传感器数据流](software/control-loop-and-sensor-dataflow.md) —— 最容易看懂真实机器人 50 Hz 的 Servo / IMU → Observation → ONNX → Action 流程。
- [机载运行时架构](software/runtime-architecture.md) —— `robotd`、Linux Daemon、各 Service 和部署边界。

## 仿真与强化学习

### 建议先看

- [第一步先做仿真](getting-started/simulation-first.md)
- [Sim-to-real 参数总表](simulation/sim-to-real-parameter-reference.md)

### 进一步深入

- [仿真与强化学习总览](simulation/model-and-rl.md)
- [技能、Policy 与运行时切换](simulation/policy-catalog-and-switching.md)
- [可复现训练与 ONNX 导出](simulation/reproducible-training-and-export.md)
- [仿真模型资产参考](simulation/model-assets-reference.md)

## 研究状态与可复现性

- [待确认问题与来源冲突](research/open-questions-and-conflicts.md)
- [上游版本基线](upstream/version-matrix.md)
- [资料来源与证据地图](sources.md)
- [研究规范](research-guidelines.md)
- [来源与许可证](legal/provenance-and-licenses.md)

## 研究生态与项目文档

- [公开文档路线图](roadmap.md)
- [已审查的逆向分析与社区项目](ecosystem/reverse-engineering-projects.md)
- [更宽范围 GitHub 仓库发现快照](ecosystem/discovered-repositories.md)

## 证据标签怎么理解

OpenMicroDuck 会刻意把这些东西分开：

- **官方产品规格**：Pollen Robotics 产品页、Press Kit、商店等明确公布的产品级事实；
- **官方源码**：官方代码和设计文档中可以直接验证的实现；
- **官方仿真模型**：公开 Simulation Asset 中的 Geometry / Dynamics，不自动等于量产实体测量值；
- **社区重建**：第三方根据公开资料推导的结果；
- **Measured / 实测**：有测试条件、可复现的真实硬件测量；
- **Unresolved / Provisional**：目前公开证据还不足，不能写成最终事实。

这个区分对 BOM、螺丝、PCB、模型文件名、Simulation Parameter 尤其重要。

## 文档规则

1. 英文和简体中文作为两套并列的主要文档树维护，中文不是英文摘要。
2. 中文页面默认继续链接中文页面；语言切换放在页面顶部。
3. 官方产品资料与官方源码优先于媒体报道和二手资料。
4. 第三方逆向结果必须明确标注“社区推导”，不能包装成官方规格。
5. 来源冲突要保留下来，不能静默选一个方便的数字。
6. 对版本敏感的实现细节，应尽量记录对应的上游 commit。
7. 写法尽量先解释“它是什么、为什么重要”，再进入参数和源码路径，避免普通读者一上来看到参数墙。
8. 不公开保密、泄露、私有、与本项目无关的专有或其它未公开工程信息。

最近一次资料检索：**2026-08-31**。
