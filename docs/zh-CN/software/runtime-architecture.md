# 机载运行时架构

> 本文总结官方 `pollen-robotics/microduck` 软件仓库公开的系统架构，只描述公开软件栈，不推断未公开电路。

## 概览

官方 Microduck 仓库是一套运行在 RK3566 级 Linux 主控上的 Rust workspace，由多个职责清晰的守护进程协作：

```text
                  客户端
       App / 手柄 / CLI / 脚本
                    │
             统一 JSON-RPC API
                    │
     ┌──────────────┼─────────────────┐
     │              │                 │
   robotd         configd           updaterd
 控制/电机       Wi-Fi/身份        签名更新
     │
     ├──── padd     手柄输入
     ├──── btd      Bluetooth 通道
     ├──── mediad   摄像头/WebRTC
     └──── tofd     深度/ToF 服务
```

本地守护进程通过 **Unix socket 上的 JSON-RPC** 通信。传输层与功能所有者被刻意分离：Bluetooth、CLI 或其它客户端可以走同一套 API，而不需要各自重新实现机器人控制协议。

## 主要服务

| 服务 | 公开职责 |
|---|---|
| `robotd` | 负责 50 Hz 控制环、电机总线、策略推理、机器人状态、技能以及控制/安全逻辑。 |
| `updaterd` | 安装签名软件发布，并支持基于健康状态的回滚。 |
| `configd` | 负责 Wi-Fi/网络、设备身份与系统配置。 |
| `btd` | 手机/客户端使用的 Bluetooth 传输通道，把请求路由到真正拥有功能的服务。 |
| `padd` | 读取游戏手柄，并把输入转换为统一机器人 API。 |
| `mediad` | 摄像头采集、编码与流媒体，包括当前 WebRTC 路径。 |
| `tofd` | 管理多区 ToF 传感器并提供深度帧/状态。 |

服务集合可能随官方软件继续演进，当前状态应以官方仓库为准。

## 控制环

当前官方配置使用 **50 Hz** 控制环。

官方仓库描述为：控制 15 个电机设备，而神经网络策略输出 14 个运动关节动作；嘴/喙电机由运行时独立控制。

当前 alpha 策略加载时会校验共同接口：

```text
observation：61 个 float
policy output：14 个 action
控制频率：50 Hz
```

多种策略/技能可以保持同一 observation/action contract 在运行时切换，因此行走、起身、坐站、踢球、翻滚、低头拾取、滚轮等行为不需要各自一套独立固件。

## 61 维 observation contract

官方 RL 仓库将当前 actor observation 描述为：

```text
48 维本体感觉
+ 13 维命令
= 61 维
```

共享命令区：

- twist：3；
- head pose：4；
- body pose：6。

某个任务不用其中一类命令时会填 0，而不是修改网络输入宽度。这正是策略可以热切换的重要约束。

## ONNX 部署

策略在独立的 `microduck_rl` 项目中训练，并导出为 **ONNX**，机载运行时通过 ONNX Runtime 加载。

官方 RL 文档特别强调 observation normalizer 会被烘焙进正式导出的 ONNX graph。手工转换、漏掉 normalizer 的 checkpoint 与真实部署 artifact 并不等价。

## 电机 / IMU I/O

`robotd` 通过 `duck-control` 和官方 Dynamixel 兼容 Rust 栈访问当前开发硬件总线。

公开源码可确认：

- 15 个电机 ID；
- ID 200 的 IMU bridge；
- 1 Mbps 串口配置；
- Radxa Zero 3W 当前开发接线上的 `/dev/ttyS2`；
- 控制环使用的关节位置、速度、电压与状态数据。

主控制 IMU 与舵机状态位于同一总线读取体系，有利于减少关节反馈与姿态数据之间的同步歧义。

## 策略之外的执行器控制

真实机器人并不是“ONNX 输出直接写电机”。公开运行时还有：

- action scale；
- 头部/腿部低通；
- 位置增益；
- 可选的电池电压适配；
- 关节行程限制；
- 跌倒、limp、恢复逻辑；
- 总线丢包容错；
- watchdog / deadman。

这些都属于 sim-to-real 的实际执行链，因为真机运行的是**策略 + 运行时控制路径**，而不是孤立的神经网络。

## Safety 与 health

官方运行时将“机器人状态”和“软件发布健康状态”区分开。电池、电机温度、loop 统计、总线计数可以用于监控，而 updater 只使用更严格、更窄的 health gate 判断是否需要回滚新版本。

公开配置包含 achieved control frequency、loop stall 和连续总线错误等阈值。因此“进程还活着”和“机器人控制工作正常”是两个不同判断。

## 多种输入路径

架构允许多客户端：

- `padd` 接游戏手柄；
- `robotctl` / Unix socket 做本地管理；
- `btd` 提供 Bluetooth 配网/控制路径；
- App/网络功能复用同一服务 contract。

设计原则是：transport 只负责传请求，真正拥有能力的服务负责行为。

## 摄像头与深度服务

### `mediad`

当前官方硬件 bring-up 使用 RK3566/Rockchip 媒体栈，通过 Rockchip MPP 做硬件 H.264，并在软件架构中接入 WebRTC。

### `tofd`

ToF 服务统一负责多区深度采集，再向其它模块提供数据，而不是让所有客户端直接访问传感器。

## 更新系统

`updaterd` 围绕签名 release、安装、安装后验证与回滚设计。对于会行走的机器人，仅仅“Linux 能启动”不足以证明升级成功：如果控制环明显降速或总线无法可靠读取，软件仍应被视为不健康。

## 主要来源

- https://github.com/pollen-robotics/microduck
- https://github.com/pollen-robotics/microduck/blob/main/README.md
- https://github.com/pollen-robotics/microduck/tree/main/docs/design
- https://github.com/pollen-robotics/microduck/blob/main/deploy/robotd.toml
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/model.rs
- https://github.com/pollen-robotics/microduck_rl

硬件侧对应关系见：[电控、总线、传感器与电源](../hardware/electronics-and-buses.md)。
