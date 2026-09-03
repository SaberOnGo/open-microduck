# Simulation and Reinforcement Learning

> Primary reference: the official `pollen-robotics/microduck_rl` repository.
>
> Core upstream status checked: **2026-09-03**.

## Official training stack

Microduck policies are trained in simulation and exported to the onboard runtime. The current official RL repository uses:

- **mjlab**;
- **MuJoCo / MuJoCo Warp** physics;
- **PPO**;
- **BAM** actuator modeling for Dynamixel XL330;
- domain randomization and system-model uncertainty;
- ONNX export for deployment.

The policies run at **50 Hz**, matching the onboard control loop.

## Shared deployment contract

The current alpha policy family uses a shared contract:

```text
actor observation: 61 dimensions
policy action:      14 dimensions
control rate:       50 Hz
```

The 61-D observation contains 48 proprioceptive values plus a 13-D command block:

```text
base angular velocity      3
projected gravity          3
joint position            14
joint velocity            14
previous actions          14
----------------------------
proprioception            48

twist command              3
head-pose command           4
body-pose command           6
----------------------------
command block              13

total                     61
```

The action vector controls the 14 leg/neck/head joints; the beak/mouth motor is outside the policy action vector.

## Task families in the official RL repository

At the time of this source sweep, the official environment registry includes families for:

- velocity-command walking;
- walking plus fall recovery;
- stand-up / recovery;
- sit ↔ stand;
- ground pick / beak-to-ground behavior;
- ball kicking;
- forward roll (`roulade`);
- roller locomotion;
- roller crouch/glide;
- slope/roller tasks;
- additional roller skills such as stand-up/spin.

The live environment registry in the upstream repository should be treated as authoritative because task names and variants can change.

## Robot model variants

The official MJCF assets include several model purposes rather than one universal XML.

A 2026-09-02 upstream re-export corrected an old naming problem: the previous curated `allcollisions` role was renamed to `groundcontact`, and a new true `robot_allcollisions.xml` was added.

| Model family | Purpose |
|---|---|
| `robot_walk.xml` | walking-oriented model with reduced body collision scope |
| `robot_groundcontact.xml` | curated collision set for ground-contact tasks |
| `robot_groundcontact_rollers.xml` | ground-contact model with passive roller mechanics |
| `robot_allcollisions.xml` | true all-part collision variant for collision inspection and experiments |
| `*_backlash.xml` | generated variants with passive backlash hinges |

This distinction matters: a model optimized for gait training may intentionally omit contacts that are required for lying on the ground or inspecting full-body collisions.

See [Simulation Model Assets Reference](model-assets-reference.md) for the current file map and the naming change.

## Actuator model: why BAM matters

The upstream project explicitly treats actuator fidelity as a major part of the sim-to-real gap. Instead of using an ideal torque source or a generic PD actuator, the training stack uses Rhoban's **BAM** model for the Dynamixel XL330 family.

The public RL documentation describes modeling of effects including:

- voltage control behavior;
- back-EMF;
- Coulomb/Stribeck/load-dependent friction;
- battery voltage variation;
- voltage sag under load;
- command delay;
- friction randomization.

This is a useful reminder that sim-to-real is not only about accurate robot geometry. For a light robot driven by small servos, motor/control behavior can dominate transfer quality.

## Backlash modeling

The official RL repository has explicit **Backlash** task variants. Each controlled servo joint receives a passive hinge representing gear play.

A particularly important detail is encoder placement in the model: the observation and firmware-PD emulation read through the backlash so the virtual encoder corresponds to the output side of the play. The network interface remains 61 observations / 14 actions.

This is more realistic than simply adding random noise to commanded positions because mechanical play changes the relationship between motor-side motion and observed output motion.

## Domain randomization

The upstream sim-to-real recipe randomizes or varies parameters such as:

- battery voltage and load sag;
- friction;
- command/observation timing effects;
- masses / centers of mass / inertia-related properties;
- contact/sole friction;
- disturbances/pushes;
- encoder-related offsets or errors;
- actuator response variation.

The exact ranges belong to the active upstream configuration. They should be read from the relevant environment files rather than copied permanently into a summary that may become stale.

## Software-in-the-loop body simulation

The official public `microduck_rl/develop` branch now contains a `duck-body` process that serves a MuJoCo body over TCP. It accepts a custom scene path:

```bash
uv run duck-body --scene path/to/scene.xml
```

This is important because the MuJoCo body is no longer useful only as a training environment: it can also be placed behind the same hardware-I/O boundary used by the real control stack.

The matching daemon-side implementation currently lives on the official public `pollen-robotics/microduck` branch `sim-remote-io`, where `robotd --sim HOST:PORT` uses a remote `RobotIo` implementation.

As of **2026-09-03**, that daemon-side work is **not merged into `microduck/main`**. It should therefore be described as an official public upstream experimental path, not a stable released feature.

For a beginner-friendly explanation of what can be changed while preserving the Microduck software contract, see [Hardware Variant Simulation](hardware-variant-simulation.md).

## Export to ONNX

The official export path bakes observation normalization into the ONNX graph. The runtime expects the exported network contract rather than an arbitrary conversion of a training checkpoint.

That distinction is essential for reproducibility:

```text
checkpoint + training normalizer
            ↓ official export
       deployable ONNX
            ↓
        robot runtime
```

A network with the same weights but different input normalization behaves as a different controller.

## Sim-to-real validation

The upstream repository includes tools to replay exported policies in CPU MuJoCo and compare trajectories/data. Public documentation also emphasizes preserving training-time filters and runtime action processing, because a policy can fail on hardware if the deployment path changes seemingly small parameters that were part of training.

Recent upstream work is another reminder that fidelity includes conventions, not only numeric parameters: the simulated ToF sensor had its left/right column convention reversed relative to the real processing path, which produced mirrored mapping until corrected.

## Public simulator ecosystem

The Microduck ecosystem already contains several independent ports and simulators. They are useful for experimentation but should not all be treated as bit-for-bit equivalents of the official mjlab baseline.

Examples include:

- browser MuJoCo/WASM + ONNX Runtime Web simulator;
- Isaac Lab / Newton MJWarp port;
- Genesis port for AMD/ROCm-oriented training;
- MJX/JAX/Brax reimplementation;
- Swift model/policy implementation.

See [../ecosystem/reverse-engineering-projects.md](../ecosystem/reverse-engineering-projects.md) for status and caveats.

## Primary sources

- https://github.com/pollen-robotics/microduck_rl
- https://github.com/pollen-robotics/microduck
- https://github.com/pollen-robotics/microduck/tree/sim-remote-io
- https://github.com/Rhoban/bam

## Related OpenMicroDuck pages

- [Hardware Variant Simulation](hardware-variant-simulation.md)
- [Simulation Model Assets Reference](model-assets-reference.md)
- [Sim-to-Real Parameter Reference](sim-to-real-parameter-reference.md)
- [Mechanical structure](../hardware/mechanical-structure.md)
- [Electronics and buses](../hardware/electronics-and-buses.md)
- [Runtime architecture](../software/runtime-architecture.md)
