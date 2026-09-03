# Simulation Model Assets Reference

**English** | [简体中文](../../zh-CN/simulation/model-assets-reference.md)

> Primary source: official `pollen-robotics/microduck_rl` repository.
>
> Model-family naming checked against `microduck_rl/develop` commit `29e887ecfbf5d37144759e5a9f8a176dfb83d547` on **2026-09-03**.

The official RL repository does not use one universal robot XML for every task. Walking, lying on the floor, rolling, and full-body contact need different collision models.

This page explains what the main public model families are for and how to avoid comparing the wrong assets.

## Where the official models live

Current upstream path:

```text
src/mjlab_microduck/robot/microduck/
```

The directory contains robot MJCF/XML files, scene wrappers, mesh assets, export configuration, and helper scripts such as the backlash-model generator.

## Important 2026-09-02 naming change

An upstream model re-export corrected a misleading old name.

The older `allcollisions` family was **not** actually “every collision on every part.” It was a curated set of collision geoms intended for parts that may contact the floor in ground tasks.

Upstream therefore changed the naming to:

```text
old curated `allcollisions` role
              ↓ renamed
         `groundcontact`
```

and introduced a new true:

```text
robot_allcollisions.xml
```

where every part can carry collision geometry.

This is not just cosmetic naming. It changes how a reader should interpret an experiment.

## Main robot model families now

| Model | Main purpose | Why it is different |
|---|---|---|
| `robot_walk.xml` | Main walking / velocity work | Walking-oriented model with reduced body-collision scope |
| `robot_groundcontact.xml` | Ground-contact tasks | Curated contact set for parts expected to touch the floor; this is the renamed role of the older misleading `allcollisions` name |
| `robot_groundcontact_rollers.xml` | Roller / skating work | Ground-contact variant plus passive roller-wheel mechanics |
| `robot_allcollisions.xml` | True full-part collision inspection / experiments | New variant in which every part carries a collision geom, apart from explicitly excluded pathological contact pairs |
| `*_backlash.xml` | Backlash variants | Adds passive gear-play hinges in series with controlled servo joints |

The current upstream tree also contains matching scene wrappers such as `scene.xml`, `scene_walk.xml`, `scene_rollers.xml`, `scene_backlash.xml`, `scene_allcollisions.xml`, and the apartment scene used by recent simulation work.

## How different are `groundcontact` and true `allcollisions`?

The upstream re-export PR reports approximately:

```text
groundcontact collision geoms: 11
true allcollisions geoms:       70
true allcollisions meshes:      37
```

The all-collisions variant explicitly excludes one known phantom self-contact pair around the neck/jaw closed-loop geometry where CAD meshes interpenetrate in all poses.

Evidence level: **official public upstream repository / merged PR**.

The PR also reports that the re-exported walking and curated ground-contact models remained physics-identical to the previous versions for joint names/order/ranges, masses, inertias, frames, and their intended collision sets; the visible CAD material colors changed.

## Why `robot_walk.xml` is not “less accurate” by definition

A simulation model is often simplified for the task it is solving.

For ordinary walking training, detailed contacts on every shell surface can make contact computation more complicated without improving the desired gait. A walking-oriented model can therefore intentionally reduce some body contacts.

That is different from a recovery or full-body-contact experiment, where the robot may physically lie on or roll across the floor.

So the correct question is not:

> Which XML is the one true Microduck model?

It is:

> Which model variant matches the behavior or physical question being tested?

## Scene files

The repository also contains `scene*.xml` files. These wrap robot models with environment elements such as:

- a floor;
- initial poses / keyframes;
- stand, sit, or folded configurations;
- convenient setup for visualization and inference tools;
- in newer work, richer environments such as an apartment.

A scene file is therefore not the same thing as the reusable robot body model itself.

The newer `duck-body` simulator also accepts a custom scene through `--scene`, which makes the distinction especially useful for hardware-variant studies.

## Mesh assets

The public model assets include visual geometry for many robot parts, including body shells, legs, feet, head/neck structures, beak-related parts, motor geometry, board/battery geometry, and roller attachments.

These assets are highly useful for:

- visualization;
- kinematic reconstruction;
- checking body hierarchy and transforms;
- collision/model comparison;
- independent simulator ports;
- community assembly studies.

But they should not automatically be described as final manufacturing CAD. Simulation meshes may omit tolerances, threads, inserts, wiring channels, production fastener details, material callouts, and other manufacturing information.

## Mass, inertia, joint axes, and limits

The official MJCF contains dynamics-related parameters such as:

- rigid-body hierarchy;
- body transforms;
- joint axes;
- joint limits;
- body mass;
- center-of-mass offsets;
- inertia values;
- collision geometry;
- named sites / reference points.

These are very valuable for simulation and analysis.

Evidence label: **official simulation model parameter**, not automatically “measured production-unit value.”

The 2026-09-02 re-export is useful evidence that these parameters are tied to the upstream CAD-to-MJCF workflow rather than being arbitrary visualization-only values.

## Roller models

Roller tasks use passive wheel joints under the feet. In the official naming convention, unactuated joints are generally named `passive_*`.

That distinction matters when code selects the 14 servo joints: passive roller joints should not accidentally become neural-network actions.

## Backlash-generated models

Backlash variants add an unactuated passive hinge in series with each of the 14 servo-controlled joints.

The model is designed so the simulated encoder observation can include motion through the backlash rather than simply adding random noise to a clean joint angle.

The neural-network interface remains unchanged:

```text
61 observations
14 actions
```

This makes it possible to compare idealized and backlash-aware simulations without redesigning the deployment interface.

## Onshape export workflow

The upstream repository records MJCF export recipes in `config_mjcf_*.json` files and uses `onshape-to-robot` in the model-generation workflow.

The 2026-09-02 re-export explicitly states that the walk / ground-contact / roller models were re-exported from updated CAD and then checked by compiled-model comparison.

This provenance helps distinguish:

- upstream-generated simulation geometry and dynamics;
- later community-transformed / combined meshes;
- production manufacturing drawings, which are not publicly released as open-source hardware.

## Asset licensing

The official RL README states:

- software: Apache-2.0;
- 3D model files: Creative Commons BY-SA-NC.

Always inspect the exact upstream file/license state before redistributing model assets or derivatives. A repository-wide software license should not be assumed to override a separate asset license.

## Recommended comparison checklist

Before comparing two simulation results, record:

```text
robot XML / scene XML
walk / groundcontact / true allcollisions
backlash or non-backlash
roller or normal feet
upstream commit SHA
task id
collision/contact configuration
actuator configuration
```

Otherwise two experiments that look like “the same Microduck” may actually use meaningfully different physics.

## Primary official sources

- https://github.com/pollen-robotics/microduck_rl
- https://github.com/pollen-robotics/microduck_rl/tree/develop/src/mjlab_microduck/robot/microduck
- https://github.com/pollen-robotics/microduck_rl/pull/29

## Related pages

- [Hardware Variant Simulation](hardware-variant-simulation.md)
- [Mechanical structure and kinematics](../hardware/mechanical-structure.md)
- [Simulation and reinforcement learning](model-and-rl.md)
- [Reproducible training and ONNX export](reproducible-training-and-export.md)
- [Provenance and licensing](../legal/provenance-and-licenses.md)
