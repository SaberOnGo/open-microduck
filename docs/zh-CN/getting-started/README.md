# 从这里开始：用公开资料理解和复现 Microduck

[English](../../en/getting-started/README.md) | **简体中文**

> 这是 OpenMicroDuck 最适合第一次阅读的入口页。这里只使用公开、可追溯的资料。

Microduck 看起来很复杂，是因为很多东西叠在了一起：机械结构、舵机、电路、Linux、仿真、强化学习、摄像头、传感器和机载软件。

最容易理解它的方法，不是一次把所有内容全部学完，而是**一层一层拆开**。

## 先用一张图看懂整个项目

```text
                    Microduck
                        │
          ┌─────────────┼─────────────┐
          │             │             │
        硬件            仿真           软件
          │             │             │
   结构/舵机/IMU      MuJoCo        robotd/Linux
   电源/各种传感器     RL/BAM        ONNX/Policy
          │             │             │
          └─────────────┼─────────────┘
                        │
                    真实机器人运动
```

如果目标是做公开复现或逆向研究，推荐顺序是：

```text
1. 先让官方虚拟机器人在仿真里动起来
2. 看懂机器人模型和关节结构
3. 复现一个官方训练任务
4. 看懂真实机器人的控制总线和传感器数据流
5. 再做小规模硬件测试台
6. 最后才考虑完整的实体研究样机
```

这个顺序非常重要。

因为在仿真里，可以先确认：机器人模型、关节顺序、Policy 接口、执行器模型和 50 Hz 控制流程是不是理解正确。这样以后遇到实体机器人问题时，不会把机械、电路、软件和 RL 问题全部混在一起。

## 按你的目的选择入口

### “我只想先看到 Microduck 在电脑里动起来”

直接看：

- [第一步先做仿真：最快让 Microduck 动起来](simulation-first.md)

这一步**不需要购买机器人硬件**。官方仓库已经公开了 MuJoCo 模型，也公开了可部署的 ONNX Policy。

### “我想把硬件参数先搞清楚”

看：

- [硬件参数总表](../hardware/parameter-reference.md)
- [结构与装配地图](../hardware/structure-and-assembly-map.md)
- [公开硬件清单与 BOM 状态](../hardware/public-bom.md)

这些页面会严格区分：

1. 官方产品规格；
2. 官方源码 / 仿真模型里能直接看到的参数；
3. 社区根据公开资料推导出来的装配结论。

### “我想做一个公开研究用途的复现版本”

看：

- [公开复现路线图](public-reproduction-roadmap.md)

它不会把“做一台 Microduck”当成一个巨大的任务，而是拆成很多可以独立验证的小阶段。

### “我想训练或者修改 Walking Policy”

看：

- [可复现训练与 ONNX 导出](../simulation/reproducible-training-and-export.md)
- [Sim-to-real 参数总表](../simulation/sim-to-real-parameter-reference.md)
- [技能、Policy 与运行时切换](../simulation/policy-catalog-and-switching.md)

### “我想搞懂真实机器人到底怎么控制舵机”

看：

- [控制循环与传感器数据流](../software/control-loop-and-sensor-dataflow.md)
- [机载运行时架构](../software/runtime-architecture.md)

最核心的一句话是：

**Microduck 的低层运动控制是一个 50 Hz 循环。**

每一轮大致做：

```text
读取舵机 + IMU
       ↓
构造 Policy Observation
       ↓
运行 ONNX Policy
       ↓
得到 14 个 Action
       ↓
缩放 / 滤波 / 安全处理
       ↓
给舵机写入新的目标位置
```

## 第一次看，只需要先记住 4 个数字

| 数字 | 代表什么 |
|---:|---|
| **15** | 当前 Runtime 中的物理电机 ID 数量，包括嘴/喙电机 |
| **14** | 当前运动 RL Policy 控制的关节数量；嘴单独控制 |
| **61** | 当前 Policy family 共用的 actor observation 宽度 |
| **50 Hz** | Policy / Runtime 控制频率 |

先记住这四个数字，后面的架构会容易理解很多。

## 哪些东西现在已经比较清楚？

公开资料已经比较完整的包括：

- 官方 MuJoCo 运动学 / 动力学模型；
- 14 个 Policy 关节及其顺序；
- Runtime 中 15 个 Dynamixel ID；
- Home Pose；
- 控制频率和串口总线工作方式；
- `imu_to_dxl` 的数据格式和 LSM6DSV16X 处理方式；
- 官方 RL Task、Domain Randomization 和 BAM 执行器模型；
- ONNX Policy 接口和导出流程；
- 大量公开仿真 Mesh、刚体层级和装配变换。

## 哪些东西现在仍然不能当成“完整量产资料”？

目前公开证据仍不足的包括：

- 完整量产电路原理图和 PCB BOM；
- 最终量产 XL330 的准确子型号；
- 完整量产螺丝清单和每一种精确长度；
- 线束长度、最终连接器和走线方式；
- 如果上游仍在调整，最终 Camera / Lens / FOV 和最终 ToF 型号；
- 完整制造公差、材料、螺纹嵌件和生产装配工艺。

遇到这些内容，应先看：[待确认问题与来源冲突](../research/open-questions-and-conflicts.md)。

## OpenMicroDuck 的证据标签

| 标签 | 含义 |
|---|---|
| **官方产品规格** | Pollen Robotics 明确公布的产品级参数 |
| **官方源码** | 能从官方代码或设计文档直接验证 |
| **官方仿真模型** | 来自官方仿真资产；不等于实体量产测量值 |
| **社区重建** | 第三方根据公开资料推导出来的结果 |
| **Measured / 实测** | 有明确测试条件、可重复的真实硬件测量 |
| **Unresolved / 待确认** | 当前公开证据仍不足 |

## 做逆向研究时，一个非常有用的习惯

不要只问：

> “Microduck 用的到底是什么零件？”

最好拆成四个问题：

```text
官方产品页面承诺了什么？
当前官方源码实际用了什么？
官方仿真模型假设了什么？
社区根据公开资料推导出了什么？
```

把这四层分开，文档才不会把“仿真模型里的东西”误写成“量产 BOM”。

## 本轮文档使用的上游版本

- `pollen-robotics/microduck` main：`590b986bd8c0d50ae02cb3ea2f59c463b6828168`
- `pollen-robotics/microduck_rl` develop：`d424a0c899f6b33cbd3daeb279913134349c0b63`
- `Rhoban/bam` main：`620a64fe67c1afe94fca81da73b128c7aed17c5f`

为什么要记 commit，见：[上游版本基线](../upstream/version-matrix.md)。
