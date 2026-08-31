# 逆向分析与社区项目索引

> 最近检查：2026-08-31。收录只表示“与 Microduck 公开研究相关”，不代表 OpenMicroDuck 对项目作出背书。复用任何内容前请重新检查当前代码、来源和许可证。

Microduck 刚公开不久，社区已经出现机械重建、网格/CAD 处理、浏览器仿真、训练框架移植、其它语言运行时和交互控制等项目。

## 机械 / 硬件重建

### `fanhao375/microduck-replica`

仓库：https://github.com/fanhao375/microduck-replica

**方向：** 根据 Pollen Robotics 公开 MJCF、STL 和源码做第三方重建。

项目公开内容包括：

- 根据 MJCF transform 生成装配图、爆炸图；
- 把世界变换应用到 STL，形成可直接在 CAD/网格工具中检查的装配体；
- 刚体树、模型尺寸与模型质量汇总；
- 关节范围提取；
- 扫描公开网格孔特征，推导以 M2 为主的紧固件体系；
- 从公开网格推导轴承几何；
- 根据官方源码整理电控、接口和总线；
- 提供从 upstream 重新生成分析结果的脚本。

**证据等级：社区重建。** 其中很多接口/芯片结论可以回到官方源码交叉确认；紧固件数量、装配制造细节等仍属于第三方推导。

**许可证注意：** 该仓库声明 scripts 为 Apache-2.0；由上游 3D 资产产生的 CAD/装配输出为 CC BY-SA-NC 4.0。复用前应检查它的 `LICENSE` / `NOTICE` 和上游资产许可。

这是本轮检索中目前与 Microduck 机械/硬件逆向最直接相关的公开仓库。

### `boris721/microduck-3d`

仓库：https://github.com/boris721/microduck-3d

**方向：** 整理、转换公开 Microduck 3D/仿真资产，包括行走/滚轮 MJCF、运动学树、按部位分类的 STL，以及合并模型脚本。

**证据等级：** 对公开模型资产的社区整理/解释。文件数量和命名与使用的 upstream snapshot 有关。

## 浏览器仿真

### `IronSpiderMan/MicroDuckModels`

仓库：https://github.com/IronSpiderMan/MicroDuckModels

使用 Three.js / React Three Fiber、MuJoCo WebAssembly 和 ONNX Runtime Web，在浏览器中运行 Microduck 模型和策略。README 记录了行走、坐站、起身、翻滚、踢球、ground-pick 和滚轮等能力，并以 50 Hz 跑策略。

## 训练框架移植

### `kabilankb/isaaclab-microduck`

仓库：https://github.com/kabilankb/isaaclab-microduck

Isaac Lab 3.0 / Newton MJWarp port，保持当前 61-D observation / 14-action contract，并以官方 mjlab 为 baseline。

**状态注意：** 当前 README 明确说部分任务已有实验结果，但 locomotion 尚不能视为可部署的官方等价实现，一些 actuator/delay/bias 对齐仍未完成。

### `Macmachi/microduck-rl-genesis`

仓库：https://github.com/Macmachi/microduck-rl-genesis

把官方 Microduck walking/sim-to-real recipe 移植到 Genesis，重点支持 AMD/ROCm。项目文档声明保持 61-D contract，重写/移植 BAM、randomization、ONNX export 和 backlash，并提供与 MuJoCo/BAM 的数值对比测试。

**证据等级：** 独立 port。任何“等价”结论都应结合当前 upstream commit 和该项目测试重新验证。

### `APX103/mjx_microduck`

仓库：https://github.com/APX103/mjx_microduck

基于 MJX/JAX/Brax 的从零重写，包含 velocity、stand-up、ground-pick、imitation 等任务。

**兼容性注意：** 当前 README 对多个任务写的是 **51-D observation**，而官方当前 alpha runtime 是 **61-D**。因此它属于独立/兼容旧接口的研究实现，不能默认直接生成当前官方 runtime 可部署策略。

### `nickoenig37/mjlab_microduck_waddle`

仓库：https://github.com/nickoenig37/mjlab_microduck_waddle

GitHub 检索到的 mjlab/Microduck walking 相关项目。其技术结果在写入 OpenMicroDuck 正式结论前应进一步检查实际代码和配置。

## Runtime / 语言移植

### `craigm26/duckkit`

仓库：https://github.com/craigm26/duckkit

以纯 Swift 实现 Microduck 模型、策略、协议和运动学等。README 描述 61-float observation、policy inference、gait/action processing、JSON-RPC、ToF/state 和测试体系。项目声明 Apache-2.0，并明确与 Pollen Robotics 无隶属关系。

## 交互 / 控制实验

### `kgediya/specs-microduck`

仓库：https://github.com/kgediya/specs-microduck

利用 Snap Spectacles 的手部跟踪，通过 WebSocket relay 控制 Microduck 模拟器。它不是硬件逆向资料，但体现了社区控制/interface 生态的发展。

## 社区项目依赖的主要官方上游

- https://github.com/pollen-robotics/microduck —— 机载 runtime 与系统软件；
- https://github.com/pollen-robotics/microduck_rl —— 官方 RL / 仿真；
- https://github.com/pollen-robotics/microduck-gst-plugins —— 媒体插件构建；
- https://github.com/Rhoban/bam —— 官方 RL 使用的执行器模型。

## 其它检索到但尚未作为正式技术来源的仓库

GitHub 还返回了 `microduck-simulator`、`microduck-courier`、`microduck-parkour`、`awesome-microduck` 等仓库和其它 fork/实验项目。OpenMicroDuck 不会因为搜索命中就直接把它们写成事实来源；正式收录技术结论前应先检查 provenance、实际实现、当前状态和 license。

## 社区来源的使用规则

社区项目适合用来发现：

- 可以从 upstream 公开资产复现的转换方法；
- 替代 simulator/toolchain；
- 值得回到官方资料验证的硬件解释；
- 有价值的脚本与可视化方法；
- upstream 中可能未充分说明的假设或矛盾。

但第三方结论不会自动覆盖官方规格。冲突时，本项目记录冲突，并以更权威来源描述 Microduck 本身。

详见 [资料来源与证据地图](../sources.md) 与 [来源和许可证](../legal/provenance-and-licenses.md)。
