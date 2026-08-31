# 待确认问题与来源冲突

[English](../../en/research/open-questions-and-conflicts.md) | **简体中文**

> 这份文档专门记录公开来源**目前还不能确认的内容**。“未知”表示“公开证据还不足”，不代表机器人里没有这个东西。

公开研究最容易犯的错误之一，就是看到资料有空白，就用一个“看起来合理”的猜测把它补满。

OpenMicroDuck 反过来做：**不确定的就明确写不确定，直到出现更强的公开来源。**

## 当前还没有完全确认的硬件细节

| 主题 | 公开来源已经能确认什么 | 还不能确认什么 |
|---|---|---|
| XL330 舵机子型号 | 官方源码确认使用 Dynamixel XL330 family | 最终量产到底固定为哪个具体 sub-variant，目前没有清晰官方完整 BOM |
| 主计算载板 | 当前官方源码把 Radxa Zero 3W 作为开发 / 参考平台；产品级确认 RK3566 | 是否所有量产 revision 永远固定使用同一块 carrier board |
| Camera | 当前开发路径能看到 IMX219 / Raspberry Pi Camera v2 风格 bring-up | 最终量产 module、lens、resolution、FOV；官方 Press Kit 仍把 resolution/FOV 标为 provisional |
| ToF | 官方源码支持 VL53L5CX / VL53L8CX family；产品级确认 8×8 ToF matrix | 最终量产 sensor model 和最终 range；range 仍是 provisional |
| 第二个 IMU | 产品级确认 2 个 IMU，机身和头部各一个；源码能看到 LSM6DSV16X control IMU，以及开发 HAT 中的 BMI088 | 两个 IMU 最终量产映射和实现方式 |
| Robot HAT | 官方源码能确认 Pollen Robotics RPI Robot HAT 以及部分挂载器件 | 完整量产 schematic 和 BOM |
| `imu_to_dxl` v2 | 官方源码确认这个 board 以及它在控制链路中的作用 | 完整 schematic、MCU/transceiver/passive BOM |
| NFC | 产品级确认两个 NFC antenna | 最终 controller/transceiver IC 和实现方式 |
| Audio | 产品级确认 microphones 和 speaker；开发源码能看到 TLV320AIC3104 codec path | 最终 microphone/speaker part number 和完整量产音频 BOM |
| 螺丝 / 轴承 | 公共 mesh 与社区研究能给出很有价值的几何推导 | 最终量产长度、数量、材料/等级、供应商件号 |
| Wiring | 公共架构能看出主要连接与总线关系 | 最终量产 harness、connector family、cable length |

## 目前比较重要的来源冲突 / 移动目标

### 产品电池规格 vs 仿真模型命名

官方产品规格明确写的是可拆卸 **NP-F550，2600 mAh**。

但部分 simulation / model asset 中出现过 `NP-F970` 命名的几何模型。

因此 OpenMicroDuck 的处理方式是：

- NP-F550 / 2600 mAh：当前**官方产品规格**；
- F970 命名模型：**仿真 / 开发证据**，不能当作产品 BOM 结论。

### Press Kit 重量 vs 商店重量

官方 Press Kit 写 **under 800 g**，当前官方商店列出 **780 g**。

这并不一定矛盾：

- “under 800 g”是更宽的发布规格；
- “780 g”是当前商店更具体的数值。

两者都可以保留，只要写清来源上下文。

### 产品规格 vs 开发实现

官方开发源码经常会比产品页更具体，但“源码里现在这样做”不等于“未来所有量产版都必须这样做”。

例如：

- Radxa Zero 3W；
- IMX219 camera path；
- VL53L5CX / VL53L8CX support；
- TLV320AIC3104 codec；
- 开发 HAT 描述中的 BMI088。

除非 Pollen Robotics 明确把这些提升为最终产品规格，否则 OpenMicroDuck 应继续标注为：**官方源码中的当前开发实现**。

## Policy 栈里哪些结论也应该绑定版本

有些软件信息虽然是公开的，但仍可能很快变化，例如：

- 最终随机器人出货的 policy 到底有哪些；
- task ID / task variant；
- 一个行为到底包含在组合 policy 里，还是单独 policy；
- domain-randomization range；
- filter / gain 默认值；
- 将来 policy generation 的 observation / command layout。

这些更适合绑定到[上游版本基线](../upstream/version-matrix.md)，不要写成“永远不会变”的机器人事实。

## 一个待确认问题应该怎样被解决

大致按下面的证据优先级：

1. 官方最终产品规格；
2. 官方源码 / 官方文档；
3. 官方仿真资产；
4. 对公开获得的真实硬件进行可复现实测；
5. 有充分方法说明的社区重建；
6. 媒体 / 二手报道。

如果以后新来源出现，应同时更新 English / 简体中文。如果新旧数值属于不同 revision，也应该保留必要的历史背景，而不是把旧结论悄悄覆盖掉。

## 哪些东西不能拿来“补空白”

不能为了把 BOM 或架构补完整，而使用：

- 私有研究笔记；
- 保密 BOM 或供应商资料；
- 未公开采购信息；
- 泄露设计文件；
- 与本项目无关的专有项目资料；
- 先利用私有知识推断，再把结果改写成仿佛来自公开来源的内容。

有时候，一个问题在公开项目里最正确的答案就是：**目前未知。**

## 相关页面

- [公开硬件清单与 BOM 状态](../hardware/public-bom.md)
- [资料来源与证据地图](../sources.md)
- [上游版本基线](../upstream/version-matrix.md)
- [研究规范](../research-guidelines.md)
