# Onshape 交互式总装基线

[English](../../en/hardware/onshape-interactive-assembly.md) | **简体中文**

> 状态：公开来源的装配参考。本文档**不是官方量产装配手册**。

## 为什么优先使用这个装配来源

当前 `pollen-robotics/microduck_rl` 的 Full-collision Model 明确写明由 `onshape-to-robot` 生成，并直接指向下面这个 Onshape Element：

- Onshape 文档：https://cad.onshape.com/documents/804927696f06d877f3f1803e/w/5b75db19292e71970de02dee/e/ef6e972847fec8d82570b35e
- Document ID：`804927696f06d877f3f1803e`
- Workspace ID：`5b75db19292e71970de02dee`
- Assembly Element ID：`ef6e972847fec8d82570b35e`
- 上游证据：`pollen-robotics/microduck_rl/src/mjlab_microduck/robot/microduck/robot_allcollisions.xml`

对于装配研究，这比合并后的 STL 更有价值。Onshape 能保留 Part Identity 和 Assembly Structure；当上游文档公开了相应装配数据时，可以用于旋转、平移、缩放、选中单个零件、隐藏/隔离零件、查看相互关系以及测量几何尺寸。

## 已经可以从公开上游确认的元件范围

官方 `microduck_rl` 导出结果和 `.part` Metadata 显示，主要装配对象存在独立 Source Part，包括：

- Dynamixel XL330 舵机几何；
- 左右 Body Shell、Head Shell；
- Trunk、Hip、Leg、Ankle、Foot、Sole 等结构件；
- 大、小两类 Bearing 几何；
- RPI Robot HAT PCB 几何；
- 该模型版本中的 Raspberry Pi Zero 2 W PCB Placeholder / Geometry；
- Battery Geometry；
- Lens 与 Lens Holder；
- Speaker；
- Motor Support、Rigidity / Support Part。

Full-collision Simulation Export 中可以直接看到 **15 个 XL330 Servo Mesh Instance**。其中 14 个构成 Policy-controlled Kinematic Chain，真实 Runtime 另外还控制 Mouth / Beak Motor。

## 目前不能确认完整存在于 Onshape 总装中的内容

公开 `microduck_rl` Asset Listing 中没有看到独立的 `screw`、`bolt` 或同类 Fastener Part；公开 Simulation Export 也没有完整 Wire Harness / Cable Routing Model。

因此下面这些内容目前必须标为 Unresolved：

- 每个安装位置对应的准确 Screw Model 与 Length；
- 每个位置的 Washer、Insert、Nut；
- Wire Routing 与 Cable Length；
- Connector Retention；
- Assembly Torque。

社区对紧固件的公开逆向结果可以单独作为 Community-derived Evidence 使用，但不能直接混入 Onshape Baseline，并包装成“官方 CAD 已确认”。

## 用于更换舵机的基线原则

这条工作流刻意限制修改范围：

1. 以上游 Onshape Assembly 作为 Reference Geometry；
2. 保留现有 Joint Center、Joint Axis Direction 和 Relative Transform；
3. Electronics、Bearing、Battery、Shell 以及与舵机无关的结构保持不变；
4. 找出所有 XL330 Instance 以及它们直接接触的 Mounting / Support Geometry；
5. 只把 XL330 Geometry 替换为 Candidate Servo Geometry；
6. 只有在 Servo Envelope、Mounting-hole Pattern、Output-shaft Position、Horn / Output Interface、Cable / Connector Clearance 确实要求变化时，才修改对应结构件；
7. 在修改其它无关结构之前，先做 Interference 与 Mechanical Travel 检查。

目标不是重新设计 Microduck，而是建立一个**可追踪的舵机替换基线**：每一处结构变化都应该能明确解释为“由更换 XL330 引起”。

## 在 Onshape 里需要重点检查什么

对每一个 XL330 安装位置，至少检查并记录：

- Servo Body Orientation；
- Output-shaft Center 与 Axis；
- Mounting Face Orientation；
- Mounting-hole Location；
- 相邻 Bearing 的 Location 与 Axis（存在时）；
- Servo 与 Link / Support 的连接关系；
- 与 Shell、相邻结构的 Clearance；
- 可见情况下的 Connector / Cable Exit Clearance；
- Physical Geometry 对 Joint Travel 的限制。

真正重要的是**坐标关系**，不是外观看起来“差不多”。

## 公开发布与 License 边界

`microduck_rl` 仓库明确写明其 3D Model Files 使用 CC BY-SA-NC License。这个声明可以明确覆盖仓库里已经发布的 Model Files；但它本身不能证明 Onshape 文档中的每一个 Editable Object 都可以按相同条款被镜像、重新发布或重新授权。

因此 OpenMicroDuck 当前只记录并链接上游 Onshape Source 与公开 Metadata，**不会在 License 未确认前，把整个 Editable Onshape Document 镜像进 OpenMicroDuck，也不会把它重新标成 OpenMicroDuck 自有 CAD。**

后续如果需要发布 OpenMicroDuck Derived Geometry，必须先保证 Source / License Chain 清晰且兼容公开仓库。

## 主要来源

- Pollen Robotics `microduck_rl` Full-collision MJCF：https://github.com/pollen-robotics/microduck_rl/blob/develop/src/mjlab_microduck/robot/microduck/robot_allcollisions.xml
- Pollen Robotics `microduck_rl` Asset Directory：https://github.com/pollen-robotics/microduck_rl/tree/develop/src/mjlab_microduck/robot/microduck/assets
- 上游 Onshape Assembly Element：https://cad.onshape.com/documents/804927696f06d877f3f1803e/w/5b75db19292e71970de02dee/e/ef6e972847fec8d82570b35e

## 相关页面

- [结构与装配地图](structure-and-assembly-map.md)
- [机械结构与运动学](mechanical-structure.md)
- [社区推导 BOM 与紧固件](community-bom-reconstruction.md)
