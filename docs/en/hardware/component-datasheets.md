# Public Component Datasheet and Documentation Index

**English** | [简体中文](../../zh-CN/hardware/component-datasheets.md)

> This page is an index of **public manufacturer / official platform documentation** for components that are already supported by public Microduck evidence. It is not a production BOM.

The goal is simple: when a reader sees a component name in OpenMicroDuck, they should have an easy path to the original technical documentation instead of relying on copied specifications.

## Main compute

### Rockchip RK3566

Role in Microduck: official product-level compute SoC.

Useful official source:

- Rockchip product information: https://www.rock-chips.com/

OpenMicroDuck uses the product/press-kit statement for the product-level fact “RK3566 with AI accelerator.” Package-level and board-level implementation details should come from the actual board/source revision being studied.

### Radxa Zero 3W

Role in Microduck: current official-source development/reference compute board.

Official documentation:

- Radxa Zero 3 documentation: https://docs.radxa.com/en/zero/zero3
- Radxa product site: https://radxa.com/products/zeros/zero3w/

Important: the product specification guarantees RK3566; Radxa Zero 3W should remain labeled as a current official-source implementation unless Pollen Robotics publishes it as a permanent production-board commitment.

## Joint actuators

### ROBOTIS Dynamixel XL330 family

Role in Microduck: official-source joint actuator family.

Official e-Manual pages:

- XL330-M077: https://emanual.robotis.com/docs/en/dxl/x/xl330-m077/
- XL330-M288: https://emanual.robotis.com/docs/en/dxl/x/xl330-m288/

The exact production Microduck sub-variant is still unresolved in public evidence. Do not choose M077 or M288 only because one looks more likely.

Useful parameters available from the ROBOTIS documentation include operating modes, control-table registers, communication protocol, voltage limits, position/velocity/current-related data, dimensions, and performance curves.

## Control IMU

### STMicroelectronics LSM6DSV16X

Role in Microduck: official-source control IMU on the `imu_to_dxl` path.

Official product page and datasheet access:

- https://www.st.com/en/mems-and-sensors/lsm6dsv16x.html

The manufacturer documentation is the preferred source for sensor ranges, output data rate, interfaces, register definitions, noise/performance characteristics, and electrical limits.

## Secondary/development IMU

### Bosch BMI088

Role in Microduck: visible in the current official development HAT description; current source comments indicate it is dormant/unused in that path.

Official product page:

- https://www.bosch-sensortec.com/products/motion-sensors/imus/bmi088/

Do not automatically identify this device as the final production “second IMU” without stronger product-level evidence.

## Audio codec

### Texas Instruments TLV320AIC3104

Role in Microduck: official-source development HAT audio codec.

Official product page:

- https://www.ti.com/product/TLV320AIC3104

Useful for codec interfaces, I2C control, I2S/audio serial formats, clocking, ADC/DAC paths, and electrical requirements.

## Camera path

### Sony IMX219 / Raspberry Pi Camera Module v2 path

Role in Microduck: current official-source camera bring-up path.

Official module documentation/reference:

- Raspberry Pi Camera Module 2: https://www.raspberrypi.com/products/camera-module-v2/
- Raspberry Pi camera documentation: https://www.raspberrypi.com/documentation/computers/camera_software.html

The official Microduck press kit still marks final camera resolution and field of view as provisional. A current development driver/module path should therefore not be used to invent the final production optical specification.

## Multi-zone ToF

### ST VL53L5CX

Official product page:

- https://www.st.com/en/imaging-and-photonics-solutions/vl53l5cx.html

### ST VL53L8CX

Official product page:

- https://www.st.com/en/imaging-and-photonics-solutions/vl53l8cx.html

Role in Microduck: both families are represented/supported in public official-source work; the product-level specification commits to a compact **8×8 ToF matrix** while the final production sensor/range remains unresolved.

The ST documentation is the preferred source for zone configuration, ranging modes, interface details, calibration concepts, timing, and electrical limits.

## Battery

### NP-F550 format, 2600 mAh product specification

Microduck's official product specification identifies a removable NP-F550 camera battery with 2600 mAh capacity.

`NP-F550` is a widely used battery form-factor/family designation rather than one single component made by only one manufacturer. For OpenMicroDuck, use Pollen Robotics' product specification for the robot-level requirement and the documentation for the exact battery under test when performing measurements.

Do not substitute data from an arbitrary third-party NP-F550 pack as if it were a Microduck production battery specification.

## How to use datasheets correctly

A component datasheet can tell us what a component **can** do. It does not by itself prove how Microduck configures that component.

For example:

```text
manufacturer datasheet
    → supported ranges / registers / limits

Microduck source
    → which mode, rate, address or interface is actually configured

physical measurement
    → what a specific real unit actually does
```

Use all three at the appropriate evidence level.

## Related pages

- [Public hardware inventory / BOM status](public-bom.md)
- [Electronics, buses, sensors, and power](electronics-and-buses.md)
- [Open questions and source conflicts](../research/open-questions-and-conflicts.md)
- [Sources and evidence map](../sources.md)
