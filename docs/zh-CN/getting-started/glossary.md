# 小白术语表：先用普通话看懂训练

[English](../../en/getting-started/glossary.md) | **简体中文**

> 不要求背单词。先知道每个词在整条流程里负责什么。

## 一张流程图

```text
训练时
机器人看到的数字（Observation）
        ↓
策略网络（Policy）给出动作（Action）
        ↓
仿真器计算结果
        ↓
奖励（Reward）告诉训练算法方向对不对
        ↓
反复练习，保存 Checkpoint，最后导出 ONNX

运行时
真实/虚拟机器人状态 → ONNX Policy → 14 个关节动作
```

## 核心词

| 术语 | 普通话解释 | 在 Microduck 里 | 容易误会的地方 |
|---|---|---|---|
| **Simulation / 仿真** | 用软件计算机器人和地面的运动 | MuJoCo 计算虚拟 Microduck | 动画好看不等于真机已经成功 |
| **Policy / 策略** | 根据当前状态决定下一步动作的函数 | 61 个输入变成 14 个动作 | 这里不是“公司政策”，也不等于整套机器人 AI |
| **Observation / 观测** | Policy 每一轮能看到的数字 | IMU、关节状态、上一轮动作和命令等 | 标准 Walking Policy 不直接读取相机图像 |
| **Action / 动作输出** | Policy 发出的下一步控制目标 | 14 个 Policy 关节目标 | Runtime 还有第 15 个嘴/喙电机 |
| **Reward / 奖励** | 训练时使用的评分规则 | 走对方向、保持直立可以得分 | 部署后的 ONNX 不会继续读取 Reward |
| **PPO** | 一种根据练习结果更新 Policy 的训练算法 | 官方训练栈采用的 RL 算法 | PPO 只负责怎么学，任务设计决定学什么 |
| **Checkpoint** | 训练中途保存的进度 | 包含当时的网络和训练状态 | 不能直接假设它等于可部署 ONNX |
| **ONNX** | 方便不同程序加载的模型文件格式 | Runtime 加载运动 Policy | 必须用正确 Exporter 保留输入归一化 |
| **Inference / 推理** | 运行已经训练好的模型 | 每 20 ms 运行一次 Policy | 推理不是重新训练，通常计算量小得多 |
| **Domain Randomization** | 训练时故意让虚拟机器人参数稍有变化 | 改变摩擦、电压、延迟等 | 不是随便乱改；范围和版本必须有记录 |
| **Sim-to-real** | 把仿真学到的行为迁移到真机 | ONNX 从 MuJoCo 进入 Runtime | 仿真成功只是开始，仍需真机验证 |
| **Daemon / 守护进程** | Linux 中长期在后台运行的小程序 | `robotd` 管运动，`updaterd` 管更新 | 它是软件角色，不是新的 AI 模型 |
| **BAM** | 更真实地模拟小型舵机非理想行为的执行器模型 | 模拟 XL330 的电压、反电动势和摩擦等 | BAM 参数不是自动等于厂家实测规格 |
| **Backlash / 齿隙** | 齿轮换方向时可能出现的空行程 | 官方提供带齿隙的 Task Variant | 不只是给角度加随机噪声 |

## 三个必须分清的句子

1. **“我跑起来了”**：加载了别人训练好的 ONNX。
2. **“我训练成功了”**：训练产物通过了仿真评估和导出验证。
3. **“我完成 sim-to-real 了”**：还必须有真实硬件测试条件和结果。

三句话不能互相代替。

## 接下来读什么

- [先选路线](choose-your-path.md)
- [第一步先做仿真](simulation-first.md)
- [行为、任务与奖励设计](../simulation/behavior-task-and-reward-design.md)
- [可复现训练与 ONNX 导出](../simulation/reproducible-training-and-export.md)
