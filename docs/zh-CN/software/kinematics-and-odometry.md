# 运动学与里程计：机器人怎么知道“身体在哪、自己走了多远”

[English](../../en/software/kinematics-and-odometry.md) | **简体中文**

> 范围：只整理 Microduck 官方公开源码。本文先解释“它干什么”，再解释代码名。

## 先看整体

机器人需要回答两个很实际的问题：

1. **脚、头、ToF 等部件现在相对身体主干在哪？**
2. **机器人相对刚开机的位置移动了多少？**

前者是**运动学（Kinematics）**，后者是**里程计（Odometry）**。

```text
关节角度 + 机器人结构模型
            │
            ▼
          运动学
            │
      ┌─────┼──────┐
      ▼     ▼      ▼
     脚     头    ToF位置
      │              │
      │              └─> 把深度换算成机器人坐标
      │
      └─> 脚底接触 + IMU
                    │
                    ▼
                  里程计
                    │
                    ▼
              估计机器人位置
```

## 运动学：根据关节角度算部件位置

官方当前 `kinematics` 模块会读取机器人模型里的关节结构和固定几何关系。

例如要算“左脚现在在哪里”，程序会把这些东西组合起来：

- 每一段结构件之间的固定位置关系；
- 当前测到的关节角度；
- 每个关节的转轴方向；
- 关节的先后连接顺序。

最后得到左脚相对身体主干的位置和朝向。

同一套方法还可以用于：

- 左右脚位置；
- 头部朝向；
- Camera / ToF 安装位置；
- 看向目标时的头部计算；
- 把 ToF 深度变成机器人坐标下的障碍物；
- 脚底接触里程计。

## 一个很重要的设计：尽量只用一份机器人几何模型

官方代码尽量直接从机器人模型里读取几何关系，而不是再手工维护一份“运行时代码尺寸表”。

```text
机器人 Model / MJCF
        │
        ├─> 仿真
        └─> 真机运行时运动学
```

这样可以避免一种很常见的问题：

> 仿真里的腿长、Joint Axis、Offset 是一套，真机代码里又抄了一套，结果两边慢慢不一致。

## ToF 的 8×8 距离怎么变成障碍物？

ToF 原始输出只是 64 个距离值，本身还不知道这些点在机器人前后左右哪里。

公开代码的处理大致是：

```text
8×8 ToF 距离
      +
头部当前4个关节角度
      +
ToF 在头上的安装位置
      +
IMU 给出的身体倾斜方向
      ↓
换算成身体坐标下的 3D 点
      ↓
判断：地面 / 太近不可信 / 障碍物 / 无有效目标
```

当前公开源码使用 45° × 45° 的 ToF 视场角；非常近的读数会被当作不可靠区域处理。具体阈值属于版本敏感参数，应以对应源码为准。

## 里程计：不用 GPS，怎么估计自己走了多远？

Microduck 当前公开的 `odometry` 主要依靠：

**脚 + 运动学 + IMU**。

最简单的理解方式是：

1. 假设当前有一个脚底点踩在地上没有滑动；
2. 运动学知道这个脚底点相对身体在哪里；
3. IMU 知道身体朝哪个方向倾斜；
4. 于是反推出身体主干在空间里的位置；
5. 当另一只脚稳定落地后，把“地面锚点”切到新的脚。

```text
当前支撑脚
    +
脚的位置计算
    +
IMU 姿态
    ↓
估计身体主干的位置
```

这个坐标系是**相对开机时的位置**。当前估计器没有靠磁力计给出绝对北方，因此朝向也是开机相对方向。

## 当前源码里需要特别注意的一点

官方 `odometry` 源码里的脚底半长、半宽目前明确写着是从早期结构带过来的 **placeholder**，等待 alpha 的真实 sole geometry 进一步确认。

因此这些数字不能直接写成：

> “Microduck 最终量产脚底尺寸就是这个。”

它只能标成当前源码中的暂定实现值。

## 为什么复现时这部分很重要？

就算 Servo ID、关节名字全抄对了，只要下面这些几何关系错了，机器人仍然会表现异常：

- Joint Center 位置；
- Joint Axis 方向；
- 每段 Link 的相对位置；
- ToF / Camera 安装姿态；
- 脚底真实尺寸。

因此对第三方复现最稳妥的原则是：

> **尽量只有一份机器人结构模型，仿真和运行时都从它推导几何关系。**

## 主要公开来源

- https://github.com/pollen-robotics/microduck/tree/main/kinematics
- https://github.com/pollen-robotics/microduck/blob/main/kinematics/src/lib.rs
- https://github.com/pollen-robotics/microduck/blob/main/kinematics/src/tof.rs
- https://github.com/pollen-robotics/microduck/tree/main/odometry
- https://github.com/pollen-robotics/microduck/blob/main/odometry/src/lib.rs

相关页面：

- [结构与装配地图](../hardware/structure-and-assembly-map.md)
- [硬件参数总表](../hardware/parameter-reference.md)
- [Autonomous Brain](autonomous-brain.md)
