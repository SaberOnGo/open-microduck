# 已发现的 Microduck 社区仓库

> GitHub 检索快照：2026-08-31。本文是**发现索引**，不是质量排名，也不代表技术背书。

Microduck 刚发布不久，GitHub 生态变化很快。本文保存本轮宽范围 `microduck` repository 检索中有实际相关性的仓库名称，并严格区分“找到”与“已经技术审查”。

已经检查并形成技术摘要的项目见：[逆向分析与社区项目索引](reverse-engineering-projects.md)。

## Pollen Robotics 官方仓库

- `pollen-robotics/microduck` —— 机载 runtime / 系统软件
- `pollen-robotics/microduck_rl` —— 官方仿真与强化学习
- `pollen-robotics/microduck-gst-plugins` —— 媒体/GStreamer 相关

## 机械 / 重建 / 3D 模型

- `fanhao375/microduck-replica` —— **已检查**；装配、BOM、紧固件与硬件重建
- `boris721/microduck-3d` —— **已检查**；公开 3D 模型整理/变换
- `poboll/microduck-replica` —— 看起来与上述重建项目存在 fork/跟踪关系，不能在未查 provenance 前当成独立成果
- `XWT985/microduck_robot` —— 已发现，待审查

## 仿真与 RL

- `IronSpiderMan/MicroDuckModels` —— 已检查；浏览器 simulator
- `nickoenig37/mjlab_microduck_waddle` —— 已发现；mjlab walking
- `kabilankb/isaaclab-microduck` —— 已检查；Isaac Lab/Newton port
- `Macmachi/microduck-rl-genesis` —— 已检查；Genesis/ROCm port
- `APX103/mjx_microduck` —— 已检查；MJX/JAX/Brax 实现
- `jvpflum/microduck-simulator` —— 已发现
- `Arvmor/microduck-simulator` —— 已发现
- `lgtkgtv/microduck_sim` —— 已发现
- `littlejohntj/microduck-sim` —— 已发现
- `SAMBAS123/microduck-sandbox` —— 已发现
- `jvpflum/microduck-lab` —— 已发现
- `AlexandreEDMOND/microduck-rl-lab` —— 已发现
- `Xuexue-Jiang/microduck-rl` —— 已发现
- `x10zyn/microduck-sim-playground` —— 已发现
- `Liyucheng1997/318_lab-microduck-simulator` —— 已发现
- `AmanPriyanshu/toodoom-the-mlx-metal-microduck` —— 已发现；MLX/Metal 相关实验

## Policy / Skill / 行为实验

- `Lulzx/microduck-backflip` —— 已发现；backflip
- `bihaokun/microduck-step-up-policy` —— 已发现；step-up policy
- `bentedesco/microduck-parkour` —— 已发现；parkour
- `selinayfilizp/microduck-courier` —— 已发现；应用实验
- `pezzonovante7/microduck-sidekick-dance` —— 已发现；舞蹈/行为实验
- `DollhouseRobotics/microduck-miniverse` —— 已发现；环境/应用实验

## Runtime / 控制 / 协议 / 语言实现

- `TommyZihao/microduck_runtime` —— README 级已检查；记录的是较早/原型风格的 Raspberry Pi Zero 2W + BNO055 runtime 路径，**不能与当前官方 RK3566 runtime 混为一谈**
- `craigm26/duckkit` —— 已检查；Swift model/policy/protocol
- `rokbenko/quackd` —— 已发现
- `agentculture/microduck-cli` —— 已发现；CLI
- `joeynyc/microduck-mcp` —— 已发现；MCP
- `aj-dev-smith/microduck-mcp` —— 已发现；MCP
- `apirrone/microduck_kinematics_rs` —— 已发现；Rust kinematics
- `apirrone/microduck_maploc_rs` —— 已发现；map/localization

## App / 媒体 / 感知 / 交互

- `apirrone/microduck_app` —— 已发现
- `apirrone/microduck_pet_detect` —— 已发现；触摸/音频分类相关
- `apirrone/microduck_sounds` —— 已发现；声音/voice
- `kgediya/specs-microduck` —— 已检查；Spectacles / AR 手势遥控
- `ThousandsOfTies/GarTalkableDuck` —— 已发现；交互应用

## Registry / Curated list

- `joeynyc/awesome-microduck` —— 已发现；资源索引
- `ob1-s/awesome-microduck` —— 已发现；资源索引
- `ob1-s/uduck-registry` —— 已发现；registry

## 普通 fork 与低信息搜索结果

宽范围 GitHub 搜索还会返回大量直接叫 `microduck` 的仓库，其中相当一部分从仓库大小/历史看属于官方仓库的 fork 或 mirror；也会混入更早的同名无关项目。本文不逐个列出，以免制造噪声和错误 attribution。

## 状态含义

- **已检查**：本轮至少阅读了与索引相关的 README/源码；
- **已发现**：搜索找到，但尚未做技术审计；
- **官方**：Pollen Robotics 所有；
- **fork/mirror**：除非存在实质差异，不应作为独立技术来源归功。

一个“已发现”项目只有在确认实际实现、upstream revision、可复现结果、license 和 provenance 后，才应该升级为 OpenMicroDuck 的正式技术来源。
