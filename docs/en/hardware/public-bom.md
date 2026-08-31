# Public Hardware Inventory / BOM Status

**English** | [简体中文](../../zh-CN/hardware/public-bom.md)

> Status: public-source reconstruction, last checked 2026-08-31.

Microduck does **not** currently have an official public hardware BOM. Pollen Robotics explicitly states that the open-source commitment covers the software stack and that the mechanical/electronic design files are not published as open-source hardware.

This page therefore distinguishes between **official product specifications**, **official-source development hardware**, and **community-derived reconstruction**.

## Evidence levels

- **Official product spec** — published by Pollen Robotics / Hugging Face on the product page, store, or press kit.
- **Official source** — directly identifiable in official source code, configuration, simulation assets, or hardware bring-up notes.
- **Community reconstruction** — independently derived from public assets; useful, but not an official production BOM.
- **Unresolved** — a subsystem is public, but the exact production part number is not yet fixed or publicly identified.

## Concrete component inventory

| Subsystem | Component / part | Qty. / detail | Evidence | Status / notes |
|---|---|---:|---|---|
| Main compute board | **Radxa Zero 3W** | 1 | Official source | Current official bring-up/reference platform. The product-level spec guarantees RK3566, not necessarily this exact carrier forever. |
| Compute SoC | **Rockchip RK3566** | 1 | Official product spec | AI accelerator included. |
| RAM | **1 GB** | 1 | Official product spec | Exact DRAM package not public. |
| Storage | **32 GB** | 1 | Official product spec | Exact flash/eMMC package not public. |
| Joint actuators | **ROBOTIS Dynamixel XL330** | **15** | Official source + product spec | Exact XL330 sub-variant (for example M077 vs M288) is not explicitly fixed in official Microduck source; do not promote a community guess to official BOM. |
| Control IMU | **STMicroelectronics LSM6DSV16X** | 1 | Official source | Located on the custom **`imu_to_dxl` v2** board; Dynamixel device ID 200. |
| IMU bridge board | **`imu_to_dxl` v2** | 1 | Official source | Custom board; complete schematic/BOM not public. |
| Robot HAT | **Pollen Robotics RPI Robot HAT** | 1 | Official source | Development/reference custom board; full schematic/BOM not public. |
| HAT audio codec | **Texas Instruments TLV320AIC3104** | 1 | Official source | I2C address **0x18**; I2S audio path; 12 MHz codec MCLK in current development overlay. |
| HAT secondary IMU | **Bosch BMI088** | 1 | Official source | I2C addresses **0x19 / 0x68** in the development HAT description; explicitly marked dormant/unused in current source comments. |
| Front camera | **Sony IMX219 / Raspberry Pi Camera v2 path** | 1 | Official source | Current Radxa media bring-up path. Product camera resolution/FOV remain provisional. |
| ToF sensor | **ST VL53L5CX and/or VL53L8CX family** | 1 | Official source | Both are supported in the official source tree; current public product spec only commits to an 8×8 ToF matrix. Exact production model unresolved. |
| ToF bus | I2C device at **0x29** | 1 | Official source | Connected through the Robot HAT/Stemma path in current development hardware. |
| Battery | **NP-F550 camera battery, 2600 mAh** | 1 | Official product spec | Removable; around one hour runtime depending on use. |
| NFC antennas | Head antenna + beak antenna | **2** | Official product spec | Exact NFC controller/transceiver part number is not public. |
| Microphones | Not publicly identified | plural | Official product spec | Exact microphone part numbers not public. |
| Speaker | Not publicly identified | 1 | Official product spec | Exact speaker part number not public. |
| Wireless | Wi-Fi + Bluetooth | onboard | Official product spec | Current Radxa Zero 3W platform supplies these functions; exact final radio package not separately specified in product documentation. |
| Camera-use indicator | dedicated REC-style indicator | 1 | Official product spec | Exact LED/device part number not public. |
| Passive roller attachments | roller assemblies | optional | Official product/accessory info + official RL assets | Passive wheel joints appear in roller MJCF variants. |

## Product-level dimensions and mass

| Item | Public value | Source status |
|---|---:|---|
| Height | **25 cm** | Official product spec |
| Width | **14 cm** | Official product spec |
| Weight | **under 800 g** in press kit; current store listing says **780 g** | Both are official public values; store value is more specific, while the press kit retains the broader launch spec |
| Motors / DoF | **15** | Official product spec |
| Policy loop | **50 Hz** | Official product/official source |

## Motor and device map

The current official runtime defines the following Dynamixel IDs:

```text
left leg        20 21 22 23 24
neck/head/mouth 30 31 32 33 34
right leg       10 11 12 13 14
imu_to_dxl      200
```

The mouth is motor index 9 and is deliberately omitted from the 14-action locomotion policy output. This is why Microduck has **15 motors but a 14-dimensional RL action vector**.

## Development HAT: publicly identifiable electronics

The official `i2c3-pihat.dts` and `aic3104-i2c3.dts` files expose unusually concrete information about the current development/reference electronics:

| Item | Publicly visible value |
|---|---|
| Compute-board compatibility | `radxa,zero-3w`, `rockchip,rk3566` |
| HAT I2C controller | RK3566 **I2C3 M0** on header pins 3/5 |
| I2C clock | **400 kHz** |
| Audio codec | **TLV320AIC3104**, address **0x18** |
| Dormant IMU | **BMI088**, addresses **0x19 / 0x68** |
| ToF | address **0x29**, via Stemma J5 path |
| Audio MCLK | **12 MHz** fixed clock |
| I2S CPU-side clock | **12.288 MHz** in the current overlay |
| Pull-ups mentioned in source comments | **R12/R13, 10 kΩ pair** |

These values describe the current official-source development implementation. They are not a published production schematic.

## What remains unknown

The following are **not** yet public as a complete production BOM:

- exact XL330 sub-variant;
- MCU/transceiver and passive-component BOM for `imu_to_dxl` v2;
- complete Robot HAT schematic and PCB BOM;
- exact production ToF model when both VL53L5CX and VL53L8CX are supported;
- exact final camera module/lens/FOV;
- exact head/body second-IMU mapping in the production robot;
- NFC controller IC;
- microphone and speaker part numbers;
- exact production fastener lengths and counts;
- exact bearing quantities and supplier part numbers;
- production wiring harnesses/connectors/cable lengths.

Unknown means “not confirmed from public sources”, not “absent from the robot”.

## Community-derived mechanical BOM

Public MJCF/STL assets make it possible to infer more than the official product sheet publishes. Independent reconstruction projects have reported:

- an **M2-dominant fastener system**;
- model-derived bearing geometries around **22×16×4 mm** and **15×10×3 mm**;
- model-derived fastener-hole statistics;
- reconstructed rigid-body grouping, masses, and assembly transforms.

Those details are intentionally kept on a separate page: [Community-derived BOM and assembly reconstruction](community-bom-reconstruction.md).

## Known source conflicts / moving targets

### NP-F550 product battery vs NP-F970-named simulation geometry

Some public simulation assets contain an `NP-F970`-named mesh. The official launch specification and store identify the product battery as **NP-F550, 2600 mAh**. OpenMicroDuck therefore records NP-F550 as the product specification and treats F970 references as model/development evidence.

### Camera and ToF

The press kit states that camera resolution/FOV and LiDAR range are still being finalized. The source tree is more concrete about development hardware (IMX219, VL53L5CX/VL53L8CX), but development-source specificity is not the same as a frozen production BOM.

## Primary official sources

- https://pollen-robotics.com/microduck/press-kit/
- https://pollen-robotics.com/microduck/
- https://store.pollen-robotics.com/products/microduck
- https://github.com/pollen-robotics/microduck
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/model.rs
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/imu.rs
- https://github.com/pollen-robotics/microduck/blob/main/deploy/audio/i2c3-pihat.dts
- https://github.com/pollen-robotics/microduck/blob/main/deploy/audio/aic3104-i2c3.dts
- https://github.com/pollen-robotics/microduck/blob/main/docs/project/media-bringup.md
- https://github.com/pollen-robotics/microduck_rl

## Community references

- https://github.com/fanhao375/microduck-replica
- https://github.com/boris721/microduck-3d

See [../ecosystem/reverse-engineering-projects.md](../ecosystem/reverse-engineering-projects.md) for the reviewed community-project index.