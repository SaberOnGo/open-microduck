# `robotd` Hardware Protocol Reference

**English** | [简体中文](../../zh-CN/software/robotd-hardware-protocol.md)

> Scope: public official Microduck source at the pinned snapshot used by this documentation sweep. This page concentrates hardware-facing values that were previously scattered across several files.

## What happens every 20 ms?

The hardware loop is simple to understand:

```text
read IMU + servo state
        ↓
build robot state
        ↓
run policy / safety logic
        ↓
write new servo targets
        ↓
repeat at 50 Hz
```

The important detail is that the servo chain and the control IMU share one Dynamixel-compatible serial path.

## Bus overview

| Item | Current public value |
|---|---|
| Reference serial device | `/dev/ttyS2` |
| Baud rate | 1,000,000 bit/s |
| Control frequency | 50 Hz |
| Tick period | 20 ms |
| Bus timeout | 30 ms |
| Physical servos | 15 |
| Locomotion-policy joints | 14 |
| Control IMU bridge | ID 200 |

## Device IDs

```text
right leg       10 11 12 13 14
left leg        20 21 22 23 24
head / mouth    30 31 32 33 34
IMU bridge      200
```

The mouth is a physical servo but is not one of the 14 locomotion-policy actions.

## Fast read each control tick

The current public bus code performs a combined synchronized read that includes the IMU bridge and servo state.

For the servo state block, the public source reads from register **124** for **12 bytes**.

That block covers the fast values needed by the loop, including actuator state such as PWM/current, velocity and position in the Dynamixel register layout used by the current servo path.

The IMU bridge is included in the same control-path transaction family so orientation and joint feedback are kept close in time.

## Slow read around once per second

Voltage and temperature do not need 50 Hz sampling.

The current public runtime reads the slow block from register **144**, length **3 bytes**, roughly once per second.

This avoids spending a second serial transaction on every 20 ms tick.

Public conversion values used by the runtime include:

- velocity: **0.229 rpm per count**;
- voltage: **0.1 V per count**.

## Write path

After the policy and safety layers produce final joint targets, the runtime uses a synchronized write for servo goal positions.

The practical sequence is therefore:

```text
SYNC READ
IMU + 15 servo states
        ↓
software / policy / safety
        ↓
SYNC WRITE
servo goal positions
```

## Startup EEPROM expectations

At the pinned public source snapshot, the runtime expects values including:

```text
return_delay_time = 0
baud_rate         = 3    # 1 Mbps code
pwm_slope         = 255
shutdown          = 52
```

Why `return_delay_time = 0` matters:

The official source notes that the factory return delay can be about **500 µs per device**. Across roughly 16 responding devices, that can consume around **8 ms**, or about **40% of a 20 ms control tick**.

This is not a cosmetic setting; it directly affects whether a shared serial bus can meet the control rate.

## Servo position gain

The current public runtime default position P gain is:

```text
P = 200
I = 0
D = 0
```

Do not confuse this register-side servo gain with:

- BAM `kp_fw` in simulation;
- an MJCF actuator `kp`;
- a high-level policy gain ratio.

They are different control layers.

## IMU block: ID 200

The current control IMU path uses an ST **LSM6DSV16X** behind `imu_to_dxl` v2.

The runtime consumes a **12-byte** block:

```text
bytes 0..5    gyro X/Y/Z, i16 little-endian
bytes 6..11   quaternion X/Y/Z, IEEE fp16
```

Quaternion `W` is reconstructed on the host.

Current public values include:

- gyro range: ±500 dps;
- gyro scale: 17.5 mdps/LSB;
- runtime converts gyro to rad/s;
- sensor-to-trunk mounting is approximately a +90° rotation around Y in the current path;
- the runtime waits for live quaternion samples before treating orientation as ready.

The current source also contains spike rejection for gyro/gravity-related signals.

## Home pose and joint order

Bus IDs alone are not enough. The runtime also has a fixed joint order and home pose.

The most important rule is:

> Runtime joint order and home pose must match the policy/training convention.

See [Hardware Parameter Reference](../hardware/parameter-reference.md) for the full 15-device map and home values.

## Safety boundary

The network does not write directly to the serial bus.

```text
ONNX action
   ↓
action scaling / filtering
   ↓
safety and limits
   ↓
final servo target
   ↓
serial write
```

This distinction matters when reproducing behavior: copying an ONNX file without the same runtime processing is not the same controller.

## What is not public here

This page documents the software-visible protocol path. It does not claim a complete production schematic for:

- the half-duplex bus transceiver;
- `imu_to_dxl` v2 MCU and circuitry;
- power distribution and protection;
- final production PCB routing.

Those remain unresolved unless independently supported by public evidence.

## Primary public sources

- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/bus.rs
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/model.rs
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/imu.rs
- https://github.com/pollen-robotics/microduck/blob/main/docs/design/robotd-design.md
- https://github.com/pollen-robotics/microduck/blob/main/deploy/robotd.toml

Related pages:

- [Control loop and sensor dataflow](control-loop-and-sensor-dataflow.md)
- [Hardware Bring-up and Calibration](../getting-started/hardware-bringup-and-calibration.md)
- [Electronics, buses, sensors and power](../hardware/electronics-and-buses.md)
