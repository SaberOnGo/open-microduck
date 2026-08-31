# OpenMicroDuck 公开文档路线图

[English](../en/roadmap.md) | **简体中文**

本路线图只跟踪 **OpenMicroDuck 公开研究与文档项目**，不是任何商业产品研发计划，也不描述私有硬件项目。

## 当前优先事项

1. 把“官方产品规格基线”与开发源码细节、社区重建结果长期分开维护。
2. 持续维护公开硬件清单，但不把它误写成官方完整 BOM。
3. 随官方 `robotd`、传感器 service 和部署行为变化，同步维护控制循环与数据流文档。
4. 跟踪官方 task / policy catalog，并用不需要先读 RL 源码的方式解释 Policy 切换。
5. 保持 training → export → ONNX → validation 的可复现流程与 `microduck_rl` 同步。
6. 跟踪 MJCF/model variant、asset 来源和许可证边界。
7. 对未确认问题保留明确清单，不用假设把空白补满。
8. 对版本敏感的研究记录上游 commit SHA。
9. 以后有公开量产实机后，增加可复现实测和验证方法。
10. 英文和简体中文按主题完整同步，中文不是英文页面的简略摘要。

## 文档范围

### 产品与证据

- 官方产品规格；
- 来源 / 证据等级；
- 上游版本基线；
- 待确认问题与来源冲突。

### 硬件

- 公开硬件清单与 BOM 状态；
- 原厂 Datasheet / 官方资料索引；
- 机械结构与运动学；
- 电控、总线、传感器、音频、电源；
- 社区推导的紧固件、轴承和装配重建。

### 软件与控制

- 机载 Runtime 架构；
- 控制循环与传感器数据流；
- transport / service boundary；
- 如果以后独立成文有明显价值，再补 update/recovery、media/remote-control 等公开 Runtime 专题。

### 仿真与强化学习

- RL 与 sim-to-real 总览；
- Policy / task catalog 和 Runtime 切换；
- 可复现训练与 ONNX 导出；
- MJCF / model asset 参考；
- actuator model、backlash、domain randomization。

### 生态、来源与许可证

- 逆向分析 / 社区项目索引；
- source / license 跟踪；
- 可复现实测与验证方法。

## 2026-08-31 文档扩展已完成

本轮已经为以下主题新增了成对的 English / 简体中文页面：

- 官方规格基线；
- 技能、Policy 与切换；
- 控制循环与传感器数据流；
- 可复现训练与 ONNX 导出；
- 上游版本基线；
- 待确认问题 / 来源冲突；
- 器件 Datasheet 索引；
- 仿真模型资产参考。

## 贡献原则

新增内容应来自公开可追溯来源，并适合放在公开仓库中。私有、保密、泄露、与本项目无关的专有资料，或其它未公开工程信息，不属于 OpenMicroDuck 的公开内容范围。

如果某个数值无法从公开来源证明，应标为“待确认 / unresolved”，而不是猜一个看起来合理的答案。

详见[研究规范](research-guidelines.md)、[资料来源与证据地图](sources.md)和[待确认问题与来源冲突](research/open-questions-and-conflicts.md)。
