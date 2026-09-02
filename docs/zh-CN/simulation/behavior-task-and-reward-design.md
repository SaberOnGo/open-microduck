# 行为、任务与奖励设计

[English](../../en/simulation/behavior-task-and-reward-design.md) | 简体中文

这篇文档解释：当要给机器人增加一个新动作时，**正式强化学习训练之前或训练迭代过程中**，前面的设计工作到底叫什么、具体要做什么。

## 这部分工作叫什么？

最合适的总称是 **Behavior / Task Design（行为 / 任务设计）**。

通常包含三部分：

- **Behavior / Task Design（行为 / 任务设计）** —— 定义机器人到底要做什么，以及怎样算成功。
- **Reward Design（奖励设计）** —— 把目标变成强化学习可以优化的分数和惩罚。
- **Curriculum Design（课程设计）** —— 对复杂动作，把任务拆成更容易学的阶段或起始状态。

PPO 只是“怎么学”的算法；这些设计决定的是 **让 PPO 学什么**。

## 一个最简单的例子：单脚站

人类需求：

> 抬起右脚，用左脚保持平衡，身体直立，不要疯狂晃动。

训练任务可以拆成：

```text
右脚离地              奖励
身体保持直立          奖励
左脚持续接触地面      奖励
支撑脚尽量踩平        奖励
身体乱晃或漂移        惩罚
关节猛烈甩动          惩罚
机器人摔倒            本回合结束 / 失败
```

具体权重不是固定答案，而是需要实验。即使代码完全正确，Reward 也可能设计错：如果评分规则漏掉了重要要求，Policy 很可能找到一种“分数很高、动作很难看”的钻空子方法。

公开项目 `microduck-lab` 的单脚站就是类似做法：同时使用单脚支撑、抬脚高度、支撑脚接触、姿态等正奖励，并对身体乱晃、漂移、动作突变、关节高速和电机负担进行惩罚。

## 如果要实现一个以前完全没有的动作

可以按下面的顺序做：

1. **先用普通话把动作说清楚。**
   例如：“先下蹲，再向前跳，双脚落地，然后恢复站立。”

2. **把‘成功’变成仿真里可以测量的东西。**
   例如：身体高度、脚是否接地、向前移动了多少、身体朝向、关节状态、落地后是否稳定。

3. **确认 Policy 能看到足够的信息。**
   Reward 不应该依赖 Policy 完全看不到、也无法推断的隐藏状态。`microduck-lab` 的训练手册明确提醒：不要奖励 Policy 无法观察到的东西。

4. **写第一版 Reward。**
   对真正重要的结果加分，对明显错误的行为扣分。通常把目标拆成几个容易理解的评分项，比写一个模糊的“动作好不好”总分更可靠。

5. **先跑短训练。**
   一开始不要直接跑最长训练。第一件事是看：目标动作有没有哪怕偶尔出现过。

6. **必须看实际动作，不要只看 Reward 曲线。**
   判断机器人到底学会了想要的动作，还是只是找到评分漏洞。

7. **根据错误动作修改任务设计，再训练。**
   如果它用错误方式拿到高分，就调整 Reward 或目标条件。如果它从来没有探索到关键动作，只改 Reward 权重往往也没用。

8. **复杂动作增加 Curriculum。**
   可以让机器人先从接近目标的位置开始，或者先训练更容易的阶段，再逐步恢复到完整任务。`microduck-lab` 对复杂动作使用了分阶段 Curriculum。

9. **验证导出的确定性 Policy。**
   导出模型后，在没有训练噪声的情况下重新评估，并直接看动作结果。

10. **最后才进入正式 sim-to-real 训练。**
    `microduck-lab` 自己把定位写得很清楚：它适合快速原型和 Reward / Curriculum 实验；最终要上真机的 Policy，仍应迁移到官方 `microduck_rl` 的完整 sim-to-real 和 Domain Randomization 流程重新训练。

## Codex 或其他 Coding Agent 可以做什么？

这部分很适合让 Coding Agent 主持大量重复工作：

```text
人用普通话描述新动作
        ↓
Agent 查看已有 Behavior 和 Observation
        ↓
起草 Reward / Curriculum 代码
        ↓
运行测试
        ↓
启动短训练
        ↓
渲染训练结果
        ↓
检查机器人哪里做错了
        ↓
修改任务设计，再训练
```

人仍然需要做最终判断，因为“Reward 很高”并不等于“这个动作就是想要的动作”。

## 新动作失败时，优先检查什么？

按这个顺序问：

1. **Policy 能看到完成动作所需的信息吗？**
2. **训练过程中，有没有任何一次 Rollout 做出过目标动作的一部分？**
3. **Reward 真正在奖励人想要的行为吗？**
4. **Policy 有没有找到钻评分规则的漏洞？**
5. **是不是需要 Curriculum，而不是单纯增加训练步数？**

这个检查顺序可以避免大量无效训练。

## 公开来源

- Jonathan Hawkins，`microduck-lab`：<https://github.com/jonathanhawkins/microduck-lab>
- `microduck-lab` Training Playbook：<https://github.com/jonathanhawkins/microduck-lab/blob/main/microduck_local/AGENTS.md>
- Pollen Robotics，`microduck_rl`：<https://github.com/pollen-robotics/microduck_rl>

来源等级：**公开上游仓库 + 公开第三方实现说明**。本文总结公开可验证的训练流程；`microduck-lab` 中的具体 Behavior Recipe 属于第三方实现，不应表述为 Pollen Robotics 官方训练配方。
