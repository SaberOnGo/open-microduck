# Autonomous Brain：高层行为怎么决定

[English](../../en/software/autonomous-brain.md) | **简体中文**

> 范围：只整理 Microduck 官方公开仓库中的信息。当前新的 daemon 架构还没有把旧版 Autonomous Brain 完整迁移进来，所以本文会区分“当前已实现”和“旧版公开设计”。

## 先看一张图

Microduck 不是用一个“大 AI 模型”把所有事情一次做完。

```text
Camera ──> 视觉检测 ─────┐
ToF ─────> 障碍物位置 ───┼─> 高层行为逻辑
声音 / BLE / 其它事件 ───┘        │
                                  ▼
                           决定下一步做什么
                         走 / 转 / 看 / 踢 / 休息
                                  │
                                  ▼
                          运动 / 技能 Policy
                                  │
                                  ▼
                              关节动作
```

高层行为逻辑主要回答：

- 现在要不要到处走？
- 前面有障碍，要不要转向？
- Camera 发现目标后，要不要看过去？
- 要不要进入踢球、跳舞、打盹等行为？

它**不负责直接算每个舵机角度**。舵机动作由下面的运动 Policy / Skill Policy 负责。

## Autonomous Brain 是另一个 AI 模型吗？

从官方公开设计看，旧版 Autonomous Brain 主要是**普通程序逻辑**：状态机 + 计时 + 记忆 + 条件规则。

官方路线图对旧版行为的公开描述大致是：

```text
energy / mood
     │
     ▼
选择一个行为状态
     │
     ├─ Chill
     ├─ LookAround
     ├─ Wander
     ├─ TurnInPlace
     ├─ Zoomies
     ├─ Startle
     ├─ Stretch
     ├─ Ruffle
     ├─ Preen
     ├─ Sneeze
     ├─ Dance
     ├─ GroundPick
     ├─ Nap
     ├─ BallPlay
     ├─ Petted
     └─ Held
```

可以把几层这样区分：

| 层 | 主要做什么 | 是否 AI 模型 |
|---|---|---|
| Camera Detector | 从画面里找目标 | 是，ONNX / RKNN |
| ToF 处理 | 把 8×8 距离变成障碍物几何信息 | 否，普通几何算法 |
| Autonomous Brain | 决定机器人下一步做什么 | 旧版公开设计主要是状态机 / 规则 |
| Locomotion Policy | 根据身体状态和命令输出 14 个关节动作 | 是，RL Policy |

## 它会看哪些信息？

官方公开设计里提到过：

- ToF 障碍信息；
- 环境声音 / 语音事件；
- Camera 检测结果；
- 被摸、被拿起等事件；
- BLE 发现附近其它 Microduck；
- 机器人当前运动状态；
- 内部 energy / mood；
- 简单的探索记忆。

不是每个行为都会同时使用所有信息。

## 它输出什么？

高层行为输出的不是舵机角度，而是**意图 / 指令**。

例如：

```text
慢慢往前走
向左转
把头看向某个方向
停止
执行左脚踢球
进入 Dance
坐下 / 休息
```

这些指令再交给 `robotd` 和对应的运动 / 技能 Policy 执行。

## 当前新的 Rust daemon 架构做到哪了？

目前官方 `microduck` 仓库已经有 Autonomous Brain 所需的大部分基础模块：

- `mediad` + `duck-detect`：Camera 感知；
- `tofd`：8×8 ToF；
- `kinematics`：把关节和传感器位置换算到机器人坐标系；
- `odometry`：位置估计；
- 声音、BLE / 社交事件；
- `robotd` 的移动、转头、Skill 指令。

但是官方路线图仍把 **M9 — The autonomous brain** 列为尚未完成的大模块。

因此，旧版 `autonomous.rs` 的 16 状态设计可以作为公开参考，但不能写成“当前新 daemon 已经完整实现”。

## 第三方复现时能不能直接沿用？

这个架构非常适合复用：

```text
传感器结果
   ↓
行为状态机
   ↓
统一意图指令
   ↓
运动 / Skill Policy
```

如果机器人目标基本相同，通常不需要从零重新设计。真正需要改的主要是：

1. 有哪些感知事件；
2. 感知结果的数据格式；
3. 想增加或删除哪些行为；
4. 下层支持哪些移动 / Skill 指令。

换摄像头、主控板或舵机，并不自动意味着高层行为逻辑要全部重写。

## 主要公开来源

- https://github.com/pollen-robotics/microduck/blob/main/docs/ideas/autonomous_behavior.md
- https://github.com/pollen-robotics/microduck/blob/main/docs/project/roadmap.md
- https://github.com/pollen-robotics/microduck/blob/main/docs/design/architecture.md
- https://github.com/pollen-robotics/microduck

相关页面：

- [机载软件架构](runtime-architecture.md)
- [50 Hz 控制循环与数据流](control-loop-and-sensor-dataflow.md)
- [技能、Policy 与运行时切换](../simulation/policy-catalog-and-switching.md)
