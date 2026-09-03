# 硬件变体仿真：软件不变，只修改物理机器人

[English](../../en/simulation/hardware-variant-simulation.md) | **简体中文**

> 公开来源状态核对：**2026-09-03**。
>
> 本页说明怎样利用 Microduck 当前公开的仿真工作，研究“软件接口保持 Microduck 兼容，但执行器和机械参数发生变化”的硬件变体。

## 1. 先用一分钟看懂

最重要的是先分清两种仿真：

```text
普通 RL 仿真
训练程序 ──> MuJoCo 机器人

硬件变体的软件在环研究
真实 Microduck 控制栈（`robotd`）
              │
              │ RobotIo / TCP 边界
              ▼
      MuJoCo 机器人模型
              │
              ├─ 执行器动力学
              ├─ 质量 / 质心 / 惯量
              ├─ 几何 / 碰撞
              ├─ 摩擦 / 接触
              └─ 齿隙等机械因素
```

第二种方式的价值在于：硬件 I/O 边界以上的软件，不需要知道下面是一台桌面上的真机，还是 MuJoCo 里的虚拟机体。

因此，只要保持 Microduck 对软件暴露出来的接口兼容，就可以在下面替换物理模型，再观察同一套控制软件和策略会怎样表现。

## 2. 目前公开上游到底做到哪一步？

这套链路有两半，而且成熟度不同。

### 已合并到 `microduck_rl/develop`

在 commit `29e887ecfbf5d37144759e5a9f8a176dfb83d547`，官方公开仓库 `pollen-robotics/microduck_rl` 已经包含 `duck-body`：

```text
src/mjlab_microduck/sim/body_server.py
```

它可以通过 TCP 提供一个 MuJoCo Microduck 机体，并且支持指定自定义场景：

```bash
uv run duck-body --scene path/to/scene.xml
```

`duck-body` 不是依赖 MuJoCo 里对象的固定数字序号，而是按关节名去找 actuator。这样修改 MJCF 后，即使对象顺序发生变化，也不容易因为“序号悄悄变了”而控制错关节。

**证据等级：官方公开仓库，已合并到 `develop`。**

### 官方公开分支，但还没有进入 `microduck/main`

对应的 daemon 侧目前位于官方公开分支：

```text
pollen-robotics/microduck: sim-remote-io
```

这个分支加入：

```bash
robotd --sim HOST:PORT
```

并在和真机相同的 `RobotIo` 边界下面加入 `RemoteIo`。

上游公开设计文档明确写明：`RobotIo` 以上继续走真实软件路径，包括 50 Hz 控制循环、ONNX Policy、Safety、跌倒检测、里程计、运动学、IPC、`robotctl` 等。

**证据等级：官方公开上游实验分支；截至 2026-09-03，尚未合并进 `main`。**

所以目前正确的说法是：这套思路已经有公开实现，可以用于研究，但 daemon 侧还不能当成稳定发布接口。

## 3. MuJoCo 里的机器人可以换吗？

可以，但最好保持 Microduck 的软件兼容边界。

已合并的 `duck-body` 提供 `--scene`，因此研究者可以让它加载另一份 MuJoCo scene，而不是只能加载默认官方场景。

如果目标只是研究硬件参数变化，最省事的做法是让修改后的模型从软件看来仍然是一台 Microduck。

建议保持这些接口不变：

- Microduck 的关节拓扑和 wire contract 使用的关节命名；
- Policy 控制的 14 个腿 / 颈 / 头关节；
- 15 关节 wire list 中现有的嘴/喙约定；
- 对应 Microduck 关节名的 actuator；
- `duck-body` 当前要求的 `trunk_base_freejoint`；
- 如果沿用当前 body-server 的传感器放置，则保留 `tof` site；
- 如果继续复用当前 alpha Policy，则保持 **61 维 observation → 14 维 action、50 Hz** 的 Policy 接口。

换句话说：**改物理实现，比改软件能看到的“骨架接口”容易得多。**

## 4. 更换执行器后，哪些参数应该跟着改？

更换舵机/执行器，不能只改一个扭矩数字。

一个有物理意义的模型通常需要同时检查下面几组参数。

### 执行器动力学

可能需要修改：

- 扭矩 / 力能力；
- 速度响应；
- 位置控制响应；
- 摩擦与静摩擦；
- 反电动势相关行为；
- 电压变化和负载压降；
- command delay；
- backlash / 齿隙；
- reflected inertia / armature；
- 如果机械行程不同，还要检查 joint limit / 可用角度范围。

### 质量属性

执行器或安装方式改变后，可能同时改变：

- link mass；
- center of mass / 质心；
- inertia tensor / 惯量张量；
- 整机质量分布。

外形看起来一样，不代表平衡行为一样。质量和惯量分布一变，双足机器人就可能明显更难站稳。

### 机械几何

不同尺寸的执行器可能要求修改：

- 支架和固定结构；
- 外壳净空；
- link geometry；
- collision geometry；
- 执行器相对关节轴的位置。

### 接触与材料

结构或材料变化后，还可能需要重新检查：

- 脚底/地面摩擦；
- 身体接触摩擦；
- contact geometry；
- damping / compliance 近似；
- TPU 等柔性结构对应的软接触假设。

## 5. 最容易漏掉：当前基线仍然是 XL330

当前上游仿真**不是通用舵机模拟器**。

官方 RL 栈使用的是面向 Dynamixel XL330 家族拟合的 BAM actuator behavior。`duck-body` 代码还把 daemon 里的 firmware gain `kp = 200` 当作参考值，并按相对比例去缩放 MuJoCo actuator gain。

所以这种修改并不充分：

```text
旧舵机扭矩 = A
新舵机扭矩 = B
只把 A 改成 B
```

如果新执行器的响应明显不同，而仿真仍然保留 XL330 拟合出来的动力学，那么它很可能仍然表现得像“改了几个数字的 XL330”。

要做可信的硬件变体研究，应尽量用公开测量或公开实验去替换、拟合或校准新的 actuator model。没有可靠数据的参数，应明确标成假设或不确定项，而不是包装成已确认事实。

## 6. 这套方法可以验证什么？

把 daemon 侧公开实验分支和 MuJoCo body 连起来后，可以用修改后的物理模型去跑 `RobotIo` 以上的真实软件路径。

适合回答的问题包括：

- 同一套 Policy 在新的 actuator response 下还能不能稳定？
- joint tracking 会不会明显变慢或振荡？
- 行走、站立、sit/stand、跌倒恢复时是否更容易失败？
- 质量和惯量变化会不会破坏平衡或恢复动作？
- 结构变化是否引入新的碰撞？
- backlash / friction 改变后，落脚和里程计表现会怎样？
- 模拟机体出现异常时，真实 Safety 路径能不能正确反应？

可以比较的客观指标包括：

- task success rate；
- episode survival / fall rate；
- body tilt；
- joint tracking error；
- 模型中的 actuator saturation / force demand；
- foot slip；
- 不希望出现的 body contact；
- recovery time；
- 有 ground truth 时的 trajectory / odometry error。

最有价值的实验不是“一次改十几个东西”，而是尽量让每次变化都有明确记录，这样性能变差时还能追到原因。

## 7. 它不能验证什么？

上游公开设计文档对边界写得很清楚。

这套 twin 不会把真实硬件 driver 也自动变成虚拟硬件。公开设计明确把下面这些放在 twin 边界之外：

- 真实 Dynamixel bus driver；
- 真实总线丢包和通信错误；
- 真实 servo encoder；
- 硬件 thermals；
- 真实 battery system；
- camera / ISP / NPU 等硬件专用路径。

因此，自定义 MuJoCo actuator model 可以研究 **`RobotIo` 以上的物理和控制行为**，但它不能证明另一种舵机协议、register map、总线 timing 或硬件 driver 在真实开发板上一定可用。

那属于另外一层硬件 bring-up 工作。

## 8. 小白最推荐的实验顺序

```text
1. 固定上游 commit
        ↓
2. 先跑官方模型，建立 baseline
        ↓
3. 复制一份 scene/model 作为硬件变体
        ↓
4. 修改 actuator + 由它引起的物理参数
        ↓
5. 保持软件能看到的 Microduck 接口不变
        ↓
6. 跑同一个 Policy / 同一组命令
        ↓
7. 比较客观指标
        ↓
8. 记录哪些是测量、推导、假设和未知项
```

不要一开始就把很多互不相关的参数一起改掉。否则即使结果坏了，也很难判断究竟是哪一个因素造成的。

## 9. 推荐把 baseline 和变体分开保存

公开研究可以使用类似结构：

```text
models/
├── upstream-baseline/
└── actuator-variant-example/
    ├── scene.xml
    ├── robot.xml
    ├── actuator-parameters.md
    └── provenance.md
```

目录名不是重点。重点是每个修改过的值都能追溯到：公开来源、公开测量，或者明确写成假设。

## 10. 结果应该怎样标证据等级？

建议统一使用：

| 标签 | 含义 |
|---|---|
| **官方来源** | 直接来自 Pollen Robotics 官方公开仓库或页面 |
| **公开实测** | 有公开测试方法和上下文的测量 |
| **社区结果** | 公开第三方实验或重建 |
| **推导** | 根据公开输入计算得到 |
| **假设** | 因证据不足而为了仿真暂时选用的值 |
| **未确认** | 当前没有足够证据 |

MuJoCo 里跑成功，只能写成**仿真结果**，不能直接写成“已证明真机等价”。

## 11. 2026-09-03 需要记住的上游状态

- `microduck_rl/develop` 已经包含 `duck-body`，并支持 `--scene`；
- body server 按 Microduck 关节名寻找 actuator；
- 当前 actuator baseline 仍然是 XL330 / BAM 方向；
- daemon 侧 `robotd --sim` 目前公开在 `sim-remote-io` 分支，还没有进入 `microduck/main`；
- 最新模型重导出把原先“只包含部分地面接触碰撞”的 `allcollisions` 角色改名为 `groundcontact`，并新增真正的 `robot_allcollisions.xml`，让所有部件都可以带 collision geometry；
- 上游 ToF simulator 最近修复过一次左右列方向约定错误，这也说明 sensor frame / coordinate convention 同样属于仿真 fidelity 的一部分。

## 主要公开来源

- https://github.com/pollen-robotics/microduck_rl
  - `src/mjlab_microduck/sim/body_server.py`
  - `src/mjlab_microduck/robot/microduck/`
- https://github.com/pollen-robotics/microduck/tree/sim-remote-io
  - `robotd/src/main.rs`
  - `docs/design/simulation.md`
- https://github.com/Rhoban/bam

## 相关 OpenMicroDuck 文档

- [仿真与强化学习](model-and-rl.md)
- [Sim-to-real 参数总表](sim-to-real-parameter-reference.md)
- [仿真模型资产参考](model-assets-reference.md)
- [`robotd` 硬件协议](../software/robotd-hardware-protocol.md)
- [硬件 Bring-up 与标定](../getting-started/hardware-bringup-and-calibration.md)
- [上游版本基线](../upstream/version-matrix.md)
