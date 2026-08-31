# Sim-to-Real Parameter Reference

**English** | [简体中文](../../zh-CN/simulation/sim-to-real-parameter-reference.md)

> Snapshot-oriented reference for the official public Microduck RL stack. These values are version-sensitive and should always be read together with the upstream commit.

Pinned RL commit used here: `d424a0c899f6b33cbd3daeb279913134349c0b63`.

## 1. What “sim-to-real parameters” means

A policy does not transfer because the 3D shape looks similar.

The complete chain is closer to:

```text
geometry / mass / inertia
        +
contacts / sole friction
        +
servo voltage / friction / delay / backlash
        +
IMU + encoder error
        +
50 Hz observation/action contract
        +
runtime action processing
        ↓
        real motion
```

For Microduck, actuator and timing fidelity are especially important because the robot is light and uses small servos.

## 2. Canonical actuator model in the current RL stack

The current official config uses BAM through `FrictionDRBamActuatorCfg`.

| Parameter | Current public value | Meaning |
|---|---:|---|
| motor name | `xl330` | actuator family label used by BAM integration |
| BAM model | `m6` | current fitted actuator model selection |
| firmware position gain | `kp_fw = 200` | matches Microduck's preserved firmware stiffness in the simulation actuator |
| battery voltage sample | **6.5–8.2 V** | per-environment input-voltage randomization |
| voltage sag gain | **0.0–0.2** | load-dependent voltage-drop gain |
| effective voltage floor | **6.0 V** | minimum after sag |
| command delay | **3–6 lag steps** | per-environment action/command delay model |
| target joints | 14 non-`passive_*` joints | passive wheels/backlash joints are excluded |
| soft joint-position limit factor | **0.9** | articulation safety/soft-limit factor in current cfg |

Source: `src/mjlab_microduck/robot/microduck_constants.py`.

### Do not confuse `kp_fw=200` with arbitrary MJCF `kp` values

The repository contains older/default XML actuator classes and fitted historical parameters. The active Microduck RL configuration wraps the robot with BAM.

Therefore:

```text
runtime servo P gain
BAM firmware gain
raw MJCF position-actuator kp
```

are different layers. Comparing their numbers without understanding the layer is misleading.

## 3. What BAM adds beyond an ideal PD actuator

The official Microduck project uses BAM specifically to model effects that simple position control misses, including:

- voltage-control behavior;
- back-EMF;
- Coulomb friction;
- Stribeck/stiction behavior;
- load-dependent friction;
- battery voltage variation;
- voltage sag under load;
- command delay.

The Microduck wrapper also adds per-environment friction scaling.

A crucial implementation detail from the public code:

> Under BAM, MuJoCo `dof_frictionloss` is zeroed for this purpose. Randomizing the stock MuJoCo friction-loss field would therefore be a silent no-op. The Microduck code scales BAM's own friction budget instead.

This is exactly the kind of detail that can make two simulations look “configured similarly” while actually behaving differently.

## 4. Backlash model

Current official Backlash variants insert an unactuated hinge in series with every one of the 14 controlled servo joints:

```text
±1° play per joint
= 2° total dead zone
```

The additional joints are named like:

```text
passive_<joint>_backlash
```

The important part is the encoder model.

The official `BacklashEncoderBamActuator` makes the simulated firmware position loop read:

```text
servo joint position + backlash joint position
```

because the real servo encoder is treated as being on the output side of the play.

That is more realistic than simply adding random noise to joint angles.

## 5. Walking-task domain randomization switches

In the pinned `microduck_velocity_env_cfg.py` snapshot:

| Randomization | Enabled? |
|---|---|
| trunk CoM | yes |
| head-assembly CoM | yes |
| kP | no |
| kD | no |
| mass + inertia | yes |
| BAM joint-friction magnitude | yes |
| joint damping | no |
| armature / reflected rotor inertia | yes |
| external velocity pushes | yes |
| IMU orientation | yes |
| encoder bias | yes |
| initial base orientation | no |

This table is useful because a range can exist in source while the corresponding toggle is currently disabled.

## 6. Domain-randomization numeric ranges

| Parameter | Current range | Notes |
|---|---:|---|
| trunk CoM | **±3 mm initially**, curriculum can expand to about **±8 mm** | enabled |
| head CoM | **±3 mm initially** | enabled; expanded through curriculum behavior |
| mass + inertia scale | **0.95–1.05×** | both scaled together; enabled |
| kP scale | 0.85–1.15× | range exists but toggle currently disabled |
| kD scale | 0.9–1.1× | disabled |
| BAM friction scale | **0.9–1.1×** | enabled |
| joint damping scale | 0.9–1.1× | disabled |
| armature scale | **0.9–1.1×** | enabled |
| velocity-push interval | **3–6 s** | enabled |
| velocity push | **−0.3 to +0.3 m/s** | additive disturbance |
| IMU mounting error | **up to 6° random-axis** | enabled |
| encoder bias | **−0.015 to +0.015 rad** ≈ **±0.86°** | constant per environment; enabled |
| initial base pitch | up to ±10° | configured but initial-orientation randomization disabled |
| initial base roll | up to ±5° | configured but disabled |

These values are excellent starting points for public reproduction because they reveal what uncertainty the official team considers important enough to train against.

They are **not measured tolerance specifications for production hardware**.

## 7. Observation/sensor uncertainty

The current policy family uses projected gravity rather than feeding a raw accelerometer vector directly in the main actor contract.

Two notable randomized sensor errors are:

### IMU mounting error

Up to **6°** around a random axis.

The source comments distinguish this from a fixed systematic pitch bias: a known fixed mounting bias should be corrected at the source/runtime rather than treated only as random noise.

### Encoder bias

Each environment can receive a constant per-joint offset in:

```text
[-0.015, +0.015] rad
≈ ±0.86°
```

This approximates joint encoder/calibration error and forces the policy not to depend on perfect zero calibration.

## 8. External disturbances

Walking training currently applies velocity pushes every **3–6 seconds** with an additive velocity change in approximately:

```text
-0.3 to +0.3 m/s
```

The source comments explain that a previous larger ±0.5 m/s disturbance was too severe relative to the robot's walking speed and encouraged an overly nervous recovery gait.

This is a useful RL lesson: “more randomization” is not automatically better.

## 9. Rough-terrain parameters

The Microduck rough-terrain generator is intentionally small-scale.

Base patch settings:

```text
patch size: 8 × 8 m
border width: 20 m
rows: 10
columns: 20
```

Terrain mixture in the pinned walking config:

| Terrain | Proportion | Current parameters |
|---|---:|---|
| flat | 25% | flat |
| pyramid stairs | 25% | step height 0–15 mm; step width 0.15 m; platform 2 m |
| random grid | 30% | cell width 0.45 m; height 0–10 mm; platform 1.5 m |
| pyramid slope | 20% | slope 0.03–0.10 ≈ 1.7°–5.7°; platform 2 m; vertical scale 1 mm |

The source explicitly notes that Microduck can only lift its feet on the order of centimeters, so generic large-robot terrain defaults are inappropriate.

### Rough-terrain contact softening

The current config softens terrain contacts to reduce edge-induced instability:

```text
solref = [0.04, 1.0]
solimp = [0.85, 0.95, 0.001, 0.5, 2.0]
```

This is a simulation-stability parameter, not a physical floor material specification.

## 10. Foot contact / friction baseline

The current robot config assigns the left/right foot collision geoms a friction coefficient tuple beginning at:

```text
1.0
```

This is a simulation contact setting. A real reproduction should measure or characterize the actual sole/surface pair rather than assuming “1.0” is a material datasheet value.

## 11. Pose-reward widths used by the walking task

These are RL reward-shaping parameters, **not mechanical tolerances**.

### Standing pose standard deviations

| Joint group | std |
|---|---:|
| hip yaw | 0.10 rad |
| hip roll | 0.05 rad |
| hip pitch | 0.15 rad |
| knee | 0.15 rad |
| ankle | 0.10 rad |

### Walking pose standard deviations

| Joint group | std |
|---|---:|
| hip yaw | 0.30 rad |
| hip roll | 0.05 rad |
| hip pitch | 0.40 rad |
| knee | 0.40 rad |
| ankle | 0.25 rad |

They show which joint deviations the current reward design tolerates more during gait, but they should not be copied into a servo limit table.

## 12. Training timebase

The current walking environment defines:

```text
NUM_STEPS_PER_ENV = 24
policy/control rate = 50 Hz
```

The official `AGENTS.md` explains curricula in terms of environment steps and strongly recommends a small smoke test first:

```bash
uv run train Mjlab-Velocity-Flat-MicroDuck \
  --env.scene.num-envs 64 \
  --agent.max_iterations 5
```

A normal quickstart then uses 4096 environments.

## 13. Runtime-side parameters that must match deployment

The pinned `microduck` runtime configuration includes important controller-side defaults such as:

| Runtime parameter | Walking default / current note |
|---|---:|
| control rate | 50 Hz |
| action scale | 0.9 |
| position gain | 200 |
| standing action scale | 1.0 |
| standing gain ratio | 0.8 |
| head target low-pass | 0.5 for the vendored alpha configuration |
| leg target low-pass | 0.7 for the vendored alpha configuration |
| voltage adaptation | off by default |
| nominal voltage for optional adaptation | 7.4 V |
| deadman timeout | 500 ms |

These values belong to the **runtime execution layer**. They are not all training-domain randomization parameters.

## 14. Important source conflict: action low-pass

This is a version-sensitive point and should not be simplified.

### Pinned runtime configuration says

The vendored alpha walking configuration uses first-order low-pass factors:

```text
head: 0.5
legs: 0.7
```

and the runtime comments say those alpha policies were trained with matching filtering.

### Current pinned `microduck_rl/develop` guidance says

`AGENTS.md` states:

> policies are unfiltered in training; do not add EMA filtering without a matched runtime flag and transfer test.

### Correct OpenMicroDuck interpretation

Do **not** conclude globally that “Microduck policies are filtered” or “Microduck policies are never filtered.”

Instead:

```text
policy artifact + training revision + runtime processing
must be treated as one matched set
```

The vendored alpha policy lineage and the current development training guidance are not safe to mix silently.

For a reproduction, record whether filtering exists in **both** training and deployment.

## 15. Runtime battery behavior versus training voltage randomization

These are related but not identical layers:

### Real runtime

Usable battery mapping:

```text
8.2 V full-under-load
6.6 V empty-under-load
```

Optional runtime action voltage adaptation is off by default in the pinned config.

### Training actuator model

BAM samples environment voltage over:

```text
6.5–8.2 V
```

and additionally models load-dependent voltage sag with an effective floor of 6.0 V.

The overlap is intentional: the policy is trained across a range that covers the real robot's useful loaded battery span and some sag behavior.

## 16. What should be measured on real hardware later?

The public simulation gives hypotheses. Physical research should eventually measure:

- command-to-motion latency;
- servo position step/trajectory response at different voltages;
- actual backlash distribution by joint;
- static/dynamic friction behavior;
- bus latency/error rate at 50 Hz;
- loaded battery sag during walking/recovery;
- joint zero/calibration offsets;
- IMU mounting/orientation residual error;
- body/link masses and CoM where practical;
- sole-ground friction/contact behavior.

A measured value should not replace the official simulation value silently. Keep both, with conditions and revision.

## 17. Minimum parameter set to preserve before changing geometry

If a third-party model is being adapted, preserve at least:

```text
50 Hz
14-action order
61-D observation order
HOME_FRAME
joint axes and sign convention
BAM actuator model or an explicitly validated equivalent
voltage range/sag model
command delay
friction randomization
mass/inertia distribution
IMU orientation convention
encoder bias handling
foot contact geometry
```

Changing many of these at once destroys the usefulness of the official policy as a baseline.

## Primary official sources

- `pollen-robotics/microduck_rl`
  - `src/mjlab_microduck/robot/microduck_constants.py`
  - `src/mjlab_microduck/actuator/friction_dr_bam.py`
  - `src/mjlab_microduck/tasks/microduck_velocity_env_cfg.py`
  - `AGENTS.md`
- `pollen-robotics/microduck`
  - `deploy/robotd.toml`
  - `duck-control/src/model.rs`
  - `duck-control/src/bus.rs`
  - `duck-control/src/imu.rs`
- `Rhoban/bam`

## Related pages

- [Simulation First](../getting-started/simulation-first.md)
- [Reproducible training and ONNX export](reproducible-training-and-export.md)
- [Hardware parameter reference](../hardware/parameter-reference.md)
- [Control loop and sensor dataflow](../software/control-loop-and-sensor-dataflow.md)
