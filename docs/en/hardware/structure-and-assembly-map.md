# Structure and Assembly Map

**English** | [简体中文](../../zh-CN/hardware/structure-and-assembly-map.md)

> Purpose: turn the official simulation model and public reconstruction work into an easy-to-read assembly map. **This is not an official manufacturing drawing or production assembly manual.**

## 1. The robot is easier to understand as five modules

```text
Microduck
├── Trunk / body core
│   ├── compute / HAT volume
│   ├── battery volume
│   ├── left hip-yaw motor
│   └── right hip-yaw motor
├── Left leg
│   └── 5 controlled joints
├── Right leg
│   └── 5 controlled joints
├── Neck + head
│   └── 4 policy-controlled joints + separate mouth motor
└── Feet / optional rollers
```

This view is more useful for reproduction than treating dozens of STL names as unrelated parts.

## 2. Official 14-joint kinematic tree

The current full-collision MJCF exposes this policy-controlled tree:

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

The real runtime has a **15th mouth/beak motor**. It is outside the 14-action locomotion policy interface.

## 3. What each leg contains conceptually

Each leg is a five-axis serial chain:

```text
trunk
 ↓
hip yaw
 ↓
hip roll
 ↓
hip pitch
 ↓
knee
 ↓
ankle
 ↓
foot / sole
```

For a mechanical research build, the most important thing to preserve first is not shell appearance. It is:

1. joint-axis direction;
2. joint-center location;
3. link-to-link transform;
4. foot/sole position;
5. mass distribution close enough to the model for meaningful comparison.

Cosmetic surfaces can be refined later.

## 4. Neck/head chain

The policy-controlled chain is:

```text
trunk
 ↓
neck_pitch
 ↓
head_pitch
 ↓
head_yaw
 ↓
head_roll
 ↓
head assembly
```

The runtime then adds separate mouth/beak control.

The official full-collision model places a large amount of inertial mass in the head assembly: the `jaw_soft` / head-roll body is about **188.8 g** in the pinned model, while the total model inertial mass is about **737.2 g**.

That means head mass and head commands can noticeably affect whole-body balance.

## 5. Useful frame/site locations in the official model

The official MJCF includes named sites that are more useful than guessing geometry from screenshots.

Examples in the pinned full-collision model include:

- trunk IMU site;
- left and right foot sites;
- head camera frame/site;
- ToF site;
- head IMU site;
- mouth-tip site.

These sites provide reproducible coordinate references for simulation and sensor-placement studies.

They should be treated as **simulation-model reference frames**, not automatic production metrology.

## 6. Official simulation-model part instances

In the pinned `robot_allcollisions.xml` snapshot, the model visibly instantiates:

| Model item | Visible instance count / note |
|---|---|
| XL330 motor mesh | 15 |
| 22×16×4 bearing mesh | 11 |
| smaller/default bearing mesh | 3 |
| left/right feet and soles | 1 pair |
| battery geometry | 1 model volume |
| Robot-HAT/PCB-like geometry | present |
| camera/lens geometry | present |
| speaker geometry | present |
| left/right shell geometry | present |

These counts are useful for understanding the released assembly model, but they are not guaranteed production purchase quantities.

### Bearing note

The large bearing asset is explicitly named:

```text
seeed_bearing__configuration__22x16x4
```

so **22 mm OD × 16 mm ID × 4 mm width** is directly visible in official simulation assets.

Public community analysis estimates the smaller/default bearing geometry at roughly **15×10×3 mm**.

Supplier, tolerance class, seal type and final production quantity remain unresolved.

## 7. STL / mesh groups: what they are actually for

The official asset set contains meshes corresponding to groups such as:

### Body/core

- `trunk_base`;
- left/right shell pieces;
- battery/support volumes;
- electronics/PCB placeholders;
- rigidity/support parts.

### Legs

- hip / yaw-to-roll pieces;
- upper legs;
- lower-leg `leg` geometry;
- ankles;
- feet;
- soles;
- rigidity plates.

### Head

- neck pieces;
- yaw/roll linkage;
- top/bottom head shell;
- face;
- jaw / soft-mouth geometry;
- lens / lens holder;
- speaker and electronics placeholders.

### Actuator/support hardware

- XL330 geometry;
- large/small bearing geometry;
- motor/support pieces.

### Roller variant

- blade/frame geometry;
- rim;
- tire;
- passive wheel joints in the roller MJCF.

The exact STL count depends on the upstream revision. A public community reconstruction reported roughly **47 STL assets** in the snapshot it analyzed; that should not be turned into a timeless product specification.

## 8. How to reconstruct the assembly from MJCF

MJCF is valuable because each body carries a transform relative to its parent.

A reproducible assembly reconstruction can therefore follow this process:

```text
1. load robot XML
2. walk the body tree
3. accumulate parent → child transforms
4. apply each geom's local transform
5. place the referenced STL/mesh in world coordinates
6. render or export the assembled result
```

This is much stronger than manually aligning meshes by eye.

The public `microduck-replica` project follows this kind of source-driven reconstruction and publishes tools/results derived from the upstream model.

## 9. Fasteners: what is known

Pollen Robotics has not published a production screw BOM.

A public community geometry analysis of the released meshes found strong M2-class hole clusters. Its reported feature counts include:

| Mesh feature | Community-reported count | Interpretation |
|---|---:|---|
| about Ø2.2 mm | 77 | M2 clearance-like holes |
| about Ø4.4 mm | 28 | M2 head/counterbore-like recesses |
| about Ø1.6 mm | 20 | M2 tapping-drill-like features |
| about Ø2.4 mm | 22 | loose M2-clearance candidates |
| about Ø2.0 mm | 12 | tighter M2-class features |
| about Ø2.7–2.8 mm | 20 | possible M2.5-class candidates |

The same analysis estimates roughly **146 structural M2-class through-hole instances** after excluding some motor/external-component features.

This is useful reverse-engineering evidence, but it does **not** prove exact production screw lengths, thread inserts, head types or counts.

## 10. Community trial-assembly purchase estimate

The public community reconstruction also suggests a deliberately conservative trial-assembly stock such as M2×4/6/8/12 screws, M2 nuts/inserts and some M2.5 hardware.

OpenMicroDuck keeps those estimates on [Community-derived BOM and fastener reconstruction](community-bom-reconstruction.md) rather than calling them an official assembly BOM.

## 11. Recommended mechanical validation order

For a public research reproduction, a useful order is:

### A. One leg chain

Validate:

- five joint axes;
- servo orientation/sign;
- link transforms;
- foot location;
- mechanical travel without interference.

### B. Mirrored second leg

Confirm that left/right signs and mirrored transforms are correct.

### C. Trunk + both legs

Check standing geometry and CoM relationship before adding the head.

### D. Neck/head chain

Add the large head mass only after lower-body geometry is understood.

### E. Shells and secondary features

Add camera/ToF/audio/cosmetic shell details without changing joint reference geometry.

This sequence makes mechanical errors easier to isolate.

## 12. What matters to simulation more than cosmetic fidelity

For locomotion, prioritize:

```text
joint centers
joint axes
link lengths/transforms
mass
center of mass
inertia
foot collision geometry
sole friction/contact
actuator behavior
```

A visually perfect shell with the wrong CoM is a worse dynamics model than a rough-looking shell with correct inertial parameters.

## 13. Model-versus-product traps

### `np_f970` filename

The simulation model includes an `np_f970`-named mesh, while the official product battery is NP-F550. Treat the model filename as historical/development geometry evidence.

### Raspberry-Pi-related PCB asset names

Some mesh names reflect older/development placeholders, while the current runtime bring-up targets Radxa Zero 3W.

### Threads and inserts

STL geometry may not preserve production thread/insertion details at all.

### Collision geometry

Collision meshes are intentionally simplified for simulation and can differ from visual/manufacturing surfaces.

## 14. What is still missing for a true manufacturing assembly manual

Public sources do not yet establish a complete set of:

- final materials;
- printer/molding/manufacturing process;
- tolerances;
- thread specifications;
- heat-set insert locations/specifications;
- exact screw lengths and final counts;
- wire routing and cable lengths;
- connector retention details;
- assembly torque values;
- production QA procedure.

OpenMicroDuck should keep those fields blank/unresolved instead of filling them by guesswork.

## Primary sources

- `pollen-robotics/microduck_rl`, `robot_allcollisions.xml` and `assets/`
- Pollen Robotics product/press material
- https://github.com/fanhao375/microduck-replica — public community reconstruction

## Related pages

- [Hardware parameter reference](parameter-reference.md)
- [Mechanical structure and kinematics](mechanical-structure.md)
- [Community-derived BOM and fasteners](community-bom-reconstruction.md)
- [Public reproduction roadmap](../getting-started/public-reproduction-roadmap.md)
