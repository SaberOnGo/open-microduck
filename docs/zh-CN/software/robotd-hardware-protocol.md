# `robotd` 硬件协议：每 20 ms 真机到底读什么、写什么

[English](../../en/software/robotd-hardware-protocol.md) | **简体中文**

> 范围：整理当前官方公开源码中的硬件接口参数。目标是把原来分散在多个 Rust 文件里的关键值集中到一页。

## 先看最简单的流程

每 20 ms，大致做一次：

```text
读取 IMU + 舵机状态
        ↓
得到机器人当前状态
        ↓
运行 Policy / 安全逻辑
        ↓
写入新的舵机目标位置
        ↓
重复，50 Hz
```

最关键的一点：

**15 个 Servo 和控制 IMU 共用同一条 Dynamixel-compatible Serial Bus。**

## Bus 总览

| 项目 | 当前公开值 |
|---|---|
| Radxa 参考串口 | `/dev/ttyS2` |
| 波特率 | 1,000,000 bit/s |
| 控制频率 | 50 Hz |
| 每轮周期 | 20 ms |
| Bus timeout | 30 ms |
| 物理 Servo | 15 |
| Locomotion Policy Joint | 14 |
| 控制 IMU Bridge | ID 200 |

## 设备 ID

```text
右腿           10 11 12 13 14
左腿           20 21 22 23 24
Head / Mouth   30 31 32 33 34
IMU Bridge     200
```

嘴/喙是第 15 个实体 Servo，但不属于 14 个 Locomotion Policy Action。

## 每个 Control Tick 的快速读取

当前公开 Bus 代码会做一次组合的同步读取，把 IMU Bridge 和 Servo 状态一起读回来。

Servo 快速状态块从寄存器 **124** 开始，读取 **12 bytes**。

这部分包含控制循环需要的快速状态，例如当前 PWM / Current、Velocity、Position 等 Dynamixel 当前状态数据。

IMU 也放在同一个控制路径里读取，这样关节状态和身体姿态的时间差尽量小。

## 大约每秒读取一次的慢数据

Voltage 和 Temperature 没必要 50 Hz 读取。

当前公开 Runtime 从寄存器 **144** 开始读取 **3 bytes**，大约每秒一次，用于 Voltage / Temperature 这类慢状态。

这样不会每 20 ms 都多花一笔串口交易。

当前源码使用的转换包括：

- Velocity：**0.229 rpm / count**；
- Voltage：**0.1 V / count**。

## 写入路径

Policy 和 Safety 最终得到关节目标位置后，再使用同步写入把目标位置发给 Servo。

所以可以简单理解为：

```text
SYNC READ
IMU + 15 Servo State
        ↓
Policy / Runtime / Safety
        ↓
SYNC WRITE
Servo Goal Position
```

## Startup 时检查的 EEPROM 参数

当前固定源码快照里包括：

```text
return_delay_time = 0
baud_rate         = 3    # 1 Mbps code
pwm_slope         = 255
shutdown          = 52
```

其中 `return_delay_time = 0` 非常重要。

官方源码解释：Factory Return Delay 大约可能达到 **500 µs / device**。如果约 16 个设备都要回答：

```text
0.5 ms × 16 ≈ 8 ms
```

而整个控制周期只有 20 ms。

也就是仅 Return Delay 就可能吃掉大约 **40%** 的一轮控制时间。

所以这个参数直接影响整条总线能不能稳定跑 50 Hz。

## Servo Position Gain

当前公开 Runtime 默认：

```text
P = 200
I = 0
D = 0
```

不要把这个 `P=200` 和下面这些混为一谈：

- Simulation BAM 的 `kp_fw`；
- MJCF Actuator 的 `kp`；
- Policy / Standing Gain Ratio。

它们属于不同控制层。

## IMU：ID 200 的 12 bytes 是什么？

当前控制 IMU 路径是：

**ST LSM6DSV16X → `imu_to_dxl` v2 → ID 200**。

Runtime 读取 **12 bytes**：

```text
bytes 0..5    Gyro X/Y/Z，i16 little-endian
bytes 6..11   Quaternion X/Y/Z，IEEE fp16
```

Quaternion 的 `W` 在主控端重新计算。

当前公开源码还可以确认：

- Gyro Range：±500 dps；
- Scale：17.5 mdps/LSB；
- Runtime 转成 rad/s；
- 当前 Sensor → Trunk 安装关系大致相当于绕 Y 轴 +90°；
- Orientation 还没收敛时，不会直接当成可用姿态；
- Gyro / Gravity 还做了简单异常跳变抑制。

## Joint Order 和 Home Pose 同样重要

只有 Servo ID 对，并不够。

Runtime 还规定了：

- Joint 顺序；
- 每个 Joint 的 Home Pose；
- 14 个 Policy Action 如何映射回 15 个物理 Servo。

最重要的规则：

> **Runtime Joint Order / Home Pose 必须和 Training Policy 使用的约定一致。**

完整表见：[硬件参数总表](../hardware/parameter-reference.md)。

## ONNX 不是直接写 Servo

真实链路是：

```text
ONNX Action
   ↓
Action Scale / Filter
   ↓
Safety / Limit
   ↓
最终 Servo Target
   ↓
Serial Bus
```

所以只拿到一个 ONNX 文件，并不等于已经复现了完整真机 Controller。

## 目前公开资料仍缺什么？

这一页描述的是**软件能看到的硬件协议**，不代表完整生产电路已经公开。

目前仍不能从公开资料确认完整：

- Half-duplex Bus Transceiver 原理图；
- `imu_to_dxl` v2 MCU 与外围电路；
- Power Distribution / Protection；
- 最终 PCB Routing。

这些继续标记为 **Unknown / Unresolved**。

## 主要公开来源

- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/bus.rs
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/model.rs
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/imu.rs
- https://github.com/pollen-robotics/microduck/blob/main/docs/design/robotd-design.md
- https://github.com/pollen-robotics/microduck/blob/main/deploy/robotd.toml

相关页面：

- [50 Hz 控制循环与数据流](control-loop-and-sensor-dataflow.md)
- [硬件 Bring-up 与标定](../getting-started/hardware-bringup-and-calibration.md)
- [电控、总线、传感器与电源](../hardware/electronics-and-buses.md)
