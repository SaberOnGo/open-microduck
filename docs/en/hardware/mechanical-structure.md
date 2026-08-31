# Mechanical Structure and Kinematics

> This page separates the **official simulation/kinematic model** from **community-derived assembly conclusions**.

## High-level geometry

Pollen Robotics' public product specification describes Microduck as approximately **25 cm tall**, **14 cm wide**, and **under 800 g**.

The official reinforcement-learning repository contains MJCF robot models exported from an Onshape workflow. Those models include rigid-body transforms, joint axes, limits, inertial properties, collision geometry, and visual meshes sufficient to reconstruct the public simulation kinematic tree.

The simulation assets are useful for studying structure, but a simulation mesh should not be assumed to be a manufacturing CAD file. Tolerances, threaded features, inserts, wire routing, material specifications, production fasteners, and assembly processes may be absent or simplified.

## Policy kinematic tree

The 14 policy-controlled joints are arranged as follows:

```text
trunk / floating base
├── left leg
│   ├── left_hip_yaw
│   ├── left_hip_roll
│   ├── left_hip_pitch
│   ├── left_knee
│   └── left_ankle
├── neck and head
│   ├── neck_pitch
│   ├── head_pitch
│   ├── head_yaw
│   └── head_roll
└── right leg
    ├── right_hip_yaw
    ├── right_hip_roll
    ├── right_hip_pitch
    ├── right_knee
    └── right_ankle
```

The onboard runtime contains a **15th motor for the mouth/beak**. That joint is intentionally skipped by the 14-action locomotion policy and is handled separately by the runtime.

This distinction explains why different public pages sometimes say “15 motors / 15 DOF” while the RL actor outputs 14 actions.

## Joint ranges visible in public models

The MJCF files contain explicit hinge limits. Community reconstruction projects have extracted these values and rendered them as tables. Because the source assets can change between branches/revisions, OpenMicroDuck recommends reading the active upstream MJCF when exact limits matter rather than treating a copied table as permanent product specification.

The current official model files are under:

`pollen-robotics/microduck_rl/src/mjlab_microduck/robot/microduck/`

Important variants include:

- `robot_walk.xml` — walking model with reduced collision scope;
- `robot_allcollisions.xml` — full-body collision model used by recovery/trick tasks;
- `robot_allcollisions_rollers.xml` — roller configuration with passive wheel joints;
- generated `*_backlash.xml` variants — insert passive backlash hinges for sim-to-real experiments.

## Rigid-body mass and inertia

The public MJCF includes per-body mass, center of mass, and inertia tensors. This is one of the most valuable public mechanical sources because it allows:

- forward/inverse kinematics experiments;
- approximate center-of-mass reconstruction;
- dynamics simulation;
- collision and contact studies;
- comparison of walking and roller configurations;
- independent visualization and assembly-tree reconstruction.

These numbers are simulation-model parameters. They should not automatically be described as metrology results from a production unit.

## Public visual/mesh assets

Community projects have catalogued the released meshes into groups such as:

- trunk and outer shells;
- hip/yaw-to-roll parts;
- left/right upper legs;
- lower legs;
- ankles, feet, and soles;
- neck and head linkage parts;
- jaw/beak parts;
- camera/lens geometry;
- motor geometry;
- bearing geometry;
- PCB/battery placeholder geometry;
- roller frames, rims, and tires.

The exact file count depends on which upstream snapshot and variant is being counted. Do not use “N STL files” as a timeless product specification.

## Community assembly reconstruction

### `fanhao375/microduck-replica`

This project uses the official MJCF transforms and public STL assets to produce:

- assembled views and exploded views;
- world-transformed STL assemblies suitable for opening in CAD/mesh tools;
- a rigid-body assembly tree;
- model-derived mass summaries;
- hole-feature analysis for approximate fastener reconstruction;
- bearing and structural feature notes.

Repository: https://github.com/fanhao375/microduck-replica

Its outputs are **third-party reconstructions**, not official manufacturing drawings.

### `boris721/microduck-3d`

This project catalogs public Microduck simulation meshes, kinematic trees, combined models, and walking/roller variants.

Repository: https://github.com/boris721/microduck-3d

## Fastener reconstruction

The `microduck-replica` project performs geometric hole analysis over public mesh assets and concludes that the structure is predominantly based on an **M2-class fastener system**. It identifies clusters of hole diameters consistent with M2 clearance/counterbore/tapping features and derives approximate purchase quantities.

This is useful evidence for understanding the public model geometry, but it is **not an official screw BOM**. Mesh simplification, print/manufacturing tolerances, inserts, hidden features, and production revisions can change the real assembly.

## Bearing reconstruction

Public meshes include bearing-shaped assets. Community analyses identify geometry corresponding approximately to:

- 22 mm OD × 16 mm ID × 4 mm width;
- a smaller bearing around 15 mm OD × 10 mm ID × 3 mm width.

Again, these are geometry-derived observations. Supplier, tolerance class, material, sealing, and production quantity are not established by the public model alone.

## Why the model is unusually useful for reverse engineering

A conventional marketing render reveals only shape. The released Microduck RL model also exposes:

1. the rigid-body hierarchy;
2. parent/child transforms;
3. joint axes and limits;
4. collision geometry;
5. body masses and inertias;
6. named sites such as feet/camera/mouth reference points;
7. passive joints used by roller and backlash models.

That is enough to reconstruct a high-quality **simulation assembly description**, but not automatically enough to reconstruct the undocumented production manufacturing package.

## Primary sources

- https://github.com/pollen-robotics/microduck_rl
- https://github.com/pollen-robotics/microduck_rl/tree/develop/src/mjlab_microduck/robot/microduck
- https://pollen-robotics.com/microduck/press-kit/

## Community sources

- https://github.com/fanhao375/microduck-replica
- https://github.com/boris721/microduck-3d

See [public-bom.md](public-bom.md) for component evidence levels and [../legal/provenance-and-licenses.md](../legal/provenance-and-licenses.md) before redistributing upstream or derivative 3D assets.
