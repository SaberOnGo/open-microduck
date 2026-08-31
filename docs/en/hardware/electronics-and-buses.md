# Electronics, Buses, Sensors, and Power

> Scope: public information visible in Pollen Robotics product material and source repositories. Development-board details are labeled separately from final product specifications.

## System overview

The public sources describe a compact Linux robot built around an **RK3566** compute platform, a shared Dynamixel motor bus, an IMU bridge device on that bus, camera/ToF/audio peripherals, Wi-Fi/Bluetooth, and a removable camera-style battery.

A simplified public-source view is:

```text
                 RK3566 Linux compute
                        │
          ┌─────────────┼──────────────┐
          │             │              │
   serial / DXL       camera        I2C / audio
          │             │              │
   ┌──────┴──────┐    CSI path     ToF / codec
   │             │
15 servos   imu_to_dxl v2
                 │
           LSM6DSV16X
```

This is a documentation abstraction, not an official schematic.

## Compute

### Product-level specification

The press kit lists:

- Rockchip **RK3566** with AI accelerator;
- **1 GB RAM**;
- **32 GB storage**;
- Wi-Fi and Bluetooth.

### Current source-tree platform

Official bring-up and deployment documentation currently uses **Radxa Zero 3 / Zero 3W** hardware running Armbian/Debian-family software. Because earlier design notes call the board selection provisional, OpenMicroDuck records the board as a current development/reference platform rather than silently treating it as an immutable production BOM item.

## Motor and sensor bus

The current upstream runtime defines:

- serial port: `/dev/ttyS2` on the Radxa Zero 3W development wiring;
- bus speed: **1,000,000 baud**;
- protocol: Dynamixel Protocol 2-compatible communication through the upstream Rust stack;
- 15 motor device IDs;
- one `imu_to_dxl` device at ID **200**;
- nominal control loop: **50 Hz**.

The official runtime comments explicitly say the 15 servos and the IMU bridge share the serial bus.

### Motor IDs

```text
left leg        20 21 22 23 24
neck/head/mouth 30 31 32 33 34
right leg       10 11 12 13 14
IMU bridge      200
```

The motor map comes from `duck-control/src/model.rs` in the official repository.

## 15 motors, 14 RL actions

The upstream runtime models 15 joints, but the alpha policy interface is **61 observations → 14 actions**.

The missing action is deliberate: the mouth/beak motor is not part of the locomotion policy action vector. Runtime code maps the 14 policy outputs around the mouth slot and controls the mouth independently.

## IMU bridge

The official `duck-control/src/imu.rs` describes an **`imu_to_dxl` v2** device using an **ST LSM6DSV16X**.

The control loop consumes a 12-byte block from the device:

- gyro x/y/z as signed 16-bit values;
- SFLP quaternion x/y/z in IEEE half precision;
- quaternion `w` reconstructed by the host.

The source notes that this block is fetched in the same bus read cycle as the servos, avoiding a separate host-side orientation-sensor polling path for the control IMU.

The public product spec separately states that the finished robot has **two IMUs, one in the body and one in the head**. The public source tree fully identifies the control-path LSM6DSV16X device, but OpenMicroDuck does not assume that every second-IMU development component is the final production head-IMU part number unless confirmed by Pollen Robotics.

## Servo family

The official RL repository models the actuator as **Dynamixel XL330** using Rhoban's BAM actuator model. The public MJCF assets also contain XL330 motor geometry.

Important simulation/runtime characteristics documented upstream include:

- voltage-dependent actuator behavior;
- back-EMF and friction modeling through BAM;
- command delay randomization;
- battery-voltage and voltage-sag randomization;
- dedicated backlash model variants.

These are discussed further in [../simulation/model-and-rl.md](../simulation/model-and-rl.md).

## Battery and power observation

The public product specification lists a **removable NP-F550, 2600 mAh** camera battery with roughly one hour of runtime depending on use.

The current runtime source describes the pack as 2S Li-ion and defines an operating mapping of approximately:

- **8.2 V**: full under load;
- **6.6 V**: empty-for-robot-operation threshold.

The runtime also states that there is no separate fuel-gauge/ADC value in its control model; it uses supply-voltage readings reported through the servo bus. These values therefore represent usable bus voltage under load, not a laboratory cell-state-of-charge curve.

## Camera

The press kit confirms a front camera but states that final resolution and field of view are still being finalized.

Official Radxa Zero 3W media bring-up documentation currently uses the **Raspberry Pi Camera v2 / IMX219** device-tree path and Rockchip's MPP hardware H.264 encoder. This is strong evidence for the current development platform, but it remains appropriate to separate that from the final product-level camera specification until Pollen Robotics freezes the part.

## ToF / “LiDAR”

The press kit describes a **compact 8×8 time-of-flight matrix**.

The official source tree contains drivers/vendor integration for both:

- ST **VL53L5CX**;
- ST **VL53L8CX**.

Because both families appear in source and the press kit does not name the final sensor, this repository records the production part number as unresolved rather than choosing one based on a community guess.

## Audio

The press kit confirms microphones and a speaker.

The current source tree contains bring-up and device-tree support for the **TI TLV320AIC3104** codec on the Radxa development path. That is documented here as current official-source evidence, not as a promise that every production revision uses the same audio board implementation.

## NFC

The product specification lists **two NFC antennas**, one in the head and one in the beak. Public product material shows NFC tags as part of interaction/accessory workflows.

## Software-visible bus reliability

The official runtime is designed to tolerate isolated serial-bus failures rather than assuming every transaction succeeds. Configuration includes a limit for consecutive failed reads before the robot is considered unhealthy, and project notes describe bus measurements performed on hardware.

This matters for reverse engineering because a 50 Hz control architecture cannot be understood from nominal baud rate alone; turnaround delay, device count, error handling, and loop timing are part of the real system behavior.

## Sources

- https://pollen-robotics.com/microduck/press-kit/
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/model.rs
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/imu.rs
- https://github.com/pollen-robotics/microduck/blob/main/deploy/robotd.toml
- https://github.com/pollen-robotics/microduck/blob/main/docs/design/robotd-design.md
- https://github.com/pollen-robotics/microduck/blob/main/docs/project/media-bringup.md
- https://github.com/pollen-robotics/microduck_rl

A more aggressive hardware reconstruction is available in the independent `fanhao375/microduck-replica` project. OpenMicroDuck treats conclusions from that repository as community-derived unless independently confirmed by the official sources above.
