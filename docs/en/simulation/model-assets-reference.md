# Simulation Model Assets Reference

**English** | [简体中文](../../zh-CN/simulation/model-assets-reference.md)

> Primary source: official `pollen-robotics/microduck_rl` repository.

The official RL repository does not use one universal robot XML for every task. It contains several MJCF variants because walking, lying on the floor, rolling, and skating need different contact models.

This page explains what the main public model families are for and how to avoid comparing the wrong assets.

## Where the official models live

Current upstream path:

```text
src/mjlab_microduck/robot/microduck/
```

The directory contains robot MJCF/XML files, scene wrappers, mesh assets, export configuration, and helper scripts such as the backlash-model generator.

## Main robot model families

| Model | Main purpose | Why it is different |
|---|---|---|
| `robot_walk.xml` | Main walking / velocity task | Reduced trunk/head contact scope; optimized for gait training rather than full-body floor interaction |
| `robot_allcollisions.xml` | Stand-up, sit/stand, ground pick, ball kick, roulade, recovery-style tasks | Full-body collision/contact is needed because the robot can lie on or roll over the floor |
| `robot_allcollisions_rollers.xml` | Roller / skating tasks | Adds passive roller-wheel mechanics and the contact structure needed for skating |
| `robot_*_backlash.xml` | Backlash variants of the main models | Adds passive gear-play hinges in series with controlled servo joints |

## Why `robot_walk.xml` is not “less accurate” by definition

A simulation model is often simplified for the task it is solving.

For ordinary walking training, detailed contacts on every shell surface can make falling/contact computation more expensive without improving the desired gait. A walking-oriented model can therefore intentionally reduce some body contacts.

That is different from a recovery task, where the robot must physically touch the floor with its trunk/head and get back up. For that task, all-collision geometry matters.

So the correct question is not:

> Which XML is the one true Microduck model?

It is:

> Which model variant matches the behavior being trained or tested?

## Scene files

The repository also contains `scene*.xml` files. These wrap robot models with environment elements such as:

- a floor;
- initial poses / keyframes;
- stand, sit, or folded configurations;
- convenient setup for visualization and `infer_policy.py`.

A scene file is therefore not the same thing as the reusable robot body model itself.

## Mesh assets

The public model assets include visual geometry for many robot parts, including body shells, legs, feet, head/neck structures, beak-related parts, motor-like geometry, battery/board placeholders, and roller attachments.

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

The upstream README states that the MJCF robot models are exported from Onshape using `onshape-to-robot`, with `config_mjcf_*.json` files associated with model generation.

This provenance is useful because it distinguishes:

- upstream-generated simulation geometry;
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
- https://github.com/pollen-robotics/microduck_rl/blob/develop/README.md

## Related pages

- [Mechanical structure and kinematics](../hardware/mechanical-structure.md)
- [Simulation and reinforcement learning](model-and-rl.md)
- [Reproducible training and ONNX export](reproducible-training-and-export.md)
- [Provenance and licensing](../legal/provenance-and-licenses.md)
