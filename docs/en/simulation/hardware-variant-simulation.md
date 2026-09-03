# Hardware Variant Simulation: Keep the Software, Change the Physical Robot

**English** | [简体中文](../../zh-CN/simulation/hardware-variant-simulation.md)

> Public-source status checked: **2026-09-03**.
>
> This page explains how the public Microduck simulation work can be used to study a hardware-compatible variant: keep the Microduck software and joint contract, while changing actuator and mechanical parameters in MuJoCo.

## 1. The idea in one minute

For a beginner, the important distinction is:

```text
Normal RL simulation
training code ──> MuJoCo robot

Hardware-variant software-in-the-loop study
real Microduck control stack (`robotd`)
              │
              │ RobotIo / TCP boundary
              ▼
      MuJoCo robot model
              │
              ├─ actuator dynamics
              ├─ mass / center of mass / inertia
              ├─ geometry / collision
              ├─ friction / contact
              └─ backlash and related mechanics
```

The second arrangement is useful because the software above the hardware-I/O boundary does not need to know whether the body is on a desk or inside MuJoCo.

A compatible research variant can therefore keep the Microduck software contract while changing the physical model underneath it.

## 2. What is public upstream today?

There are two halves, and their maturity is different.

### Merged in `microduck_rl/develop`

At commit `29e887ecfbf5d37144759e5a9f8a176dfb83d547`, the official public `pollen-robotics/microduck_rl` repository contains `duck-body` in:

```text
src/mjlab_microduck/sim/body_server.py
```

It serves a MuJoCo Microduck body over TCP. The command accepts a custom scene path:

```bash
uv run duck-body --scene path/to/scene.xml
```

The body server finds actuators by joint name rather than relying on raw MuJoCo index order. This is important because editing an MJCF file can silently reorder model objects.

**Evidence level:** official public repository, merged into `develop`.

### Public upstream branch, not `microduck/main`

The matching daemon-side work currently lives on the official public branch:

```text
pollen-robotics/microduck: sim-remote-io
```

That branch adds:

```bash
robotd --sim HOST:PORT
```

and a `RemoteIo` implementation behind the same `RobotIo` boundary used by the control stack.

The upstream design document states that everything above `RobotIo` is intended to remain the real code path: the 50 Hz loop, ONNX policies, safety, fall detection, odometry, kinematics, IPC calls, `robotctl`, and related runtime behavior.

**Evidence level:** official public upstream experimental branch; **not merged into `main` as of 2026-09-03**.

This distinction matters. The concept is publicly implemented and usable for research, but the daemon-side interface should not yet be treated as a stable released feature.

## 3. Can the MuJoCo body be changed?

Yes, within the compatibility boundary.

The merged `duck-body` command has a `--scene` argument, so a researcher can point it at another MuJoCo scene instead of being limited to the default official scene.

For the most direct path, the modified model should still behave like a Microduck from the software's point of view.

Keep these contracts stable:

- Microduck joint topology and joint naming used by the wire contract;
- the 14 policy-controlled leg/neck/head joints;
- the existing mouth/beak convention on the 15-joint wire list;
- actuator names corresponding to the expected Microduck joints;
- the `trunk_base_freejoint` expected by the body server;
- the `tof` site if using the current body-server sensor placement;
- the policy interface when reusing the current alpha policies: **61-D observation → 14-D action at 50 Hz**.

In other words, changing the physical implementation is much easier than changing the robot's software-visible skeleton.

## 4. What should change when an actuator changes?

A servo substitution is not only a torque-number edit.

A physically meaningful model may need updates in several groups.

### Actuator dynamics

Possible changes include:

- torque / force capability;
- speed response;
- position-control response;
- friction and stiction;
- back-EMF-related behavior;
- voltage dependence and load sag behavior;
- command delay;
- backlash;
- reflected inertia / armature;
- joint limits or usable travel, when mechanically different.

### Mass properties

Changing an actuator or its mounting can change:

- link mass;
- center of mass;
- inertia tensor;
- total robot mass distribution.

A robot with the same outer shape can still balance differently if these values move.

### Mechanical geometry

A different actuator package may require changes to:

- brackets or supports;
- shell clearances;
- link geometry;
- collision geometry;
- actuator location relative to the joint axis.

### Contact and materials

Mechanical changes can also require revisiting:

- sole/contact friction;
- body-contact friction;
- contact geometry;
- damping/compliance approximations;
- flexible or soft-part assumptions where relevant.

## 5. The XL330 assumption that must not be missed

The current upstream simulation is not a generic servo simulator.

The official RL stack uses BAM actuator behavior fitted for the Dynamixel XL330 family. The body-server code also treats the daemon's firmware gain value around `kp = 200` as a reference and scales the MuJoCo actuator gain relative to that value.

That means this is **not** enough:

```text
old servo torque = A
new servo torque = B
change only A -> B
```

If the new actuator has a materially different response, a simulation that keeps the XL330-fitted dynamics may still behave like an XL330 with a changed number.

For a credible hardware-variant study, the actuator model should be replaced, fitted, or otherwise calibrated to public measurements for the actuator being studied. If no trustworthy measurements exist, the uncertainty should be stated rather than hidden.

## 6. What this setup can test

When the daemon-side public branch and the MuJoCo body are used together, the setup can exercise the real software path above `RobotIo` against modified physics.

Useful questions include:

- Does the same policy remain stable with the modified actuator response?
- Does joint tracking become slower or more oscillatory?
- Does the robot fall more often during walking, standing, sit/stand, or recovery?
- Do changed mass and inertia values alter balance or recovery behavior?
- Do geometry changes introduce collisions that were absent in the baseline model?
- Does backlash or friction change foot placement and odometry behavior?
- Does a software safety path react correctly when the simulated body behaves badly?

Useful comparison metrics can include:

- task success rate;
- episode survival / fall rate;
- body tilt;
- joint tracking error;
- actuator saturation or force demand in the model;
- foot slip;
- unwanted body contacts;
- recovery time;
- trajectory or odometry error when a task exposes ground truth.

The strongest experiment changes one documented model assumption at a time and compares it against a pinned baseline.

## 7. What it does **not** test

The upstream simulation design is explicit about its boundary.

The twin does not make the real hardware drivers virtual. In particular, the public design lists items such as these outside the twin boundary:

- the real Dynamixel bus driver;
- physical bus errors and dropped packets;
- the real servo encoder;
- hardware thermals;
- the real battery system;
- hardware-specific camera / ISP / NPU paths.

Therefore, a custom MuJoCo actuator model can test **physical/control behavior above `RobotIo`**, but it does not prove that a different electrical servo protocol, firmware register map, bus timing, or hardware driver will work on a real board.

That is a separate hardware bring-up problem.

## 8. Beginner workflow

A simple, reproducible study can follow this order:

```text
1. Pin the upstream commits
        ↓
2. Run the official model as the baseline
        ↓
3. Copy the scene/model for a hardware variant
        ↓
4. Change actuator + dependent physical parameters
        ↓
5. Keep the software-visible Microduck contract unchanged
        ↓
6. Run the same policy / command sequence
        ↓
7. Compare objective metrics
        ↓
8. Record what was measured, inferred, or still unknown
```

Do not start by changing many unrelated parameters at once. If the result becomes worse, it should still be possible to identify why.

## 9. A useful file split

A public research project can keep variants understandable by separating the baseline from modified models, for example:

```text
models/
├── upstream-baseline/
└── actuator-variant-example/
    ├── scene.xml
    ├── robot.xml
    ├── actuator-parameters.md
    └── provenance.md
```

The important part is not the exact directory names. The important part is that every changed value can be traced to a public source, public measurement, or clearly labeled assumption.

## 10. Evidence labels recommended for results

Use explicit labels:

| Label | Meaning |
|---|---|
| **Official source** | directly present in an official public Pollen Robotics repository/page |
| **Public measurement** | measurement published with enough method/context to evaluate it |
| **Community result** | public third-party experiment or reconstruction |
| **Derived** | calculated from public inputs |
| **Assumption** | value chosen for simulation because evidence is incomplete |
| **Unconfirmed** | not enough evidence yet |

A successful MuJoCo run should be described as a **simulation result**, not as proof of real-hardware equivalence.

## 11. Current upstream details worth remembering

As of the 2026-09-03 snapshot:

- `microduck_rl/develop` includes the `duck-body` server and accepts `--scene`;
- the body is addressed by Microduck joint names;
- the current actuator baseline is still XL330/BAM-oriented;
- the daemon-side `robotd --sim` path is public on `sim-remote-io`, not yet on `microduck/main`;
- the latest model re-export renamed the older curated `allcollisions` role to `groundcontact` and introduced a new true `robot_allcollisions.xml` model where every part can carry collision geometry;
- the upstream ToF simulator recently fixed a left/right column convention error, demonstrating why sensor frames and coordinate conventions are part of simulation fidelity too.

## Primary public sources

- https://github.com/pollen-robotics/microduck_rl
  - `src/mjlab_microduck/sim/body_server.py`
  - `src/mjlab_microduck/robot/microduck/`
- https://github.com/pollen-robotics/microduck/tree/sim-remote-io
  - `robotd/src/main.rs`
  - `docs/design/simulation.md`
- https://github.com/Rhoban/bam

## Related OpenMicroDuck pages

- [Simulation and Reinforcement Learning](model-and-rl.md)
- [Sim-to-Real Parameter Reference](sim-to-real-parameter-reference.md)
- [Simulation Model Assets Reference](model-assets-reference.md)
- [`robotd` Hardware Protocol](../software/robotd-hardware-protocol.md)
- [Hardware Bring-up and Calibration](../getting-started/hardware-bringup-and-calibration.md)
- [Upstream Version Matrix](../upstream/version-matrix.md)
