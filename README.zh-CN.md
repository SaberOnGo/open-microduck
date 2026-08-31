# OpenMicroDuck

<p align="center"><strong>🌐 Language / 语言</strong></p>
<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/ENGLISH-1f6feb?style=for-the-badge" alt="English" height="44"></a>&nbsp;&nbsp;
  <a href="README.zh-CN.md"><img src="https://img.shields.io/badge/%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-d73a49?style=for-the-badge" alt="简体中文" height="44"></a>
</p>

**独立、非官方的 Microduck 研究、逆向分析、仿真与技术资料整理项目。**

OpenMicroDuck 将已经公开的 **Microduck** 技术信息整理成容易阅读、来源可追溯的工程参考资料。重点覆盖公开硬件、BOM 研究、机械结构、电控、机载软件、仿真、强化学习、Sim-to-real 参数以及社区可复现的逆向分析。

> OpenMicroDuck 与 Pollen Robotics、Hugging Face 不存在隶属、授权、赞助或官方合作关系。Microduck 及其相关名称、Logo、商标和品牌资产归各自权利人所有。

本项目**不声称 Microduck 是开源硬件**。Pollen Robotics 已明确说明，“开源”针对软件栈；机械与电子设计文件并未作为开源硬件发布。

## 第一次看 Microduck？从这里开始

OpenMicroDuck 的目录现在按“普通人先看懂，再逐步深入”的方式组织，不需要第一天同时学会机器人学、强化学习和电路。

| 如果你想…… | 第一篇先看…… |
|---|---|
| 几分钟看懂整个项目 | [从这里开始](docs/zh-CN/getting-started/README.md) |
| 不买硬件，先让 Microduck 在电脑里动起来 | [第一步先做仿真](docs/zh-CN/getting-started/simulation-first.md) |
| 按阶段规划公开研究复现 | [公开复现路线图](docs/zh-CN/getting-started/public-reproduction-roadmap.md) |
| 查 Motor ID、Home Pose、Mass、Bus / IMU / Battery 参数 | [硬件参数总表](docs/zh-CN/hardware/parameter-reference.md) |
| 看懂结构件怎么连接、怎么装 | [结构与装配地图](docs/zh-CN/hardware/structure-and-assembly-map.md) |
| 查 BAM、Delay、Backlash、Voltage、Domain Randomization | [Sim-to-real 参数总表](docs/zh-CN/simulation/sim-to-real-parameter-reference.md) |

推荐的公开研究顺序：

```text
官方 Model + 现成 ONNX 先在 Simulation 跑起来
                 ↓
看懂 Joint / Mass / Structure
                 ↓
复现一个 Training Task
                 ↓
看懂 50 Hz Bus + IMU Dataflow
                 ↓
做小型 Hardware Bench
                 ↓
验证机械子组件
                 ↓
完整实体研究样机 + Sim-to-real 对比
```

## 先记住 4 个数字，就能看懂大半架构

| 数字 | 代表什么 |
|---:|---|
| **15** | 当前 Runtime 中的物理 Motor ID 数量，包括嘴/喙电机 |
| **14** | Locomotion RL Policy 控制的关节数量 |
| **61** | 当前 Policy Family 共用的 Actor Observation 宽度 |
| **50 Hz** | Locomotion Policy / Runtime 控制频率 |

## 已确认器件速览

只要公开资料能够确认到具体型号，这里就直接写出器件名。表中的“开发/参考平台”表示该器件能从当前官方源码或 Hardware Bring-up 文档直接确认，但不等于官方承诺最终量产版本永远使用同一料号。

| 子系统 | 已确认器件 | 状态 |
|---|---|---|
| 主控开发板 | **Radxa Zero 3W** | 官方源码中的当前开发/参考平台 |
| 主控 SoC | **Rockchip RK3566** | 官方产品规格 |
| 内存 / 存储 | **1 GB RAM / 32 GB 存储** | 官方产品规格 |
| 执行器 | **ROBOTIS Dynamixel XL330 ×15** | 官方源码；XL330 具体子型号尚未明确固定 |
| 主控制 IMU | **ST LSM6DSV16X**，位于 **`imu_to_dxl` v2** | 官方源码 |
| Audio Codec | **Texas Instruments TLV320AIC3104** | 官方源码中的开发硬件 |
| HAT 第二颗 IMU | **Bosch BMI088** | 官方源码中的开发硬件；当前标注 Dormant / Unused |
| 前置 Camera | **Sony IMX219 / Raspberry Pi Camera v2 Path** | 官方源码中的开发硬件 |
| 8×8 ToF | **ST VL53L5CX / VL53L8CX Family Support** | 官方源码；最终量产准确型号仍待确认 |
| Battery | **NP-F550，2600 mAh** | 官方产品规格 |
| NFC | **2 个天线：Head + Beak** | 官方产品规格；Controller IC 未公开 |
| Audio Transducer | Microphone + Speaker | 官方产品规格；准确料号未公开 |

## 文档地图

### 新手 / 公开复现入口

- [从这里开始](docs/zh-CN/getting-started/README.md)
- [第一步先做仿真](docs/zh-CN/getting-started/simulation-first.md)
- [公开复现路线图](docs/zh-CN/getting-started/public-reproduction-roadmap.md)

### 硬件与机械

- [硬件参数总表](docs/zh-CN/hardware/parameter-reference.md)
- [结构与装配地图](docs/zh-CN/hardware/structure-and-assembly-map.md)
- [公开硬件清单与 BOM 状态](docs/zh-CN/hardware/public-bom.md)
- [社区推导 BOM、紧固件、轴承与装配重建](docs/zh-CN/hardware/community-bom-reconstruction.md)
- [机械结构与运动学](docs/zh-CN/hardware/mechanical-structure.md)
- [电控、总线、传感器与电源](docs/zh-CN/hardware/electronics-and-buses.md)
- [公开器件 Datasheet 与官方资料索引](docs/zh-CN/hardware/component-datasheets.md)

### 软件、控制、仿真与训练

- [控制循环与传感器数据流](docs/zh-CN/software/control-loop-and-sensor-dataflow.md)
- [机载运行时架构](docs/zh-CN/software/runtime-architecture.md)
- [仿真与强化学习](docs/zh-CN/simulation/model-and-rl.md)
- [技能、Policy 与运行时切换](docs/zh-CN/simulation/policy-catalog-and-switching.md)
- [可复现训练与 ONNX 导出](docs/zh-CN/simulation/reproducible-training-and-export.md)
- [仿真模型资产参考](docs/zh-CN/simulation/model-assets-reference.md)
- [Sim-to-real 参数总表](docs/zh-CN/simulation/sim-to-real-parameter-reference.md)

### 研究状态、社区与来源

- [官方规格基线](docs/zh-CN/product/official-specifications.md)
- [待确认问题与来源冲突](docs/zh-CN/research/open-questions-and-conflicts.md)
- [上游版本基线](docs/zh-CN/upstream/version-matrix.md)
- [已审查的逆向分析与社区项目](docs/zh-CN/ecosystem/reverse-engineering-projects.md)
- [资料来源与证据地图](docs/zh-CN/sources.md)
- [研究规范](docs/zh-CN/research-guidelines.md)
- [来源与许可证](docs/zh-CN/legal/provenance-and-licenses.md)
- [完整中文文档索引](docs/zh-CN/README.md)

## 证据规则

技术结论必须区分：

- **官方产品规格**：产品页、Press Kit、商店等公开产品级事实；
- **官方源码**：能从上游源码或设计文档直接确认；
- **官方仿真模型**：公开 Simulation Asset 中的参数 / Geometry，不自动等于量产实体测量值；
- **社区重建**：第三方根据公开资产或观察独立推导；
- **Measured / 实测**：记录测试条件、可重复的真实 Hardware Measurement；
- **Unresolved / Provisional**：当前证据不足，不能写成最终量产事实。

不同来源发生冲突时，应保留冲突记录，而不是把推断静默改写成“官方规格”。

## 语言与目录结构

英文是仓库默认语言；简体中文不是摘要，而是与英文并列维护的主要文档语言。

```text
open-microduck/
├── README.md
├── README.zh-CN.md
└── docs/
    ├── en/
    │   ├── getting-started/   新手 / 公开复现路线
    │   ├── product/           官方产品基线
    │   ├── hardware/          器件、机械、Bus、参数
    │   ├── software/          Runtime 与控制
    │   ├── simulation/        Model、RL、Sim-to-real
    │   ├── research/          待确认问题
    │   ├── ecosystem/         社区项目
    │   ├── upstream/          上游版本快照
    │   └── legal/             来源 / License
    └── zh-CN/                 与英文对应的简体中文文档树
```

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

本仓库目前尚未选择统一的 Repository-wide License。第三方资料继续受其原始许可证和限制约束。部分上游 Microduck 3D 模型资产采用 **CC BY-SA-NC**，软件仓库适用各自声明的软件许可证。复制或再分发第三方资产前，请先查看来源与许可说明。

---

**搜索关键词：** Microduck、Microduck 逆向、Microduck 逆向分析、Microduck 硬件、Microduck BOM、Microduck 电子元器件、Microduck 拆解、Microduck CAD、Microduck 仿真、Microduck 强化学习、Microduck RL、Dynamixel XL330、LSM6DSV16X、Radxa Zero 3W、Microduck robot model、Microduck sim-to-real.
