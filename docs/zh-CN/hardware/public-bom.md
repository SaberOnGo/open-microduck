# 公开硬件清单 / BOM 状态

> 状态：基于公开来源整理，最近检查时间 2026-08-31。

Microduck 目前**没有官方公开的完整硬件 BOM**。Pollen Robotics 在 Press Kit 中明确说明：其“开源”表述针对软件栈，机械与电子设计文件并未作为开源硬件发布。

因此本文使用“**公开硬件清单**”而不是“官方 BOM”。每一项都标注证据等级。

## 证据等级

- **官方产品规格**：Pollen Robotics / Hugging Face 正式公开的产品或 Press Kit 信息。
- **官方源码**：能够从 Pollen Robotics 官方源码、配置、仿真模型或硬件 bring-up 文档中直接确认。
- **社区重建**：第三方根据公开资产独立推导，具有参考价值，但不等于官方规格。
- **暂定**：出现在当前开发资料中，但不一定代表最终量产选型。

## 公开硬件清单

| 子系统 | 已公开的部件 / 属性 | 证据 | 说明 |
|---|---|---|---|
| 整机尺寸 | 高 25 cm、宽 14 cm | 官方产品规格 | 来自 Press Kit。 |
| 整机质量 | 低于 800 g | 官方产品规格 | 官方 RL 仓库描述约 800 g；第三方从模型求出的更精确数字不能等同于量产实测重量。 |
| 主控 SoC | Rockchip RK3566，带 AI 加速器 | 官方产品规格 | Press Kit 同时列出 1 GB RAM、32 GB 存储。 |
| 当前开发板 | Radxa Zero 3 / Zero 3W | 官方源码、暂定 | 官方硬件 bring-up / 部署文档使用 Radxa Zero 3/3W；部分设计文档曾明确称该开发板选择为 provisional，因此要与最终产品的 RK3566 规格区分。 |
| 电机数量 | 15 个 | 官方产品规格 | 官方运行时模型为：左腿 5 + 颈/头/嘴 5 + 右腿 5。 |
| 舵机系列 | Dynamixel XL330 | 官方源码 | 官方 RL 使用针对 Dynamixel XL330 的 BAM 执行器模型，MJCF 中也有 XL330 几何。 |
| 策略控制关节 | 14 个 | 官方源码 | 左腿 5 + 颈/头 4 + 右腿 5；嘴是第 15 个电机，不进入运动策略 action vector。 |
| 喙 / 嘴 | 可动、可抓取 | 官方产品规格 + 源码 | 运行时源码有独立 mouth joint 以及开合范围处理。 |
| 主控制 IMU | `imu_to_dxl` v2 上的 LSM6DSV16X | 官方源码 | `duck-control` 明确解码该器件，并与 Dynamixel 总线一起读取。 |
| IMU 总数 | 2 个：机身 + 头部 | 官方产品规格 | Press Kit 未完整公开两颗量产 IMU 的具体芯片型号，不应把开发板上的所有 IMU 自动当成最终量产料号。 |
| 测距 | 紧凑型 8×8 ToF 阵列 | 官方产品规格 | 官方源码同时包含 ST VL53L5CX / VL53L8CX 支持；最终量产具体型号在官方固定前应视为未确认。 |
| 摄像头 | 前置摄像头 | 官方产品规格 | Press Kit 明确写着分辨率/FOV 仍在最终确定；当前 Radxa Zero 3W bring-up 使用 Raspberry Pi Camera v2 / IMX219 路径。 |
| 音频 | 麦克风 + 扬声器 | 官方产品规格 | 当前官方源码中包含 TLV320AIC3104 的开发硬件支持。 |
| NFC | 2 个天线：头部 + 喙部 | 官方产品规格 | 用于 NFC 标签触发交互。 |
| 无线连接 | Wi-Fi + Bluetooth | 官方产品规格 | 官方运行时包含 BLE 配网/手柄，以及网络/WebRTC 相关模块。 |
| 电池 | 可拆卸 NP-F550 摄像机电池，2600 mAh | 官方产品规格 | 续航约 1 小时，取决于使用情况。官方控制源码描述了 2S Li-ion 的可用电压范围，并通过舵机总线读取供电电压。 |
| 轮滑附件 | 可选被动滚轮 | 官方产品/配件信息 + RL 资产 | 官方 RL 仓库有独立 roller 模型，被动轮关节不进入策略执行器集合。 |
| 轴承 / 紧固件 | 官方没有 BOM | 社区重建 | 公开仿真网格里可看到轴承几何与孔特征；第三方已根据模型反推大致轴承与 M2 紧固件体系。量产实物验证前都应保留“模型推导”标签。 |
| 自制 PCB | 开发/参考资产中能够确认存在，但原理图未公开 | 官方源码 + 社区重建 | 官方源码能够暴露接口与设备行为，但目前没有公开完整量产 PCB BOM / 原理图。 |

## 当前官方运行时中的电机 ID

官方 `duck-control/src/model.rs` 定义了 15 个 Dynamixel ID：

```text
左腿          20 21 22 23 24
颈/头/嘴      30 31 32 33 34
右腿          10 11 12 13 14
IMU 板        200（不是电机）
```

同一源码明确说明：嘴位于 index 9，并有意从 14 维策略动作输出中跳过。

## 哪些内容不能写成“官方 BOM”

社区项目已经从公开 MJCF/STL、源码和几何中推导出很多有价值的信息，例如：精确紧固件数量、轴承数量、PCB 外形尺寸、内部支架几何、装配顺序等。

这些结论可以用于研究，但除非 Pollen Robotics 官方确认，或在量产实机上进行了可复现测量，否则在 OpenMicroDuck 中必须继续标为**社区重建**。

## 已知冲突 / 变化中的信息

### 电池模型几何与正式产品电池

部分公开仿真资产和第三方仓库中存在 `NP-F970` 命名的网格，或讨论 F970 兼容几何；但 2026 年官方 Press Kit 明确写的是**可拆卸 NP-F550、2600 mAh**。因此本项目把 NP-F550 作为产品规格，把 F970 相关内容仅作为模型/开发阶段证据。

### 摄像头与 ToF 的具体芯片

Press Kit 明确写着摄像头分辨率/FOV、LiDAR 测距范围仍在最终确定。当前官方源码中确实存在 IMX219 和 ST 多区 ToF 的具体驱动/bring-up，但这些开发选择不能自动提升为永久不变的量产 BOM。

### 精确整机重量

官方产品口径是“低于 800 g”，官方 RL 仓库写“约 800 g”。第三方从公开 MJCF 中计算出的精确模型质量属于仿真资产结果，不等同于生产实机上秤。

## 主要官方来源

- https://pollen-robotics.com/microduck/press-kit/
- https://pollen-robotics.com/microduck/
- https://github.com/pollen-robotics/microduck
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/model.rs
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/imu.rs
- https://github.com/pollen-robotics/microduck_rl

## 社区重建参考

- https://github.com/fanhao375/microduck-replica
- https://github.com/boris721/microduck-3d

更多项目见：[社区逆向项目索引](../ecosystem/reverse-engineering-projects.md)。
