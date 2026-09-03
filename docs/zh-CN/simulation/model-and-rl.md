# 仿真与强化学习

> 主要参考：官方 `pollen-robotics/microduck_rl` 仓库。
>
> 核心上游状态最近一次核对：**2026-09-03**。

## 官方训练栈

Microduck 的动作策略在仿真中训练，再导出到机载运行时。当前官方 RL 仓库使用：

- **mjlab**；
- **MuJoCo / MuJoCo Warp**；
- **PPO**；
- 面向 Dynamixel XL330 的 **BAM** 执行器模型；
- domain randomization；
- ONNX 部署导出。

策略控制频率为 **50 Hz**，与机载控制环一致。

## 统一部署接口

当前 alpha 策略家族使用：

```text
actor observation：61 维
policy action：     14 维
控制频率：          50 Hz
```

61 维 observation = 48 维本体感觉 + 13 维命令：

```text
base angular velocity      3
projected gravity          3
joint position            14
joint velocity            14
previous actions          14
----------------------------
本体感觉                   48

twist command              3
head-pose command           4
body-pose command           6
----------------------------
命令区                     13

总计                       61
```

14 维 action 控制腿、颈和头部关节；嘴/喙电机不进入策略 action vector。

## 官方 RL 中的任务类型

最近一次检索时，官方环境包含：

- 速度命令行走；
- 行走 + 跌倒恢复；
- 起身；
- 坐下 ↔ 站起；
- 低头拾取/喙触地；
- 踢球；
- 前滚翻（`roulade`）；
- 滚轮运动；
- 滚轮下蹲/滑行；
- 坡面滚轮任务；
- 其它滚轮技能。

任务名和变体会随官方仓库变化，应以 upstream 当前 live registry 为准。

## 多种机器人模型

官方不是用一个 XML 处理所有任务。

2026-09-02 上游重新导出模型时修正了一个旧命名问题：原先经过筛选的 `allcollisions` 角色改名为 `groundcontact`，同时新增真正的 `robot_allcollisions.xml`。

| 模型 | 用途 |
|---|---|
| `robot_walk.xml` | walking-oriented，身体碰撞范围更简化 |
| `robot_groundcontact.xml` | 为倒地/接地任务保留经过挑选的 collision set |
| `robot_groundcontact_rollers.xml` | ground-contact 模型 + 被动 roller mechanics |
| `robot_allcollisions.xml` | 真正的全零件碰撞 variant，用于 collision inspection / experiment |
| `*_backlash.xml` | 插入被动齿隙关节的 sim-to-real 变体 |

这意味着“用于训练行走的模型”和“用于检查全身接触的模型”本来就可能不同。

当前文件结构和这次命名变化见[仿真模型资产参考](model-assets-reference.md)。

## BAM 执行器模型

官方项目明确把执行器 fidelity 视为 sim-to-real gap 的核心来源之一。训练并非使用理想 torque source 或普通 PD，而是使用 Rhoban 的 **BAM** 模型来描述 Dynamixel XL330。

公开资料涉及：

- 电压控制规律；
- 反电动势；
- Coulomb / Stribeck / load-dependent friction；
- 电池电压变化；
- 负载压降；
- command delay；
- friction randomization。

对于这种轻量机器人，小型舵机的真实性可能比单纯把外形模型做得更精细更影响迁移效果。

## 齿隙模型

官方 RL 仓库提供专门的 **Backlash** 任务变体：每个受控舵机串联一个无执行器的被动 hinge 来表示齿轮间隙。

重要的是编码器观测也“穿过”这个齿隙模型，使虚拟 encoder 更接近输出端反馈，而不是简单在关节角上加随机噪声。网络接口仍保持 61 observation / 14 action。

## Domain randomization

官方 sim-to-real recipe 会变化或随机化的因素包括：

- 电池电压与负载压降；
- 摩擦；
- 命令/观测时序；
- 质量、质心、惯量相关参数；
- 脚底/接触摩擦；
- 外部 push；
- 编码器偏差/误差；
- 执行器响应差异。

具体范围应读取当前 upstream env config，避免把一次版本中的数字永久复制成固定规格。

## 软件在环的 MuJoCo Body

官方公开的 `microduck_rl/develop` 现在已经包含 `duck-body`，可以通过 TCP 提供一个 MuJoCo 机体，并支持自定义 scene：

```bash
uv run duck-body --scene path/to/scene.xml
```

这意味着 MuJoCo body 不再只能作为“训练环境”使用；它也可以放到真实控制软件所使用的 hardware-I/O 边界下面。

对应的 daemon 侧实现目前位于官方公开分支：

```text
pollen-robotics/microduck: sim-remote-io
```

这个分支通过 `robotd --sim HOST:PORT` 使用 remote `RobotIo`。

截至 **2026-09-03**，daemon 侧这部分**还没有合并到 `microduck/main`**。因此正确标签应该是“官方公开上游实验路径”，而不是稳定发布功能。

如果想用小白方式理解“哪些硬件参数可以改、哪些 Microduck 软件接口应该保持不变”，看[硬件变体仿真](hardware-variant-simulation.md)。

## ONNX 导出

官方导出流程会把 observation normalization 烘焙到 ONNX graph 中：

```text
checkpoint + training normalizer
            ↓ 官方导出
       可部署 ONNX
            ↓
        robot runtime
```

因此“权重相同但输入归一化不同”的网络并不是同一个控制器。

## Sim-to-real 验证

官方仓库提供在 CPU MuJoCo 中回放 ONNX 等工具，也反复强调训练时 filter、runtime action processing 等必须和真实部署保持一致。某些看似很小的低通、scale 或反馈差异，都可能让仿真正常的策略在真机上明显退化。

最近的上游 ToF 修复还说明了一点：仿真 fidelity 不只是数值参数。模拟 ToF 的左右列方向约定曾经和真实处理路径相反，导致 mapping 左右镜像，修正 coordinate convention 后才恢复正常。

## 社区仿真生态

目前已经出现多个独立实现：

- 浏览器 MuJoCo/WASM + ONNX Runtime Web；
- Isaac Lab / Newton MJWarp；
- 面向 AMD/ROCm 的 Genesis port；
- MJX/JAX/Brax 重写；
- Swift 模型/策略实现。

这些项目很有研究价值，但不能默认都与官方 mjlab baseline bit-for-bit 等价。状态和差异见[社区逆向项目索引](../ecosystem/reverse-engineering-projects.md)。

## 主要来源

- https://github.com/pollen-robotics/microduck_rl
- https://github.com/pollen-robotics/microduck
- https://github.com/pollen-robotics/microduck/tree/sim-remote-io
- https://github.com/Rhoban/bam

## 相关文档

- [硬件变体仿真](hardware-variant-simulation.md)
- [仿真模型资产参考](model-assets-reference.md)
- [Sim-to-real 参数总表](sim-to-real-parameter-reference.md)
- [机械结构](../hardware/mechanical-structure.md)
- [电控与总线](../hardware/electronics-and-buses.md)
- [机载运行时](../software/runtime-architecture.md)
