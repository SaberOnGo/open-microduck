# Microduck 公开复现路线图

[English](../../en/getting-started/public-reproduction-roadmap.md) | **简体中文**

> 这是一份根据公开 Microduck 资料整理的研究路线图。它不是 Pollen Robotics 官方装机手册，也不会把尚未公开的量产硬件信息包装成“已经完整逆向”。

## 先说结论

不要把“复现 Microduck”当成一个任务。

更实际的公开研究路线应该拆成：

```text
阶段 0  固定上游版本
阶段 1  官方模型 + 官方 ONNX 先在仿真里跑起来
阶段 2  复现一个官方训练 Task
阶段 3  建立参数 / 证据地图
阶段 4  用小型测试台验证舵机与控制总线
阶段 5  验证 IMU 与控制时序
阶段 6  验证机械子组件
阶段 7  再组合完整实体研究样机
阶段 8  做 Simulation ↔ Hardware 对比
```

每个阶段都应该有明确的“通过标准”，再进入下一步。

## 阶段 0：先固定参考版本

记录：

- `microduck` commit；
- `microduck_rl` commit；
- BAM commit；
- 产品页 / Press Kit 检查日期。

原因：官方项目仍然很活跃。第三方研究还没做完时，上游的 Camera Path、Policy、Model、Gain 或 Randomization Range 都可能已经变化。

**这个阶段的产物：**一套可重复定位的公开资料快照。

## 阶段 1：先让官方 Robot 在 Simulation 里运动

先使用官方 MJCF 和官方已经训练好的 ONNX Policy。

此时不要先改 Geometry，也不要先重新训练。

确认：

- Model 能加载；
- Policy 能加载；
- 61-D Observation / 14-D Action 接口正常；
- Joint 顺序理解正确；
- Walking / Standing 行为基本合理。

详见：[第一步先做仿真](simulation-first.md)。

**需要硬件：**不需要。

**产物：**一条已知可以工作的 Software Baseline。

## 阶段 2：复现一个官方 Training Task

建议先从 Flat Velocity Task 开始。

先跑官方建议的 64 env / 5 iteration Smoke Test，再跑正常训练；通过官方 Exporter 导出 ONNX，再在 CPU MuJoCo 里验证真正导出的 Policy。

这个阶段不是为了马上“训练得比官方更好”，而是完整理解：

```text
MJCF
 ↓
Environment
 ↓
PPO Checkpoint
 ↓
Exporter
 ↓
ONNX
 ↓
Inference
```

**需要硬件：**不需要。

**产物：**自己可以重复跑通的训练 / 部署链路。

## 阶段 3：买完整硬件之前，先建立参数地图

每一个重要参数都建议至少有这些字段：

```text
参数名
数值
单位
来源
来源 commit
证据等级
它影响什么
```

OpenMicroDuck 的：

- [硬件参数总表](../hardware/parameter-reference.md)
- [Sim-to-real 参数总表](../simulation/sim-to-real-parameter-reference.md)

就是这一步的公开起点。

这个阶段一定要允许出现 **Unknown / Unresolved**。

“目前不知道最终连接器”远比自己猜一个然后写进 BOM 更可靠。

**需要硬件：**不需要。

**产物：**有公开证据支撑的参数基线。

## 阶段 4：先做舵机 / 控制总线测试台

完整 15 轴结构还没有之前，就可以先验证电控假设。

官方 Runtime 已经公开得很具体：

- Dynamixel-compatible Bus；
- 1 Mbps；
- 当前 Runtime 的 Motor ID 已知；
- 启动时会校正几个关键 EEPROM Register；
- 目标控制频率 50 Hz；
- Runtime Position P Gain 默认 200；
- 每一轮 Control Tick 做一次组合 State Read，再做一次 Target Write。

小型测试台首先要回答：

- 串口 / Bus Interface 是否理解正确？
- Packet Read / Write 是否正常？
- Timing 是否达到预期？
- Position / Velocity / Voltage 单位是否转换正确？
- Target Position 能不能安全控制？

这个阶段研究的是 **Protocol + Timing**，不是 Walking。

**需要硬件：**只需要完成当前测试所需的最小公开兼容执行器 / 接口组合，不需要一次准备整台机器人。

**产物：**已经验证的舵机 / Bus 控制实现。

## 阶段 5：IMU + 同步状态测试

当前官方 Runtime 把 `imu_to_dxl` v2 放在和舵机相同的 Dynamixel Bus 上，ID 是 200。

重要公开信息包括：

- LSM6DSV16X；
- Gyro + SFLP Quaternion；
- Runtime 使用 12-byte Data Block；
- Gyro ±500 dps；
- 17.5 mdps/LSB；
- Sensor → Trunk 坐标转换；
- Runtime 中的 Spike Rejection / Ready 处理。

第三方公开研究并不需要复制一个**未公开 PCB Layout**，才能研究这个软件接口。

第一目标应该是：

> 能不能提供和官方 Runtime / Policy 所期待的“等价状态信息和时序”？

**产物：**Joint State + Orientation 数据链路。

## 阶段 6：机械结构先分组件验证

不要第一天就追求“整台外壳一次打印出来”。

可以拆成：

```text
左腿
右腿
Neck / Head Linkage
Trunk / Battery / Electronics Volume
Feet / Sole
Optional Roller
```

官方 MJCF 可以直接用于理解：

- Joint Parent / Child；
- Joint Axis 和 Range；
- Body Transform；
- Simulation Mass / Inertia；
- Collision Geometry；
- Mesh Placement。

M2 孔系、轴承几何等，可以参考公开社区重建，但必须继续标为 **Community Reconstruction**。

不要默认 Simulation Mesh 一定包含最终量产的螺纹、公差、嵌件、走线和加工方式。

**产物：**轴线、相对几何和公开 Simulation Model 基本一致的机械子组件。

## 阶段 7：再组合完整实体研究样机

前面几层都理解之后，才把它们合起来：

```text
Compute
 + Motor Bus
 + IMU
 + Power
 + 15 Motors
 + Structure
 + Runtime
 + ONNX Policies
```

Camera、ToF、NFC、Audio 都是 Microduck 的重要功能，但它们不是证明 14-Action Locomotion Loop 能工作的前置条件。

完全可以把这些功能作为独立子系统逐步加入。

也就是说：

**第一次验证 Walking，不应该被“声音、摄像头、NFC 还没做完”卡死。**

## 阶段 8：开始真正做 Sim-to-real 对比

现在才开始逐项对比 Simulation 和真实硬件，例如：

- Home Pose / Joint Zero Offset；
- Joint Position Response；
- Command Delay；
- Backlash；
- Friction；
- Battery Voltage / Voltage Sag；
- IMU Orientation Error；
- Encoder Bias；
- Body Mass / CoM；
- Sole Contact / Friction；
- Control Loop Timing。

不要采用“反正调到会走就行”的方式。

每改一个参数，都最好记录：

```text
为什么改？
依据是什么？
改之前测到了什么？
改之后发生了什么？
```

## 哪些功能可以后做？

如果当前目标只是研究 Locomotion，以下内容可以独立后做：

- Camera Streaming；
- ToF 应用；
- NFC；
- Audio / Voice；
- WebRTC Remote Media；
- 最终外壳外观一致性；
- Roller Accessories。

核心 Locomotion 链路其实小得多：

```text
机械结构
 + 14 个 Locomotion Joint
 + Joint State
 + IMU Orientation / Angular Rate
 + 50 Hz Runtime
 + 正确的 Policy Interface
```

## 哪些东西绝对不要悄悄猜？

没有公开证据前继续标为 Unresolved：

- 量产 PCB Schematic / BOM；
- 最终 Wiring Harness；
- 量产螺丝精确长度和数量；
- 未公开制造公差；
- 官方只确认到“器件家族”时的准确子型号；
- 从另一个 Robot Revision 直接复制过来的数字。

## 第三方公开研究项目也建议把目录分清楚

例如：

```text
research/
├── sources/          # 公开来源、commit、license
├── parameters/       # 有证据的参数表
├── simulation/       # Model / Policy 实验
├── hardware-tests/   # 可复现 Hardware Bench Test
├── mechanics/        # 公开模型推导的机械研究
└── reports/          # 结果和待确认问题
```

这样可以防止一个“临时实现选择”最后被误传成“Microduck 官方规格”。

## 接下来继续看

- [硬件参数总表](../hardware/parameter-reference.md)
- [结构与装配地图](../hardware/structure-and-assembly-map.md)
- [Sim-to-real 参数总表](../simulation/sim-to-real-parameter-reference.md)
- [待确认问题与来源冲突](../research/open-questions-and-conflicts.md)
