# 技能、Policy 与运行时切换

[English](../../en/simulation/policy-catalog-and-switching.md) | **简体中文**

> 主要来源：官方 `pollen-robotics/microduck_rl` 与 `pollen-robotics/microduck` 仓库。

Microduck 并不是用“一个超大的神经网络”负责所有动作。官方公开的 RL 项目里有**多个 task / policy family**，而机器人运行时给这些 policy 提供统一接口，所以可以在不更换整套机器人软件的情况下切换不同技能。

可以先把它理解成：

```text
上层命令 / 当前选择的技能
              │
              ▼
         Policy 选择
              │
   ┌──────────┼───────────┐
   ▼          ▼           ▼
 行走       站起       坐下/站立 ...
 ONNX       ONNX          ONNX
   └──────────┼───────────┘
              ▼
        统一 61 维输入
        统一 14 维输出
              │
              ▼
         robotd @ 50 Hz
```

## 为什么多个 Policy 可以共用同一套 Runtime

官方 RL 项目让当前主要 policy family 共享同一个 actor 接口：

```text
actor observation: 61 个值
policy action:      14 个值
control rate:       50 Hz
```

61 维 observation 可以简单拆成：

```text
48 维本体感觉 proprioception
+ 13 维 command
= 61
```

其中 13 维 command 又包括：

- twist command：3；
- head pose command：4；
- body pose command：6。

如果某个 task 用不到其中一部分 command，一般不会改变网络输入长度，而是把不用的部分补 0。这样不同技能不需要各自设计完全不同的输入格式。

## 当前公开的主要 Task / Policy Family

具体 task 名称以后可能继续变化，因此应以官方仓库实时 registry 为准。按 2026-08-31 的官方 README，主要 family 包括：

| Task family | 通俗理解 |
|---|---|
| `Velocity` | 主要行走 policy，可接收速度和头部姿态命令 |
| `VelStand` | 把行走和跌倒恢复放进同一个 policy |
| `StandUp` | 从趴着、仰躺、坐姿等状态站起来并保持站立 |
| `SitStand` | 在坐下和站立之间受控切换 |
| `GroundPick` | 身体下蹲，让鸟嘴接近 / 触碰地面，再返回站立 |
| `BallKick` | 向前踢一个小球 |
| `Roulade` | 向前翻滚并重新回到双脚 |
| `Velocity ... Rollers` | 装上被动 roller 后进行速度跟踪 |
| `Swizzle` | 对称的 roller 滑行动作 |
| `RollerCrouch` | 滑行过程中下蹲 |
| `RollerSlope` | 在斜坡上使用 roller 滑行 |
| `RollerStandUp` | 装着 roller 时从地面站起 |
| `Spin` | 使用 roller 原地快速旋转 |

其中一些 family 还有 Flat / Rough 地形版本，官方项目也会自动注册 Backlash 版本。

## 每个技能都要重新刷固件吗？

**不用。**

Runtime 可以在统一的 **61 输入 / 14 输出**接口背后 hot-swap 不同 policy。换句话说，从行走切到站起、翻滚或坐下，更像是切换不同的控制模型，而不是重新安装一套机器人固件。

官方 `scripts/infer_policy.py` 甚至可以在仿真里一次同时载入多个 ONNX，例如 walking、standing、sit/stand、roulade，用来演练这种切换方式。

## 但“多个 Policy”不等于“每个小动作一个模型”

这里也很容易误解。

例如：

- `VelStand` 一个 policy 里同时包含行走和跌倒恢复；
- `SitStand` 一个 policy 同时处理“坐下”和“站起”两个方向；
- `StandUp` 可以处理多个不同初始姿态。

所以实际设计是混合方式：

- 相近的行为可以放到一个 policy 里共同训练；
- 差异很大的动作可以使用不同 policy；
- Runtime 维持统一接口，让这些 policy 可以共存和切换。

## 为什么 15 个电机，却只有 14 维 Action？

Microduck 有 **15 个电机**，但 locomotion policy 的 action vector 是 **14 维**。

这 14 个 RL 控制关节覆盖两条腿和 neck/head。可活动鸟嘴 / mouth 的电机由 Runtime 单独控制，没有放进这 14 维 locomotion action 中。

所以：

- “Microduck 有 15 个 motors”正确；
- “RL policy 输出 14 actions”也正确。

## Backlash Policy Variant 是什么

官方 RL 项目给主要 task 提供了 Backlash 版本。它不是简单给角度加随机噪声，而是在每个受控舵机关节串联一个表示齿隙的 passive hinge。

关键是：**神经网络接口依然保持 61 observations / 14 actions。**

也就是说，仿真中的机械模型可以变得更接近真实机器人，但部署接口不需要跟着改变。

## 更高层的 AI 做什么

底层 RL policy 解决的是：

- 关节怎样动才能稳定走路？
- 跌倒后怎么把身体重新撑起来？
- 怎么坐下、翻滚、滑行？

而更高层的 application / agent 可以负责：

- 现在应该选择哪个技能？
- 应该给 walking policy 什么速度命令？
- 什么时候停止当前动作，切到另一个技能？

把“高层决策”和“高速电机控制”分开，是机器人里非常常见的架构，因为两者需要的反应速度和安全要求完全不同。

## 主要官方来源

- https://github.com/pollen-robotics/microduck_rl/blob/develop/README.md
- https://github.com/pollen-robotics/microduck_rl/tree/develop/src/mjlab_microduck/tasks
- https://github.com/pollen-robotics/microduck_rl/blob/develop/scripts/infer_policy.py
- https://github.com/pollen-robotics/microduck

## 相关页面

- [仿真与强化学习](model-and-rl.md)
- [控制循环与传感器数据流](../software/control-loop-and-sensor-dataflow.md)
- [仿真模型资产参考](model-assets-reference.md)
