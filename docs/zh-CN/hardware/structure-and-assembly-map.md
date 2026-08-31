# Microduck 结构与装配地图

[English](../../en/hardware/structure-and-assembly-map.md) | **简体中文**

> 目标：把官方 Simulation Model 和公开社区重建资料，整理成普通读者也能看懂的结构地图。**这不是官方 Manufacturing Drawing，也不是量产装配手册。**

## 1. 不要先看几十个 STL 文件，先把 Robot 看成 5 个模块

```text
Microduck
├── Trunk / Body Core
│   ├── Compute / HAT 空间
│   ├── Battery 空间
│   ├── 左 Hip-yaw Motor
│   └── 右 Hip-yaw Motor
├── 左腿
│   └── 5 个受控关节
├── 右腿
│   └── 5 个受控关节
├── Neck + Head
│   └── 4 个 Policy 关节 + 1 个独立 Mouth Motor
└── Feet / Optional Rollers
```

这样理解，比一上来面对几十个没有上下文的 Mesh 名称清楚得多。

## 2. 官方 14-Joint Kinematic Tree

当前 Full-collision MJCF 里的 Policy 控制树：

```text
trunk_base
│
├── left_hip_yaw
│   └── left_hip_roll
│       └── left_hip_pitch
│           └── left_knee
│               └── left_ankle
│
├── neck_pitch
│   └── head_pitch
│       └── head_yaw
│           └── head_roll
│
└── right_hip_yaw
    └── right_hip_roll
        └── right_hip_pitch
            └── right_knee
                └── right_ankle
```

真实 Runtime 还有第 **15 个 Mouth / Beak Motor**，但它不进入 14-Action Locomotion Policy。

## 3. 每条腿其实就是一个 5 轴串联机构

```text
Trunk
 ↓
Hip Yaw
 ↓
Hip Roll
 ↓
Hip Pitch
 ↓
Knee
 ↓
Ankle
 ↓
Foot / Sole
```

公开机械复现时，第一优先级不是把 Shell 做得一模一样，而是：

1. Joint Axis 方向；
2. Joint Center 位置；
3. Link-to-link Transform；
4. Foot / Sole 相对位置；
5. Mass Distribution 足够接近 Simulation Model，才能做有意义的对比。

外观可以后面再细化。

## 4. Neck / Head 结构

Policy 控制链：

```text
Trunk
 ↓
neck_pitch
 ↓
head_pitch
 ↓
head_yaw
 ↓
head_roll
 ↓
Head Assembly
```

然后 Runtime 再独立控制嘴/喙。

固定版本官方 Full-collision Model 里，`jaw_soft` / Head-roll Body 自己就大约 **188.8 g**；整个模型的 Inertial Mass 总和大约 **737.2 g**。

也就是说，Head Assembly 对这么小的机器人来说非常重。

这也是为什么 Head Motion、Head Command 和 Neck Dynamics 会明显影响整机 Balance。

## 5. 官方 Model 里有很多“参考坐标点”

MJCF 不只是 Mesh。

它还包含对逆向研究很有用的 Named Site，例如：

- Trunk IMU Site；
- Left / Right Foot Site；
- Head Camera Frame / Site；
- ToF Site；
- Head IMU Site；
- Mouth-tip Site。

这些 Site 比从图片里“目测摄像头大概在哪”可靠得多，可以作为 Simulation / Sensor Placement 的公开坐标参考。

但仍然要注明：它们是**Simulation Model Reference Frame**，不自动等于量产实体测量坐标。

## 6. 官方 Simulation Model 里直接能数出来的 Part Instance

固定版本 `robot_allcollisions.xml` 中，可以直接看到：

| Model Item | Visible Instance / 说明 |
|---|---|
| XL330 Motor Mesh | 15 个 |
| 22×16×4 Bearing Mesh | 11 个 |
| Smaller / Default Bearing Mesh | 3 个 |
| Left / Right Foot + Sole | 各 1 套 |
| Battery Geometry | 1 个模型空间 |
| Robot-HAT / PCB-like Geometry | 有 |
| Camera / Lens Geometry | 有 |
| Speaker Geometry | 有 |
| Left / Right Shell Geometry | 有 |

这些数量是**官方 Simulation Model Instance 数量**，不保证等于量产采购数量。

### 大轴承

官方 Asset Name 直接写成：

```text
seeed_bearing__configuration__22x16x4
```

所以 **22 mm OD × 16 mm ID × 4 mm Width** 是可以直接从官方仿真资产确认的几何信息。

### 小轴承

公开社区分析把 Smaller / Default Bearing 的几何估算为大约：

```text
15 × 10 × 3 mm
```

但 Supplier、Tolerance Class、Seal Type 和最终 Production Quantity 都还不能确认。

## 7. STL / Mesh 到底可以按什么类别看？

### Body / Core

- `trunk_base`；
- Left / Right Shell；
- Battery / Support Volume；
- Electronics / PCB Placeholder；
- Rigidity / Support Part。

### Legs

- Hip / Yaw-to-roll Part；
- Upper Leg；
- Lower-leg `leg`；
- Ankle；
- Foot；
- Sole；
- Rigidity Plate。

### Head

- Neck；
- Yaw / Roll Linkage；
- Top / Bottom Head Shell；
- Face；
- Jaw / Soft Mouth；
- Lens / Lens Holder；
- Speaker / Electronics Placeholder。

### Actuator / Support

- XL330 Geometry；
- Large / Small Bearing Geometry；
- Motor Support Part。

### Roller Variant

- Blade / Frame；
- Rim；
- Tire；
- Roller MJCF 中的 Passive Wheel Joint。

准确 STL 数量会随着上游 Revision 变化。

公开社区重建对它分析的版本报告了大约 **47 个 STL Asset**。这个数字适合作为某个 Snapshot 的参考，不应该写成永远不变的产品规格。

## 8. 怎样从 MJCF 还原装配位置？

MJCF 最有价值的地方之一是：每个 Body 都有相对 Parent 的 Transform。

因此可以按下面的方式重建：

```text
1. Load Robot XML
2. 遍历 Body Tree
3. 累积 Parent → Child Transform
4. 再乘每个 Geom 自己的 Local Transform
5. 把对应 STL / Mesh 放到 World Coordinate
6. Render 或 Export 完整装配结果
```

这比人工拖动 STL “看起来差不多对齐”可靠很多。

公开 `microduck-replica` 项目就是这类 Source-driven Reconstruction 的重要社区参考。

## 9. 螺丝现在知道到什么程度？

Pollen Robotics 没有公开量产 Screw BOM。

公开社区项目对 released Mesh 进行圆柱孔特征扫描后，发现非常明显的 M2-class Hole Cluster：

| Mesh Feature | 社区报告数量 | 推导含义 |
|---|---:|---|
| 约 Ø2.2 mm | 77 | M2 Clearance-like Hole |
| 约 Ø4.4 mm | 28 | M2 Head / Counterbore-like Recess |
| 约 Ø1.6 mm | 20 | M2 Tapping-drill-like Feature |
| 约 Ø2.4 mm | 22 | 较松 M2 Clearance Candidate |
| 约 Ø2.0 mm | 12 | 更紧的 M2-class Feature |
| 约 Ø2.7–2.8 mm | 20 | 可能的 M2.5-class Candidate |

同一分析在排除部分 Motor / External-component Feature 后，估算大约有 **146 个 Structural M2-class Through-hole Instance**。

这个结论很有逆向价值，但它仍然**不能证明：**

- 每个孔最后一定上螺丝；
- 螺丝准确长度；
- Head Type；
- 是否使用 Heat-set Insert；
- 量产版本是否改过结构。

## 10. 社区给出的 Trial-assembly 采购估算放在哪里？

公开社区重建还给出了比较保守的 Trial-assembly Stock，例如 M2×4 / 6 / 8 / 12、M2 Nut / Insert，以及少量 M2.5 Hardware。

OpenMicroDuck 把这些单独放在：

[社区推导 BOM、紧固件、轴承与装配重建](community-bom-reconstruction.md)

而不是把它写成“Microduck 官方螺丝 BOM”。

## 11. 如果要做机械研究，推荐的验证顺序

### A. 先做一条腿链

验证：

- 5 个 Joint Axis；
- Servo Orientation / Sign；
- Link Transform；
- Foot Location；
- 整个范围运动时有没有明显机械干涉。

### B. 再做镜像的另一条腿

确认左右 Sign 和 Mirrored Transform 没有写反。

### C. Trunk + 双腿

先看 Standing Geometry 和 CoM 关系，不要急着加很重的 Head Assembly。

### D. Neck / Head

Lower Body 理解正确后，再加入 Head Mass 和 Neck Chain。

### E. Shell / Secondary Feature

最后再加入 Camera / ToF / Audio / Cosmetic Shell Detail，同时保持已经确定的 Joint Reference Geometry 不被外观修改破坏。

这样每一步出错时更容易定位。

## 12. 对 Locomotion 来说，什么比“外观一模一样”更重要？

优先级通常应该是：

```text
Joint Center
Joint Axis
Link Length / Transform
Mass
Center of Mass
Inertia
Foot Collision Geometry
Sole Friction / Contact
Actuator Behavior
```

一个外壳看起来 100% 相似、但 CoM 完全不对的模型，动力学意义反而比一个外观粗糙但惯性参数正确的模型更差。

## 13. 模型和量产之间几个最容易踩的坑

### `np_f970` Filename

Simulation Model 有 `np_f970` 命名 Mesh，但当前官方 Product Battery 是 NP-F550。

所以它只能作为历史 / Development Geometry Evidence。

### Raspberry-Pi-related PCB Asset Name

某些 Mesh Name 保留了旧开发 Placeholder，而当前 Runtime Bring-up 已经是 Radxa Zero 3W。

### Thread / Insert

STL 很可能根本没有完整保留真实 Thread / Insert 工艺。

### Collision Geometry

Collision Mesh 通常为了 Simulation 简化，不能等同于 Manufacturing Surface。

## 14. 要成为真正“制造装配手册”，现在还缺什么？

公开资料还没有完整给出：

- Final Material；
- Printing / Molding / Manufacturing Process；
- Tolerance；
- Thread Specification；
- Heat-set Insert Location / Spec；
- 每种 Screw 的精确长度与最终数量；
- Wire Routing / Cable Length；
- Connector Retention；
- Assembly Torque；
- Production QA Procedure。

这些字段应该继续留空 / 标 Unresolved，而不是为了让表格“看起来完整”就硬猜。

## 主要来源

- `pollen-robotics/microduck_rl` 的 `robot_allcollisions.xml` 与 `assets/`
- Pollen Robotics Product / Press Material
- https://github.com/fanhao375/microduck-replica — 公开社区重建项目

## 相关页面

- [硬件参数总表](parameter-reference.md)
- [机械结构与运动学](mechanical-structure.md)
- [社区推导 BOM 与紧固件](community-bom-reconstruction.md)
- [公开复现路线图](../getting-started/public-reproduction-roadmap.md)
