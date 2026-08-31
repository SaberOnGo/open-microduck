# Public Hardware Inventory / BOM Status

> Status: public-source reconstruction, last checked 2026-08-31.

Microduck does **not** currently have an official public hardware BOM. Pollen Robotics' press kit explicitly says that the open-source statement covers the software stack and that the mechanical/electronic design files are not published as open-source hardware.

This page therefore uses the term **public hardware inventory**, not “official BOM”. Each row states the evidence level.

## Evidence levels

- **Official product spec** — public Pollen Robotics product/press material.
- **Official source** — identifiable in Pollen Robotics source code, configuration, simulation model, or hardware bring-up notes.
- **Community reconstruction** — derived by third parties from public assets; useful, but not an official specification.
- **Provisional** — visible in current development material but not necessarily a final production choice.

## Public inventory

| Subsystem | Publicly identified component / property | Evidence | Notes |
|---|---|---|---|
| Robot size | 25 cm tall, 14 cm wide | Official product spec | Press kit; dimensions described as product specs. |
| Robot mass | under 800 g | Official product spec | The official RL repo describes the model as ~800 g. Third-party model reconstructions report lower exact model-derived values; those are not treated as production weight. |
| Compute SoC | Rockchip RK3566 with AI accelerator | Official product spec | 1 GB RAM, 32 GB storage are listed in the press kit. |
| Current development board | Radxa Zero 3 / Zero 3W | Official source, provisional | Upstream hardware bring-up and deployment docs use Radxa Zero 3/3W. Some design docs explicitly describe the board choice as provisional during development, so the board identity should be distinguished from the final public RK3566 product spec. |
| Motors | 15 motors | Official product spec | Upstream runtime models 15 joints: 5 left leg + 5 neck/head/mouth + 5 right leg. |
| Servo family | Dynamixel XL330 | Official source | The RL stack uses a BAM actuator model for Dynamixel XL330; the MJCF includes XL330 geometry. |
| Policy-controlled joints | 14 | Official source | 5 left leg + 4 neck/head + 5 right leg. The mouth is the 15th motor and is controlled outside the locomotion policy action vector. |
| Mouth / beak | articulated grasping beak | Official product spec + source | Runtime source includes a separate mouth joint and open/closed travel handling. |
| Main control IMU | LSM6DSV16X on `imu_to_dxl` v2 | Official source | The control source explicitly decodes this device and reads it on the Dynamixel bus. |
| Total IMUs | 2, body + head | Official product spec | The exact production chip identity of both IMUs is not fully specified by the public press kit. Do not assume that every development-board IMU seen in source is a final production part. |
| Range sensor | compact 8×8 ToF matrix | Official product spec | Upstream source includes support for ST VL53L5CX/VL53L8CX families. Exact production model should be treated as unresolved until officially fixed. |
| Camera | front camera | Official product spec | Resolution/FOV are explicitly described as not final in the press kit. Current hardware bring-up uses a Raspberry Pi Camera v2 / IMX219 path on Radxa Zero 3W. |
| Audio | microphones + speaker | Official product spec | Current source tree contains TLV320AIC3104 support for the development hardware audio path. |
| NFC | 2 antennas: head + beak | Official product spec | Intended for tag-triggered interactions. |
| Connectivity | Wi-Fi + Bluetooth | Official product spec | Upstream runtime includes BLE provisioning/gamepad paths and network/WebRTC components. |
| Battery | removable NP-F550 camera battery, 2600 mAh | Official product spec | Around one hour runtime depending on use. Upstream control source describes a 2S Li-ion operating span and reads supply voltage through the servo bus. |
| Rollers | optional passive roller attachments | Official product/accessory info + RL assets | RL repo includes separate roller robot models with passive wheel joints. |
| Bearings / fasteners | not officially BOM'd | Community reconstruction | Public simulation meshes contain bearing geometry and hole features; independent projects have derived approximate bearing and M2 fastener systems. Treat these as model-derived until verified on production hardware. |
| Custom PCBs | present in development/reference assets, schematics not public | Official source + community reconstruction | Public source identifies interfaces and device behavior, but no official complete production PCB BOM/schematic is published. |

## Official motor map in the current runtime

The upstream `duck-control/src/model.rs` defines 15 Dynamixel IDs:

```text
left leg       20 21 22 23 24
neck/head/beak 30 31 32 33 34
right leg      10 11 12 13 14
IMU board      200 (not a motor)
```

The same source states that the mouth occupies index 9 and is intentionally omitted from the 14-action policy output.

## What is *not* an official BOM

Several useful details circulating in community projects come from the released MJCF/STL assets, source-code inspection, or inferred wiring. Examples include exact fastener counts, bearing quantities, PCB dimensions, internal bracket geometry, and assembly ordering.

These can be valuable engineering observations, but they must remain labeled as **community reconstruction** unless confirmed by Pollen Robotics or by reproducible measurements on production hardware.

## Known source conflicts / moving targets

### Battery geometry versus product battery

Some public simulation assets and community repositories contain an `NP-F970`-named mesh or discuss F970-compatible geometry. The official 2026 press kit specifies a **removable NP-F550, 2600 mAh** battery for the product. This repository therefore treats NP-F550 as the product specification and the F970 references as model/development evidence only.

### Exact camera and ToF part numbers

The product press kit intentionally leaves camera resolution/FOV and LiDAR range provisional. The current source tree contains concrete drivers and hardware bring-up for IMX219 and ST multi-zone ToF devices, but those development choices should not automatically be promoted to immutable production BOM entries.

### Exact modeled mass

The official product statement is “under 800 g” and the RL repository says ~800 g. Third-party transforms of the public MJCF report a more precise model mass. Precision from a simulation asset is not the same thing as a production scale measurement.

## Primary sources

- https://pollen-robotics.com/microduck/press-kit/
- https://pollen-robotics.com/microduck/
- https://github.com/pollen-robotics/microduck
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/model.rs
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/imu.rs
- https://github.com/pollen-robotics/microduck_rl

## Community reconstruction references

- https://github.com/fanhao375/microduck-replica
- https://github.com/boris721/microduck-3d

See [../ecosystem/reverse-engineering-projects.md](../ecosystem/reverse-engineering-projects.md) for a broader project index and provenance notes.
