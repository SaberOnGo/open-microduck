# OpenMicroDuck 公开文档路线图

[English](../en/roadmap.md) | **简体中文**

本路线图只跟踪 **OpenMicroDuck 公开研究与文档项目**，不是任何商业产品研发计划，也不描述私有硬件项目。

## 当前优先事项

1. 让第一次接触机器人的普通读者也能顺着看懂：先给项目地图和分阶段复现路线，再进入参数细节。
2. 长期区分官方产品规格、官方源码开发实现、官方仿真模型参数和社区重建结果。
3. 维护详细的公开硬件 / 控制参数总表，但不把它误写成官方完整量产 BOM。
4. 把公开 MJCF / Mesh 转成容易理解的结构与装配地图，同时明确“Simulation Model ≠ Manufacturing Package”。
5. 随官方 `robotd`、Sensor Service、Policy 和 Deployment 行为变化，同步维护控制循环与数据流。
6. 跟踪官方 Policy / Task，并保留 Observation Order、Action Order、Filter、Gain、Control Rate 等 Training / Runtime 匹配信息。
7. 保持 Simulation → Training → Export → ONNX → Validation 的可复现流程与 `microduck_rl` 同步。
8. 维护独立的 Sim-to-real 参数总表，覆盖 BAM、Backlash、Voltage、Delay、Friction、Mass / CoM / Inertia、IMU / Encoder Error、Contact 和 Terrain。
9. 对硬件未知项保留明确清单，不用假设把 BOM 空白补满。
10. 对版本敏感的研究记录上游 Commit SHA；以后有公开实机时，增加可复现实测。
11. 英文和简体中文按主题完整同步，中文不是英文页面的简略摘要。

## 推荐阅读路线

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
再进入 Runtime / RL / 来源与许可证等详细页面
```

公开复现路线会刻意分阶段，让研究者先独立验证 Software、Simulation、Bus Timing、Sensor Convention 和 Mechanical Subassembly，再把它们组合成完整系统。

## 文档范围

### 新手与公开复现

- 普通读者能看懂的项目地图；
- 使用官方 MJCF + 现成官方 ONNX 的 Simulation-first Quickstart；
- 从 Software Baseline 到 Hardware Validation 的分阶段公开复现路线。

### 产品与证据

- 官方产品规格；
- 来源 / 证据等级；
- 上游版本基线；
- 待确认问题与来源冲突。

### 硬件

- 公开硬件清单与 BOM 状态；
- 详细 Hardware / Control Parameter Reference；
- 原厂 Datasheet / 官方资料索引；
- 结构与装配地图；
- 机械结构与运动学；
- 电控、Bus、Sensor、Audio、Power；
- 社区推导的 Fastener / Bearing / Assembly Reconstruction。

### 软件与控制

- 机载 Runtime 架构；
- 50 Hz 控制循环与传感器数据流；
- Servo ID、Home Pose、Bus Timing、IMU Convention；
- Transport / Service Boundary；
- 如果以后独立成文有明显价值，再补 Update / Recovery、Media / Remote-control 等公开 Runtime 专题。

### 仿真与强化学习

- RL 与 Sim-to-real 总览；
- Policy / Task Catalog 和 Runtime 切换；
- 可复现训练与 ONNX 导出；
- MJCF / Model Asset 参考；
- BAM、Backlash、Domain Randomization、Contact、Terrain 等详细参数地图；
- 明确记录不同 Policy Lineage / Revision 之间的 Runtime Filter 等来源差异。

### 生态、来源与许可证

- 逆向分析 / 社区项目索引；
- Source / License 跟踪；
- 可复现实测与验证方法。

## 2026-08-31 已完成的两轮文档扩展

当前已经为以下主题建立成对的 English / 简体中文页面。

### 基础资料组

- 官方规格基线；
- 技能、Policy 与切换；
- 控制循环与传感器数据流；
- 可复现训练与 ONNX 导出；
- 上游版本基线；
- 待确认问题 / 来源冲突；
- 器件 Datasheet 索引；
- 仿真模型资产参考。

### 逆向 / 复现组

- 从这里开始；
- 第一步先做仿真；
- 公开复现路线图；
- 详细硬件参数总表；
- 结构与装配地图；
- Sim-to-real 参数总表。

## 下一步值得继续补的公开研究

在公开证据足够时，可以继续增加：

- 自动从固定版本 MJCF 提取 Joint Limit、Inertial Mass、Site、Mesh Instance Count 的可复现 Script / Table；
- Servo Latency、Backlash、Voltage Sag、IMU Orientation、Sole Friction 等公开测量方法；
- 上游 Microduck 更新后的 Revision-to-revision Parameter Diff；
- 在官方源码证据充分时，增加更清晰的公开 Wiring / Interface Diagram；
- 继续验证社区装配结论，但始终和官方量产事实分开。

## 贡献原则

新增内容应来自公开可追溯来源，并适合放在公开仓库中。私有、保密、泄露、与本项目无关的专有资料，或其它未公开工程信息，不属于 OpenMicroDuck 的公开内容范围。

如果某个数值无法从公开来源证明，应标为“待确认 / Unresolved”，而不是猜一个看起来合理的答案。

详见：[从这里开始](getting-started/README.md)、[研究规范](research-guidelines.md)、[资料来源与证据地图](sources.md)和[待确认问题与来源冲突](research/open-questions-and-conflicts.md)。
