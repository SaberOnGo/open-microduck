# 上游版本基线

[English](../../en/upstream/version-matrix.md) | **简体中文**

> 目的：让 OpenMicroDuck 的研究结论对应到明确的公开上游版本，而不是只写一个会不断变化的 `main` / `develop`。

Microduck 目前仍处在非常活跃的开发阶段。今天正确的源码细节，之后可能因为新的 commit 改变，例如 task、模型文件、collision family、Runtime 默认参数或实验分支。

因此，这里单独保存 OpenMicroDuck 当前资料检索所对应的版本基线。

## 2026-09-03 核心官方来源快照

| 上游来源 | Branch / 页面 | 本次核对版本 | 在 OpenMicroDuck 中主要用于 |
|---|---|---|---|
| `pollen-robotics/microduck` | `main` | `2c61dcc1f03440541cdc0729f7a375b2a9ea3005` | 机载 Runtime、daemon、motor/IMU 控制、部署配置、硬件 bring-up |
| `pollen-robotics/microduck` | `sim-remote-io` | `0cd676d6fbb6e90a762c84aa63abe7a02dbc9495` | **官方公开实验分支**：`robotd --sim`、`RemoteIo`、software-in-the-loop；不是 `main` |
| `pollen-robotics/microduck_rl` | `develop` | `29e887ecfbf5d37144759e5a9f8a176dfb83d547` | MuJoCo/mjlab、robot model、BAM、`duck-body`、ToF simulation、backlash、ONNX export/publish |
| `Rhoban/bam` | `main` | `620a64fe67c1afe94fca81da73b128c7aed17c5f` | 官方 RL 栈使用的 actuator model |
| Pollen Robotics Microduck Press Kit | 实时网页 | 2026-09-03 核对 | 官方产品规格，以及哪些参数仍属于 provisional |
| Pollen Robotics Microduck 产品 / Store 页面 | 实时网页 | 2026-09-03 核对 | 当前公开产品定位和可用性信息 |

## 相比 OpenMicroDuck 的 2026-09-02 快照，发生了什么？

### `microduck/main`：`9f7eaad... → 2c61dcc...`

新的 main revision 主要改进 daemon crash-loop 时的 health reporting。

它**没有**把 `robotd --sim` 合并进主线。

这点很重要：当前 `main` 仍然没有 `sim-remote-io` 分支里的 `--sim` 参数。

### `microduck_rl/develop`：`5946fd9... → 29e887e...`

这次变化对仿真研究很重要，不是普通文档更新。

主要包括：

1. **模型重新导出与 collision family 命名修正**
   - 原来经过挑选的 `allcollisions` 角色改名为 `groundcontact`；
   - 新增真正的 `robot_allcollisions.xml`；
   - 上游 PR 说明重新导出的旧模型在 joint name/order/range、mass、inertia、frame 和原有 collision set 上保持 physics-identical，主要可见变化是 CAD material color。

2. **`duck-body` MuJoCo body server**
   - `src/mjlab_microduck/sim/body_server.py` 可以通过 TCP 提供一个模拟 Microduck body；
   - 支持 `--scene` 指定另一份 MuJoCo scene；
   - 按 Microduck joint name 映射 actuator，而不是依赖对象序号。

3. **ToF coordinate convention 修复**
   - 模拟 ToF 的左右列方向曾和真实处理路径相反；
   - 在 body-server 分支合并前已经修复。

4. **CPU inference 路径加入 BAM**
   - CPU MuJoCo inference 路径更新为使用 BAM `m6` actuator behavior。

5. **Policy publish 支持**
   - 上游加入了发布已导出 ONNX 和 manifest 的工具链。

因此，凡是涉及当前仿真行为的文档，都应该优先参考 2026-09-03 这组 baseline，而不是继续把 2026-09-02 当作最新状态。

## 实验分支状态：`sim-remote-io`

官方公开的 `pollen-robotics/microduck` 当前存在：

```text
sim-remote-io
```

在本次固定的 branch revision 中，它包含：

```text
robotd --sim HOST:PORT
```

并把模拟器边界放在 `duck_control::io::RobotIo`。

上游公开设计文档说明，真实 50 Hz 控制循环、ONNX Policy、Safety、跌倒检测、里程计、运动学、IPC、`robotctl` 等仍然位于这个边界以上；模拟 body 替换的是下面的 hardware-I/O 部分。

因为它**没有合并进 `main`**，OpenMicroDuck 对它应统一标为：

> 官方公开上游实验分支

而不是稳定或正式发布功能。

## 为什么要记录 Commit SHA？

因为 branch name 只是一个会移动的指针。

例如：

```text
2026-09-03
microduck_rl/develop → commit A

以后
microduck_rl/develop → commit B
```

如果 A 和 B 之间修改了 task、domain randomization、MJCF、collision family、simulator interface 或 observation 规则，那么只写“参考 develop”就很难复现当时结论。

记录 commit SHA 后，第三方就可以回到当时完全相同的公开源码状态。

## 哪些信息最应该绑定版本？

特别容易随版本变化的内容包括：

- task registry / task ID；
- reward function；
- domain-randomization 范围；
- robot MJCF；
- 模型家族含义（`walk`、`groundcontact`、`allcollisions`、roller、backlash）；
- mass、inertia、collision geometry、joint limit；
- actuator configuration；
- observation / action contract；
- export / normalization 行为；
- Runtime 默认 gain、filter；
- simulator / runtime protocol boundary；
- serial device path 和开发板 bring-up；
- 官方明确标为 provisional 的产品规格。

像“Microduck 有 15 个 motors”这种产品级事实没那么容易改变，但同样应该保留官方来源。

## 实时网页和 Git Commit 不一样

产品页、Press Kit 一般没有 commit SHA。

对于这种来源，应该记录**核对日期**。如果某个参数特别关键，可以保存简短来源说明，但不要大段复制受版权保护的网页内容。

如果以后官方网页变了，应更新当前结论，并在确实有研究价值时保留历史冲突说明。

## 新研究建议怎样记录来源

对版本敏感的 main/develop 源码：

```text
Source: pollen-robotics/microduck_rl
Branch: develop
Commit: 29e887ecfbf5d37144759e5a9f8a176dfb83d547
Path: src/mjlab_microduck/...
Checked: 2026-09-03
```

对实验分支：

```text
Source: pollen-robotics/microduck
Branch: sim-remote-io
Commit: 0cd676d6fbb6e90a762c84aa63abe7a02dbc9495
Status: official public upstream experimental branch; not main
Checked: 2026-09-03
```

对实时产品页：

```text
Source: Pollen Robotics Microduck Press Kit
URL: https://pollen-robotics.com/microduck/press-kit/
Checked: 2026-09-03
Evidence level: Official product spec
```

## 以后怎么更新这份表

每次重新检索官方项目时：

1. 更新最新 revision 和检查日期；
2. 检查所有版本敏感的 OpenMicroDuck 文档是否需要同步修改；
3. 单独跟踪实验分支，不要静默把实验分支当成 mainline；
4. 如果发现来源冲突，不要静默把旧结论改成新的“事实”；
5. English 和简体中文同步更新。

## 主要来源

- https://github.com/pollen-robotics/microduck
- https://github.com/pollen-robotics/microduck/tree/sim-remote-io
- https://github.com/pollen-robotics/microduck_rl
- https://github.com/Rhoban/bam
- https://pollen-robotics.com/microduck/press-kit/
- https://pollen-robotics.com/microduck/

## 相关页面

- [硬件变体仿真](../simulation/hardware-variant-simulation.md)
- [仿真模型资产参考](../simulation/model-assets-reference.md)
- [资料来源与证据地图](../sources.md)
- [待确认问题与来源冲突](../research/open-questions-and-conflicts.md)
- [可复现训练与 ONNX 导出](../simulation/reproducible-training-and-export.md)
