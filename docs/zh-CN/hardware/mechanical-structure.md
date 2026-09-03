# 机械结构与运动学

> 本文严格区分**官方公开的仿真/运动学模型**与**社区根据公开资产推导出的装配结论**。
>
> 模型家族命名最近一次核对：**2026-09-03**。

## 整体尺寸

Pollen Robotics 的公开产品规格描述 Microduck 约 **25 cm 高、14 cm 宽、低于 800 g**。

官方强化学习仓库公开了由 Onshape 工作流导出的 MJCF 机器人模型。这些模型包含刚体变换、关节轴、关节行程、惯量参数、碰撞几何和视觉网格，因此能够重建公开仿真模型的运动学树。

但需要特别注意：**仿真网格不等于生产工程 CAD**。配合公差、螺纹、热熔嵌件、走线、材料规格、量产紧固件和装配工艺可能缺失、简化或与量产版不同。

## 策略控制的运动学树

14 个由策略直接控制的关节结构如下：

```text
躯干 / floating base
├── 左腿
│   ├── left_hip_yaw
│   ├── left_hip_roll
│   ├── left_hip_pitch
│   ├── left_knee
│   └── left_ankle
├── 颈部和头部
│   ├── neck_pitch
│   ├── head_pitch
│   ├── head_yaw
│   └── head_roll
└── 右腿
    ├── right_hip_yaw
    ├── right_hip_roll
    ├── right_hip_pitch
    ├── right_knee
    └── right_ankle
```

官方机载运行时还包含**第 15 个嘴/喙电机**。它有意从 14 维运动策略 action 输出中跳过，由运行时单独控制。

因此公开资料里同时出现“15 motors / 15 DOF”和“RL 输出 14 actions”并不矛盾：前者统计整机电机，后者只统计策略直接控制的运动关节。

## 公开模型中的关节行程

MJCF 文件包含明确的 hinge range。社区项目已经把这些值提取并整理成表格，但由于官方模型会随分支和版本变化，OpenMicroDuck 不把某一次拷贝出来的行程表视为永久不变的量产规格。

需要精确数值时，应直接查看当前官方模型：

`pollen-robotics/microduck_rl/src/mjlab_microduck/robot/microduck/`

当前主要模型包括：

- `robot_walk.xml`：walking-oriented，减少部分身体碰撞；
- `robot_groundcontact.xml`：为倒地/接地任务保留经过挑选的身体 collision；
- `robot_groundcontact_rollers.xml`：ground-contact + 被动滚轮 mechanics；
- `robot_allcollisions.xml`：较新的真正 all-part collision variant，用于 collision inspection / experiment；
- `*_backlash.xml`：加入被动回差关节，用于 sim-to-real 回差实验。

这里的 `groundcontact` 命名很重要：上游把旧的 curated `allcollisions` 角色改了名，因为它从来都不是“每个零件都带 collision”。当前文件地图见[仿真模型资产参考](../simulation/model-assets-reference.md)。

## 刚体质量与惯量

公开 MJCF 中包含每个刚体的：

- 质量；
- 质心位置；
- 惯量张量；
- 父子刚体变换。

因此它特别适合进行：

- 正/逆运动学研究；
- 整机质心估算；
- 动力学仿真；
- 碰撞与接触研究；
- 行走版与滚轮版结构比较；
- 第三方装配关系可视化。

但这些数字属于**仿真模型参数**，不能自动描述成量产实物的精密测量结果。

2026-09-02 上游模型重新导出提供了一个很有价值的公开证据：上游比较结果说明，重新导出的旧模型在 mass、inertia、frame 等动力学属性上保持 physics-identical，而可见变化主要是 material color。这说明这些参数和 CAD → MJCF 工作流是连在一起的，而不是单纯为了显示外观随便填写。

## 公开网格资产

社区项目已经把官方公开的仿真网格归类为：

- 躯干和外壳；
- 髋部与 yaw-to-roll 连杆；
- 左右大腿；
- 小腿；
- 踝、脚和脚底；
- 颈部与头部连杆；
- 下颚/喙结构；
- 摄像头与镜头几何；
- 舵机外形；
- 轴承几何；
- PCB / 电池占位几何；
- 轮滑支架、轮毂和轮胎。

不同项目统计出的 STL 数量可能不同，因为使用的上游 commit、模型变体和计数方法不同。因此“N 个 STL”不应写成永久产品规格。

## 社区装配重建

### `fanhao375/microduck-replica`

该项目利用官方 MJCF 变换与公开 STL 资产生成：

- 装配图和爆炸图；
- 已应用世界变换、可直接在 CAD/网格工具中打开的装配 STL；
- 刚体装配树；
- 基于模型的质量汇总；
- 孔特征扫描与紧固件推导；
- 轴承和结构特征说明。

仓库：https://github.com/fanhao375/microduck-replica

这些结果属于**第三方重建**，不是 Pollen Robotics 官方生产装配图。

### `boris721/microduck-3d`

该项目整理公开 Microduck 网格、运动学树、合并模型，以及行走/滚轮两种模型。

仓库：https://github.com/boris721/microduck-3d

## 紧固件反推

`microduck-replica` 对公开 STL 中的圆柱孔特征进行几何分析，结论是公开模型整体以 **M2 级紧固件体系**为主，并识别出与 M2 过孔、沉孔和攻丝底孔相符的孔径聚类，同时估算了采购数量。

这对理解公开模型很有价值，但它**不是官方螺丝 BOM**。仿真网格简化、打印/加工公差、嵌件、隐藏结构以及量产 revision 都可能改变真实装配。

## 轴承反推

公开网格中存在轴承形状资产。社区分析得到大致几何：

- 外径约 22 mm × 内径约 16 mm × 宽约 4 mm；
- 另一种较小轴承约外径 15 mm × 内径 10 mm × 宽 3 mm。

这只能说明模型几何。供应商、精度等级、密封形式、材料与量产数量不能仅靠仿真网格确定。

## 为什么这套公开模型对逆向研究价值很高

普通产品渲染图通常只能看到外形，而 Microduck RL 公开模型还提供：

1. 刚体层级；
2. 父子变换；
3. 关节轴和关节限制；
4. 碰撞几何；
5. 刚体质量与惯量；
6. 脚、摄像头、嘴等命名 site；
7. 滚轮和回差模型中的被动关节。

这些信息足以重建高质量的**仿真装配描述**，但不等于获得了未公开的生产制造包。

## 官方来源

- https://github.com/pollen-robotics/microduck_rl
- https://github.com/pollen-robotics/microduck_rl/tree/develop/src/mjlab_microduck/robot/microduck
- https://github.com/pollen-robotics/microduck_rl/pull/29
- https://pollen-robotics.com/microduck/press-kit/

## 社区来源

- https://github.com/fanhao375/microduck-replica
- https://github.com/boris721/microduck-3d

组件证据等级见[公开硬件清单](public-bom.md)，修改物理参数但保持软件接口不变的思路见[硬件变体仿真](../simulation/hardware-variant-simulation.md)。复制或再分发上游/衍生 3D 资产前，请阅读[来源与许可证](../legal/provenance-and-licenses.md)。
