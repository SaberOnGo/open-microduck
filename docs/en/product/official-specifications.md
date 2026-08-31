# Official Microduck Specifications

**English** | [简体中文](../../zh-CN/product/official-specifications.md)

> Source status: **official product specification**. Last checked: **2026-08-31**.

This page is the simple, product-level baseline for Microduck. It answers one question: **what has Pollen Robotics publicly confirmed about the robot itself?**

It intentionally does not mix product specifications with community reconstruction or development-board details. For those topics, see the hardware and research pages linked below.

## Quick overview

| Item | Official public information |
|---|---|
| Robot type | Small biped robot for physical AI, reinforcement learning, education, and play |
| Motors / degrees of freedom | **15** |
| Height | **25 cm** |
| Width | **14 cm** |
| Weight | **under 800 g** in the press kit; the store currently lists **780 g** |
| Compute | **Rockchip RK3566** with AI accelerator |
| Memory | **1 GB RAM** |
| Storage | **32 GB** |
| Policy loop | **50 Hz** |
| Camera | Front camera with dedicated camera-use indicator |
| Depth / range sensor | Compact **8×8 time-of-flight** LiDAR/ToF matrix |
| IMUs | **2**, one in the body and one in the head |
| Beak | Articulated grasping beak |
| Audio | Microphones and speaker |
| NFC | **2 antennas**, one in the head and one in the beak |
| Wireless | Wi-Fi and Bluetooth |
| Battery | Removable **NP-F550**, **2600 mAh**, around one hour depending on use |
| Controller | Game controller included |

## What “open source” means here

Pollen Robotics explicitly states that the open-source commitment covers the **software stack**: robot control software, simulation, reinforcement-learning training tools, and the sim-to-real workflow.

The official press kit also explicitly states that the **mechanical and electronic design files are not published as open-source hardware**.

Therefore OpenMicroDuck uses this wording:

- **official open-source software** — yes;
- **official open-source hardware design** — no;
- public simulation meshes and model data may still exist, but they must not be described as an official production CAD/BOM release.

## Publicly described abilities

Official launch material describes Microduck as able to perform behaviors including walking, sitting/crouching, getting back up from common falls, roller skating, and picking up objects with its beak.

These visible abilities should not be interpreted as one single neural network doing everything. The official RL project contains multiple task/policy families that share a common deployment interface. See [Policy catalog and switching](../simulation/policy-catalog-and-switching.md).

## Specifications that are still provisional

The official press kit explicitly says that several values are still being finalized. As of this source check, they include:

- camera resolution;
- camera field of view;
- LiDAR/ToF range;
- radio versions;
- SDK languages;
- age recommendation.

These should remain labeled **provisional / not final** until Pollen Robotics publishes final values.

## Product specification vs implementation detail

A useful rule when reading this repository is:

```text
product page / press kit
        ↓
what the finished product officially promises

current source code / bring-up files
        ↓
what a current development implementation uses

simulation assets
        ↓
what the training model represents

community reconstruction
        ↓
what third parties can reasonably derive from public evidence
```

All four are useful, but they are not interchangeable.

For example, the product specification confirms an RK3566 computer. Current official source also shows Radxa Zero 3W as a development/reference platform. That does not automatically mean every production revision must use exactly that carrier board forever.

## Primary official sources

- https://pollen-robotics.com/microduck/
- https://pollen-robotics.com/microduck/press-kit/
- https://store.pollen-robotics.com/products/microduck
- https://github.com/pollen-robotics/microduck
- https://github.com/pollen-robotics/microduck_rl

## Related OpenMicroDuck pages

- [Public hardware inventory / BOM status](../hardware/public-bom.md)
- [Electronics, buses, sensors, and power](../hardware/electronics-and-buses.md)
- [Mechanical structure and kinematics](../hardware/mechanical-structure.md)
- [Sources and evidence map](../sources.md)
