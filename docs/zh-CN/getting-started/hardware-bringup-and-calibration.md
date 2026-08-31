# 硬件 Bring-up 与标定：第一次上真机怎么一步一步做

[English](../../en/getting-started/hardware-bringup-and-calibration.md) | **简体中文**

> 这是一套根据官方公开源码整理出的**公开研究流程**，不是 Microduck 官方量产工厂作业指导书。官方参数与第三方建议测试步骤会分开写。

## 目标

不要整机装完以后，机器人一摔倒才开始猜哪里错了。

正确顺序应该是：

```text
电源
 ↓
串口总线
 ↓
1 个舵机
 ↓
全部 Servo ID
 ↓
IMU
 ↓
50 Hz 控制循环
 ↓
关节零位 / Home Pose
 ↓
Head + ToF / Camera 方向
 ↓
安全站立
 ↓
Walking Policy
```

哪一层没通过，就先停在哪一层。

这样电路、机械、软件和 RL 问题不会混在一起。

## 第 1 步：只检查电源

还不让机器人运动，先确认：

- 电源极性正确；
- 电压在预期范围；
- 没有异常发热；
- Linux 主控能稳定启动；
- 舵机总线能读到合理电压。

当前官方 Runtime 使用的工作电压映射大约是：

```text
8.2 V → 满电
6.6 V → 负载下达到机器人停止工作的低电量点
```

这是 Runtime 的工作范围，不是完整电池化学规格。

## 第 2 步：先接 1 个舵机

不要第一天就接 15 个。

先确认一个 Servo：

1. 能正常应答；
2. 能读取 ID；
3. 能读取当前位置；
4. 小幅度写入目标位置后会运动；
5. 正负方向符合预期；
6. 电压和温度读数合理。

一个舵机都没跑通，就没有必要继续怀疑 RL。

## 第 3 步：检查全部公开 ID

当前官方 Runtime 的 ID 映射是：

```text
右腿           10 11 12 13 14
左腿           20 21 22 23 24
Head / Mouth   30 31 32 33 34
IMU Bridge     200
```

不要只相信“线接好了”。应实际扫描并记录每个设备是否稳定应答。

建议至少检查：

| 项目 | 通过标准 |
|---|---|
| 预期 ID | 都能连续应答 |
| 重复 ID | 没有 |
| Position | 稳定、数值合理 |
| Temperature | 静止时合理 |
| Voltage | 接近总线实际电压 |
| 通讯错误 | 足够低，能够稳定跑 50 Hz |

## 第 4 步：匹配 Bus 参数

当前官方公开 Runtime 包括：

- Radxa 参考路径串口：`/dev/ttyS2`；
- 波特率：**1 Mbps**；
- 控制频率：**50 Hz**；
- 每轮：**20 ms**；
- Bus timeout：**30 ms**；
- 固定快照中的 EEPROM 期望值包括 `return_delay_time = 0`、1 Mbps 对应 baud code、`pwm_slope = 255`、`shutdown = 52`。

这里最关键的一点是：

> 很多设备串在同一条总线上时，Servo Factory Return Delay 会吃掉宝贵的 20 ms 控制周期。

所以不能默认出厂设置一定适合整机 50 Hz 控制。

## 第 5 步：先把 IMU 方向搞对

当前官方控制 IMU 是：

**LSM6DSV16X → `imu_to_dxl` v2 → ID 200**。

站立前至少确认：

- 左右转时，Gyro 对应轴变化正确；
- 机器人直立时，Projected Gravity 大致朝下；
- Orientation Filter 已经收敛；
- IMU 到身体主干的安装方向与 Runtime 一致。

IMU 方向错，实体机器人明明站着，软件也可能认为它已经倒了。

## 第 6 步：Joint Zero 与 Home Pose

这是最重要的标定之一。

Runtime Home Pose 必须和 Training Environment 的 `HOME_FRAME` 对上。

当前公开 Home Pose 见：[硬件参数总表](../hardware/parameter-reference.md)。

建议研究流程：

1. 把一个关节机械放到目标参考姿态；
2. 读取 Encoder；
3. 小幅运动确认正方向；
4. 记录“实体零位 ↔ Runtime Joint Angle”的关系；
5. 14 个 Policy Joint 全部检查；
6. 提高刚度、站立前，再肉眼检查一次整机 Home Pose。

不要用“后来在 Observation 里偷偷加 Offset”的方法掩盖错误机械零位。

## 第 7 步：先跑 50 Hz Hold，不要马上 Walking

先让机器人安全保持姿态，然后看：

- 实际 Loop Frequency；
- Missed Tick；
- Bus Read Failure；
- Stale IMU Sample；
- Commanded Position 与 Measured Position；
- Motor Temperature；
- 负载下 Bus Voltage。

官方项目已经在自己的 Radxa 硬件上验证过接近稳定 50 Hz，但第三方实体机仍然必须自己测。

## 第 8 步：Head Sensor 单独测试

### ToF

依次确认：

1. 8×8 Frame 会持续更新；
2. 面对平墙时距离矩阵合理；
3. 转动 Head 后，换算出来的 3D 点方向也正确变化；
4. Floor Filter 正常；
5. ToF 实际安装方向与 Model 一致。

### Camera

依次确认：

1. Camera 能被系统识别；
2. 图像方向正确；
3. 软件记录的安装旋转角和实体一致；
4. Exposure 可用；
5. 先把硬件编码 / 视频流跑通；
6. 最后才开启 `duck-detect` 等视觉 AI。

**Camera Bring-up 和 Camera AI 是两个不同问题。**

## 第 9 步：机械结构按子组件验证

推荐：

```text
一条腿
 ↓
第二条腿
 ↓
Head
 ↓
Foot / Sole Contact
 ↓
整机
```

每个链条检查：

- Joint Axis；
- Joint Center；
- 实际可运动范围；
- Link 相对方向；
- 明显 Backlash；
- 结构干涉；
- 线材是否限制运动。

## 第 10 步：第一次加载 Policy

优先 Stand / Hold，再进入动态 Walking。

第一次动态测试应：

- 速度命令保守；
- 在不会摔坏机器人的安全环境测试；
- 同时观察温度、电压、Loop Statistic；
- 记录准确的 ONNX、Runtime 配置和上游 commit；
- 每次只改一个变量。

如果真机和 Simulation 差很多，优先按这个顺序排查：

```text
Joint Zero / Direction
→ IMU Frame
→ Joint Order
→ Timing / Bus Error
→ Action Scale / Filter / Gain
→ Mechanics / Backlash / Friction
→ Mass / CoM / Contact Model
→ 最后才考虑 RL 重新调参或训练
```

硬件约定都没确认之前，不应该第一反应就是“重新训练”。

## 目前公开资料仍然没有给出的量产标定资料

当前公开资料不足以确认完整量产工厂流程，因此本文不会自己编造：

- Factory Jig 尺寸；
- 量产 Servo Offset 公差；
- 最终线束限制；
- 量产 Camera Intrinsic Calibration；
- 量产 ToF Extrinsic Tolerance；
- 最终 EOL（End-of-Line）验收阈值。

这些保持 **Unknown / Unresolved**。

## 主要公开来源

- https://github.com/pollen-robotics/microduck/blob/main/docs/project/roadmap.md
- https://github.com/pollen-robotics/microduck/blob/main/docs/design/robotd-design.md
- https://github.com/pollen-robotics/microduck/blob/main/scripts/board-test.sh
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/model.rs
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/imu.rs
- https://github.com/pollen-robotics/microduck/blob/main/deploy/robotd.toml

相关页面：

- [公开复现路线图](public-reproduction-roadmap.md)
- [硬件参数总表](../hardware/parameter-reference.md)
- [`robotd` 硬件协议](../software/robotd-hardware-protocol.md)
