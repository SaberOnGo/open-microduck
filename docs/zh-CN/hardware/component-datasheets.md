# 公开器件 Datasheet 与官方资料索引

[English](../../en/hardware/component-datasheets.md) | **简体中文**

> 这份页面只整理**已经有 Microduck 公开证据支撑的器件**对应的原厂 / 官方平台资料。它不是量产 BOM。

目的很简单：OpenMicroDuck 文档里一旦出现具体器件型号，读者应该能方便地继续查原始技术资料，而不是只能依赖二手参数表。

## 主计算平台

### Rockchip RK3566

在 Microduck 中的角色：官方产品级确认的主 SoC。

官方资料入口：

- Rockchip 产品网站：https://www.rock-chips.com/

OpenMicroDuck 对“RK3566 + AI accelerator”这个产品级结论，优先引用 Microduck 官方产品页 / Press Kit。具体 package、board-level implementation 则应该继续结合当前板卡和官方源码版本判断。

### Radxa Zero 3W

在 Microduck 中的角色：当前官方源码里使用的开发 / 参考计算板。

官方资料：

- Radxa Zero 3 文档：https://docs.radxa.com/en/zero/zero3
- Radxa 产品页：https://radxa.com/products/zeros/zero3w/

需要注意：Microduck 产品级规格承诺的是 RK3566；Radxa Zero 3W 应继续标注成“当前官方源码实现 / 参考平台”，除非以后 Pollen Robotics 明确把它写成固定量产载板。

## 关节执行器

### ROBOTIS Dynamixel XL330 family

在 Microduck 中的角色：官方源码确认的关节舵机 family。

官方 e-Manual：

- XL330-M077：https://emanual.robotis.com/docs/en/dxl/x/xl330-m077/
- XL330-M288：https://emanual.robotis.com/docs/en/dxl/x/xl330-m288/

目前公开证据还不能把最终量产 Microduck 明确锁定到某个具体 sub-variant。不能因为 M077 或 M288“看起来更像”就自行当成官方 BOM。

ROBOTIS 官方资料可以用于查：

- operating mode；
- control table；
- communication protocol；
- voltage limit；
- position / velocity / current 相关数据；
- 尺寸和性能曲线等。

## 控制 IMU

### STMicroelectronics LSM6DSV16X

在 Microduck 中的角色：官方源码确认的 `imu_to_dxl` 控制 IMU。

官方产品页 / Datasheet 入口：

- https://www.st.com/en/mems-and-sensors/lsm6dsv16x.html

传感器量程、ODR、接口、register、noise / performance、电气限制等，应优先看 ST 官方资料。

## 第二 / 开发 IMU

### Bosch BMI088

在 Microduck 中的角色：当前官方 development HAT 描述里能看到这个器件；源码注释表明该路径当前处于 dormant / unused 状态。

官方产品页：

- https://www.bosch-sensortec.com/products/motion-sensors/imus/bmi088/

不能仅凭这里出现 BMI088，就自动把它写成“最终量产第二 IMU”，除非以后有更强的官方产品级证据。

## 音频 Codec

### Texas Instruments TLV320AIC3104

在 Microduck 中的角色：官方源码中的开发 HAT 音频 codec。

官方产品页：

- https://www.ti.com/product/TLV320AIC3104

可以用于查 codec interface、I2C control、I2S/audio serial format、clock、ADC/DAC path、电气要求等。

## Camera 路径

### Sony IMX219 / Raspberry Pi Camera Module v2 路径

在 Microduck 中的角色：当前官方源码 camera bring-up 路径。

官方资料：

- Raspberry Pi Camera Module 2：https://www.raspberrypi.com/products/camera-module-v2/
- Raspberry Pi Camera 文档：https://www.raspberrypi.com/documentation/computers/camera_software.html

Microduck 官方 Press Kit 目前仍明确把最终 camera resolution 和 FOV 标为 provisional。因此，不能用当前 development module / driver path 去自行定义最终量产光学参数。

## Multi-zone ToF

### ST VL53L5CX

官方产品页：

- https://www.st.com/en/imaging-and-photonics-solutions/vl53l5cx.html

### ST VL53L8CX

官方产品页：

- https://www.st.com/en/imaging-and-photonics-solutions/vl53l8cx.html

在 Microduck 中的角色：公开官方源码中能看到这两个 family 的相关支持；产品级只明确承诺 compact **8×8 ToF matrix**，最终量产 sensor model 和 range 仍未完全确认。

ST 官方文档适合继续查：

- zone configuration；
- ranging mode；
- interface；
- calibration；
- timing；
- electrical limit。

## 电池

### NP-F550 规格，产品级标称 2600 mAh

Microduck 官方产品规格写的是可拆卸 NP-F550 camera battery，2600 mAh。

`NP-F550` 更像一个广泛使用的电池规格 / family，并不是某一家厂商唯一的一颗器件型号。

所以在 OpenMicroDuck 中：

- 机器人级要求以 Pollen Robotics 官方产品规格为准；
- 如果未来实测某一块具体电池，则应同时记录那块电池自己的品牌和 datasheet / label 信息。

不能拿任意第三方 NP-F550 的参数，直接当成 Microduck 量产电池的官方参数。

## Datasheet 应该怎样正确使用

Datasheet 能说明一个器件**具备哪些能力**，但不能自动证明 Microduck 实际怎样配置它。

可以这样理解：

```text
原厂 Datasheet
    → 器件支持的范围 / register / limit

Microduck 官方源码
    → 实际使用了哪个 mode、rate、address、interface

真实硬件实测
    → 某台具体机器最终表现怎样
```

三种证据都有价值，但来源等级不一样。

## 相关页面

- [公开硬件清单与 BOM 状态](public-bom.md)
- [电控、总线、传感器与电源](electronics-and-buses.md)
- [待确认问题与来源冲突](../research/open-questions-and-conflicts.md)
- [资料来源与证据地图](../sources.md)
