# 上游版本基线

[English](../../en/upstream/version-matrix.md) | **简体中文**

> 目的：让 OpenMicroDuck 的研究结论对应到明确的公开上游版本，而不是只写一个会不断变化的 `main` / `develop`。

Microduck 目前还处在非常活跃的开发阶段。今天正确的源码细节，之后可能因为官方提交新的 commit 而变化，例如 task 名称、模型文件、设备路径、Runtime 默认参数等。

因此，这里单独保存 OpenMicroDuck 当前资料检索所对应的版本基线。

## 2026-08-31 资料快照

| 上游来源 | Branch / 页面 | 本次核对版本 | 在 OpenMicroDuck 中主要用于 |
|---|---|---|---|
| `pollen-robotics/microduck` | `main` | `590b986bd8c0d50ae02cb3ea2f59c463b6828168` | 机载 Runtime、daemon、motor/IMU 控制、部署配置、硬件 bring-up |
| `pollen-robotics/microduck_rl` | `develop` | `d424a0c899f6b33cbd3daeb279913134349c0b63` | MuJoCo/mjlab 训练、task registry、机器人模型、BAM、backlash、ONNX export |
| `Rhoban/bam` | `main` | `620a64fe67c1afe94fca81da73b128c7aed17c5f` | 官方 RL 栈使用的 actuator model |
| Pollen Robotics Microduck Press Kit | 实时网页 | 2026-08-31 核对 | 官方产品规格，以及哪些参数仍属于 provisional |
| Pollen Robotics Microduck 产品页 / 商店 | 实时网页 | 2026-08-31 核对 | 当前产品定位、包装内容、销售页规格和可用性 |

## 为什么要记录 Commit SHA？

因为 branch name 只是一个会移动的指针。

例如：

```text
2026-08-31
microduck_rl/develop → commit A

以后
microduck_rl/develop → commit B
```

如果 A 和 B 之间修改了 task、domain randomization、MJCF 或 observation 规则，那么只写“参考 develop”就很难复现当时的结论。

记录 commit SHA 后，第三方就可以回到当时完全相同的公开源码状态。

## 哪些信息最应该绑定版本？

特别容易随版本变化的内容包括：

- task registry / task ID；
- reward function；
- domain-randomization 范围；
- robot MJCF；
- mass、inertia、collision geometry、joint limit；
- actuator configuration；
- observation / action contract；
- export / normalization 行为；
- Runtime 默认 gain、filter；
- serial device path 和开发板 bring-up；
- 官方明确标为 provisional 的产品规格。

像“Microduck 有 15 个 motors”这种产品级事实没那么容易改变，但同样应该保留官方来源。

## 实时网页和 Git Commit 不一样

产品页、Press Kit 一般没有 commit SHA。

对于这种来源，应该记录**核对日期**。如果某个参数非常关键，可以在公开研究记录中保留简要来源说明，但不要大段复制受版权保护的网页内容。

如果以后官方网页变了，应更新当前结论，并在确实有研究价值时保留历史冲突说明。

## 新研究建议怎样记录来源

对版本敏感的源码信息，建议使用这种格式：

```text
Source: pollen-robotics/microduck_rl
Branch: develop
Commit: d424a0c899f6b33cbd3daeb279913134349c0b63
Path: src/mjlab_microduck/...
Checked: 2026-08-31
```

对实时产品页：

```text
Source: Pollen Robotics Microduck Press Kit
URL: https://pollen-robotics.com/microduck/press-kit/
Checked: 2026-08-31
Evidence level: Official product spec
```

## 以后怎么更新这份表

每次重新检索官方项目时：

1. 更新最新 revision 和检查日期；
2. 检查所有版本敏感的 OpenMicroDuck 文档是否需要同步修改；
3. 如果发现来源冲突，不要静默把旧结论改成新的“事实”；
4. English 和简体中文同步更新。

## 主要来源

- https://github.com/pollen-robotics/microduck
- https://github.com/pollen-robotics/microduck_rl
- https://github.com/Rhoban/bam
- https://pollen-robotics.com/microduck/press-kit/
- https://pollen-robotics.com/microduck/

## 相关页面

- [资料来源与证据地图](../sources.md)
- [待确认问题与来源冲突](../research/open-questions-and-conflicts.md)
- [可复现训练与 ONNX 导出](../simulation/reproducible-training-and-export.md)
