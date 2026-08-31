# 从这里开始：普通人也能看懂的 Microduck

[English](../../en/getting-started/README.md) | **简体中文**

> 这里只整理公开、可追溯的资料。这一页不要求读者先懂机器人、强化学习或 Linux。

## 先用一张图看懂整台机器人

```text
                 真实机器人硬件
        结构 + 电机 + 电池 + 各种传感器
                         │
                         ▼
                       感知
          Camera / ToF / IMU / 关节状态
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
          看懂外部环境            看懂自己身体
         视觉 / ToF 几何          关节 / IMU
              │                     │
              └──────────┬──────────┘
                         ▼
                    高层行为判断
             “往那里走 / 看左边 / 踢球”
                         │
                         ▼
                      运动 AI
              61 个输入 → ONNX → 14 个动作
                         │
                         ▼
                 安全处理 + 电机控制
                         │
                         ▼
                      15 个电机
```

仿真主要是在没有真实硬件时，先把“运动 AI + 机器人模型”这一段跑通。

## 哪些地方用了 AI？

不是所有东西都是 AI：

- **Camera 目标检测**：用了 AI 模型。
- **ToF 深度处理**：主要是普通几何和过滤算法。
- **高层自主行为**：旧版主要是状态机 + 规则；新的 daemon 架构还没有完整迁移完。
- **走路、站立、翻滚等运动**：使用强化学习 Policy，导出成 ONNX。
- **电机总线、安全、更新、网络**：普通软件代码。

所以不能把“机器人上有 Camera / ToF”理解成“Walking AI 直接在看图像和深度图”。

## 先记住 4 个数字

| 数字 | 代表什么 |
|---:|---|
| **15** | 当前 Runtime 中的物理电机 ID，包括嘴/喙电机 |
| **14** | 运动 Policy 控制的关节数量 |
| **61** | 当前运动 Policy 共用的输入宽度 |
| **50 Hz** | 运动控制频率：每 20 ms 一轮 |

## 按目的选入口

| 你想做什么 | 先看这一页 |
|---|---|
| 先让虚拟 Microduck 动起来 | [第一步先做仿真](simulation-first.md) |
| 看懂整套软件怎么配合 | [Microduck 软件架构：一眼看懂](../software/runtime-architecture.md) |
| 看懂 50 Hz 运动控制 | [控制循环：Microduck 到底怎么动起来](../software/control-loop-and-sensor-dataflow.md) |
| 查硬件参数 | [硬件参数总表](../hardware/parameter-reference.md) |
| 看懂结构怎么装 | [结构与装配地图](../hardware/structure-and-assembly-map.md) |
| 按阶段做公开复现 | [公开复现路线图](public-reproduction-roadmap.md) |
| 训练或修改运动 Policy | [可复现训练与 ONNX 导出](../simulation/reproducible-training-and-export.md) |
| 查 Sim-to-real 参数 | [Sim-to-real 参数总表](../simulation/sim-to-real-parameter-reference.md) |

## 推荐的公开复现顺序

不要把“做一台 Microduck”当成一个大任务。更容易排错的顺序是：

```text
1. 官方机器人模型 + 现成 ONNX 先在仿真里跑起来
2. 看懂关节、质量和结构
3. 复现一个训练任务
4. 看懂真实机器人的 50 Hz 电机 + IMU 控制
5. 单独测试小块硬件
6. 验证机械子组件
7. 再做完整研究样机
8. 最后比较仿真和真机差异
```

仿真先做，是因为可以先确认机器人模型、关节顺序、Policy 接口和控制逻辑。以后真机出问题时，就不会把机械、电路、软件和 RL 问题混在一起。

## 哪些公开信息已经比较清楚？

目前公开资料已经能比较明确地说明：

- 14 个 Policy 关节和 15 个 Runtime 电机 ID；
- Home Pose 和仿真关节范围；
- 50 Hz 控制流程和 1 Mbps 电机总线；
- 主控制 IMU 数据路径；
- 61 维运动 Policy 接口；
- 官方 MuJoCo 模型、RL Task 和大量 Sim-to-real 参数；
- Camera、ToF、运动学和当前机载软件架构；
- 大量公开 Mesh、刚体质量和装配变换。

## 哪些还不能当成完整量产资料？

目前公开证据仍不足的包括：

- 完整量产原理图和 PCB BOM；
- 最终线束长度、连接器和走线；
- 如果官方仍在调整，最终 Camera / Lens / FOV；
- 如果仍支持多个候选器件，最终量产 ToF 型号；
- 完整量产螺丝表、材料和制造公差；
- 完整生产装配工艺。

没有公开证据的地方继续标记为未知，不靠猜测补齐。

## 证据标签

| 标签 | 含义 |
|---|---|
| **官方产品规格** | Pollen Robotics 明确公布的产品级事实 |
| **官方源码** | 官方代码或文档中可以直接验证 |
| **官方仿真模型** | 来自官方 Simulation Asset，不自动等于量产实体测量 |
| **社区重建** | 第三方根据公开资料推导 |
| **Measured / 实测** | 有测试条件、可重复的真实硬件测量 |
| **Unresolved / 待确认** | 当前公开证据不足 |

## 当前参数整理使用的上游版本

- `pollen-robotics/microduck` main：`590b986bd8c0d50ae02cb3ea2f59c463b6828168`
- `pollen-robotics/microduck_rl` develop：`d424a0c899f6b33cbd3daeb279913134349c0b63`
- `Rhoban/bam` main：`620a64fe67c1afe94fca81da73b128c7aed17c5f`

版本敏感信息见：[上游版本基线](../upstream/version-matrix.md)。
