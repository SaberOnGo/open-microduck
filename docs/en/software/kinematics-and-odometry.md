# Kinematics and Odometry

**English** | [简体中文](../../zh-CN/software/kinematics-and-odometry.md)

> Scope: public official Microduck source. This page explains what the geometry code does before naming implementation details.

## Why this layer exists

The robot needs to answer two simple questions:

1. **Where is a body part or sensor relative to the trunk?**
2. **Where has the robot moved relative to where it started?**

Those are handled by **kinematics** and **odometry**.

```text
joint angles + robot model
          │
          ▼
      kinematics
          │
   ┌──────┼─────────┐
   ▼      ▼         ▼
 feet    head      ToF pose
   │                 │
   │                 └─> depth points in robot coordinates
   │
   └─> contact + IMU
             │
             ▼
          odometry
             │
             ▼
     estimated robot position
```

## Kinematics: where is each part?

Microduck's current official `kinematics` crate reads the same MJCF-style robot geometry used by the robot model, then compiles the body/joint chains once.

For a query such as “where is the left foot?”, it combines:

- the fixed link transforms from the model;
- the current measured joint angles;
- the joint axes and order.

The result is a pose relative to the trunk.

This is useful for:

- left/right foot position;
- head orientation;
- camera/ToF mounting pose;
- gaze calculations;
- converting ToF measurements into robot-frame points;
- contact-based odometry.

## One source of geometry

A valuable design choice in the official code is that geometry is taken from the robot model instead of maintaining a second hand-written table.

```text
robot model / MJCF
        │
        ├─> simulation
        └─> runtime kinematics
```

This reduces a common reproduction failure: the simulator and runtime silently using different link lengths, joint axes, or offsets.

## ToF reprojection

The ToF sensor returns 64 slant ranges in an 8×8 grid. Those distances are not yet “obstacle positions”.

The public runtime geometry path combines:

```text
8×8 ToF ranges
      +
head joint angles
      +
ToF mounting pose
      +
trunk orientation from IMU
      ↓
3D points in trunk coordinates
      ↓
classify as floor / too close / obstacle / empty
```

The current public code uses a 45° × 45° ToF field of view and treats very short returns around the sub-10 cm region as unreliable. See the source for version-sensitive thresholds.

## Odometry: where did the robot move?

Microduck's public `odometry` crate estimates motion from **legs + IMU**, without GPS or wheel encoders.

The basic idea is simple:

1. assume one foot contact point is planted on the floor;
2. use forward kinematics to know where that contact point is relative to the trunk;
3. use the IMU for trunk orientation;
4. infer the trunk position from the planted contact;
5. when another foot corner becomes the new stable low point, move the contact anchor to it.

```text
stance-foot contact
       +
foot kinematics
       +
IMU orientation
       ↓
estimated trunk position
```

The world frame is relative to startup. There is no magnetometer in this estimator, so heading follows the IMU's boot-relative yaw.

## Important current public implementation details

At the pinned official snapshot used by this documentation sweep:

- kinematics is evaluated from compiled joint/site chains rather than rebuilding the whole tree for every query;
- foot and head geometry comes from the embedded alpha robot model;
- odometry uses the left/right foot sites and IMU orientation;
- the contact switch is debounced across multiple control ticks;
- current sole half-extents in the odometry source are explicitly marked as a placeholder carried from earlier geometry, so they should **not** be promoted to final alpha production dimensions.

That last point is important for reverse engineering: a value present in source can still be documented by upstream as provisional.

## Why this matters for reproduction

A third-party reproduction that only copies joint names and servo IDs can still fail if these geometric relationships are wrong:

- joint center position;
- joint axis direction;
- link-to-link transform;
- sensor mounting pose;
- foot sole geometry.

For simulation and runtime to agree, the safest rule is:

> **Keep one robot geometry source and derive kinematics from it.**

## Primary public sources

- https://github.com/pollen-robotics/microduck/tree/main/kinematics
- https://github.com/pollen-robotics/microduck/blob/main/kinematics/src/lib.rs
- https://github.com/pollen-robotics/microduck/blob/main/kinematics/src/tof.rs
- https://github.com/pollen-robotics/microduck/tree/main/odometry
- https://github.com/pollen-robotics/microduck/blob/main/odometry/src/lib.rs

Related pages:

- [Structure and assembly map](../hardware/structure-and-assembly-map.md)
- [Hardware parameter reference](../hardware/parameter-reference.md)
- [Autonomous Brain](autonomous-brain.md)
