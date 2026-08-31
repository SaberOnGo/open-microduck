# Microduck 软件架构：一眼看懂

[English](../../en/software/runtime-architecture.md) | **简体中文**

> 本页只整理官方公开软件。先讲机器人怎么工作，再讲代码名称。

## 整套软件先看这一张图

Microduck 不是“一个大 AI 模型控制所有东西”。它是分层工作的：

```text
Camera ──► 视觉 AI ──────────────┐
                                 │
ToF ────► 距离 / 障碍物算法 ─────┼──► 高层行为判断
                                 │      “往那里走”
声音 / 蓝牙 / 其它输入 ───────────┘      “看左边”
                                        “踢球”
                                           │
                                           ▼
                                      运动 RL 模型
                                   身体状态 + 运动指令
                                           │
                                           ▼
                                      14 个关节动作
                                           │
                                           ▼
                                   安全 / 限位 / 滤波
                                           │
                                           ▼
                                        15 个电机
```

只要先记住四层：

- **感知**：看见周围发生了什么。
- **高层行为**：决定接下来想做什么。
- **运动 AI**：决定身体怎样动。
- **电机控制**：安全地把动作发给舵机。

## 哪些地方用了 AI？

| 部分 | 当前公开实现主要怎么做 |
|---|---|
| Camera 目标检测 | AI 模型：`duck_detect.onnx` / `duck_detect.rknn` |
| ToF 深度处理 | 普通几何和过滤算法 |
| 高层自主行为 | 旧版主要是状态机 + 规则；新版尚未完整迁移 |
| 走路、站立、翻滚等运动 | 强化学习 Policy，导出成 ONNX |
| 安全、限位、总线、更新、网络 | 普通软件代码 |

所以“AI 机器人”不等于所有传感器都直接送进一个神经网络。

## 那些 `robotd`、`mediad` 到底是什么？

官方软件主要用 **Rust** 编写，运行在 Linux 上。

Linux 里长期在后台运行的小程序通常叫 **daemon（守护进程）**。不用记这个名词，只需要记它们各自干什么：

| 代码名 | 普通话解释 |
|---|---|
| `robotd` | **身体控制器**：50 Hz 运动循环、运动 Policy、安全逻辑。 |
| `mediad` | **摄像头和视频**：采集 Camera、视觉检测、WebRTC 视频。 |
| `tofd` | **深度传感器**：读取 8×8 ToF。 |
| `padd` | **手柄读取**：把摇杆和按键变成机器人指令。 |
| `btd` | **蓝牙通道**：通过 Bluetooth 传递支持的指令。 |
| `configd` | **设置**：Wi-Fi、设备身份、系统配置。 |
| `updaterd` | **软件更新**：安装签名版本，失败时可以回滚。 |
| `robotctl` | **管理工具**：开发者查看状态、测试和控制机器人。 |

为什么拆开？因为 Camera 出问题时，不应该把走路控制一起搞崩。

## 机器人走路到底怎么运行？

低层运动控制每秒运行 **50 次**，也就是每 **20 ms** 一轮：

```text
读取关节 + IMU
      ↓
组成 61 个输入数字
      ↓
运行一个 ONNX 运动 Policy
      ↓
得到 14 个动作
      ↓
缩放 / 滤波 / 安全 / 限位
      ↓
写入新的舵机目标
      ↓
重复
```

当前 Runtime 有 **15 个物理电机 ID**。

运动 AI 控制其中 **14 个关节**，嘴/喙电机单独处理。

这 61 个输入主要是机器人自己的姿态、关节状态和运动命令。**Camera 图像和原始 8×8 ToF 数据不在标准 61 维 Walking Policy 里。**

想看 61 维具体是什么，见：[控制循环与传感器数据流](control-loop-and-sensor-dataflow.md)。

## Camera 在哪里？

```text
Camera
  ↓
mediad
  ├──► 视频 / WebRTC
  └──► duck-detect
           ↓
       目标在哪里
```

视觉检测可以使用：

- RK3566 NPU + RKNN 模型；
- CPU + ONNX 模型。

## ToF 在哪里？

```text
8×8 ToF
   ↓
 tofd
   ↓
64 个距离值
   ↓
运动学 + 几何算法
   ↓
地面 / 空区域 / 障碍物位置
```

这里主要是传统代码，不是神经网络。

## 谁决定“接下来做什么”？

这是感知和运动 AI 中间的一层：

```text
“前面有东西”
      ↓
高层行为逻辑
      ↓
“向左转，再往前走”
      ↓
运动 Policy
```

旧版 Microduck Runtime 有一套主要由**状态机和规则**组成的自主行为系统，包括 Mood / Energy、探索记忆、ToF 避障、Wander、LookAround、BallPlay、Nap 等。

当前新的 daemon 架构还没有把这套完整 Autonomous Brain 全部迁移完成。官方 Roadmap 仍把它列为后续主要工作之一。

这表示的是**软件正在迁移**，不是 Camera 或 ToF 没有开源。

## 这些后台程序怎么互相说话？

大部分本地控制和状态消息使用 **JSON-RPC + Unix socket**。

普通读者可以简单理解成：

> 同一块 Linux 主控上的几个后台程序，用很小的结构化消息互相发指令和状态。

因此手柄、蓝牙、命令行工具都可以复用同一套机器人控制接口，而不是每种控制方式重新写一套电机协议。

## 对公开复现最重要的意义

如果第三方做兼容研究，不需要一次重写整套系统。

可以按层替换：

```text
传感器
  ↓
感知
  ↓
行为指令
  ↓
运动 Policy
  ↓
电机接口
```

换了硬件，可以主要改硬件接口；想增加新行为，可以主要改行为层；不一定需要重新训练所有 Walking Policy。

## 主要公开来源

- https://github.com/pollen-robotics/microduck
- https://github.com/pollen-robotics/microduck/blob/main/docs/design/architecture.md
- https://github.com/pollen-robotics/microduck/blob/main/docs/project/roadmap.md
- https://github.com/pollen-robotics/microduck/tree/main/mediad
- https://github.com/pollen-robotics/microduck/tree/main/tof
- https://github.com/pollen-robotics/microduck/tree/main/duck-detect
- https://github.com/pollen-robotics/microduck/tree/main/kinematics
- https://github.com/pollen-robotics/microduck_rl
