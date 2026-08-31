# 控制循环与传感器数据流

[English](../../en/software/control-loop-and-sensor-dataflow.md) | **简体中文**

> 主要来源：Microduck 官方 runtime 与 RL 仓库。

这份文档用尽量直白的方式解释 Microduck 底层控制时，数据到底怎么走：从舵机和 IMU 读出来，进入 Policy，再变成新的电机目标值。

最核心的一点是：真实机器人运行的是一个 **50 Hz 闭环控制系统**。也就是大约每 20 ms，就会重新读取机器人状态、构造 Policy 输入、运行神经网络、处理输出，再把新的关节目标发给电机。

## 最简版本

```text
14 个受控舵机 + 控制 IMU
              │
              ▼
         同步读取状态
              │
              ▼
       关节位置 / 速度
       姿态 / 角速度数据
              │
              ▼
       Observation 构造
           61 个值
              │
              ▼
          ONNX Policy
          14 个 Action
              │
              ▼
缩放 / 滤波 / 限位 / 安全处理
              │
              ▼
        写入舵机目标值
              │
              └────── 50 Hz 循环重复
```

Microduck 总共有 15 个电机，但鸟嘴 / mouth 电机不属于这 14 维 locomotion policy action，由 Runtime 单独控制。

## 一次 Control Tick 里发生什么

把一次控制循环简化以后，大致是：

1. **读取机器人状态。** Runtime 从 motor/control bus 获取关节状态和 IMU 数据。
2. **构造 Observation。** 把原始状态整理成 Policy 需要的 61 个输入值。
3. **运行 ONNX 网络。** 当前选中的 Policy 输出 14 个 action。
4. **处理 Action。** Runtime 再做 scaling、filter、joint limit、gain、安全逻辑等处理。
5. **写回新的关节目标。** 把结果发给受控舵机。
6. **以 50 Hz 重复。**

所以，真实机器人上执行的控制器不能简单理解成“一个 ONNX 文件”。更准确的说法是：

```text
Policy
+ Observation 构造
+ Runtime 滤波
+ 执行器规则
+ 安全逻辑
+ 真实硬件
```

这些部分共同决定最后的动作表现。

## 电机与 IMU 的控制路径

当前官方 Runtime 公开了一套 Dynamixel 风格的控制总线，其中既有舵机设备，也有用于控制 IMU 的 `imu_to_dxl` 设备。

公开源码可以确认：

- 15 个 motor ID；
- `imu_to_dxl` 设备 ID 为 **200**；
- 当前开发配置串口速率为 **1 Mbps**；
- 鸟嘴电机不属于 14 维 locomotion action。

让舵机状态和控制 IMU 通过同一控制路径读取，有助于让关节状态和姿态数据在时间上更加一致。

## 61 维 Observation 里有什么

官方 RL 项目给出的共享 actor observation 是：

```text
base angular velocity      3
projected gravity          3
joint position            14
joint velocity            14
previous actions          14
----------------------------
proprioception            48

twist command              3
head-pose command           4
body-pose command           6
----------------------------
command block              13

total                     61
```

也就是说，这 61 维主要是**本体感觉 proprioception**：机器人自己的姿态、关节状态，以及上层要求它执行什么动作。

## 走路 Policy 会直接看摄像头或 ToF 图像吗？

根据目前公开的 61 维 actor contract，**标准底层 locomotion policy 并没有把摄像头图像或 8×8 ToF frame 直接放进这 61 个输入值中。**

这不代表摄像头和 ToF 没用。它们可以服务于其它软件，例如：

- 环境感知；
- 远程操作；
- 应用层逻辑；
- 与物体相关的行为；
- 将来的视觉 / 感知 Policy。

关键区别是：

```text
底层 locomotion policy
    主要看机器人自身状态 + command

Camera / ToF service
    给其它感知和应用路径提供环境信息
```

不能因为机器人上有某个传感器，就默认每一个神经网络都会使用它。

## 为什么输入里还有 Previous Actions

61 维 Observation 里包含上一个控制周期的 14 个 action。

这让 Policy 知道“上一帧自己刚刚要求关节做了什么”，因此可以利用非常短期的控制历史，而不需要通过图像序列或者额外的长历史缓存来获得这类信息。

## Runtime 的滤波和安全处理为什么重要

官方 Runtime 里还能看到很多执行器相关处理，例如：

- action scaling；
- 一些关节的 low-pass filter；
- position gain；
- joint travel 处理；
- fall / limp / recovery 状态；
- watchdog / deadman；
- 总线错误处理。

这些看起来不像“AI”，但对 sim-to-real 很重要。

如果训练时假设了一套动作处理流程，而真实机器人部署时偷偷多加了滤波器、删掉了滤波器，或者 gain 不同，即使 ONNX 权重完全一样，机器人也可能表现不同。

所以可以记住一句话：**ONNX 不是完整控制器。**

## Camera 和 ToF 在软件架构中的位置

官方 Runtime 把不同硬件职责拆成独立服务。目前源码中：

- `mediad` 负责 camera / media 路径；
- `tofd` 负责 multi-zone ToF；
- `robotd` 负责实时机器人控制循环和 Policy execution。

这样做的好处是，普通 App 不需要直接碰低层硬件，也不需要每个 App 自己实现一次摄像头、ToF 或 motor protocol。

## 50 Hz 到底意味着什么

50 Hz 表示目标控制周期大约是 **20 ms**。

Runtime 还会检查实际循环频率和 bus error。如果控制循环频繁卡住，即使 Linux 进程还活着，机器人也不能算“运行正常”。

对会走路、会跌倒的机器人来说，“程序没崩”与“实时控制仍然健康”是两回事。

## 主要官方来源

- https://github.com/pollen-robotics/microduck
- https://github.com/pollen-robotics/microduck/blob/main/docs/design/robotd-design.md
- https://github.com/pollen-robotics/microduck/blob/main/deploy/robotd.toml
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/model.rs
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/imu.rs
- https://github.com/pollen-robotics/microduck_rl/blob/develop/README.md

## 相关页面

- [机载运行时架构](runtime-architecture.md)
- [技能、Policy 与运行时切换](../simulation/policy-catalog-and-switching.md)
- [仿真与强化学习](../simulation/model-and-rl.md)
- [电控、总线、传感器与电源](../hardware/electronics-and-buses.md)
