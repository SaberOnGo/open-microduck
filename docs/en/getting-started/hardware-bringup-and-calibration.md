# Hardware Bring-up and Calibration

**English** | [简体中文](../../zh-CN/getting-started/hardware-bringup-and-calibration.md)

> This is a **public research bring-up method**, not an official Microduck manufacturing procedure. Official source values are labeled separately from recommended validation steps.

## The goal

Do not assemble a full robot and then ask why it falls.

Bring the system up in layers:

```text
power
  ↓
serial bus
  ↓
one servo
  ↓
all servo IDs
  ↓
IMU
  ↓
50 Hz state loop
  ↓
joint zero / home pose
  ↓
head + ToF / camera orientation
  ↓
stand safely
  ↓
walking policy
```

If one layer fails, stop there. This keeps electrical, mechanical and RL problems separate.

## Stage 1 — Power only

Before commanding motion, verify:

- supply polarity and expected voltage range;
- no unexpected heating;
- the compute board boots reliably;
- the servo bus voltage is visible where expected.

The current official runtime maps roughly **8.2 V = full** and **6.6 V = empty-for-robot-operation under load**. This is a runtime operating map, not a complete battery-cell specification.

## Stage 2 — Bring up one servo first

Use one known servo before connecting the whole chain.

Check:

1. the device answers;
2. its ID can be read;
3. position can be read;
4. a very small safe position change can be commanded;
5. the reported position changes in the expected direction;
6. voltage and temperature readings are plausible.

This verifies the physical bus, protocol and direction assumptions before 15 devices are involved.

## Stage 3 — Verify all public runtime IDs

The current public runtime maps:

```text
right leg       10 11 12 13 14
left leg        20 21 22 23 24
head / mouth    30 31 32 33 34
IMU bridge      200
```

A reproduction should scan and record what actually answers instead of assuming wiring is correct.

A useful pass/fail table is:

| Check | Pass condition |
|---|---|
| expected ID present | device answers repeatedly |
| duplicate ID | none |
| position read | stable and plausible |
| temperature | plausible at rest |
| voltage | close to bus voltage |
| communication errors | low enough for stable 50 Hz operation |

## Stage 4 — Match the bus settings

Current official runtime values include:

- serial port on the Radxa reference path: `/dev/ttyS2`;
- baud rate: **1,000,000 bit/s**;
- control period: **20 ms**;
- control frequency: **50 Hz**;
- bus timeout: **30 ms**;
- expected startup EEPROM values include `return_delay_time = 0`, baud code for 1 Mbps, `pwm_slope = 255`, and `shutdown = 52` in the pinned source snapshot.

The important practical point is that factory return delay can consume a large fraction of a 20 ms control tick when many devices share the bus. Verify configuration rather than assuming factory defaults are suitable.

## Stage 5 — Verify the IMU before enabling a policy

The current public control IMU path uses `imu_to_dxl` ID **200** with an ST **LSM6DSV16X**.

Before standing the robot, verify:

- gyro values change on the correct axes when the body rotates;
- projected gravity points approximately downward when upright;
- the orientation estimate converges before policy enable;
- the sensor-to-trunk orientation matches the runtime convention.

A wrong IMU axis convention can make a physically upright robot look fallen to software.

## Stage 6 — Joint zero and home pose

This is one of the most important steps.

The runtime home pose must match the training `HOME_FRAME`. The current public values are listed in [Hardware Parameter Reference](../hardware/parameter-reference.md).

Recommended research procedure:

1. mechanically place one joint in its intended reference pose;
2. read its encoder value;
3. confirm direction: positive command should move in the model's positive direction;
4. store the mapping between physical zero and runtime joint angle;
5. repeat for all policy joints;
6. verify the full home pose visually before torque is raised.

Do not compensate a wrong mechanical zero by silently changing RL observations later. Keep the zero convention explicit.

## Stage 7 — Validate the 50 Hz closed loop without walking

Before loading a walking policy, run a safe hold/stand test and measure:

- achieved loop frequency;
- missed ticks;
- bus read failures;
- stale IMU samples;
- commanded vs measured joint position;
- motor temperature;
- bus voltage under load.

The official project reports hardware validation around 50 Hz on its Radxa path, but a third-party build must measure its own system.

## Stage 8 — Verify head sensors separately

### ToF

Check:

1. the 8×8 frame updates at the expected rate;
2. a flat wall produces a stable spatial pattern;
3. moving the head changes the reprojected points in the correct direction;
4. floor rejection behaves sensibly;
5. the sensor orientation matches the robot model.

### Camera

Check:

1. the camera enumerates;
2. image orientation is correct;
3. the published mount rotation matches the physical installation;
4. exposure is usable;
5. hardware encoding / stream path works before adding vision inference;
6. only then enable `duck-detect` or another visual model.

Sensor bring-up and AI inference are separate problems.

## Stage 9 — Mechanical subassemblies before full walking

Validate one chain at a time:

```text
one leg
  ↓
second leg
  ↓
head chain
  ↓
feet / sole contact
  ↓
full robot
```

For each chain, compare measured motion with the public model:

- joint axis direction;
- approximate joint center;
- usable range;
- link orientation;
- obvious backlash;
- interference or cable restriction.

## Stage 10 — First policy run

Use the safest available policy first: stand/hold before dynamic walking.

For the first dynamic run:

- use conservative speed commands;
- keep a physical support / safe test area;
- monitor temperature, voltage and loop statistics;
- record which exact model, runtime configuration and upstream commit are used;
- change one variable at a time.

If the robot behaves differently from simulation, debug in this order:

```text
joint zero / direction
→ IMU frame
→ joint order
→ timing / bus errors
→ action scaling / filtering / gains
→ mechanics / backlash / friction
→ model mass / CoM / contact assumptions
→ RL tuning
```

Do not start by retraining the policy if the hardware conventions have not been verified.

## What is still not publicly defined as a production procedure?

Public official material does not currently provide a complete final manufacturing calibration package covering every production tolerance, fixture and acceptance limit.

Therefore this page intentionally does **not** invent:

- factory jig dimensions;
- production servo-offset tolerances;
- final cable routing limits;
- production camera intrinsic calibration;
- production ToF extrinsic tolerance;
- final end-of-line acceptance thresholds.

Those remain unresolved until supported by public evidence.

## Primary public sources

- https://github.com/pollen-robotics/microduck/blob/main/docs/project/roadmap.md
- https://github.com/pollen-robotics/microduck/blob/main/docs/design/robotd-design.md
- https://github.com/pollen-robotics/microduck/blob/main/scripts/board-test.sh
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/model.rs
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/imu.rs
- https://github.com/pollen-robotics/microduck/blob/main/deploy/robotd.toml

Related pages:

- [Public Reproduction Roadmap](public-reproduction-roadmap.md)
- [Hardware Parameter Reference](../hardware/parameter-reference.md)
- [Robotd Hardware Protocol](../software/robotd-hardware-protocol.md)
