# Interactive Onshape Assembly Baseline

**English** | [简体中文](../../zh-CN/hardware/onshape-interactive-assembly.md)

> Status: public-source assembly reference. This page does **not** claim to be an official manufacturing assembly manual.

## Why this is the preferred assembly reference

The current `pollen-robotics/microduck_rl` full-collision model states that it was generated with `onshape-to-robot` and points directly to this Onshape element:

- Onshape document: https://cad.onshape.com/documents/804927696f06d877f3f1803e/w/5b75db19292e71970de02dee/e/ef6e972847fec8d82570b35e
- Document ID: `804927696f06d877f3f1803e`
- Workspace ID: `5b75db19292e71970de02dee`
- Assembly element ID: `ef6e972847fec8d82570b35e`
- Upstream evidence: `pollen-robotics/microduck_rl/src/mjlab_microduck/robot/microduck/robot_allcollisions.xml`

For assembly inspection, this source is more useful than a merged STL because Onshape can preserve part identity and assembly structure. When the upstream document exposes the relevant assembly data, it can be used to rotate, pan, zoom, select parts, hide/isolate components, inspect relationships, and measure geometry.

## Publicly verified component coverage

The official `microduck_rl` export and its `.part` metadata show separate source parts for major assembly items, including:

- Dynamixel XL330 servo geometry;
- left/right shells and head shells;
- trunk, hip, leg, ankle, foot and sole structure;
- large and smaller bearing geometry;
- RPI Robot HAT PCB geometry;
- Raspberry Pi Zero 2 W PCB placeholder/geometry used by that model revision;
- battery geometry;
- lens and lens holder;
- speaker;
- motor supports and rigidity/support parts.

The full-collision simulation export visibly instantiates **15 XL330 servo meshes**. Fourteen correspond to the policy-controlled kinematic chain and the real robot runtime additionally controls the mouth/beak motor.

## What is not verified as a complete Onshape assembly item set

No independent `screw`, `bolt` or equivalent fastener parts are present in the released `microduck_rl` asset listing. The public simulation export also does not provide a complete cable/wire-harness model.

Therefore OpenMicroDuck must currently treat the following as unresolved:

- exact per-location screw model and length;
- washers, inserts and nuts at every location;
- cable routing and cable lengths;
- connector retention details;
- assembly torque values.

Community fastener reconstruction may be used as separately labelled evidence, but it must not be merged into the upstream Onshape baseline as if it were official CAD.

## Baseline for servo replacement work

The intended modification workflow is deliberately narrow:

1. use the upstream Onshape assembly as the reference geometry;
2. preserve the existing joint centers, joint-axis directions and relative transforms;
3. keep electronics, bearings, battery, shells and unrelated structure unchanged;
4. identify all XL330 instances and their immediate mounting/support geometry;
5. replace only the servo geometry with the candidate servo geometry;
6. modify only structure that must change because of servo envelope, mounting-hole pattern, output-shaft position, horn/output interface or cable/connector clearance;
7. check interference and mechanical travel before changing unrelated parts.

The goal is **not** to redesign Microduck. The goal is to create a controlled servo-substitution baseline where changes can be traced directly to the actuator replacement.

## What to inspect in Onshape

For each XL330 installation, inspect and record:

- servo body orientation;
- output-shaft center and axis;
- mounting-face orientation;
- mounting-hole locations;
- adjacent bearing location and axis where present;
- servo-to-link/support relationship;
- clearance to shells and neighboring structure;
- connector/cable exit clearance where visible;
- joint limits implied by the physical geometry.

The most important comparison is the **coordinate relationship**, not visual similarity.

## Publishing and licensing boundary

The `microduck_rl` repository states that its 3D model files are licensed under CC BY-SA-NC. That statement clearly covers the released repository model files; it does not by itself prove that every editable object in the referenced Onshape document may be mirrored or republished under the same terms.

For that reason OpenMicroDuck currently links to the upstream Onshape source and records public metadata, but does **not** mirror the editable Onshape document or export/relicense it as an OpenMicroDuck-owned CAD asset until the applicable upstream license is verified.

Derived OpenMicroDuck geometry may be published later only when its source/license chain is clear and compatible with the public repository.

## Primary sources

- Pollen Robotics `microduck_rl` full-collision MJCF: https://github.com/pollen-robotics/microduck_rl/blob/develop/src/mjlab_microduck/robot/microduck/robot_allcollisions.xml
- Pollen Robotics `microduck_rl` asset directory: https://github.com/pollen-robotics/microduck_rl/tree/develop/src/mjlab_microduck/robot/microduck/assets
- Upstream Onshape assembly element: https://cad.onshape.com/documents/804927696f06d877f3f1803e/w/5b75db19292e71970de02dee/e/ef6e972847fec8d82570b35e

## Related pages

- [Structure and assembly map](structure-and-assembly-map.md)
- [Mechanical structure and kinematics](mechanical-structure.md)
- [Community-derived BOM and fasteners](community-bom-reconstruction.md)
