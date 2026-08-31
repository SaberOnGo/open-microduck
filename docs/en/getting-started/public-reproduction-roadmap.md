# Public Reproduction Roadmap

**English** | [简体中文](../../zh-CN/getting-started/public-reproduction-roadmap.md)

> This is a public research roadmap built from public Microduck sources. It is not an official Pollen Robotics build manual and does not claim that unpublished production hardware has been reconstructed.

## The short version

Do not treat “reproduce Microduck” as one task.

A practical public research path is:

```text
Stage 0  Pin the upstream versions
Stage 1  Run official model + official ONNX in simulation
Stage 2  Reproduce one training task
Stage 3  Build a parameter/evidence map
Stage 4  Test the servo/control bus on a small bench
Stage 5  Test IMU + control timing
Stage 6  Validate mechanical subassemblies
Stage 7  Assemble a full research robot
Stage 8  Compare simulation and hardware
```

Each stage should have a clear pass/fail result before the next one begins.

## Stage 0 — freeze a reference snapshot

Record:

- `microduck` commit;
- `microduck_rl` commit;
- BAM commit;
- product/press-page check date.

Why: official development is active. A camera path, policy, model, gain or randomization range can change while a third-party project is still being built.

**Output:** a reproducible source snapshot.

## Stage 1 — make the official robot move in simulation

Use the official MJCF and already-trained ONNX policies.

Do **not** modify geometry or train a new policy yet.

Verify:

- model loads;
- policy loads;
- 61-D observation / 14-D action contract works;
- joint ordering is understood;
- walking/standing behavior is plausible.

See [Simulation First](simulation-first.md).

**Hardware required:** none.

**Output:** known-good software baseline.

## Stage 2 — reproduce one official training task

Start with the Flat Velocity task.

First run the official 64-env / 5-iteration smoke test, then a normal training run. Export through the official exporter and validate the exported ONNX in CPU MuJoCo.

The objective is not to improve the policy yet. It is to understand the full chain:

```text
MJCF → environment → PPO checkpoint → exporter → ONNX → inference
```

**Hardware required:** none.

**Output:** independently reproduced training/deployment pipeline.

## Stage 3 — make a parameter map before buying a full robot

Create a table for every important parameter with these columns:

```text
parameter
value
unit
source
source commit
status/evidence level
what it affects
```

The OpenMicroDuck [Hardware parameter reference](../hardware/parameter-reference.md) and [Sim-to-real parameter reference](../simulation/sim-to-real-parameter-reference.md) provide the starting point.

At this stage, explicitly mark unknowns. An unresolved connector, fastener or PCB detail is better than a guessed “final BOM.”

**Hardware required:** none.

**Output:** public evidence-backed parameter baseline.

## Stage 4 — servo/control-bus bench

Before a 15-axis structure exists, validate the electrical/control assumptions with a small bench.

The public runtime gives a very concrete reference:

- Dynamixel-compatible bus;
- 1 Mbps;
- current runtime IDs are known;
- startup corrects important EEPROM registers;
- target control rate is 50 Hz;
- Runtime P gain defaults to 200;
- one combined state read and one target write are performed per control tick.

A small bench can answer basic questions such as:

- is the serial interface correct?
- are read/write timing and packet handling understood?
- do position/velocity/voltage readings match expected units?
- can target positions be commanded safely?

This stage is about **protocol and timing**, not walking.

**Hardware required:** only the minimum public-compatible actuator/interface setup needed for the chosen experiment; a complete robot is unnecessary.

**Output:** verified actuator/control-bus implementation.

## Stage 5 — IMU and synchronized state bench

The current official runtime reads an `imu_to_dxl` v2 board at Dynamixel ID 200 on the same bus transaction family as the servos.

Important public details include:

- LSM6DSV16X;
- gyro + SFLP quaternion data;
- 12-byte runtime block;
- gyro ±500 dps format;
- 17.5 mdps/LSB scale;
- sensor-to-trunk orientation handling;
- filtering/rejection behavior in the runtime.

A third-party research build does not have to copy an unpublished PCB layout to reproduce the **observable software contract**. The first goal is to reproduce equivalent state information and timing.

**Output:** joint state + orientation data that matches the policy/runtime expectations.

## Stage 6 — mechanical subassemblies, not the full shell at once

Break mechanics into independently inspectable chains:

```text
left leg
right leg
neck/head linkage
trunk / battery / electronics volume
feet / soles
optional rollers
```

Use the official MJCF for:

- joint parent/child relationships;
- joint axes and ranges;
- body transforms;
- simulation mass/inertia;
- collision geometry;
- mesh placement.

Use community reconstruction only where it is clearly labeled, for example M2-class hole analysis and bearing geometry.

Do not assume the released simulation meshes contain final production threads, tolerances, inserts or wire routing.

**Output:** mechanically consistent subassemblies whose axes and geometry match the public model closely enough for simulation comparison.

## Stage 7 — complete research assembly

Only after the previous stages are understood should the full system be combined:

```text
compute
 + motor bus
 + IMU
 + power
 + 15 motors
 + structure
 + runtime
 + ONNX policies
```

Camera, ToF, NFC and audio are useful Microduck features, but they are not required to prove the core 14-action locomotion loop. They can be integrated as separate subsystems rather than blocking first locomotion.

This distinction is important: **walking should not depend on finishing every accessory.**

## Stage 8 — sim-to-real comparison

Now compare simulation and hardware one variable at a time.

Useful categories include:

- home pose and joint zero offsets;
- joint position response;
- command delay;
- backlash;
- friction;
- battery voltage / voltage sag;
- IMU orientation error;
- encoder bias;
- body mass / CoM;
- sole contact/friction;
- control-loop timing.

Do not immediately “tune until it walks.” Record which mismatch is being changed and what measurement supports the change.

## What can be postponed?

For first locomotion research, these can usually be treated as separate tracks:

- camera streaming;
- ToF applications;
- NFC;
- audio/voice;
- WebRTC remote media;
- final cosmetic shell fidelity;
- roller accessories.

The core locomotion dependency chain is much smaller:

```text
mechanics
 + 14 locomotion joints
 + joint state
 + IMU orientation/rate
 + 50 Hz runtime
 + correct policy interface
```

## What should never be guessed silently?

Keep these explicitly unresolved until public evidence or reproducible measurement exists:

- production PCB schematic/BOM;
- final wiring harness details;
- exact production fastener lengths/counts;
- undocumented manufacturing tolerances;
- exact production part variants when upstream only identifies a family;
- values copied from another robot revision.

## Recommended project folders for a third-party public study

A clear research project can separate evidence from implementation:

```text
research/
├── sources/          # public links, commits, licenses
├── parameters/       # evidence-backed tables
├── simulation/       # model/policy experiments
├── hardware-tests/   # reproducible bench measurements
├── mechanics/        # public-model-derived reconstruction notes
└── reports/          # results and unresolved questions
```

This prevents a temporary implementation choice from becoming “the Microduck specification.”

## Next pages

- [Hardware parameter reference](../hardware/parameter-reference.md)
- [Structure and assembly map](../hardware/structure-and-assembly-map.md)
- [Sim-to-real parameter reference](../simulation/sim-to-real-parameter-reference.md)
- [Open questions and source conflicts](../research/open-questions-and-conflicts.md)
