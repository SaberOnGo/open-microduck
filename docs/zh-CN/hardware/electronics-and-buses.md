# 电控、总线、传感器与电源

> 范围：Pollen Robotics 官方产品资料和公开源码中能够验证的信息。开发板/开发阶段实现与最终产品规格分开标注。

## 系统概览

公开资料显示，Microduck 是一套以 **RK3566** Linux 计算平台为核心的小型机器人系统，主要由 Dynamixel 电机总线、挂在同一总线上的 IMU bridge、摄像头、ToF、音频、Wi-Fi/Bluetooth 和可拆卸摄像机电池组成。

根据公开来源可抽象为：

```text
                 RK3566 Linux 主控
                        │
          ┌─────────────┼──────────────┐
          │             │              │
   串口 / DXL         摄像头         I2C / 音频
          │             │              │
   ┌──────┴──────┐    CSI 路径     ToF / Codec
   │             │
15 个舵机   imu_to_dxl v2
                 │
           LSM6DSV16X
```

这是一张根据公开资料整理的说明图，**不是官方原理图**。

## 计算平台

### 产品级规格

官方 Press Kit 列出：

- Rockchip **RK3566**，带 AI 加速器；
- **1 GB RAM**；
- **32 GB 存储**；
- Wi-Fi 与 Bluetooth。

### 当前官方源码中的开发平台

官方 bring-up 和部署文档当前使用 **Radxa Zero 3 / Zero 3W** 与 Armbian/Debian 系软件。由于早期设计资料曾把开发板选择标为 provisional，OpenMicroDuck 将它记录为当前官方源码可验证的开发/参考平台，而不是擅自写成永久不变的量产 BOM。

## 电机与传感器主总线

当前官方运行时定义：

- Radxa Zero 3W 开发接线上的串口：`/dev/ttyS2`；
- 总线速率：**1,000,000 baud**；
- Dynamixel Protocol 2 兼容通信；
- 15 个电机 ID；
- 一个 ID 为 **200** 的 `imu_to_dxl` 设备；
- 名义控制频率：**50 Hz**。

官方 `robotd.toml` 的注释明确说明，15 个舵机与 `imu_to_dxl` 板共享这条串口总线。

### 电机 ID

```text
左腿          20 21 22 23 24
颈/头/嘴      30 31 32 33 34
右腿          10 11 12 13 14
IMU bridge     200
```

ID 映射来自官方 `duck-control/src/model.rs`。

## 为什么是 15 个电机，但 RL 只有 14 个动作

官方运行时建模了 15 个 joint，而当前 alpha 策略接口为 **61 维 observation → 14 维 action**。

少掉的 action 是有意设计：嘴/喙电机不进入运动策略 action vector。运行时会绕过 mouth slot 映射 14 个策略输出，并独立控制嘴部。

## IMU bridge

官方 `duck-control/src/imu.rs` 明确描述了使用 **ST LSM6DSV16X** 的 **`imu_to_dxl` v2**。

控制环每次读取一个 12 字节数据块：

- gyro x/y/z：有符号 16 位；
- SFLP quaternion x/y/z：IEEE half precision；
- `w` 由主机根据单位四元数约束恢复。

官方源码说明，这个 IMU 数据块与舵机状态在同一总线读取周期内获取，因此主控制 IMU 不需要另开一条主机侧轮询通道。

官方产品规格另行说明整机拥有**两个 IMU：机身一个、头部一个**。公开源码已经明确识别主控制路径上的 LSM6DSV16X，但在 Pollen Robotics 正式确认之前，OpenMicroDuck 不把开发阶段看到的其它 IMU 器件自动写成最终量产头部 IMU 型号。

## 舵机系列

官方 RL 仓库用 Rhoban BAM 模型对 **Dynamixel XL330** 建模，公开 MJCF 资产中也包含 XL330 几何。

官方仿真/运行时公开的重要执行器特性包括：

- 电压相关的执行器响应；
- BAM 中的反电动势与摩擦建模；
- command delay 随机化；
- 电池电压与负载压降随机化；
- 专门的齿隙/backlash 模型变体。

详见 [仿真与强化学习](../simulation/model-and-rl.md)。

## 电池与电源观测

官方产品规格列出：**可拆卸 NP-F550、2600 mAh 摄像机电池**，根据使用方式续航约 1 小时。

当前官方控制源码把电池描述为 2S Li-ion，并使用大致如下的机器人工作区间：

- **8.2 V**：带载满电附近；
- **6.6 V**：机器人工作意义上的低电阈值。

运行时源码同时说明其控制模型没有独立 fuel gauge / ADC 值，而是使用舵机总线报告的供电电压。因此这些数字代表**带载总线可用电压**，不是实验室意义上的电芯 SOC 曲线。

## 摄像头

Press Kit 确认前置摄像头，但明确表示最终分辨率和 FOV 尚在确定。

官方 Radxa Zero 3W 的媒体 bring-up 文档当前使用 **Raspberry Pi Camera v2 / IMX219** 的设备树路径，并通过 Rockchip MPP 做硬件 H.264 编码。这是当前开发平台的强证据，但在官方冻结最终摄像头规格之前，不应把它无条件升级成永久量产 BOM。

## ToF / “LiDAR”

Press Kit 将测距器描述为**紧凑型 8×8 time-of-flight matrix**。

官方源码 vendor/driver 中同时存在：

- ST **VL53L5CX**；
- ST **VL53L8CX**。

由于两代器件都存在于源码、Press Kit 又没有指定最终料号，本项目将最终量产具体型号保留为“未确定”，而不是依据第三方推测二选一。

## 音频

Press Kit 确认麦克风与扬声器。

当前官方源码的 Radxa 开发路径中包含 **TI TLV320AIC3104** codec 的 bring-up 与设备树支持。因此本文把它记录为“当前官方源码证据”，而不是声称所有量产 revision 永远使用同一套音频板实现。

## NFC

官方产品规格列出**两个 NFC 天线**：头部一个、喙部一个。公开产品资料中 NFC tag 被用于触发交互与附件玩法。

## 总线可靠性也是架构的一部分

官方运行时并不假定每次串口事务都成功，而是对孤立总线错误做容错，并设置连续读取失败阈值。官方项目文档也记录了真机上的总线测量。

因此理解 50 Hz 控制系统不能只看“1 Mbps”这个标称值；设备数量、返回延迟、错误处理、调度和实际 loop timing 都属于系统行为的一部分。

## 来源

- https://pollen-robotics.com/microduck/press-kit/
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/model.rs
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/imu.rs
- https://github.com/pollen-robotics/microduck/blob/main/deploy/robotd.toml
- https://github.com/pollen-robotics/microduck/blob/main/docs/design/robotd-design.md
- https://github.com/pollen-robotics/microduck/blob/main/docs/project/media-bringup.md
- https://github.com/pollen-robotics/microduck_rl

独立项目 `fanhao375/microduck-replica` 对这些公开源码做了更激进的电控重建。OpenMicroDuck 对其独立推导部分统一标记为“社区重建”，除非能够再次从上述官方来源确认。
