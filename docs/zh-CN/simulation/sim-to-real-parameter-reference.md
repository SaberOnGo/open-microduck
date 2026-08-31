# Microduck Sim-to-real 参数总表

[English](../../en/simulation/sim-to-real-parameter-reference.md) | **简体中文**

> 这是一份按上游版本固定的官方公开 RL 参数参考。这里的数字很多都属于版本敏感参数，必须和对应 commit 一起看。

本页使用的 `microduck_rl` commit：`d424a0c899f6b33cbd3daeb279913134349c0b63`。

## 1. “Sim-to-real 参数”到底是什么意思？

Policy 能从 Simulation 转移到真实机器人，并不是因为 3D 外观看起来像。

真正影响迁移的是一整条链：

```text
Geometry / Mass / Inertia
        +
Contact / Sole Friction
        +
Servo Voltage / Friction / Delay / Backlash
        +
IMU / Encoder Error
        +
50 Hz Observation / Action Contract
        +
Runtime Action Processing
        ↓
      真实运动
```

Microduck 很轻，而且使用小型 Servo，所以 **Actuator Fidelity 和 Timing** 尤其重要。

## 2. 当前官方 RL 使用的核心 Actuator Model

当前官方 Config 通过 `FrictionDRBamActuatorCfg` 使用 BAM。

| 参数 | 当前公开值 | 含义 |
|---|---:|---|
| Motor Name | `xl330` | BAM Integration 使用的执行器 Family Label |
| BAM Model | `m6` | 当前选择的 Fitted Actuator Model |
| Firmware Position Gain | `kp_fw = 200` | 仿真执行器中保留 Microduck Firmware Stiffness |
| Battery Voltage Sample | **6.5–8.2 V** | 每个 Environment 的输入电压 Randomization |
| Voltage Sag Gain | **0.0–0.2** | Load-dependent Voltage Drop Gain |
| Effective Voltage Floor | **6.0 V** | Sag 之后的最低有效电压 |
| Command Delay | **3–6 Lag Step** | Command / Action Delay Model |
| Target Joint | 14 个非 `passive_*` Joint | Passive Wheel / Backlash Joint 不被驱动 |
| Soft Joint Position Limit Factor | **0.9** | 当前 Articulation Config |

来源：`src/mjlab_microduck/robot/microduck_constants.py`。

### 不要把所有叫 `kp` 的数字放在一起比较

仓库里同时可能看到：

```text
真实 Runtime Servo P Gain
BAM Firmware Gain
Raw MJCF Position Actuator kp
```

这些属于不同控制层，含义和单位可能都不一样。

所以看到 `200`、`0.55` 或其它 `kp`，不能直接说“官方参数互相冲突”。

## 3. BAM 比简单 PD 多模拟了什么？

官方 Microduck RL 使用 BAM 来覆盖理想 Position Controller 很难表达的因素，例如：

- Voltage-control Behavior；
- Back-EMF；
- Coulomb Friction；
- Stribeck / Stiction；
- Load-dependent Friction；
- Battery Voltage Variation；
- Load 下的 Voltage Sag；
- Command Delay。

Microduck 自己的 Wrapper 还加入了每个 Environment 不同的 Friction Scale。

### 一个非常容易踩坑的公开细节

BAM 工作时，MuJoCo 自己的 `dof_frictionloss` 在这条执行器路径里不是主要摩擦来源。

官方 `FrictionDRBamActuator` 是直接缩放 BAM 自己计算出来的 Friction Budget。

所以如果第三方只去 Randomize MuJoCo `dof_frictionloss`，可能表面上“写了摩擦 Randomization”，实际上对 BAM Actuator 没起到预期作用。

## 4. Backlash 怎么模拟？

当前官方 Backlash Variant 会给 14 个 Servo Joint 每一个都串联一个不驱动的 Hinge：

```text
每个 Joint ±1° Play
总 Dead Zone = 2°
```

额外 Joint 的命名类似：

```text
passive_<joint>_backlash
```

关键不只是“加一个空隙”。

官方 `BacklashEncoderBamActuator` 让 Firmware Position Loop 读取：

```text
Servo Joint Position
+
Backlash Joint Position
```

也就是让虚拟 Encoder 看到 Output Side 的实际角度变化。

这比简单往 Joint Angle 上加随机噪声更接近“齿轮间隙”。

## 5. Walking Task 当前打开了哪些 Domain Randomization？

固定版本 `microduck_velocity_env_cfg.py`：

| Randomization | 当前是否开启 |
|---|---|
| Trunk CoM | 开 |
| Head Assembly CoM | 开 |
| kP | 关 |
| kD | 关 |
| Mass + Inertia | 开 |
| BAM Joint Friction | 开 |
| Joint Damping | 关 |
| Armature / Reflected Rotor Inertia | 开 |
| External Velocity Push | 开 |
| IMU Orientation | 开 |
| Encoder Bias | 开 |
| Initial Base Orientation | 关 |

这个表非常重要。

因为“源码里存在一个 Range”并不代表它当前一定参与训练，必须同时看 `ENABLE_*` Toggle。

## 6. Domain Randomization 具体数字

| 参数 | 当前 Range | 说明 |
|---|---:|---|
| Trunk CoM | 初始 **±3 mm**，Curriculum 可扩到约 **±8 mm** | 开启 |
| Head CoM | 初始 **±3 mm** | 开启 |
| Mass + Inertia Scale | **0.95–1.05×** | 两者一起缩放；开启 |
| kP Scale | 0.85–1.15× | Range 存在，但当前关闭 |
| kD Scale | 0.9–1.1× | 关闭 |
| BAM Friction Scale | **0.9–1.1×** | 开启 |
| Joint Damping Scale | 0.9–1.1× | 关闭 |
| Armature Scale | **0.9–1.1×** | 开启 |
| Velocity Push Interval | **3–6 s** | 开启 |
| Velocity Push | **−0.3 ～ +0.3 m/s** | Additive Disturbance |
| IMU Mounting Error | **最大 6° Random-axis** | 开启 |
| Encoder Bias | **−0.015 ～ +0.015 rad**，约 **±0.86°** | 每个 Environment 固定偏置；开启 |
| Initial Base Pitch | 最大 ±10° | 参数存在，但 Base Orientation Randomization 当前关闭 |
| Initial Base Roll | 最大 ±5° | 当前关闭 |

这些数字非常有价值，因为它们说明：官方训练时认为哪些“不确定性”值得主动让 Policy 适应。

但它们是 **Training Randomization Range，不是量产硬件公差规格。**

## 7. Sensor / Observation 误差

当前主要 Actor Contract 使用 Projected Gravity，而不是把一个 Raw Accelerometer Vector 直接塞进 Actor Observation。

两个特别值得关注的 Sensor Error：

### IMU Mounting Error

最大 **6° Random-axis**。

源码注释特别区分：

- Random Mounting Error；
- 已知的固定 Systematic Pitch Bias。

如果真实硬件有一个明确固定的安装偏差，更合理的做法是从 Runtime / Sensor Source 修正，而不是只靠训练 Randomization 去“硬扛”。

### Encoder Bias

每个 Environment 的 Joint Encoder 可以有一个固定偏置：

```text
[-0.015, +0.015] rad
≈ ±0.86°
```

这相当于让 Policy 不能假设所有 Joint Zero 都完美无误。

## 8. External Disturbance

当前 Walking Training 大约每 **3–6 秒**施加一次 Velocity Push：

```text
-0.3 ～ +0.3 m/s
```

源码注释还记录了一个很有价值的训练经验：之前更大的 ±0.5 m/s Disturbance 相对这台小机器人 Walking Speed 太激烈，容易把 Policy 训练成一直处于高度紧张的 Fall-recovery Style。

这说明：

**Randomization 不是越大越好。**

## 9. Rough Terrain 参数

Microduck 的 Rough Terrain 特意按小机器人尺度设计。

基础 Patch：

```text
Size：8 × 8 m
Border：20 m
Rows：10
Columns：20
```

当前 Terrain Mixture：

| Terrain | 比例 | 当前参数 |
|---|---:|---|
| Flat | 25% | 平地 |
| Pyramid Stairs | 25% | Step Height 0–15 mm；Step Width 0.15 m；Platform 2 m |
| Random Grid | 30% | Grid Width 0.45 m；Height 0–10 mm；Platform 1.5 m |
| Pyramid Slope | 20% | Slope 0.03–0.10，约 1.7°–5.7°；Platform 2 m；Vertical Scale 1 mm |

源码直接说明：Microduck 脚能抬起的高度也就是厘米级，所以不能直接套用给大型 Robot 用的 Rough Terrain Default。

### Rough Terrain Contact Softening

当前 Config 为减少 Box Edge 导致的数值不稳定，会把 Terrain Contact 调软：

```text
solref = [0.04, 1.0]
solimp = [0.85, 0.95, 0.001, 0.5, 2.0]
```

这属于 Simulation Stability Parameter，不是说真实地面材料有这样的“物理参数”。

## 10. Foot Contact / Friction Baseline

当前 Robot Config 给 Left / Right Foot Collision Geom 的 Friction Tuple 第一项设置为：

```text
1.0
```

这是 Simulation Contact Setting。

真正实体研究时，应该测量或表征具体 Sole + Floor 的摩擦行为，而不是把 `1.0` 当成某个橡胶材料 Datasheet 值。

## 11. Walking Reward 中 Pose 的宽松程度

下面这些是 **RL Reward-shaping Parameter，不是机械公差。**

### Standing Pose Std

| Joint Group | Std |
|---|---:|
| Hip Yaw | 0.10 rad |
| Hip Roll | 0.05 rad |
| Hip Pitch | 0.15 rad |
| Knee | 0.15 rad |
| Ankle | 0.10 rad |

### Walking Pose Std

| Joint Group | Std |
|---|---:|
| Hip Yaw | 0.30 rad |
| Hip Roll | 0.05 rad |
| Hip Pitch | 0.40 rad |
| Knee | 0.40 rad |
| Ankle | 0.25 rad |

它们反映当前 Reward Design 在 Walking 时允许哪些 Joint 有更大的偏离，不应该复制到 Servo Mechanical Limit 表里。

## 12. Training Timebase

当前 Walking Environment：

```text
NUM_STEPS_PER_ENV = 24
Policy / Control Rate = 50 Hz
```

官方 `AGENTS.md` 强烈建议长训练之前先跑小型 Smoke Test：

```bash
uv run train Mjlab-Velocity-Flat-MicroDuck \
  --env.scene.num-envs 64 \
  --agent.max_iterations 5
```

正常 Quickstart 再使用 4096 Environment。

## 13. Runtime 这一侧也有必须匹配的参数

固定版本 `microduck` Runtime Config 的重要默认值：

| Runtime Parameter | Walking Default / 当前说明 |
|---|---:|
| Control Rate | 50 Hz |
| Action Scale | 0.9 |
| Position Gain | 200 |
| Standing Action Scale | 1.0 |
| Standing Gain Ratio | 0.8 |
| Head Target Low-pass | Vendored Alpha Config 为 0.5 |
| Leg Target Low-pass | Vendored Alpha Config 为 0.7 |
| Voltage Adaptation | 默认 Off |
| Optional Nominal Voltage | 7.4 V |
| Deadman Timeout | 500 ms |

这些属于 **Runtime Execution Layer**，不是 Training DR Range。

## 14. 一个必须单独记录的来源差异：Action Low-pass

这里不能简单写成一句“Microduck 有滤波”或者“没有滤波”。

### 固定版本 Runtime Config 说

Vendored Alpha Walking Config 使用一阶 Low-pass：

```text
Head：0.5
Legs：0.7
```

而 `robotd.toml` 的注释说明这套 Alpha Policy 按匹配的 Filter 训练。

### 同一时期当前 `microduck_rl/develop` 的 `AGENTS.md` 又明确说

当前 Policy Training 是 **Unfiltered**，不要没有匹配 Runtime Flag / Transfer Test 就随便添加 EMA。

### OpenMicroDuck 应该怎样解释？

不能把其中任意一句扩大成“所有 Microduck Policy 永远都这样”。

正确做法是把：

```text
Policy Artifact
+ Training Revision
+ Runtime Action Processing
```

看成一个必须匹配的整体。

Vendored Alpha Policy Lineage 和当前 Development Training Guidance 不能在没有验证的情况下混用。

所以第三方复现时一定要记录：

```text
Training 有没有 Filter？
Deployment 有没有 Filter？
Alpha / Revision 是哪一套？
```

## 15. 真实 Battery 和 Training Voltage Randomization 的关系

这也是两个相关、但不完全相同的层。

### Runtime / Real Robot

当前可用电量映射：

```text
8.2 V = Full under load
6.6 V = Empty for robot use under load
```

Pinned Runtime Config 的 Action Voltage Adaptation 默认关闭。

### Training / BAM

BAM 每个 Environment 从：

```text
6.5–8.2 V
```

采样输入电压，并进一步加入 Load-dependent Voltage Sag，最低 Effective Voltage 6.0 V。

这使 Training Range 覆盖真实 Robot 的主要 Loaded Battery Working Span，同时给了一些 Sag Margin。

## 16. 以后拿到真实 Hardware，最值得测哪些东西？

Simulation 提供的是 Hypothesis / Baseline。

真正硬件研究最值得逐步测量：

- Command → Motion Latency；
- 不同 Voltage 下 Servo Position Response；
- 每个 Joint 的 Backlash Distribution；
- Static / Dynamic Friction；
- 50 Hz 下 Bus Latency / Error Rate；
- Walking / Recovery 时 Loaded Battery Sag；
- Joint Zero / Calibration Offset；
- IMU Mounting Residual Error；
- 能测到的 Body / Link Mass 和 CoM；
- Sole-ground Friction / Contact。

实测以后，不要悄悄把 Simulation Parameter 覆盖掉。

应该同时保存：

```text
官方 Simulation Value
真实 Measured Value
测试条件
硬件 Revision
```

## 17. 在改 Robot Geometry 之前，至少先保住哪些参数？

如果第三方要改模型，最低限度建议先保持：

```text
50 Hz
14-Action Order
61-D Observation Order
HOME_FRAME
Joint Axis / Sign Convention
BAM Actuator，或经过明确验证的等价模型
Voltage Range / Sag Model
Command Delay
Friction Randomization
Mass / Inertia Distribution
IMU Orientation Convention
Encoder Bias Handling
Foot Contact Geometry
```

一次改变太多东西，就会失去“官方 Policy 作为 Baseline”的价值。

## 主要官方来源

- `pollen-robotics/microduck_rl`
  - `src/mjlab_microduck/robot/microduck_constants.py`
  - `src/mjlab_microduck/actuator/friction_dr_bam.py`
  - `src/mjlab_microduck/tasks/microduck_velocity_env_cfg.py`
  - `AGENTS.md`
- `pollen-robotics/microduck`
  - `deploy/robotd.toml`
  - `duck-control/src/model.rs`
  - `duck-control/src/bus.rs`
  - `duck-control/src/imu.rs`
- `Rhoban/bam`

## 相关页面

- [第一步先做仿真](../getting-started/simulation-first.md)
- [可复现训练与 ONNX 导出](reproducible-training-and-export.md)
- [硬件参数总表](../hardware/parameter-reference.md)
- [控制循环与传感器数据流](../software/control-loop-and-sensor-dataflow.md)
