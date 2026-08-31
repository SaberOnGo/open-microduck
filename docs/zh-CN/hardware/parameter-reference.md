# Microduck 硬件参数总表

[English](../../en/hardware/parameter-reference.md) | **简体中文**

> 这是一份方便研究和仿真时查阅的公开参数总表。**它不是官方量产 BOM。** 每一部分都会说明参数属于哪一种证据。

## 1. 先看最重要的一页速查

| 项目 | 当前公开值 | 证据等级 |
|---|---|---|
| 产品高度 | 约 25 cm | 官方产品规格 |
| 产品宽度 | 约 14 cm | 官方产品规格 |
| 产品重量 | 低于 800 g；当前商店资料也出现过 780 g | 官方产品规格 |
| 电机数量 | 15 | 官方产品 / 源码 |
| Policy 控制关节 | 14 | 官方源码 / RL |
| 独立 Mouth / Beak Motor | 1 | 官方源码 |
| Runtime 控制频率 | 50 Hz | 官方源码 |
| 每个 Control Tick | 20 ms | 由 50 Hz 直接换算 |
| Motor / IMU 总线 | Dynamixel-compatible Serial，1 Mbps | 官方源码 |
| Control IMU Bus ID | 200 | 官方源码 |
| 主控制 IMU | ST LSM6DSV16X，位于 `imu_to_dxl` v2 | 官方源码 |
| 产品主 SoC | Rockchip RK3566 | 官方产品规格 |
| 当前开发主板 | Radxa Zero 3W | 官方源码 |
| 产品 RAM / Storage | 1 GB / 32 GB | 官方产品规格 |
| 产品 ToF | 8×8 Matrix | 官方产品规格 |
| 当前源码 ToF 支持 | VL53L5CX / VL53L8CX Family | 官方源码；最终量产型号仍待确认 |
| 当前 Camera Bring-up | IMX219 / Raspberry Pi Camera v2 Path | 官方源码；最终产品 Camera 参数仍可能变化 |
| 产品电池 | 可拆卸 NP-F550，2600 mAh | 官方产品规格 |
| Runtime 可用电压映射 | 8.2 V 满 → 6.6 V 负载下空 | 官方源码 |

## 2. 15 个电机到底怎么排？

当前官方 Runtime 明确定义了 **15 个物理 Motor ID**。

Locomotion Policy 只控制其中 14 个，嘴/喙电机故意从 Policy Action Vector 中跳过。

| Runtime Index | Joint | Dynamixel ID | Home Pose | Policy 控制？ |
|---:|---|---:|---:|---|
| 0 | `left_hip_yaw` | 20 | 0° | 是 |
| 1 | `left_hip_roll` | 21 | −5.00° | 是 |
| 2 | `left_hip_pitch` | 22 | −26.24° | 是 |
| 3 | `left_knee` | 23 | −0.28° | 是 |
| 4 | `left_ankle` | 24 | +25.95° | 是 |
| 5 | `neck_pitch` | 30 | +20.00° | 是 |
| 6 | `head_pitch` | 31 | +20.00° | 是 |
| 7 | `head_yaw` | 32 | 0° | 是 |
| 8 | `head_roll` | 33 | 0° | 是 |
| 9 | `mouth` | 34 | Home 为 0° | **否，单独控制** |
| 10 | `right_hip_yaw` | 10 | 0° | 是 |
| 11 | `right_hip_roll` | 11 | +5.00° | 是 |
| 12 | `right_hip_pitch` | 12 | +26.24° | 是 |
| 13 | `right_knee` | 13 | +0.28° | 是 |
| 14 | `right_ankle` | 14 | −25.95° | 是 |

来源：官方 `pollen-robotics/microduck` 的 `duck-control/src/model.rs`，commit `590b986...`。

这个源码快照中的 Mouth Command Range：

```text
Closed：-5°
Fully Open：+30°
```

### 为什么 Home Pose 特别重要？

官方源码专门提醒：Runtime Home Pose 必须和 Training Environment 的 `HOME_FRAME` 一致。

Policy 看到的 Joint Position 是相对这个 Home Frame 的偏移。如果 Home Angle 错了，就等于 14 个 Observation Slot 中持续存在一个固定误差。

所以 **Home Pose 是最重要的 Sim-to-real 参数之一。**

## 3. 官方 Full-collision Simulation Model 的 Joint Limit

下面这些是**官方仿真模型参数**，不是在说零售实体机器的机械硬限位一定和它完全一样。

来源快照：`microduck_rl` 的 `robot_allcollisions.xml`，commit `d424a0c...`。

| Policy Joint | Model Range |
|---|---:|
| `left_hip_yaw` | −25° ～ +30° |
| `left_hip_roll` | −22° ～ +22° |
| `left_hip_pitch` | −90° ～ +90° |
| `left_knee` | −90° ～ +90° |
| `left_ankle` | −90° ～ +90° |
| `neck_pitch` | −90° ～ +60° |
| `head_pitch` | −90° ～ +90° |
| `head_yaw` | −170° ～ +170° |
| `head_roll` | −25° ～ +25° |
| `right_hip_yaw` | −30° ～ +25° |
| `right_hip_roll` | −22° ～ +22° |
| `right_hip_pitch` | −90° ～ +90° |
| `right_knee` | −90° ～ +90° |
| `right_ankle` | −90° ～ +90° |

注意：这些 MJCF Range 比正常站立和走路时实际使用的角度范围大得多。

## 4. 官方 Simulation Model 的质量参数

`robot_allcollisions.xml` 给每一个刚体都写了 Inertial Mass。

把本轮固定版本里的 15 个 Rigid Body Mass 相加：

```text
约 737.243 g
```

这是**官方 Simulation Model 的质量总和**，不是拿一台量产机器放秤上的实测结果。

对应各刚体：

| Body / Link | Mass |
|---|---:|
| `trunk_base` | 199.224 g |
| 左 Hip-yaw Link | 23.041 g |
| 左 Hip-roll Link | 6.189 g |
| 左 Upper Leg | 48.207 g |
| 左 Lower Leg | 21.584 g |
| 左 Ankle / Foot Link | 30.025 g |
| `neck` | 36.841 g |
| `neck_pitch` Link | 5.720 g |
| `yaw_roll_motion` | 48.600 g |
| Head-roll / `jaw_soft` Body | 188.766 g |
| 右 Hip-yaw Link | 23.041 g |
| 右 Hip-roll Link | 6.189 g |
| 右 Upper Leg | 48.207 g |
| 右 Lower Leg | 21.584 g |
| 右 Ankle / Foot Link | 30.025 g |

可以很直观地看到：Head Assembly 占整台小机器质量的比例很大。

所以对这种 700 多克级别的小型双足机器人来说，Head / Neck Dynamics 绝不是可以完全忽略的东西。

## 5. Motor Bus 和 Timing

本轮固定官方 Runtime 源码中的实现：

```text
当前 Radxa Zero 3W Port：/dev/ttyS2
Baud：1,000,000 bit/s
Control Loop：50 Hz
Period：20 ms
Servo Device：15 个
IMU Bridge：ID 200
```

每个正常 Control Tick 大致做：

```text
1 次组合 sync_read
  ├─ 先读取 imu_to_dxl ID 200
  └─ 再读取 15 个 Servo

然后

1 次 sync_write
  └─ 写入 Servo Goal Position
```

官方源码特意把 IMU ID 放在前面，让 IMU Response 在 Servo Burst 之前回来。

### Servo State Read

当前代码从 Dynamixel Register Address **124** 开始读取 **12 bytes**。

这个范围覆盖 Present PWM / Current / Velocity / Position 等数据，Runtime 使用其中自己需要的字段。

公开源码里的重要换算参数：

- Dynamixel Velocity：**0.229 rpm/count**，之后再转换到 rad/s；
- Bus Voltage：**0.1 V/count**；
- Voltage / Temperature Slow Read：大约 **1 Hz**；
- Bus Read Timeout：**30 ms**。

## 6. 启动时 Runtime 会检查哪些 Servo EEPROM 参数？

官方当前源码会校正 / 固定：

| Register | Expected Value | 作用 |
|---|---:|---|
| `return_delay_time` | 0 | 避免 Factory Delay 大量占用 20 ms Tick |
| `baud_rate` | 3 | Dynamixel 中对应 1 Mbps；必须和 Runtime 一致 |
| `pwm_slope` | 255 | 当前 Alpha 固定设置 |
| `shutdown` | 52 | 当前 Runtime 使用的错误保护 Mask |

这里最值得理解的是 `return_delay_time`。

官方源码直接给出计算：

```text
Factory return_delay_time = 250
≈ 500 μs / Device
16 Device × 500 μs
≈ 8 ms
```

20 ms 才是一整个 50 Hz Control Tick。

也就是说，仅仅 Factory Return Delay 就可能吃掉大约 **40% 的 Control Period**。

这说明一些看起来很小的 Servo Register，实际上会直接影响双足控制时序。

## 7. Runtime P Gain = 200，但不要和仿真 Gain 混为一谈

当前 Runtime 默认：

```text
Position P Gain = 200
I = 0
D = 0
```

这是**真实 Servo Register / Runtime 控制层**的参数。

BAM 或 MJCF 里也会出现 `kp`、actuator gain、forcerange 等数字，但它们可能属于不同模型、不同单位。

因此绝对不要看到两个都叫 `kp`，就直接说“官方参数冲突”。

Runtime 还会对 Standing、Skill、Safety State 使用不同的 Gain Ratio / Gain Handling，具体以对应版本 `robotd.toml` 为准。

## 8. Control IMU：`imu_to_dxl` v2

当前官方控制源码明确识别：

```text
Sensor：ST LSM6DSV16X
Bridge：imu_to_dxl v2
Dynamixel ID：200
```

Runtime 在和 Servo 同一类 Transaction 中读取一个 **12-byte Block**。

### 12-byte 数据怎么排？

| Bytes | 数据 |
|---|---|
| 0–5 | Gyro X/Y/Z，Little-endian Signed 16-bit |
| 6–11 | SFLP Quaternion X/Y/Z，IEEE Half Float；W 在 Runtime 中重建 |

源码还明确给出：

- Gyro Range：±500 dps；
- Gyro Scale：**17.5 mdps/LSB**；
- Runtime 转成 rad/s；
- Quaternion 会进一步变成 Projected Gravity / Orientation，进入控制状态。

SFLP Decoder 会先等待大约 **25 个有效 Quaternion Sample** 才进入 Ready，大约是 100 Hz 下的 0.25 s。

Runtime 还对 Gyro / Gravity 相关数据做类似 Median-of-three 的 Spike Rejection。

### IMU 安装方向

公开源码记录的默认 Sensor-to-trunk 方向大约是绕 Y 轴 +90°，Raw Axis 转成 Trunk Frame 的对应关系可以概括为：

```text
[ +raw_z, +raw_y, -raw_x ]
```

这类坐标轴转换非常关键。

**IMU 型号完全正确，但安装方向/Axis Mapping 错了，一样可以让正常 Policy 立刻失效。**

## 9. Battery / Power 参数

### 产品级电池

官方产品资料：

```text
NP-F550
2600 mAh
2S Li-ion Class
可拆卸
```

### Runtime 电量映射

当前公开控制路径没有看到一个独立 Fuel Gauge 作为主要电量来源，而是使用 Servo 自己报告的 Supply Voltage。

固定版本源码把负载下可用范围映射成：

```text
8.2 V → 100%
7.4 V → 50%
6.6 V → 0%
```

官方源码特别说明：**6.6 V 是“机器人负载下已经不适合继续工作的可用下限”，不是电芯化学意义上的绝对空电。**

机器人运动时 Voltage 会 Sag，这个区别对 Simulation / Hardware 对比很重要。

## 10. 当前 Development Compute / HAT Interface

这一节是**官方源码开发实现**，不是完整量产 Schematic。

### Compute

- 产品 SoC：RK3566；
- 当前官方 Bring-up：Radxa Zero 3W；
- 当前 Motor / IMU Serial：`/dev/ttyS2`。

### HAT I2C

官方 Device-tree Overlay 显示：

```text
RK3566 I2C3 M0
40-pin Header Pin 3 / 5
400 kHz
SDA：GPIO1_A0
SCL：GPIO1_A1
```

源码注释还写出了 HAT 上一对 **10 kΩ Pull-up：R12 / R13**，并提醒长线缆电容可能导致需要降到 200 kHz。

### 这条开发 I2C Bus 上公开看到的器件

| Device / Function | 公开信息 |
|---|---|
| TLV320AIC3104 Audio Codec | I2C `0x18` |
| BMI088 | `0x19` / `0x68`；当前源码注释标为 Dormant / 未使用路径 |
| ToF | I2C `0x29`，经 HAT / Stemma Path |

这套 Overlay 会把 I2C3 Remux 到 Header，并关闭冲突的 FUSB302 USB-C PD Controller Path。源码说明 USB-C 默认 5 V 行为仍存在，而 Robot Power 由 HAT 方案提供。

## 11. Audio Development Path

官方 Device-tree Bring-up 已经把很多信息写得很清楚：

```text
Codec：TLV320AIC3104
I2C Address：0x18
I2S：I2S3 / 2 Channel
Codec MCLK：12.000 MHz
CPU-side I2S System Clock：12.288 MHz
Linux Sound Card Name：aic3104
```

这些足以研究当前 Development Audio Architecture，但仍不能当成完整量产 Audio Schematic。

## 12. Camera 与 ToF

### Camera

当前官方 Rockchip / Radxa Media Bring-up 使用 **IMX219 / Raspberry Pi Camera v2 类 Path**。

最终产品 Camera Resolution / FOV 仍应该优先按最新官方 Product / Press Material，而不能因为某一个 Development Module 就提前写死。

### ToF

产品层明确承诺：**8×8 Depth / ToF Matrix**。

官方源码支持 ST Multi-zone Family，包括 **VL53L5CX 和 VL53L8CX**。

如果产品页还没有锁定准确型号，就继续把最终 Production Part 标为 Unresolved。

另外，当前 Runtime Architecture 把 ToF 放在独立 Service 中，并没有把 8×8 Depth Matrix 直接塞进 61-D Locomotion Observation。

## 13. 官方 Simulation Model 还透露了哪些“零件数量”？

固定版本 `robot_allcollisions.xml` 的 Visual Instance 中可以直接看到：

- 15 个 `xl330` Motor Mesh；
- **11 个**明确命名为 `seeed_bearing__configuration__22x16x4` 的大轴承 Mesh Instance；
- **3 个**较小的 `seeed_bearing__configuration_default` Mesh Instance；
- Battery、PCB/HAT、Speaker、Lens、Shell、Foot、Sole 等结构 / 占位资产。

这些是**Simulation Model Instance 数量，不是量产采购数量。**

其中大轴承 Asset Name 直接写出了 **22×16×4 mm**。

社区公开几何分析把较小的 Default Bearing 估算为大约 **15×10×3 mm**。

## 14. 特别小心“模型文件名陷阱”

官方 Simulation Asset 中保留了一些历史 / Development Placeholder 命名。

两个非常典型的例子：

- Model 里有 `np_f970` 名称的 Mesh，但当前官方产品规格是 **NP-F550**；
- Asset Library 有 Raspberry-Pi-related PCB 名称，但当前官方 Runtime Bring-up 已经明确使用 **Radxa Zero 3W**。

所以必须记住：

> **Asset Filename ≠ 当前量产 BOM。**

Simulation Asset 主要用于理解 Geometry、Volume、Assembly Placement 和 Dynamics，不能拿旧文件名覆盖更新的 Product / Runtime Evidence。

## 15. 现在还不能确定的东西

下面这些暂时不要写成“量产已确认”：

- XL330 精确子型号；
- `imu_to_dxl` v2 完整 Schematic / BOM；
- Robot HAT 完整 Schematic / BOM；
- 如果产品资料仍然只写 Family，最终 Production ToF Part；
- 最终 Camera Module / Lens / FOV；
- 第二 IMU 的最终 Production Role / Location；
- NFC Controller IC；
- Microphone / Speaker 精确型号；
- 完整 Fastener Length / Count；
- Production Bearing Spec / Quantity；
- Wiring Harness / Connector / Cable Length；
- Manufacturing Material / Tolerance / Insert。

## 主要来源

- https://github.com/pollen-robotics/microduck
- `duck-control/src/model.rs`
- `duck-control/src/bus.rs`
- `duck-control/src/imu.rs`
- `deploy/robotd.toml`
- `deploy/audio/i2c3-pihat.dts`
- `deploy/audio/aic3104-i2c3.dts`
- https://github.com/pollen-robotics/microduck_rl
- `src/mjlab_microduck/robot/microduck/robot_allcollisions.xml`
- Microduck 官方 Product Page / Press Kit

## 相关页面

- [公开硬件清单](public-bom.md)
- [结构与装配地图](structure-and-assembly-map.md)
- [社区推导 BOM 与紧固件](community-bom-reconstruction.md)
- [Sim-to-real 参数总表](../simulation/sim-to-real-parameter-reference.md)
