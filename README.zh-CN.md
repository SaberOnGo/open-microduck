# OpenMicroDuck

<p align="center"><strong>🌐 Language / 语言</strong></p>
<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/ENGLISH-1f6feb?style=for-the-badge" alt="English" height="44"></a>&nbsp;&nbsp;
  <a href="README.zh-CN.md"><img src="https://img.shields.io/badge/%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-d73a49?style=for-the-badge" alt="简体中文" height="44"></a>
</p>

**独立、非官方的 Microduck 研究、逆向分析、仿真与技术资料整理项目。**

OpenMicroDuck 将已经公开的 **Microduck** 技术信息整理成可追溯来源的工程参考资料，重点覆盖公开硬件信息、BOM、电子元器件、机械结构、电控、软件架构、仿真、强化学习、互操作研究以及社区可复现的逆向分析成果。

**English summary:** OpenMicroDuck is an independent, unofficial Microduck reverse-engineering and technical documentation project covering publicly verifiable hardware, BOM research, electronics, mechanics, simulation, reinforcement learning, and community projects.

> OpenMicroDuck 与 Pollen Robotics、Hugging Face 不存在隶属、授权、赞助或官方合作关系。Microduck 及其相关名称、Logo、商标和品牌资产归各自权利人所有。

本项目**不声称 Microduck 是开源硬件**。Pollen Robotics 已明确说明，“开源”针对软件栈；机械与电子设计文件并未作为开源硬件发布。

## 已确认器件速览

只要公开资料能够确认到具体型号，这里就直接写出器件名。表中的“开发/参考平台”表示该器件能够从当前官方源码或硬件 bring-up 文档中直接确认，但不等于官方承诺最终量产版本永远使用同一料号。

| 子系统 | 已确认器件 | 状态 |
|---|---|---|
| 主控开发板 | **Radxa Zero 3W** | 官方源码中的当前开发/参考平台 |
| 主控 SoC | **Rockchip RK3566** | 官方产品规格 |
| 内存 / 存储 | **1 GB RAM / 32 GB 存储** | 官方产品规格 |
| 执行器 | **ROBOTIS Dynamixel XL330 ×15** | 官方源码；XL330 的具体子型号尚未被官方源码明确固定 |
| 主控制 IMU | **ST LSM6DSV16X**，位于 **`imu_to_dxl` v2** 板 | 官方源码 |
| 音频 Codec | **Texas Instruments TLV320AIC3104** | 官方源码中的开发硬件 |
| HAT 上第二颗 IMU | **Bosch BMI088** | 官方源码中的开发硬件；标注为 dormant / unused |
| 前置摄像头 | **Sony IMX219 / Raspberry Pi Camera v2 路径** | 官方源码中的开发硬件 |
| 8×8 ToF | **ST VL53L5CX / VL53L8CX 系列** | 官方源码同时支持；最终量产具体型号未固定 |
| 电池 | **NP-F550，2600 mAh** | 官方产品规格 |
| NFC | **2 个天线：头部 + 喙部** | 官方产品规格；控制芯片未公开 |
| 音频器件 | 麦克风 + 扬声器 | 官方产品规格；具体料号未公开 |

更完整的器件清单、I2C 地址、总线参数、板卡名称、未确认项，以及社区推导出的紧固件/轴承信息，见下面的硬件文档。

## 文档

### 硬件

- [公开硬件清单与 BOM 状态](docs/zh-CN/hardware/public-bom.md)
- [社区推导 BOM、紧固件、轴承与装配重建](docs/zh-CN/hardware/community-bom-reconstruction.md)
- [机械结构与运动学](docs/zh-CN/hardware/mechanical-structure.md)
- [电控、总线、传感器与电源](docs/zh-CN/hardware/electronics-and-buses.md)

### 软件、仿真与训练

- [机载运行时架构](docs/zh-CN/software/runtime-architecture.md)
- [仿真与强化学习](docs/zh-CN/simulation/model-and-rl.md)

### 研究生态与来源

- [已审查的逆向分析与社区项目](docs/zh-CN/ecosystem/reverse-engineering-projects.md)
- [更宽范围 GitHub 仓库发现快照](docs/zh-CN/ecosystem/discovered-repositories.md)
- [资料来源与证据地图](docs/zh-CN/sources.md)
- [研究规范](docs/zh-CN/research-guidelines.md)
- [来源与许可证](docs/zh-CN/legal/provenance-and-licenses.md)
- [中文文档索引](docs/zh-CN/README.md)

## 证据规则

技术结论应区分：

- **官方产品规格**：正式产品页、Press Kit、商店等公开资料；
- **官方源码**：能够从上游源码、配置、仿真资产或硬件 bring-up 文档直接确认；
- **社区重建**：第三方根据公开资产或观察独立推导；
- **未验证 / 暂定**：开发资料中存在，但尚不能视为最终量产规格。

不同来源发生冲突时，应保留冲突记录，而不是把推断静默改写成“官方规格”。

## 语言目录结构

英文是仓库默认语言；简体中文不是摘要，而是与英文并列维护的主要文档语言。

```text
open-microduck/
├── README.md                 英文首页（默认）
├── README.zh-CN.md           简体中文首页
├── docs/
│   ├── en/                   英文文档树
│   └── zh-CN/                简体中文文档树
├── hardware/                 公开研究输出 / 代码 / 资产
├── simulation/               公开研究输出 / 代码 / 资产
├── control/                  公开研究输出 / 代码 / 资产
└── learning/                 公开研究输出 / 代码 / 资产
```

以后增加日语、法语、德语等语言时，可增加 `docs/ja/`、`docs/fr/`、`docs/de/` 等同级目录。

## 主要上游资料

- Pollen Robotics Microduck：https://github.com/pollen-robotics/microduck
- Microduck RL：https://github.com/pollen-robotics/microduck_rl
- 产品页面：https://pollen-robotics.com/microduck/
- Press Kit：https://pollen-robotics.com/microduck/press-kit/

## 参与贡献

欢迎提交有公开来源支撑的技术修正、可复现公开实测、基于公开来源的独立重建、仿真验证，以及与 Microduck 相关的公开项目链接。

提交前请阅读 [CONTRIBUTING.zh-CN.md](CONTRIBUTING.zh-CN.md)、[DISCLAIMER.zh-CN.md](DISCLAIMER.zh-CN.md) 和[研究规范](docs/zh-CN/research-guidelines.md)。

不得提交泄露、保密、私有、与本项目无关的专有或其它未公开工程资料；不得提交非法获得的专有文件、私密凭据，或没有相应授权/许可的第三方内容。

## 许可证状态

本仓库目前尚未选择统一的 repository-wide license。第三方资料继续受其原始许可证和限制约束。部分上游 Microduck 3D 模型资产采用 **CC BY-SA-NC**，而软件仓库适用各自声明的软件许可证。复制或再分发第三方资产前，请先查看来源与许可说明。

---

**搜索关键词：** Microduck、Microduck 逆向、Microduck 逆向分析、Microduck 硬件、Microduck BOM、Microduck 电子元器件、Microduck 拆解、Microduck CAD、Microduck 仿真、Microduck 强化学习、Microduck RL、Dynamixel XL330、LSM6DSV16X、Radxa Zero 3W、Microduck robot model、Microduck sim-to-real.