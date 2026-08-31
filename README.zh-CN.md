# OpenMicroDuck

[English](README.md) | [简体中文](README.zh-CN.md)

**独立、非官方的 Microduck 研究、逆向分析、仿真与技术资料整理项目。**

> OpenMicroDuck 与 Pollen Robotics、Hugging Face 不存在隶属、授权、赞助或官方合作关系。Microduck 及其相关名称、Logo、商标和品牌资产归各自权利人所有。

OpenMicroDuck 将互联网上已经公开的 **Microduck** 技术信息整理为可追溯来源的工程参考资料，重点覆盖公开硬件信息、机械结构、软件架构、仿真、强化学习、互操作研究以及社区可复现的逆向分析成果。

本项目**不声称 Microduck 是开源硬件**。Pollen Robotics 目前明确说明，其“开源”表述针对软件栈；机械与电子设计文件并未作为开源硬件发布。

## 本项目整理什么

- 来自公开资料和官方源码的硬件清单；
- 与官方规格分开保存的社区推导 BOM、紧固件、轴承和装配重建；
- 电机、关节、传感器、主控、电池、总线与控制环信息；
- 基于官方公开仿真资产整理的机械与运动学结构；
- 官方运行时、仿真和强化学习架构；
- 社区公开的逆向、CAD 重建、仿真、工具和兼容项目；
- 资料出处、证据等级、许可证说明以及不同来源之间的已知矛盾。

## 从这里开始

| 主题 | 中文 | English |
|---|---|---|
| 文档索引 | [docs/zh-CN/README.md](docs/zh-CN/README.md) | [docs/en/README.md](docs/en/README.md) |
| 公开硬件清单 / BOM 状态 | [docs/zh-CN/hardware/public-bom.md](docs/zh-CN/hardware/public-bom.md) | [docs/en/hardware/public-bom.md](docs/en/hardware/public-bom.md) |
| 社区推导 BOM / 紧固件重建 | [docs/zh-CN/hardware/community-bom-reconstruction.md](docs/zh-CN/hardware/community-bom-reconstruction.md) | [docs/en/hardware/community-bom-reconstruction.md](docs/en/hardware/community-bom-reconstruction.md) |
| 机械结构 | [docs/zh-CN/hardware/mechanical-structure.md](docs/zh-CN/hardware/mechanical-structure.md) | [docs/en/hardware/mechanical-structure.md](docs/en/hardware/mechanical-structure.md) |
| 电控与总线 | [docs/zh-CN/hardware/electronics-and-buses.md](docs/zh-CN/hardware/electronics-and-buses.md) | [docs/en/hardware/electronics-and-buses.md](docs/en/hardware/electronics-and-buses.md) |
| 运行时架构 | [docs/zh-CN/software/runtime-architecture.md](docs/zh-CN/software/runtime-architecture.md) | [docs/en/software/runtime-architecture.md](docs/en/software/runtime-architecture.md) |
| 仿真与强化学习 | [docs/zh-CN/simulation/model-and-rl.md](docs/zh-CN/simulation/model-and-rl.md) | [docs/en/simulation/model-and-rl.md](docs/en/simulation/model-and-rl.md) |
| 社区逆向项目索引 | [docs/zh-CN/ecosystem/reverse-engineering-projects.md](docs/zh-CN/ecosystem/reverse-engineering-projects.md) | [docs/en/ecosystem/reverse-engineering-projects.md](docs/en/ecosystem/reverse-engineering-projects.md) |
| 资料来源与证据 | [docs/zh-CN/sources.md](docs/zh-CN/sources.md) | [docs/en/sources.md](docs/en/sources.md) |
| 许可与来源说明 | [docs/zh-CN/legal/provenance-and-licenses.md](docs/zh-CN/legal/provenance-and-licenses.md) | [docs/en/legal/provenance-and-licenses.md](docs/en/legal/provenance-and-licenses.md) |

## 证据规则

技术结论应尽量明确区分以下类型：

- **官方产品规格**：Pollen Robotics / Hugging Face 正式公开的产品信息；
- **官方源码**：官方软件、仿真模型、配置文件或硬件 bring-up 文档中能够直接验证的信息；
- **社区重建**：第三方基于公开资产、测量或观察独立推导出的结论；
- **未验证 / 暂定**：开发分支中存在、推理上合理，但尚不能视为最终量产规格的信息。

如果官方产品资料与第三方逆向结论存在冲突，本项目优先采用官方资料，同时记录冲突，不把第三方推断静默写成官方事实。

## 仓库结构

```text
open-microduck/
├── README.md
├── README.zh-CN.md
├── docs/
│   ├── en/                 英文文档
│   └── zh-CN/              简体中文文档
├── hardware/               本项目自行产生的公开硬件研究资料
├── simulation/             本项目自行产生的公开仿真研究资料
├── control/                本项目自行产生的公开控制/互操作研究资料
└── learning/               本项目自行产生的公开训练与可复现研究资料
```

未来增加日语、法语、德语等语言时，可增加 `docs/ja/`、`docs/fr/`、`docs/de/` 等同级目录，不改变英文主文档路径。

## 主要上游资料

- Pollen Robotics Microduck：https://github.com/pollen-robotics/microduck
- Microduck RL：https://github.com/pollen-robotics/microduck_rl
- 产品页面：https://pollen-robotics.com/microduck/
- Press Kit / 公开规格：https://pollen-robotics.com/microduck/press-kit/

社区项目统一收录在“逆向项目索引”文档中。收录只表示与研究主题相关，不表示 OpenMicroDuck 对其准确性、许可证或实现方式作出背书。

## 参与贡献

欢迎提交有公开来源支撑的技术修正、可复现公开实测、基于公开来源的独立重建、仿真验证，以及与 Microduck 相关的公开项目链接。

提交前请阅读 [CONTRIBUTING.zh-CN.md](CONTRIBUTING.zh-CN.md)、[DISCLAIMER.zh-CN.md](DISCLAIMER.zh-CN.md) 和研究规范。

不得提交泄露、保密、私有、与本项目无关的专有或其它未公开工程资料；不得提交非法获得的专有文件、私密凭据，或没有相应授权/许可的第三方内容。

## 许可证状态

本仓库目前尚未选择统一的 repository-wide license。第三方资料继续受其原始许可证和限制约束。尤其需要注意：部分上游 Microduck 3D 模型资产采用 **CC BY-SA-NC**，而软件仓库则适用各自声明的软件许可证。复制或再分发第三方资产前，请先查看本项目的来源与许可说明。

---

**搜索关键词：** Microduck、Microduck 逆向、Microduck 硬件、Microduck BOM、Microduck 拆解、Microduck CAD、Microduck 仿真、Microduck 强化学习、Microduck RL、Dynamixel XL330、Microduck robot model、Microduck sim-to-real。