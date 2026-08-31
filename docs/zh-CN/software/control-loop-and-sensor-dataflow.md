# 控制循环：Microduck 到底怎么动起来

[English](../../en/software/control-loop-and-sensor-dataflow.md) | **简体中文**

> 本页只讲低层运动控制，用普通话解释官方公开 Runtime 和 RL 代码。

## 整个循环先看这一张图

Microduck 每秒更新运动 **50 次**：

```text
读取关节 + IMU
      ↓
组成 61 个输入数字
      ↓
运行当前运动 AI
      ↓
得到 14 个关节动作
      ↓
缩放 / 滤波 / 安全 / 限位
      ↓
给舵机写入新的目标位置
      ↓
20 ms 后重复
```

这就是低层运动控制的核心。

## 为什么有 15 个电机，却只有 14 个 AI 输出？

当前 Runtime 有 **15 个物理电机 ID**。

运动 Policy 控制其中 **14 个关节**。嘴/喙电机单独控制，所以不在 14 个 Policy Action 里。

## 61 个输入到底是什么？

大部分是机器人自己身体的状态：

| 输入 | 数量 | 普通话解释 |
|---|---:|---|
| 身体旋转速度 | 3 | 身体正在怎么转 |
| 重力方向 | 3 | 身体现在向哪边倾斜 |
| 关节位置 | 14 | 每个关节现在在哪里 |
| 关节速度 | 14 | 每个关节动得多快 |
| 上一次动作 | 14 | AI 上一轮让关节怎么动 |
| 运动命令 | 13 | 要求机器人怎么走、怎么看、身体怎么摆 |
| **总计** | **61** | |

13 个命令值可以再拆成：

```text
走路 / 转向命令   3
头部目标          4
身体姿态目标      6
```

## Camera 和 ToF 不在这 61 个输入里

这是理解 Microduck 很关键的一点。

标准运动 Policy **不会直接吃**：

- Camera 图像；
- 原始 8×8 ToF 深度图。

它们的关系是：

```text
Camera / ToF
     ↓
感知 + 高层行为判断
     ↓
生成“往哪走、怎么看”等命令
     ↓
61 维运动 Policy
```

也就是说：

- 感知和高层逻辑负责 **去哪里、为什么动**；
- 运动 AI 负责 **身体具体怎么动**。

## AI 输出后，还要经过普通控制代码

神经网络的 14 个输出不会直接写进电机。

Runtime 还会处理：

- Action Scale；
- 可选低通滤波；
- 关节行程限制；
- 舵机增益；
- 跌倒 / Limp / 恢复；
- Deadman / Watchdog；
- 总线错误处理。

所以真实控制器应该理解成：

```text
运动 Policy
+ Runtime 控制规则
+ Safety
+ 真实硬件
```

不是只有一个 ONNX 文件。

## 电机和 IMU 怎么进主控？

当前公开开发路径使用 Dynamixel 兼容串口总线：

```text
15 个舵机 + IMU Bridge ID 200
             │
             ▼
          1 Mbps UART
             │
             ▼
           robotd
```

主控制 IMU 和舵机状态走同一套控制读取路径，可以让关节状态和身体姿态尽量接近同一时刻。

Motor ID、寄存器、IMU 数据格式等细节见：

- [硬件参数总表](../hardware/parameter-reference.md)
- [电控、总线、传感器与电源](../hardware/electronics-and-buses.md)

## 为什么还要输入“上一次动作”？

Policy 会看到上一轮自己的 14 个输出。

这样它能知道“刚才让身体做了什么”，不需要为了这点短期记忆再引入 Camera 或额外的循环神经网络。

## 最后只记住这三句话

```text
高层软件：决定“往哪动”。
运动 AI：决定“关节怎么动”。
Runtime / Safety：决定“哪些动作真的可以发给电机”。
```

## 主要公开来源

- https://github.com/pollen-robotics/microduck
- https://github.com/pollen-robotics/microduck/blob/main/docs/design/robotd-design.md
- https://github.com/pollen-robotics/microduck/blob/main/deploy/robotd.toml
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/obs.rs
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/model.rs
- https://github.com/pollen-robotics/microduck_rl

## 相关页面

- [Microduck 软件架构：一眼看懂](runtime-architecture.md)
- [技能、Policy 与运行时切换](../simulation/policy-catalog-and-switching.md)
- [Sim-to-real 参数总表](../simulation/sim-to-real-parameter-reference.md)
