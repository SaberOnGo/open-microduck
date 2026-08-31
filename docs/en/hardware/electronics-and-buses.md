# Electronics, Buses, Sensors, and Power

**English** | [简体中文](../../zh-CN/hardware/electronics-and-buses.md)

> Scope: public information visible in Pollen Robotics product material and official source repositories. Development/reference hardware is labeled separately from final product specifications.

## Named electronics quick reference

| Function | Publicly identified hardware | Interface / address | Evidence status |
|---|---|---|---|
| Linux compute board | **Radxa Zero 3W** | 40-pin header, CSI, Wi-Fi/Bluetooth | Official-source development/reference platform |
| SoC | **Rockchip RK3566** | — | Official product specification |
| Servo bus | **15 × ROBOTIS Dynamixel XL330** | UART2 `/dev/ttyS2`, Dynamixel Protocol 2, **1 Mbps** | Official source |
| Main control IMU | **ST LSM6DSV16X** | `imu_to_dxl` v2, Dynamixel ID **200** | Official source |
| Audio codec | **TI TLV320AIC3104** | I2C **0x18**, I2S audio | Official-source development hardware |
| HAT IMU | **Bosch BMI088** | I2C **0x19 / 0x68** | Official-source development hardware; dormant/unused |
| Front camera | **Sony IMX219 / Raspberry Pi Camera v2 path** | MIPI CSI | Official-source development hardware |
| ToF | **ST VL53L5CX / VL53L8CX** | I2C **0x29** | Both supported in official source; final production part unresolved |
| Product battery | **NP-F550, 2600 mAh** | removable 2S-class camera battery | Official product specification |
| NFC | two antennas | head + beak | Official product specification; controller IC not public |

## Public-source system view

```text
                         Radxa Zero 3W
                      Rockchip RK3566 Linux
                              │
        ┌─────────────────────┼────────────────────┐
        │                     │                    │
 UART2 / ttyS2             MIPI CSI              I2C3 M0
 Dynamixel V2              IMX219 path          400 kHz
 1 Mbps                       │                    │
        │                     │          ┌─────────┼──────────┐
        │                     │          │         │          │
        │                     │    TLV320AIC3104  BMI088   ToF 0x29
        │                     │       0x18       0x19/0x68  VL53L5/8CX
        │
   ┌────┴────────────────────────────┐
   │                                 │
15 × Dynamixel XL330          imu_to_dxl v2
                                     │
                               LSM6DSV16X
                               device ID 200
```

This is a documentation diagram reconstructed from public source, **not an official schematic**.

## Main compute platform

### Product-level specification

Pollen Robotics publicly specifies:

- **Rockchip RK3566** with AI accelerator;
- **1 GB RAM**;
- **32 GB storage**;
- Wi-Fi and Bluetooth.

### Current official-source board

The current bring-up, media, device-tree, and deployment files target **Radxa Zero 3W**. The compatibility strings visible in official overlays include:

```text
radxa,zero-3w
rockchip,rk3566
```

OpenMicroDuck therefore records Radxa Zero 3W as the current official-source development/reference board, while keeping the product-level promise at RK3566.

## Servo / IMU bus

The current runtime defines:

- port: **`/dev/ttyS2`**;
- baud: **1,000,000**;
- protocol: Dynamixel Protocol 2-compatible communication;
- nominal control loop: **50 Hz**;
- 15 servo IDs plus `imu_to_dxl` ID 200.

### Device IDs

```text
left leg        20 21 22 23 24
neck/head/mouth 30 31 32 33 34
right leg       10 11 12 13 14
imu_to_dxl      200
```

The 15 servos and IMU bridge share the same bus. The mouth motor is excluded from the 14-dimensional locomotion policy output.

## `imu_to_dxl` v2

Official `duck-control/src/imu.rs` names the sensor as **ST LSM6DSV16X**.

The control loop consumes a 12-byte block:

- gyro x/y/z as `i16` little-endian values;
- SFLP quaternion x/y/z as IEEE binary16;
- quaternion `w` reconstructed on the host.

The source also makes clear that this IMU block is read in the same shared bus transaction path as the servos.

What is **not** public: the full schematic/BOM of the `imu_to_dxl` v2 board, including its MCU, bus-interface circuitry, regulator choices, and passive-component values.

## Pollen Robotics RPI Robot HAT

The official source tree explicitly refers to a **Pollen Robotics RPI Robot HAT** on the current Radxa development path.

### Publicly visible HAT devices

| Device | Public value |
|---|---|
| Audio codec | **TI TLV320AIC3104**, I2C **0x18** |
| Secondary IMU | **Bosch BMI088**, **0x19 / 0x68**, marked dormant/unused |
| ToF path | **0x29** through Stemma J5 |
| I2C bus | RK3566 **I2C3 M0**, header pins 3/5 |
| I2C frequency | **400 kHz** |
| Audio codec MCLK | **12 MHz** fixed clock |
| CPU-side I2S clock in current overlay | **12.288 MHz** |
| I2C pull-up pair mentioned by official source comments | **R12/R13, 10 kΩ** |

### Important I2C3 mux detail

Official `i2c3-pihat.dts` documents that the HAT uses RK3566 I2C3 on its M0 pinmux. The same controller is otherwise used in M1 by the Radxa board's **FUSB302** USB-C PD controller. The official overlay re-muxes I2C3 to the HAT pins and disables the FUSB302 device-tree node for that mode.

This is a development-platform implementation detail, but it is useful because it makes the board-level wiring much less ambiguous than a generic product sheet.

## Camera path

Official media bring-up targets **Raspberry Pi Camera v2 / Sony IMX219** on Radxa Zero 3W and uses Rockchip MPP for hardware H.264 encoding.

The product press kit separately says that final camera resolution and field of view are still being finalized. Therefore:

- **IMX219 is confirmed in the current official development path**;
- **the final production camera module/lens is not yet safe to label as frozen BOM**.

## ToF sensor

The product specification commits to a compact **8×8 time-of-flight matrix**.

The official source tree vendors/supports both:

- **ST VL53L5CX**;
- **ST VL53L8CX**.

The current HAT wiring describes the ToF device at **I2C address 0x29**. Because both generations appear in official source, OpenMicroDuck does not choose one as the final production part without stronger evidence.

## Audio path

The development audio path is concrete:

```text
RK3566 I2C3 ──> TLV320AIC3104 @ 0x18   control
RK3566 I2S3 ──> TLV320AIC3104          audio data
12 MHz fixed clock ──> codec MCLK
```

The product itself publicly specifies microphones and a speaker, but their exact transducer part numbers are not public.

## Battery and voltage observation

Official product documentation specifies a removable **NP-F550, 2600 mAh** battery.

The current runtime uses servo-reported bus voltage and defines a usable-under-load mapping around:

- **8.2 V** full;
- **6.6 V** empty-for-robot-operation.

The runtime comments state that the control model does not use a separate fuel-gauge/ADC measurement for this value.

## Product-level sensors not fully identified by part number

Public product material also confirms:

- **2 IMUs**, one in the body and one in the head;
- **2 NFC antennas**, one in the head and one in the beak;
- microphones and speaker;
- dedicated camera-use indicator.

The current source tree identifies LSM6DSV16X and a dormant BMI088 in development electronics, but public evidence is not yet strong enough to map every production body/head IMU to a final chip number.

## Sources

- https://pollen-robotics.com/microduck/press-kit/
- https://store.pollen-robotics.com/products/microduck
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/model.rs
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/imu.rs
- https://github.com/pollen-robotics/microduck/blob/main/deploy/robotd.toml
- https://github.com/pollen-robotics/microduck/blob/main/deploy/audio/i2c3-pihat.dts
- https://github.com/pollen-robotics/microduck/blob/main/deploy/audio/aic3104-i2c3.dts
- https://github.com/pollen-robotics/microduck/blob/main/docs/project/media-bringup.md
- https://github.com/pollen-robotics/microduck_rl

For the broader inventory, see [Public hardware inventory and BOM status](public-bom.md). For model-derived screws, bearings, and assembly data, see [Community-derived BOM reconstruction](community-bom-reconstruction.md).