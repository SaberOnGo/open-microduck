# OpenMicroDuck 小白友好内容审查（2026-09-02）

> 目的：回答“还应该补什么”，不把建议写成已经实现的功能。本文只使用公开资料，并区分官方事实、当前仓库事实、建议和待验证项。

## 实施状态（2026-09-02）

本轮已经完成：官方在线 Sandbox 首页入口、按目标选路线、小白术语表、症状式排错、官方真机用户入口、HF Jobs 费用与取消提醒、中英文配对页面，以及资料错误 / 复现失败 / 新来源三类 Issue Form。

仍需项目所有者决定或后续实测：许可证与 GitHub Description、Topics / Pages / Discussions、Windows 与不同 GPU 的实测矩阵、原创结构图和各平台成功截图。

## 结论

OpenMicroDuck 已经有较完整的中英文技术资料，真正欠缺的不是更多参数，而是让第一次接触机器人、Linux 和强化学习的人顺利完成第一次体验的闭环。

最优先的顺序应是：**网页直接体验 → 看懂十个核心词 → 按自己的电脑选择路线 → 跑出一个可核对的结果 → 出错时按现象排查 → 最后才进入训练和真机。**

## 已经做得好的部分（当前仓库事实）

- 根 README 已提供“20 秒看懂”、按目的选入口和 15 / 14 / 61 / 50 Hz 四个核心数字。
- 完成本轮补充后，中文、英文各有 36 篇主题文档；仓库共检查 92 个 Markdown 文件，未发现失效的仓库内相对链接。
- 已明确区分官方产品规格、官方源码、官方仿真模型、社区重建、实测和待确认内容。
- 已有仿真优先、训练与导出、硬件 Bring-up、参数表、来源地图和版本基线。

这些基础应保留。后续重点是减少新手的选择成本，而不是继续把首页变长。

## P0：优先补充

### 1. 把官方在线 Sandbox 放到第一入口

**官方事实：** Pollen Robotics 产品页直接提供在线 Simulator；官方 Hugging Face Space 在浏览器中运行 MuJoCo WebAssembly 和 ONNX Runtime Web，加载真实训练好的 walking、sit、roll、kick 和 roller policies，不需要本地安装 Python 或 CUDA。

- [Pollen Robotics Microduck 产品页](https://pollen-robotics.com/microduck/)
- [官方 Microduck Sandbox](https://huggingface.co/spaces/pollen-robotics/microduck-simulator)

**建议：** README 第一屏增加“30 秒在线体验”按钮，并给出 3 步说明：打开网页、用 WASD/方向键控制、按 Space 重置。说明这是官方在线仿真，不是 OpenMicroDuck 自制工具，也不代表真机已经验证。

### 2. 修正固定版本与 Hugging Face Jobs 的冲突

**审查时的仓库事实：** 文档固定 `microduck_rl` 到 `d424a0c...`，同时告诉无本地 GPU 的读者可使用 `--hf-jobs`。该问题已在本轮修改中修正。

**官方事实：** 官方在后续 commit `5946fd9...` 修复了 `train --hf-jobs` 因同名 CLI entry point 冲突而不能正常拦截的问题。该 commit 的父提交包含 `d424a0c...`，因此当前固定版本早于修复。

- [官方修复 commit 5946fd9](https://github.com/pollen-robotics/microduck_rl/commit/5946fd9cdbc58956424420153e51975af3b30d77)
- [官方 microduck_rl README](https://github.com/pollen-robotics/microduck_rl/blob/develop/README.md)

**建议：** 二选一：更新经过复核的上游基线；或明确写出“若使用 HF Jobs，至少需要包含 5946fd9 修复的版本”。更新 SHA 后必须重新检查版本敏感的模型、任务、参数和中英文页面，不能只替换字符串。

### 3. 增加“一眼选路线”表

建议在首页只保留以下五条路线：

| 我想做什么 | 难度 | 需要什么 | 第一站 |
|---|---:|---|---|
| 只是想看看 Microduck 怎么动 | 0 | 浏览器 | 官方 Sandbox |
| 看懂机器人和强化学习 | 1 | 不需要编程 | 小白概念页 |
| 本地运行现成 Policy | 2 | 电脑、命令行 | CPU 仿真教程 |
| 训练自己的动作 | 3 | NVIDIA CUDA GPU，或付费云 GPU | 训练路线 |
| 使用官方真机 / 做研究样机 | 3–5 | 实体硬件、安全空间 | 分开的真机入口 |

不要把“使用官方成品”“复刻研究样机”“训练 Policy”混成同一条路。

### 4. 增加术语表，但每页仍需当场解释

最少解释：仿真、Policy、Observation、Action、Reward、PPO、Checkpoint、ONNX、Inference、Domain Randomization、Sim-to-real、Daemon。

每个词采用三行格式：

```text
它是什么：一句普通话。
在 Microduck 里做什么：一个具体例子。
容易误会什么：一句边界说明。
```

例如 Reward 只在训练时提供“得分方向”，部署后的 ONNX Policy 不会继续看 Reward。

### 5. 给教程补齐“开始前”和“成功长什么样”

每篇动手教程统一使用：

1. 适合谁；
2. 预计时间；
3. 系统 / GPU / 磁盘 / 账号 / 是否收费；
4. 可复制命令；
5. 预期输出或成功画面；
6. 验收清单；
7. 按现象排错；
8. 下一步；
9. 来源、commit 和核对日期。

当前教程已有命令和验收清单，但 OS 支持边界、安装 `uv`、W&B/HF 登录、预期终端输出和具体错误处理仍不够完整。

### 6. 云训练必须先显示费用与账号影响

**官方事实：** 官方 RL 仓库支持把训练提交到 Hugging Face Jobs；Hugging Face 官方说明 Jobs 需要正的 credit balance，并按所选硬件的运行时间计费。

- [官方 HF Jobs 训练说明](https://github.com/pollen-robotics/microduck_rl/blob/develop/scripts/hf/README.md)
- [Hugging Face Jobs 定价与计费](https://huggingface.co/docs/hub/jobs-pricing)

**建议：** 在任何 `--hf-jobs` 命令之前放醒目的“会创建云端资源并可能收费”提示，先教 `--dry-run`，再说明 namespace、token、W&B、timeout、取消任务和产物位置。价格会变化，只链接实时定价页，不把价格写死。

## P1：第二批补充

### 7. 单独增加“我有官方真机”入口

官方 runtime 已经提供 `robotctl`、手柄配对、`duckctl`、更新与回滚等用户操作资料。OpenMicroDuck 目前主要解释架构和研究样机 Bring-up，缺少普通购买用户的短入口。

- [官方 Microduck runtime](https://github.com/pollen-robotics/microduck)
- [官方用户 Cheat Sheet](https://github.com/pollen-robotics/microduck/blob/main/docs/robot/cheatsheet.md)

**建议：** 不复制整份官方命令手册，只做中文导航：第一次开机、手柄、查看健康状态、更新、查看日志、何时回到官方文档。安全卡需说明 `relax` 会断开舵机保持力，机器人会倒下；浏览器里的 `stop` 不是切断舵机电源的急停。

### 8. 把排错从“知识分类”改成“症状分类”

建议新增 FAQ / Troubleshooting：

- `uv` 找不到；
- `uv sync` 下载超时；
- 没检测到 CUDA GPU；
- Viewer 没窗口或黑屏；
- W&B run path / 登录失败；
- ONNX 输入不是 `[1, 61]` 或输出不是 `[1, 14]`；
- 仿真会动但动作明显异常；
- HF Job 已提交但不知道如何看日志或停止计费。

每项固定为“你看到什么 → 最可能是哪一层 → 先运行哪个只读检查 → 如何恢复”。具体报错文本和平台命令必须实际验证后再发布。

### 9. 增加原创视觉，而不是继续堆长表格

本轮仓库扫描没有发现本地图片资产。建议优先制作：

- 一张“网页体验—本地仿真—训练—导出—真机”的路线图；
- 一张 15 个物理电机与 14 个 Policy 动作的标注图；
- 一张 Observation → Policy → Action 的儿童也能理解的动态图或分镜；
- 每个 Quickstart 一张“成功画面”。

优先自行绘制；引用或修改官方/社区图片前重新核对许可和 attribution。

### 10. 区分同名社区项目

GitHub 上存在不止一个 `microduck-lab`。社区索引应显示“作者 / 运行平台 / 用途 / 是否官方 / 能否直接用于真机 / 最后核对日期”，不能只显示项目名。社区工具可以降低门槛，但应明确它们不等于官方完整 sim-to-real 流程。

## P2：仓库治理和长期维护

### 11. 处理“open-source”描述与无许可证状态

**当前仓库事实：** 根目录没有 `LICENSE`，贡献指南也明确尚未选择统一许可证；GitHub 仓库 Description 却使用了 “open-source”。这仍需项目所有者决定，本轮未代替所有者选择许可证或修改远端仓库信息。

**GitHub 官方说明：** 没有许可证时默认版权法适用，其他人通常没有复制、分发或制作衍生作品的许可；公开可见不等于开源许可。

- [GitHub：Licensing a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)

**建议：** 项目所有者决定原创文档和原创代码的许可（可以分开），并明确排除第三方资产；在决定之前，把 GitHub Description 改为 “independent public research and documentation project”，不要自称 open-source project。此项需要项目所有者作许可证选择，不能由文档作者代替决定。

### 12. 改善 GitHub 发现和反馈入口

审查时的 GitHub API 检查显示 homepage 和 topics 为空，未启用 Pages / Discussions，仓库内也没有 `.github/ISSUE_TEMPLATE`。本轮已经补上三类 Issue Form；其余远端设置仍需项目所有者处理。

建议：

- 增加 topics：`microduck`、`robotics`、`reinforcement-learning`、`mujoco`、`sim-to-real`、`documentation`、`reverse-engineering`；
- 后续把 Markdown 发布成带侧栏、全文搜索、上一页/下一页和中英文切换的文档站；
- 增加“资料错误”“复现失败”“新来源/社区项目”三类 Issue Form，强制填写 OS、GPU、commit、命令、错误和来源；
- CI 检查仓库内链接、Markdown 基本格式和中英文主题文件是否成对存在；
- 定期比较上游 SHA，但由人工决定参数结论是否变化。

## 推荐实施顺序

第一批只做四件事：在线 Sandbox 入口、版本冲突修正、五路线首页、术语表。第二批再做系统矩阵、成功截图和症状式 FAQ。GitHub Pages、Issue Forms 和许可证决策可以独立推进。

这样首页会更短，第一次成功会更快，深入文档仍保留现有技术精度。

## 事实边界

- 官方产品页和 Press Kit 说明开放的是软件栈，不应把 Microduck 写成开源硬件：[官方 Press Kit](https://pollen-robotics.com/microduck/press-kit/)。
- 在线 Sandbox 能证明官方策略在其浏览器仿真环境运行，不证明任何第三方实体复刻已经完成真机验证。
- “Windows 原生是否完整支持官方训练栈”、具体最低 GPU/显存和各类错误修复命令，本轮没有完成逐平台实测，应保持为待验证，不能凭 `uv` 本身支持 Windows就推断整个 RL 栈支持 Windows。
