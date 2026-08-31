# 仿真模型资产参考

[English](../../en/simulation/model-assets-reference.md) | **简体中文**

> 主要来源：官方 `pollen-robotics/microduck_rl` 仓库。

官方 RL 项目并不是所有动作都使用同一个万能 XML。行走、倒地、翻滚、滑行对碰撞和接触的需求不同，所以官方仓库里有多套 MJCF variant。

这份文档专门解释这些公开模型分别用来做什么，避免把不同物理模型混在一起比较。

## 官方模型在哪里

当前上游路径：

```text
src/mjlab_microduck/robot/microduck/
```

这里包括 robot MJCF/XML、scene wrapper、mesh asset、export configuration，以及生成 backlash model 的辅助脚本。

## 主要 Robot Model Family

| Model | 主要用途 | 为什么不同 |
|---|---|---|
| `robot_walk.xml` | 主要 walking / velocity task | trunk/head 接触范围更简化，重点是 gait training，而不是全身躺地接触 |
| `robot_allcollisions.xml` | StandUp、SitStand、GroundPick、BallKick、Roulade、恢复类 task | 机器人会趴、躺、翻滚，因此需要更完整的身体 collision/contact |
| `robot_allcollisions_rollers.xml` | Roller / skating task | 加入被动 roller wheel 以及滑行所需的接触结构 |
| `robot_*_backlash.xml` | 主要模型的 Backlash variant | 在受控舵机关节串联 passive gear-play hinge |

## `robot_walk.xml` 更简单，不代表它一定“不准确”

仿真模型经常会针对任务做合理简化。

普通 walking training 的目标是让双腿稳定跟踪速度。如果把身体每一个外壳面都做成复杂 contact，可能增加计算量，却不一定让 gait 更好。

但恢复 / 翻滚任务不一样：机器人必须真的用头、身体接触地面，再把自己撑起来。这时 full-body collision 就非常重要。

所以不应该问：

> 哪一个 XML 才是唯一真正的 Microduck？

更合理的问题是：

> 当前训练 / 测试的行为，应该用哪一种模型？

## Scene 文件是什么

仓库里还有 `scene*.xml`。

这些文件通常会把 robot model 和环境组合起来，例如：

- floor；
- initial pose / keyframe；
- STAND / SIT / FOLD 等姿态；
- viewer 和 `infer_policy.py` 使用的快速场景。

因此 scene file 和“机器人本体模型”不是完全同一个概念。

## Mesh 资产有什么用

公开模型里包含很多机器人部件的 visual geometry，例如：

- body shell；
- leg / foot；
- head / neck；
- beak 相关结构；
- motor-like geometry；
- battery / board placeholder；
- roller attachment 等。

这些 mesh 很适合：

- 可视化；
- 运动学重建；
- 检查 rigid-body hierarchy 和 transform；
- collision / model 对比；
- 移植到其它 simulator；
- 社区装配研究。

但它们不能自动等同于最终 manufacturing CAD。

仿真 mesh 可能没有：

- 公差；
- 螺纹；
- insert；
- wiring channel；
- 最终螺丝长度；
- 材料标注；
- 其它制造细节。

## Mass、Inertia、Joint Axis、Limit

官方 MJCF 里公开了很多动力学相关参数，例如：

- rigid-body hierarchy；
- body transform；
- joint axis；
- joint limit；
- body mass；
- center-of-mass offset；
- inertia；
- collision geometry；
- site / reference point。

这些参数对仿真和分析非常有价值。

但来源标签应该是：**官方仿真模型参数**，不能自动写成“量产实机测量值”。

## Roller Model

Roller task 会在脚下加入被动 wheel joint。

官方命名中，这类不由电机直接驱动的关节通常使用 `passive_*`。

这个区别很重要，因为 Policy 仍然只应该输出 14 个 servo action，不能因为模型里多了被动轮子，就误把 passive joint 也当成神经网络 action。

## Backlash Model

Backlash variant 会在 14 个受控舵机关节里分别串联一个不驱动的 passive hinge，用来表示齿隙。

它的设计不是“干净关节角 + 随机噪声”，而是让虚拟 encoder 看到经过齿隙后的真实输出侧运动。

神经网络接口仍保持：

```text
61 observations
14 actions
```

因此可以在不重做 Runtime 接口的情况下，对比理想模型与考虑 backlash 的模型。

## Onshape Export 流程

上游 README 说明，这些 MJCF robot model 来自 Onshape，并通过 `onshape-to-robot` 导出；仓库中还有对应的 `config_mjcf_*.json`。

这条来源链很重要，因为它能帮助区分：

- 上游官方生成的 simulation geometry；
- 社区后来做的 transformed / combined mesh；
- 没有作为 open-source hardware 发布的量产 manufacturing drawing。

## Asset License

官方 RL README 当前说明：

- software：Apache-2.0；
- 3D model file：Creative Commons BY-SA-NC。

在重新分发模型或衍生资产前，应再次检查具体上游文件和许可证状态。

不能因为仓库代码是 Apache-2.0，就默认里面所有 3D asset 也自动是 Apache-2.0。

## 做 Simulation 对比前建议记录什么

至少记录：

```text
robot XML / scene XML
是否 Backlash
是否 Roller
上游 commit SHA
task id
collision/contact configuration
actuator configuration
```

否则两段看起来都是“Microduck simulation”的实验，背后可能其实使用了明显不同的物理模型。

## 主要官方来源

- https://github.com/pollen-robotics/microduck_rl
- https://github.com/pollen-robotics/microduck_rl/tree/develop/src/mjlab_microduck/robot/microduck
- https://github.com/pollen-robotics/microduck_rl/blob/develop/README.md

## 相关页面

- [机械结构与运动学](../hardware/mechanical-structure.md)
- [仿真与强化学习](model-and-rl.md)
- [可复现训练与 ONNX 导出](reproducible-training-and-export.md)
- [来源与许可证](../legal/provenance-and-licenses.md)
