# 仿真模型资产参考

[English](../../en/simulation/model-assets-reference.md) | **简体中文**

> 主要来源：官方 `pollen-robotics/microduck_rl` 仓库。
>
> 模型家族命名最近一次核对：`microduck_rl/develop` commit `29e887ecfbf5d37144759e5a9f8a176dfb83d547`，日期 **2026-09-03**。

官方 RL 项目并不是所有动作都使用同一个万能 XML。行走、倒地、翻滚、滑行和真正的全身接触，对 collision/contact 的要求不同，所以官方仓库里有多套 MJCF variant。

这份文档专门解释这些公开模型分别用来做什么，避免把不同物理模型混在一起比较。

## 官方模型在哪里

当前上游路径：

```text
src/mjlab_microduck/robot/microduck/
```

这里包括 robot MJCF/XML、scene wrapper、mesh asset、export configuration，以及生成 backlash model 的辅助脚本。

## 2026-09-02 一个很重要的命名变化

上游重新导出模型时，修正了一个容易让人误解的旧名字。

旧的 `allcollisions` 家族**并不是真正“每个零件都有碰撞”**。它其实只是为倒地/接地任务保留一组经过挑选的 collision geom。

因此上游把原来的角色改名为：

```text
旧的 curated `allcollisions`
             ↓ 改名
        `groundcontact`
```

同时新增真正的：

```text
robot_allcollisions.xml
```

让所有部件都可以带 collision geometry。

这不只是改文件名。它会直接影响读者怎样理解某一次仿真实验用了什么物理模型。

## 现在主要的 Robot Model Family

| Model | 主要用途 | 为什么不同 |
|---|---|---|
| `robot_walk.xml` | 主要 walking / velocity 工作 | walking-oriented，身体 collision 范围更简化 |
| `robot_groundcontact.xml` | 倒地/接地类 task | 为预期会接触地面的部件保留经过挑选的 collision；它就是旧 `allcollisions` 角色的新名字 |
| `robot_groundcontact_rollers.xml` | Roller / skating 工作 | ground-contact 结构 + 被动 roller wheel |
| `robot_allcollisions.xml` | 真正的全零件碰撞检查 / 实验 | 新增 true all-collisions variant，除明确排除的异常接触对外，每个部件都有 collision geom |
| `*_backlash.xml` | Backlash variant | 在受控舵机关节串联 passive gear-play hinge |

当前上游还包含对应的 scene wrapper，例如 `scene.xml`、`scene_walk.xml`、`scene_rollers.xml`、`scene_backlash.xml`、`scene_allcollisions.xml`，以及最近仿真工作使用的 apartment scene。

## `groundcontact` 和真正 `allcollisions` 差多少？

上游合并的模型重导出 PR 给出的规模大约是：

```text
groundcontact collision geoms：11
true allcollisions geoms：      70
true allcollisions meshes：     37
```

true all-collisions variant 还明确排除了一个 neck / jaw closed-loop 周围的虚假 self-contact pair，因为 CAD mesh 在所有姿态下都会有几毫米互相穿插。

证据等级：**官方公开上游仓库 / 已合并 PR**。

该 PR 同时说明：重新导出的 walking 和 curated ground-contact 模型，在 joint name/order/range、mass、inertia、frame 和原有 collision set 上与之前版本保持 physics-identical；主要可见变化是 CAD material color。

## `robot_walk.xml` 更简单，不代表它一定“不准确”

仿真模型经常会针对任务做合理简化。

普通 walking training 的目标是让双腿稳定跟踪速度。如果把身体每一个外壳面都做成复杂 contact，可能增加计算和接触复杂度，却不一定让 gait 更好。

但恢复 / 翻滚 / 全身接触实验不一样：机器人会真的用头、身体碰到地面。这时更完整的 collision geometry 就很重要。

所以不应该问：

> 哪一个 XML 才是唯一真正的 Microduck？

更合理的问题是：

> 当前训练 / 测试的行为或物理问题，应该用哪一种模型？

## Scene 文件是什么

仓库里还有 `scene*.xml`。

这些文件通常会把 robot model 和环境组合起来，例如：

- floor；
- initial pose / keyframe；
- STAND / SIT / FOLD 等姿态；
- viewer 和 inference 工具使用的快速场景；
- 新一些的工作里还会加入 apartment 等更完整环境。

因此 scene file 和“机器人本体模型”不是完全同一个概念。

新的 `duck-body` simulator 还支持用 `--scene` 指定自定义场景，所以这一区分对硬件变体仿真尤其重要。

## Mesh 资产有什么用

公开模型里包含很多机器人部件的 visual geometry，例如：

- body shell；
- leg / foot；
- head / neck；
- beak 相关结构；
- motor geometry；
- board / battery geometry；
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
- 完整材料标注；
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

2026-09-02 的模型重导出还是一个很有价值的公开证据：这些 mass / inertia / frame 等参数和上游 CAD → MJCF 工作流是连在一起的，并不只是为了“显示外观”随便填的数字。

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

上游仓库用 `config_mjcf_*.json` 保存 MJCF export recipe，并在模型生成链里使用 `onshape-to-robot`。

2026-09-02 的重导出明确说明，walk / ground-contact / roller 模型重新从更新后的 CAD 导出，并通过 compiled-model comparison 检查。

这条来源链有助于区分：

- 上游官方生成的 simulation geometry / dynamics；
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
walk / groundcontact / true allcollisions
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
- https://github.com/pollen-robotics/microduck_rl/pull/29

## 相关页面

- [硬件变体仿真](hardware-variant-simulation.md)
- [机械结构与运动学](../hardware/mechanical-structure.md)
- [仿真与强化学习](model-and-rl.md)
- [可复现训练与 ONNX 导出](reproducible-training-and-export.md)
- [来源与许可证](../legal/provenance-and-licenses.md)
