# 电控、总线、传感器与电源

[English](../../en/hardware/electronics-and-buses.md) | **简体中文**

> 范围：Pollen Robotics 官方产品资料与官方源码中能够验证的信息。开发/参考硬件与最终量产产品规格分开标注。

## 明确电子器件速查

| 功能 | 已公开器件 | 接口 / 地址 | 证据状态 |
|---|---|---|---|
| Linux 主控板 | **Radxa Zero 3W** | 40-pin、CSI、Wi-Fi/Bluetooth | 官方源码中的开发/参考平台 |
| SoC | **Rockchip RK3566** | — | 官方产品规格 |
| 舵机总线 | **15 × ROBOTIS Dynamixel XL330** | UART2 `/dev/ttyS2`、Dynamixel Protocol 2、**1 Mbps** | 官方源码 |
| 主控制 IMU | **ST LSM6DSV16X** | `imu_to_dxl` v2、Dynamixel ID **200** | 官方源码 |
| 音频 Codec | **TI TLV320AIC3104** | I2C **0x18**、I2S | 官方源码中的开发硬件 |
| HAT IMU | **Bosch BMI088** | I2C **0x19 / 0x68** | 官方源码中的开发硬件；当前标注 dormant/unused |
| 前置摄像头 | **Sony IMX219 / Raspberry Pi Camera v2 路径** | MIPI CSI | 官方源码中的开发硬件 |
| ToF | **ST VL53L5CX / VL53L8CX** | I2C **0x29** | 官方源码同时支持；量产具体型号未确认 |
| 产品电池 | **NP-F550，2600 mAh** | 可拆卸摄像机电池 | 官方产品规格 |
| NFC | 两个天线 | 头部 + 喙部 | 官方产品规格；控制 IC 未公开 |

## 根据公开源码整理的系统图

```text
                         Radxa Zero 3W
                      Rockchip RK3566 Linux
                              │
        ┌─────────────────────┼────────────────────┐
        │                     │                    │
 UART2 / ttyS2             MIPI CSI              I2C3 M0
 Dynamixel V2              IMX219 路径          400 kHz
 1 Mbps                       │                    │
        │                     │          ┌─────────┼──────────┐
        │                     │          │         │          │
        │                     │   TLV320AIC3104  BMI088    ToF 0x29
        │                     │      0x18       0x19/0x68  VL53L5/8CX
        │
   ┌────┴────────────────────────────┐
   │                                 │
15 × Dynamixel XL330          imu_to_dxl v2
                                     │
                               LSM6DSV16X
                               device ID 200
```

这是一张根据公开源码整理的说明图，**不是官方原理图**。

## 主控平台

### 产品级规格

Pollen Robotics 已公开：

- **Rockchip RK3566**，带 AI 加速器；
- **1 GB RAM**；
- **32 GB 存储**；
- Wi-Fi + Bluetooth。

### 当前官方源码中的开发板

当前 bring-up、媒体、设备树和部署文件都指向 **Radxa Zero 3W**。官方 overlay 中可直接看到兼容字符串：

```text
radxa,zero-3w
rockchip,rk3566
```

因此 OpenMicroDuck 把 Radxa Zero 3W 记录为**当前官方源码可验证的开发/参考板**，而产品级不变规格只写 RK3566。

## 舵机 / IMU 共用总线

当前官方运行时定义：

- 端口：**`/dev/ttyS2`**；
- 波特率：**1,000,000**；
- 协议：Dynamixel Protocol 2 兼容；
- 名义控制频率：**50 Hz**；
- 15 个舵机 ID + `imu_to_dxl` ID 200。

### 设备 ID

```text
左腿           20 21 22 23 24
颈/头/嘴       30 31 32 33 34
右腿           10 11 12 13 14
imu_to_dxl      200
```

15 个舵机与 IMU bridge 共用同一条总线。嘴部电机不进入 14 维 locomotion policy action。

## `imu_to_dxl` v2

官方 `duck-control/src/imu.rs` 明确写出传感器为 **ST LSM6DSV16X**。

控制环读取 12 字节数据：

- gyro x/y/z：`i16` little-endian；
- SFLP quaternion x/y/z：IEEE binary16；
- quaternion `w` 由主机恢复。

源码还说明，IMU 数据与舵机状态走同一共享总线读取路径。

目前**没有公开** `imu_to_dxl` v2 的完整原理图/BOM，所以 MCU、总线收发电路、稳压器和被动器件不能擅自补成“已知料号”。

## Pollen Robotics RPI Robot HAT

官方源码明确称当前 Radxa 开发路径上的定制板为 **Pollen Robotics RPI Robot HAT**。

### 当前源码已经明确的 HAT 器件

| 器件 / 参数 | 公开值 |
|---|---|
| 音频 Codec | **TI TLV320AIC3104**，I2C **0x18** |
| 第二颗 IMU | **Bosch BMI088**，**0x19 / 0x68**，当前标注 dormant/unused |
| ToF 路径 | **0x29**，经 Stemma J5 |
| I2C 总线 | RK3566 **I2C3 M0**，header pin 3/5 |
| I2C 频率 | **400 kHz** |
| Codec MCLK | **12 MHz** 固定时钟 |
| 当前 overlay 的 CPU 侧 I2S 时钟 | **12.288 MHz** |
| 官方源码注释明确提到的 I2C 上拉 | **R12/R13，一对 10 kΩ** |

### I2C3 复用细节

官方 `i2c3-pihat.dts` 说明，HAT 使用 RK3566 I2C3 的 M0 pinmux。Radxa 原本在 M1 位置用同一个控制器连接 **FUSB302** USB-C PD 控制器；官方 overlay 会把 I2C3 重新复用到 HAT 的 pin 3/5，并在该模式下禁用 FUSB302 设备树节点。

这属于开发平台细节，但它让公开接线比“只有产品规格表”具体得多。

## 摄像头

官方媒体 bring-up 使用 **Raspberry Pi Camera v2 / Sony IMX219** 路径，并在 Radxa Zero 3W 上通过 Rockchip MPP 做硬件 H.264 编码。

同时 Press Kit 又明确说最终 camera resolution / FOV 仍在确定。因此应区分：

- **当前官方开发路径确认 IMX219**；
- **最终量产摄像头模组和镜头尚不能写死**。

## ToF

官方产品规格确认**8×8 time-of-flight matrix**。

官方源码同时 vendor/support：

- **ST VL53L5CX**；
- **ST VL53L8CX**。

当前 HAT 接线把 ToF 设备放在 **I2C 地址 0x29**。因为两代器件都存在于官方源码，所以不能在没有更强证据时擅自挑一个写成最终量产 BOM。

## 音频

当前开发音频路径已经非常明确：

```text
RK3566 I2C3 ──> TLV320AIC3104 @ 0x18   控制
RK3566 I2S3 ──> TLV320AIC3104          音频数据
12 MHz fixed clock ──> codec MCLK
```

产品规格另外确认 microphones + speaker，但具体麦克风和扬声器料号目前没有公开。

## 电池与电压观测

官方产品资料明确写 **NP-F550、2600 mAh** 可拆卸电池。

当前官方运行时通过舵机报告的总线电压工作，定义的带载可用区间大致为：

- **8.2 V**：满电附近；
- **6.6 V**：机器人工作意义上的空电阈值。

源码注释同时说明，这个控制模型没有使用独立 fuel-gauge / ADC 数值来生成该电量读数。

## 已确认存在但具体料号仍不完整的产品器件

官方产品资料还确认：

- **2 个 IMU**，body + head 各一个；
- **2 个 NFC 天线**，head + beak 各一个；
- microphones + speaker；
- 专用 camera-use indicator。

当前源码能够确认 LSM6DSV16X 和开发 HAT 上 dormant 的 BMI088，但现有公开证据还不足以把最终量产 body/head 两颗 IMU 完整映射到固定芯片料号。

## 来源

- https://pollen-robotics.com/microduck/press-kit/
- https://store.pollen-robotics.com/products/microduck
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/model.rs
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/imu.rs
- https://github.com/pollen-robotics/microduck/blob/main/deploy/robotd.toml
- https://github.com/pollen-robotics/microduck/blob/main/deploy/audio/i2c3-pihat.dts
- https://github.com/pollen-robotics/microduck/blob/main/deploy/audio/aic3104-i2c3.dts
- https://github.com/pollen-robotics/microduck/blob/main/docs/project/media-bringup.md
- https://github.com/pollen-robotics/microduck_rl

更完整的部件表见：[公开硬件清单与 BOM 状态](public-bom.md)。模型推导出的螺丝、轴承和装配信息见：[社区推导 BOM](community-bom-reconstruction.md)。