# 资料来源与证据地图

> 核心官方来源最近一次核对：2026-09-02。社区仓库发现快照仍为 2026-08-31。

OpenMicroDuck 是一个以来源可追溯为基本原则的公开研究项目。关于 Microduck 的技术结论应尽可能回到官方资料、可复现实验，或明确标注为社区推导。

## 来源优先级

1. **官方产品规格 / Press Kit**：产品级事实和最终公开口径优先来源。
2. **Pollen Robotics 官方源码与文档**：运行时行为、当前接口、开发硬件与实现细节。
3. **官方 RL / 仿真资产**：训练模型、运动学、惯量、碰撞、策略与 sim-to-real recipe。
4. **公开取得实机上的可复现测量**：补充官方没有明确给出的真实硬件行为。
5. **社区重建**：适合派生几何、转换资产、替代实现和待验证假设，但必须保留标签。
6. **媒体 / 二手报道**：用于背景，不覆盖更权威的官方技术来源。

## 当前上游版本快照

本轮版本敏感文档对应到以下公开上游 revision：

| 来源 | 本次核对版本 |
|---|---|
| `pollen-robotics/microduck` `main` | `9f7eaad1008fffd90ef871a33a18aecd066b51a9` |
| `pollen-robotics/microduck_rl` `develop` | `5946fd9cdbc58956424420153e51975af3b30d77` |
| `Rhoban/bam` `main` | `620a64fe67c1afe94fca81da73b128c7aed17c5f` |
| Pollen Robotics 产品页 / Press Kit / Sandbox | 2026-09-02 核对 |

为什么要记录这些版本、以后怎样更新，见[上游版本基线](upstream/version-matrix.md)。

## 官方产品资料

### 产品页

https://pollen-robotics.com/microduck/

主要用于产品定位、主要规格、附件、开源软件说明和 50 Hz policy loop 等。

### Press Kit

https://pollen-robotics.com/microduck/press-kit/

目前最适合引用的产品级规格来源，包括：15 个电机、25 cm × 14 cm、低于 800 g、RK3566 / 1 GB / 32 GB、摄像头、8×8 ToF、两个 IMU、可动喙、音频、NFC、无线连接、NP-F550 2600 mAh，以及“开源仅指软件、不是开源硬件”的明确说明。

Press Kit 还明确列出仍处于 provisional 状态的规格，因此具体 camera/FOV、LiDAR range、radio version 等不应被第三方开发资料提前固定成量产规格。

面向普通读者的产品级整理见 [Microduck 官方规格基线](product/official-specifications.md)。

### 官方浏览器 Sandbox

https://huggingface.co/spaces/pollen-robotics/microduck-simulator

用于新手零安装体验。官方 Space 说明它在浏览器中运行 MuJoCo WebAssembly 和 ONNX Runtime Web，并使用公开的官方 Robot Model 与 Policy。它是仿真体验，不是第三方真机验证。

## 官方机载软件

https://github.com/pollen-robotics/microduck

重点路径：

| 路径 | 主要证据 |
|---|---|
| `README.md` | daemon 架构与 runtime 总览 |
| `duck-control/src/model.rs` | 15 joint ID、mouth index、IMU ID、baud、battery mapping 等 |
| `duck-control/src/imu.rs` | LSM6DSV16X / `imu_to_dxl` v2 数据格式 |
| `deploy/robotd.toml` | 当前串口、50 Hz、策略 contract、runtime/safety 配置 |
| `docs/design/robotd-design.md` | 控制循环、硬件和 Runtime 设计依据 |
| `docs/design/architecture.md` | service boundary 和系统架构 |
| `docs/design/app-path-design.md` | 本地 / Bluetooth / API routing 架构 |
| `docs/project/media-bringup.md` | Radxa/RK3566 当前媒体硬件实测与 bring-up |
| `tof/` | 多区 ToF 支持 |
| `deploy/audio/` | 当前音频 codec / device-tree bring-up |

需要精确复现时应记录 commit SHA，因为官方仓库仍在快速演进。

OpenMicroDuck 的易读整理：

- [机载运行时架构](software/runtime-architecture.md)
- [控制循环与传感器数据流](software/control-loop-and-sensor-dataflow.md)

## 官方 RL / 仿真

https://github.com/pollen-robotics/microduck_rl

重点区域：

| 路径 / 区域 | 主要证据 |
|---|---|
| `README.md` | 训练栈、任务、61-D/14-action、BAM/backlash |
| `src/mjlab_microduck/robot/microduck/` | MJCF、mesh、碰撞、惯量和关节树 |
| `src/mjlab_microduck/robot/microduck_constants.py` | robot/model/actuator 配置常量 |
| `src/mjlab_microduck/actuator/` | BAM、摩擦与随机化 |
| `src/mjlab_microduck/tasks/` | observation、reward、event、domain randomization |
| `scripts/export.py` | 正式 ONNX 导出 |
| `scripts/infer_policy.py` | CPU MuJoCo inference / 对比流程 |

官方 README 当前声明软件为 Apache-2.0，3D model files 为 Creative Commons BY-SA-NC。再分发前仍应检查实际文件与最新 license 状态。

OpenMicroDuck 的整理和教程：

- [仿真与强化学习](simulation/model-and-rl.md)
- [技能、Policy 与运行时切换](simulation/policy-catalog-and-switching.md)
- [可复现训练与 ONNX 导出](simulation/reproducible-training-and-export.md)
- [仿真模型资产参考](simulation/model-assets-reference.md)

## 执行器模型

https://github.com/Rhoban/bam

官方 Microduck RL 用于提高 Dynamixel 执行器仿真 fidelity。

## 器件原厂 / 官方平台资料

对于已经有公开 Microduck 证据支持的 RK3566 / Radxa Zero 3W、Dynamixel XL330、LSM6DSV16X、BMI088、TLV320AIC3104、IMX219 / Raspberry Pi camera path、VL53L5CX / VL53L8CX 等器件，见[公开器件 Datasheet 与官方资料索引](hardware/component-datasheets.md)。

需要注意：原厂 Datasheet 说明器件“能做什么”；要证明 Microduck 实际怎样配置这个器件，仍然应该回到 Microduck 官方源码。

## 已检查的社区来源

- https://github.com/fanhao375/microduck-replica
- https://github.com/boris721/microduck-3d
- https://github.com/IronSpiderMan/MicroDuckModels
- https://github.com/kabilankb/isaaclab-microduck
- https://github.com/Macmachi/microduck-rl-genesis
- https://github.com/APX103/mjx_microduck
- https://github.com/craigm26/duckkit
- https://github.com/kgediya/specs-microduck

详细用途和 caveat 见 [逆向分析与社区项目索引](ecosystem/reverse-engineering-projects.md)。

## OpenMicroDuck 证据标签

- **官方产品规格**：官方当前产品口径；
- **官方源码**：可在官方代码/文档/模型中直接验证；
- **Measured**：有条件说明的物理实测；
- **Observed**：黑盒、拆解、协议等直接观察；
- **社区重建 / Inferred**：由公开证据推导但未获官方确认；
- **Assumed**：研究中的临时假设；
- **Provisional**：官方或源码中存在，但明确尚未最终冻结。

## 来源冲突怎么处理

发现冲突时：

1. 先判断是否来自不同 revision；
2. 区分产品规格、开发实现和仿真资产；
3. 比较日期/commit；
4. 无法消除时把冲突保留下来；
5. 绝不把第三方推导静默写成“官方规格”。

本仓库已记录的例子包括：正式 NP-F550 电池规格与 F970 命名的仿真几何、Press Kit 与商店页面重量精度差异，以及尚未冻结的 camera/ToF 产品规格与当前开发驱动之间的区别。

持续维护的未确认清单见[待确认问题与来源冲突](research/open-questions-and-conflicts.md)。

## 可复现性说明

URL 适合找到可读来源；但凡结论依赖具体代码、模型或参数，最好同时记录 Git commit SHA。Microduck 目前仍处在快速开发期，`main` / `develop` 后续都会继续变化。
