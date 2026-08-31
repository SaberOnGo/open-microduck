# Microduck 官方规格基线

[English](../../en/product/official-specifications.md) | **简体中文**

> 来源等级：**官方产品规格**。最近核对：**2026-08-31**。

这份文档只回答一个简单问题：**Pollen Robotics 目前已经公开确认了 Microduck 的哪些产品级信息？**

这里不会把社区逆向结果、开发板细节、仿真模型参数混进“官方规格”里。那些内容会放到硬件、仿真和研究文档中分别说明。

## 一眼看懂

| 项目 | 官方公开信息 |
|---|---|
| 类型 | 面向 Physical AI、强化学习、教育和互动的小型双足机器人 |
| 电机 / 自由度 | **15** |
| 高度 | **25 cm** |
| 宽度 | **14 cm** |
| 重量 | Press Kit 写 **低于 800 g**；官方商店当前列出 **780 g** |
| 主计算平台 | **Rockchip RK3566**，带 AI accelerator |
| 内存 | **1 GB RAM** |
| 存储 | **32 GB** |
| Policy 控制循环 | **50 Hz** |
| 摄像头 | 前置摄像头，并带专门的摄像头使用指示灯 |
| 距离 / 深度传感器 | 紧凑型 **8×8 Time-of-Flight** LiDAR / ToF 矩阵 |
| IMU | **2 个**，机身一个、头部一个 |
| 鸟嘴 | 可活动、可抓取物体 |
| 音频 | 麦克风和扬声器 |
| NFC | **2 个天线**，头部一个、鸟嘴一个 |
| 无线连接 | Wi-Fi、Bluetooth |
| 电池 | 可拆卸 **NP-F550**，**2600 mAh**，续航约 1 小时，取决于使用情况 |
| 控制器 | 随机附带 game controller |

## “Open source” 在这里具体指什么

Pollen Robotics 已明确说明，Microduck 的开源范围是**软件栈**，包括机器人控制软件、仿真环境、强化学习训练工具以及 sim-to-real 工作流。

官方 Press Kit 同时明确说明：**机械设计文件和电子设计文件并没有作为 open-source hardware 发布。**

因此 OpenMicroDuck 采用下面的表述：

- **官方开源软件**：是；
- **官方开源硬件设计**：不是；
- 即使公开仓库中存在仿真 mesh、MJCF 或结构模型，也不能把它们描述成官方量产 CAD / 完整 BOM。

## 官方公开描述的能力

官方发布资料展示或描述了 Microduck 的多种行为，例如：

- 行走；
- 坐下 / 蹲下；
- 从常见跌倒姿态重新站起；
- 使用 roller 滑行；
- 用鸟嘴拾取物体。

这些功能并不等于“一个神经网络负责全部动作”。官方 RL 项目实际上包含多个 task / policy family，并通过统一的部署接口切换。详见[技能、Policy 与切换机制](../simulation/policy-catalog-and-switching.md)。

## 目前仍未最终确定的规格

官方 Press Kit 明确标注，下面这些信息仍在 finalizing：

- 摄像头分辨率；
- 摄像头视场角（FOV）；
- LiDAR / ToF 测距范围；
- 无线 radio version；
- SDK language；
- 年龄建议。

在官方给出最终值之前，这些项目都应该继续标注为 **provisional / 未最终确定**。

## 产品规格、源码实现、仿真模型之间怎么区分

阅读 OpenMicroDuck 时，可以用下面这个简单规则：

```text
产品页 / Press Kit
        ↓
官方承诺的产品级规格

当前官方源码 / bring-up 文件
        ↓
当前开发实现实际使用的硬件与软件

仿真资产
        ↓
训练模型里使用的结构和参数

社区重建
        ↓
第三方根据公开证据推导出的结果
```

这四类信息都很有价值，但不能混为一谈。

例如，官方产品规格确认了 RK3566；当前官方源码还显示 Radxa Zero 3W 是开发 / 参考平台之一。但这并不能自动推出“以后所有量产版本永远固定使用同一块载板”。

## 主要官方来源

- https://pollen-robotics.com/microduck/
- https://pollen-robotics.com/microduck/press-kit/
- https://store.pollen-robotics.com/products/microduck
- https://github.com/pollen-robotics/microduck
- https://github.com/pollen-robotics/microduck_rl

## OpenMicroDuck 相关页面

- [公开硬件清单与 BOM 状态](../hardware/public-bom.md)
- [电控、总线、传感器与电源](../hardware/electronics-and-buses.md)
- [机械结构与运动学](../hardware/mechanical-structure.md)
- [资料来源与证据地图](../sources.md)
