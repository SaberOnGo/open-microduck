# 公开硬件清单 / BOM 状态

[English](../../en/hardware/public-bom.md) | **简体中文**

> 状态：基于公开来源整理，最近检查时间 2026-08-31。

Microduck 目前**没有官方公开的完整硬件 BOM**。Pollen Robotics 已明确说明：“开源”针对软件栈，机械与电子设计文件并未作为开源硬件发布。

因此本文严格区分：**官方产品规格**、**官方源码中的开发硬件**、**社区重建**和**尚未确认的量产料号**。

## 证据等级

- **官方产品规格**：Pollen Robotics / Hugging Face 产品页、商店、Press Kit 等正式公开信息。
- **官方源码**：能够从官方源码、配置、仿真资产或硬件 bring-up 文档中直接确认。
- **社区重建**：第三方根据公开资产独立推导，具有参考价值，但不是官方量产 BOM。
- **未确认**：子系统已经公开，但具体量产料号尚未固定或未被公开。

## 明确器件清单

| 子系统 | 器件 / 料号 | 数量 / 细节 | 证据 | 状态 / 说明 |
|---|---|---:|---|---|
| 主控开发板 | **Radxa Zero 3W** | 1 | 官方源码 | 当前官方 bring-up / 参考平台。产品级规格明确的是 RK3566，不代表以后任何 revision 都必须使用同一载板。 |
| 主控 SoC | **Rockchip RK3566** | 1 | 官方产品规格 | 带 AI 加速器。 |
| 内存 | **1 GB RAM** | 1 | 官方产品规格 | 具体 DRAM 芯片未公开。 |
| 存储 | **32 GB** | 1 | 官方产品规格 | 具体 Flash/eMMC 料号未公开。 |
| 关节执行器 | **ROBOTIS Dynamixel XL330** | **15** | 官方源码 + 官方产品规格 | 官方 Microduck 源码没有明确固定 XL330 的具体子型号（如 M077/M288），不能把社区猜测直接写成官方 BOM。 |
| 主控制 IMU | **STMicroelectronics LSM6DSV16X** | 1 | 官方源码 | 位于定制 **`imu_to_dxl` v2** 板；Dynamixel 设备 ID 为 200。 |
| IMU bridge 板 | **`imu_to_dxl` v2** | 1 | 官方源码 | 定制板；完整原理图/BOM 未公开。 |
| Robot HAT | **Pollen Robotics RPI Robot HAT** | 1 | 官方源码 | 当前开发/参考定制板；完整原理图/BOM 未公开。 |
| HAT 音频 Codec | **Texas Instruments TLV320AIC3104** | 1 | 官方源码 | I2C 地址 **0x18**；I2S 音频；当前 overlay 中 codec MCLK 为 12 MHz。 |
| HAT 第二颗 IMU | **Bosch BMI088** | 1 | 官方源码 | 开发 HAT 中地址 **0x19 / 0x68**；官方源码注释明确写为 dormant / unused。 |
| 前置摄像头 | **Sony IMX219 / Raspberry Pi Camera v2 路径** | 1 | 官方源码 | 当前 Radxa 媒体 bring-up 路径；量产分辨率/FOV 仍属 provisional。 |
| ToF | **ST VL53L5CX / VL53L8CX 系列** | 1 | 官方源码 | 官方源码同时支持两代器件；官方产品只承诺 8×8 ToF 阵列，量产具体型号尚未确认。 |
| ToF 总线地址 | **0x29** | 1 | 官方源码 | 当前开发硬件通过 Robot HAT / Stemma 路径连接。 |
| 电池 | **NP-F550 摄像机电池，2600 mAh** | 1 | 官方产品规格 | 可拆卸；根据使用情况约 1 小时续航。 |
| NFC 天线 | 头部 + 喙部 | **2** | 官方产品规格 | NFC 控制/收发芯片具体料号未公开。 |
| 麦克风 | 未公开具体料号 | 多个 | 官方产品规格 | 只确认 Microphones。 |
| 扬声器 | 未公开具体料号 | 1 | 官方产品规格 | 只确认 Speaker。 |
| 无线连接 | Wi-Fi + Bluetooth | 板载 | 官方产品规格 | 当前 Radxa Zero 3W 提供相关能力；量产最终无线芯片未被产品资料单独固定。 |
| 摄像头使用指示灯 | REC 风格专用指示 | 1 | 官方产品规格 | 具体 LED/驱动器件未公开。 |
| 被动轮滑附件 | Roller assemblies | 可选 | 官方产品/配件信息 + 官方 RL 资产 | roller MJCF 中存在被动轮关节。 |

## 产品级尺寸与重量

| 项目 | 公开数值 | 状态 |
|---|---:|---|
| 高度 | **25 cm** | 官方产品规格 |
| 宽度 | **14 cm** | 官方产品规格 |
| 重量 | Press Kit 写 **under 800 g**；当前官方商店写 **780 g** | 两者都是官方值；商店值更具体，Press Kit 保留更宽口径 |
| 电机 / DoF | **15** | 官方产品规格 |
| 策略控制频率 | **50 Hz** | 官方产品/官方源码 |

## 电机与设备 ID

当前官方运行时定义：

```text
左腿           20 21 22 23 24
颈/头/嘴       30 31 32 33 34
右腿           10 11 12 13 14
imu_to_dxl      200
```

嘴部是 motor index 9，并被有意排除在 14 维 locomotion policy action 之外。因此 Microduck 是**15 个电机，但 RL action 是 14 维**。

## 当前开发 HAT 已经能够明确到的电子器件

官方 `i2c3-pihat.dts` 与 `aic3104-i2c3.dts` 暴露了非常具体的开发硬件信息：

| 项目 | 官方源码可见值 |
|---|---|
| 主控板兼容标识 | `radxa,zero-3w`, `rockchip,rk3566` |
| HAT I2C 控制器 | RK3566 **I2C3 M0**，header pin 3/5 |
| I2C 频率 | **400 kHz** |
| 音频 Codec | **TLV320AIC3104**，地址 **0x18** |
| HAT IMU | **BMI088**，地址 **0x19 / 0x68**，当前标注 dormant/unused |
| ToF | 地址 **0x29**，经 Stemma J5 路径 |
| 音频 MCLK | **12 MHz** 固定时钟 |
| I2S CPU 侧时钟 | 当前 overlay 为 **12.288 MHz** |
| 源码注释中明确的上拉 | **R12/R13，一对 10 kΩ** |

这些数据描述的是**当前官方源码中的开发/参考实现**，不是官方公开的量产原理图。

## 仍未公开或未确认的部分

目前仍不能从公开资料确认完整量产料号的包括：

- XL330 的具体子型号；
- `imu_to_dxl` v2 的 MCU、半双工收发器和完整被动器件 BOM；
- Robot HAT 完整原理图和 PCB BOM；
- VL53L5CX / VL53L8CX 中最终量产到底采用哪一款；
- 最终摄像头模组、镜头和 FOV；
- 两颗量产 IMU 与 body/head 的最终芯片映射；
- NFC 控制芯片；
- 麦克风和扬声器具体型号；
- 量产螺丝长度/数量；
- 轴承数量、供应商和完整料号；
- 线束、连接器和线缆长度。

“未确认”只表示**公开资料没有证实**，不代表机器人里没有这些器件。

## 社区推导的机械 BOM

官方 MJCF/STL 使社区能够进一步推导出：

- 以 **M2** 为主的紧固件体系；
- 大约 **22×16×4 mm** 与 **15×10×3 mm** 的模型轴承几何；
- 从网格孔特征推导的紧固件孔统计；
- 刚体分组、质量和装配变换。

这些信息统一放在独立页面：[社区推导 BOM、紧固件、轴承与装配重建](community-bom-reconstruction.md)，避免与官方规格混淆。

## 已知冲突 / 变化中的信息

### NP-F550 产品规格 vs `NP-F970` 命名模型

部分公开仿真资产中存在 `NP-F970` 命名网格；但官方 launch Press Kit 和官方商店明确写的是 **NP-F550、2600 mAh**。因此 OpenMicroDuck 以 NP-F550 作为产品规格，F970 只保留为模型/开发阶段证据。

### Camera / ToF

Press Kit 明确表示摄像头分辨率/FOV、LiDAR range 仍在最终确定。源码则已经明确到 IMX219、VL53L5CX/VL53L8CX 等开发硬件。**源码更具体，不等于量产 BOM 已经冻结。**

## 主要官方来源

- https://pollen-robotics.com/microduck/press-kit/
- https://pollen-robotics.com/microduck/
- https://store.pollen-robotics.com/products/microduck
- https://github.com/pollen-robotics/microduck
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/model.rs
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/imu.rs
- https://github.com/pollen-robotics/microduck/blob/main/deploy/audio/i2c3-pihat.dts
- https://github.com/pollen-robotics/microduck/blob/main/deploy/audio/aic3104-i2c3.dts
- https://github.com/pollen-robotics/microduck/blob/main/docs/project/media-bringup.md
- https://github.com/pollen-robotics/microduck_rl

## 社区参考

- https://github.com/fanhao375/microduck-replica
- https://github.com/boris721/microduck-3d

更多已审查项目见：[社区逆向项目索引](../ecosystem/reverse-engineering-projects.md)。