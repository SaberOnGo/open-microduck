# OpenMicroDuck 文档 — 简体中文

[English](../en/README.md) | **简体中文**

这是 OpenMicroDuck 的简体中文文档树。这里整理 Microduck 已公开、可追溯来源的技术资料，以及相关开源与社区研究项目。

如果是第一次看这个项目，推荐阅读顺序：**官方规格 → 控制数据流 → Policy/技能 → 仿真与强化学习 → 详细硬件资料**。

## 产品规格基线

- [Microduck 官方规格基线](product/official-specifications.md)

## 硬件

- [公开硬件清单与 BOM 状态](hardware/public-bom.md)
- [公开器件 Datasheet 与官方资料索引](hardware/component-datasheets.md)
- [社区推导 BOM、紧固件、轴承与装配重建](hardware/community-bom-reconstruction.md)
- [机械结构与运动学](hardware/mechanical-structure.md)
- [电控、总线、传感器与电源](hardware/electronics-and-buses.md)

## 软件与控制

- [机载运行时架构](software/runtime-architecture.md)
- [控制循环与传感器数据流](software/control-loop-and-sensor-dataflow.md)

## 仿真与强化学习

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

## 文档规则

1. 英文和简体中文作为两套并列的主要文档树维护，不把中文做成英文摘要。
2. 中文文档中的普通导航默认继续进入中文文档；语言切换放在页面或章节顶部。
3. 官方产品资料与官方源码优先于媒体报道和二手资料。
4. 第三方逆向结果必须明确写成“社区推导”，不能包装成官方规格。
5. 不同来源有冲突时保留冲突记录，不静默选择更方便的数字。
6. 对版本敏感的实现细节，应尽量记录对应的上游 commit。
7. 不公开保密、泄露、私有、与本项目无关的专有或其它未公开工程信息。

最近一次资料检索：**2026-08-31**。
