# Microduck Hardware Parameter Reference

**English** | [简体中文](../../zh-CN/hardware/parameter-reference.md)

> A one-stop public parameter table for research and simulation. **This is not an official production BOM.** Every section states what kind of evidence it uses.

## 1. Quick reference

| Item | Public value | Evidence |
|---|---|---|
| Product height | about 25 cm | Official product spec |
| Product width | about 14 cm | Official product spec |
| Product mass | under 800 g; current store material has also stated 780 g | Official product spec |
| Motors | 15 | Official product/source |
| Policy-controlled joints | 14 | Official source/RL |
| Separate mouth/beak motor | 1 | Official source |
| Runtime control rate | 50 Hz | Official source |
| Control period | 20 ms | Derived directly from 50 Hz |
| Motor/IMU bus | Dynamixel-compatible serial, 1 Mbps | Official source |
| Control IMU bus ID | 200 | Official source |
| Main control IMU | ST LSM6DSV16X on `imu_to_dxl` v2 | Official source |
| Product compute SoC | Rockchip RK3566 | Official product spec |
| Current development compute board | Radxa Zero 3W | Official source |
| Product RAM / storage | 1 GB / 32 GB | Official product spec |
| Product ToF | 8×8 matrix | Official product spec |
| Current source ToF support | VL53L5CX / VL53L8CX family | Official source; final production part unresolved |
| Current camera bring-up | IMX219 / Raspberry Pi Camera v2 path | Official source; product camera details remain revision-sensitive |
| Product battery | removable NP-F550, 2600 mAh | Official product spec |
| Runtime usable battery mapping | 8.2 V full → 6.6 V empty-under-load | Official source |

## 2. The 15-motor map

The current official runtime defines **15 physical motor IDs**. The locomotion policy controls 14 of them; the mouth is intentionally skipped by the policy action vector.

| Runtime index | Joint | Dynamixel ID | Home pose | Policy action? |
|---:|---|---:|---:|---|
| 0 | `left_hip_yaw` | 20 | 0° | yes |
| 1 | `left_hip_roll` | 21 | −5.00° | yes |
| 2 | `left_hip_pitch` | 22 | −26.24° | yes |
| 3 | `left_knee` | 23 | −0.28° | yes |
| 4 | `left_ankle` | 24 | +25.95° | yes |
| 5 | `neck_pitch` | 30 | +20.00° | yes |
| 6 | `head_pitch` | 31 | +20.00° | yes |
| 7 | `head_yaw` | 32 | 0° | yes |
| 8 | `head_roll` | 33 | 0° | yes |
| 9 | `mouth` | 34 | 0° home | **no — separate control** |
| 10 | `right_hip_yaw` | 10 | 0° | yes |
| 11 | `right_hip_roll` | 11 | +5.00° | yes |
| 12 | `right_hip_pitch` | 12 | +26.24° | yes |
| 13 | `right_knee` | 13 | +0.28° | yes |
| 14 | `right_ankle` | 14 | −25.95° | yes |

Source: `pollen-robotics/microduck`, `duck-control/src/model.rs`, commit `590b986...`.

The mouth command range in this source snapshot is:

```text
closed: -5°
open:  +30°
```

### Why the Home Pose matters

The official source explicitly warns that the runtime Home Pose must match the training `HOME_FRAME`. The policy observes joint positions relative to that frame, so a wrong home angle becomes a constant error in the observation.

This is one of the most important sim-to-real parameters to preserve.

## 3. Joint limits in the official full-collision simulation model

These are **official simulation-model joint limits**, not a claim about certified mechanical hard stops on a retail unit.

Snapshot: `microduck_rl` `robot_allcollisions.xml`, commit `d424a0c...`.

| Policy joint | Range in model |
|---|---:|
| `left_hip_yaw` | −25° to +30° |
| `left_hip_roll` | −22° to +22° |
| `left_hip_pitch` | −90° to +90° |
| `left_knee` | −90° to +90° |
| `left_ankle` | −90° to +90° |
| `neck_pitch` | −90° to +60° |
| `head_pitch` | −90° to +90° |
| `head_yaw` | −170° to +170° |
| `head_roll` | −25° to +25° |
| `right_hip_yaw` | −30° to +25° |
| `right_hip_roll` | −22° to +22° |
| `right_hip_pitch` | −90° to +90° |
| `right_knee` | −90° to +90° |
| `right_ankle` | −90° to +90° |

Do not confuse these broad MJCF limits with the smaller angles normally used while standing or walking.

## 4. Official simulation mass model

The full-collision MJCF stores an inertial mass on each rigid body. Summing the 15 inertial bodies in the pinned snapshot gives approximately:

```text
737.243 g
```

That value is an **official simulation-model mass total**, not a scale measurement of a production robot.

The same model contains the following rigid-body inertial masses:

| Body / link | Mass |
|---|---:|
| `trunk_base` | 199.224 g |
| left hip-yaw link | 23.041 g |
| left hip-roll link | 6.189 g |
| left upper leg | 48.207 g |
| left lower leg | 21.584 g |
| left ankle/foot link | 30.025 g |
| `neck` | 36.841 g |
| `neck_pitch` link | 5.720 g |
| `yaw_roll_motion` | 48.600 g |
| head-roll / `jaw_soft` body | 188.766 g |
| right hip-yaw link | 23.041 g |
| right hip-roll link | 6.189 g |
| right upper leg | 48.207 g |
| right lower leg | 21.584 g |
| right ankle/foot link | 30.025 g |

The head assembly is a large fraction of the modeled mass. That helps explain why head/neck dynamics matter strongly to a robot of this scale.

## 5. Motor bus and timing

**Official source implementation** at the pinned runtime commit:

```text
port: /dev/ttyS2 on current Radxa Zero 3W wiring
baud: 1,000,000 bit/s
control loop: 50 Hz
period: 20 ms
servo devices: 15
IMU bridge device: ID 200
```

The current bus code performs, per healthy control tick:

```text
1 combined sync_read
  ├─ imu_to_dxl ID 200 first
  └─ 15 servo devices

then

1 sync_write
  └─ servo goal positions
```

The IMU is deliberately requested first so its response arrives before the servo burst.

### State read layout

The current servo state read begins at Dynamixel register address 124 and reads 12 bytes. It covers present PWM/current/velocity/position data; the runtime consumes the fields it needs.

Useful conversion constants visible in the public source include:

- Dynamixel velocity unit: **0.229 rpm/count** before conversion to rad/s;
- bus voltage: **0.1 V/count** in the slower sensor read;
- slow voltage/temperature read: approximately **1 Hz**;
- bus read timeout: **30 ms**.

## 6. Important startup servo settings

The official runtime asserts/corrects several EEPROM values at startup:

| Register | Expected value | Why it matters |
|---|---:|---|
| `return_delay_time` | 0 | factory delay would waste a large fraction of the 20 ms tick budget across 16 devices |
| `baud_rate` | 3 | Dynamixel encoding for 1 Mbps; must match runtime baud |
| `pwm_slope` | 255 | pinned current alpha setting |
| `shutdown` | 52 | current error-mask setting used by runtime |

The source explains the most important one numerically: the factory `return_delay_time=250` corresponds to about 500 μs/device. Across 16 devices that is about **8 ms**, roughly **40% of a 20 ms control period**.

This is a good example of why seemingly minor servo-register details can affect locomotion timing.

## 7. Position gain: keep the layers separate

The current runtime default is:

```text
position P gain = 200
I = 0
D = 0
```

This is a **real-servo register/control setting**.

It must not be confused with gains or fitted parameters that appear inside BAM or MJCF actuator models. Those values can have different meanings and units.

The runtime also uses a softer standing gain ratio and special gain handling for skills/safety states; see the source `robotd.toml` for the pinned revision.

## 8. Control IMU: `imu_to_dxl` v2

The current official control source identifies:

```text
sensor: ST LSM6DSV16X
bridge: imu_to_dxl v2
Dynamixel ID: 200
```

The runtime reads a **12-byte block** in the same transaction family as the servos.

### Runtime data block

| Bytes | Data |
|---|---|
| 0–5 | gyro X/Y/Z as little-endian signed 16-bit integers |
| 6–11 | SFLP quaternion X/Y/Z as IEEE half floats; W is reconstructed |

The source states:

- gyro range used by the bridge: ±500 dps;
- gyro scale: **17.5 mdps/LSB**;
- runtime exposes angular velocity in rad/s;
- quaternion is converted into projected gravity/orientation information used by the policy.

The decoder waits for approximately **25 live quaternion samples** before declaring the SFLP stream ready, around 0.25 s at 100 Hz.

It also applies a median-of-three style spike rejection to gyro/gravity-related values.

### Sensor mounting transform

The public source documents a default sensor-to-trunk mounting rotation of approximately +90° around Y, with the raw axes mapped so the runtime trunk frame corresponds to:

```text
[ +raw_z, +raw_y, -raw_x ]
```

This kind of orientation mapping is critical: a correct IMU with the wrong axis convention can make a good policy fail immediately.

## 9. Battery and power values

### Product-level battery

Official product material identifies a removable:

```text
NP-F550
2600 mAh
2S Li-ion class
```

### Runtime battery mapping

The current runtime has no separate fuel-gauge measurement in the public control path. It uses the supply voltage reported by the servos.

The pinned source maps the usable loaded range as:

```text
8.2 V → 100%
7.4 V → 50%
6.6 V → 0%
```

The source explicitly describes 6.6 V as an **under-load usable floor**, not the electrochemical empty voltage of the cells.

This distinction matters because voltage sags while the robot is moving.

## 10. Current development compute/HAT interfaces

This section describes **official-source development hardware**, not a published production schematic.

### Compute

- RK3566 product SoC;
- current official bring-up targets Radxa Zero 3W;
- current motor/IMU serial port is `/dev/ttyS2`.

### HAT I2C

The published device-tree overlay shows:

```text
RK3566 I2C3 M0
40-pin header pins 3/5
400 kHz
SDA: GPIO1_A0
SCL: GPIO1_A1
```

The source comments mention a single **10 kΩ pull-up pair R12/R13** on the HAT and note that cable capacitance may require 200 kHz in some cases.

### Devices visible on this development I2C path

| Device/function | Public-source detail |
|---|---|
| TLV320AIC3104 audio codec | I2C `0x18` |
| BMI088 | `0x19` / `0x68`; source comments describe it as dormant/unused in the current path |
| ToF | I2C `0x29`, via the HAT/Stemma path |

The same overlay remuxes I2C3 to the header and disables the conflicting FUSB302 USB-C PD-controller path; source comments note that USB-C default 5 V behavior still exists while robot power is supplied through the HAT design.

## 11. Audio development path

The official device-tree bring-up identifies:

```text
codec: TLV320AIC3104
I2C address: 0x18
I2S: I2S3, 2 channels
codec MCLK: 12.000 MHz
CPU-side I2S system clock: 12.288 MHz
Linux sound-card name: aic3104
```

Again, this is excellent evidence for the current development implementation but not a complete production audio schematic.

## 12. Camera and ToF

### Camera

Current official Rockchip/Radxa media bring-up uses an **IMX219 / Raspberry Pi Camera v2-style path**.

Product-level camera resolution/FOV should still be treated according to the current official product/press wording rather than inferred from one development module.

### ToF

The product promises an **8×8 depth/ToF matrix**.

The official source tree has support for the ST multi-zone family including **VL53L5CX and VL53L8CX**. The exact final production sensor should remain unresolved until upstream product evidence fixes it.

The runtime architecture exposes ToF through a dedicated service instead of putting its 8×8 matrix directly into the 61-D locomotion policy observation.

## 13. What the official simulation model reveals about parts

The pinned `robot_allcollisions.xml` contains visual instances for:

- 15 `xl330` motor meshes;
- **11** instances of the mesh explicitly named `seeed_bearing__configuration__22x16x4`;
- **3** instances of a smaller/default bearing mesh;
- battery, PCB/HAT, speaker, lens, shells, feet, soles and other structural placeholders.

These are **simulation-model instances**, not guaranteed production purchase quantities.

The large bearing asset name directly encodes a **22×16×4 mm** geometry. Community analysis estimates the smaller/default bearing geometry at roughly **15×10×3 mm**.

## 14. Model naming traps

The simulation asset names contain historical/development placeholders. Two especially important examples:

- the model contains an `np_f970`-named mesh, while current official product material specifies an **NP-F550** battery;
- the asset library contains Raspberry-Pi-related PCB naming even though the current official runtime bring-up targets **Radxa Zero 3W**.

Therefore:

> **Asset filename ≠ current production BOM.**

Use model assets to understand geometry and assembly placement, not to override newer product/runtime evidence.

## 15. What is still unresolved

The following should not be presented as confirmed production facts yet:

- exact XL330 sub-variant;
- full `imu_to_dxl` v2 schematic/BOM;
- full Robot HAT schematic/BOM;
- exact production ToF part if product documentation remains generic;
- final camera module/lens/FOV;
- exact production role/location of the second IMU;
- NFC controller IC;
- microphone and speaker part numbers;
- full fastener lengths/counts;
- production bearing specifications/quantities;
- wiring harness/connectors/cable lengths;
- manufacturing materials/tolerances/inserts.

## Primary sources

- https://github.com/pollen-robotics/microduck
- `duck-control/src/model.rs`
- `duck-control/src/bus.rs`
- `duck-control/src/imu.rs`
- `deploy/robotd.toml`
- `deploy/audio/i2c3-pihat.dts`
- `deploy/audio/aic3104-i2c3.dts`
- https://github.com/pollen-robotics/microduck_rl
- `src/mjlab_microduck/robot/microduck/robot_allcollisions.xml`
- official Microduck product page / press kit

## Related pages

- [Public hardware inventory](public-bom.md)
- [Structure and assembly map](structure-and-assembly-map.md)
- [Community-derived BOM and fasteners](community-bom-reconstruction.md)
- [Sim-to-real parameter reference](../simulation/sim-to-real-parameter-reference.md)
