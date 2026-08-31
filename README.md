# OpenMicroDuck

**English** | [简体中文](README.zh-CN.md)

**Independent, unofficial Microduck research, reverse-engineering, simulation, and documentation project.**

> OpenMicroDuck is not affiliated with, endorsed by, sponsored by, or officially connected with Pollen Robotics or Hugging Face. Microduck and related names, logos, trademarks, and branding belong to their respective owners.

OpenMicroDuck organizes publicly available information about **Microduck** into a source-driven technical reference. It focuses on public hardware information, mechanical structure, software architecture, simulation, reinforcement learning, interoperability research, and reproducible community reverse engineering.

The repository does **not** claim that Microduck is open-source hardware. Pollen Robotics states that the open-source commitment covers the software stack; the mechanical and electronic design files are not published as open-source hardware.

## Confirmed components at a glance

The table below names concrete parts whenever public sources allow it. “Development/reference” means the part is directly visible in the current official source tree but is not necessarily guaranteed to be the final production BOM item.

| Subsystem | Identified component | Status |
|---|---|---|
| Main compute | **Radxa Zero 3W** | Official-source development/reference platform |
| SoC | **Rockchip RK3566** | Official product specification |
| Memory / storage | **1 GB RAM / 32 GB storage** | Official product specification |
| Actuators | **ROBOTIS Dynamixel XL330 ×15** | Official source; exact XL330 sub-variant not confirmed |
| Control IMU | **ST LSM6DSV16X** on **`imu_to_dxl` v2** | Official source |
| Audio codec | **Texas Instruments TLV320AIC3104** | Official-source development hardware |
| Secondary HAT IMU | **Bosch BMI088** | Official-source development hardware; marked dormant/unused |
| Front camera | **Sony IMX219 / Raspberry Pi Camera v2 path** | Official-source development hardware |
| 8×8 ToF | **ST VL53L5CX / VL53L8CX family support** | Official source; final production part unresolved |
| Battery | **NP-F550, 2600 mAh** | Official product specification |
| NFC | **2 antennas: head + beak** | Official product specification; controller IC not publicly identified |
| Audio transducers | microphones + speaker | Official product specification; exact parts not publicly identified |

For evidence, bus addresses, board names, unresolved parts, and community-derived fasteners/bearings, see the hardware documentation below.

## Documentation

### Hardware

- [Public hardware inventory and BOM status](docs/en/hardware/public-bom.md)
- [Community-derived BOM, fasteners, bearings, and assembly reconstruction](docs/en/hardware/community-bom-reconstruction.md)
- [Mechanical structure and kinematics](docs/en/hardware/mechanical-structure.md)
- [Electronics, buses, sensors, and power](docs/en/hardware/electronics-and-buses.md)

### Software, simulation, and learning

- [Onboard runtime architecture](docs/en/software/runtime-architecture.md)
- [Simulation and reinforcement learning](docs/en/simulation/model-and-rl.md)

### Research ecosystem and provenance

- [Reviewed reverse-engineering and community projects](docs/en/ecosystem/reverse-engineering-projects.md)
- [Broader GitHub repository discovery snapshot](docs/en/ecosystem/discovered-repositories.md)
- [Sources and evidence map](docs/en/sources.md)
- [Research guidelines](docs/en/research-guidelines.md)
- [Provenance and licensing](docs/en/legal/provenance-and-licenses.md)
- [Documentation index](docs/en/README.md)

## Evidence policy

Technical statements should distinguish:

- **Official product spec** — published product/press/store information;
- **Official source** — directly visible in upstream source code, configuration, simulation assets, or hardware bring-up notes;
- **Community reconstruction** — independently derived from public assets or observation;
- **Unverified / provisional** — plausible or present in development material but not established as a final production specification.

When sources disagree, the discrepancy is recorded instead of silently turning an inference into an official specification.

## Language structure

English is the default repository language. Simplified Chinese is a first-class documentation language rather than a summary translation.

```text
open-microduck/
├── README.md                 English home page
├── README.zh-CN.md           Simplified Chinese home page
├── docs/
│   ├── en/                   English documentation tree
│   └── zh-CN/                Simplified Chinese documentation tree
├── hardware/                 public research outputs / code / assets
├── simulation/               public research outputs / code / assets
├── control/                  public research outputs / code / assets
└── learning/                 public research outputs / code / assets
```

Future languages can be added as sibling trees such as `docs/ja/`, `docs/fr/`, or `docs/de/`.

## Primary upstream references

- Pollen Robotics Microduck: https://github.com/pollen-robotics/microduck
- Microduck RL: https://github.com/pollen-robotics/microduck_rl
- Product page: https://pollen-robotics.com/microduck/
- Press kit: https://pollen-robotics.com/microduck/press-kit/

## Contributions

Corrections, source-backed technical notes, reproducible public measurements, independent reconstructions from public sources, simulation validation, and links to relevant public projects are welcome.

Please read [CONTRIBUTING.md](CONTRIBUTING.md), [DISCLAIMER.md](DISCLAIMER.md), and the [research guidelines](docs/en/research-guidelines.md).

Do not submit leaked, confidential, private, unrelated proprietary, or otherwise non-public engineering information; unlawfully obtained proprietary files; private credentials; or third-party material without compatible rights and attribution.

## License status

No repository-wide license has been selected yet. Third-party materials retain their original licenses and restrictions. In particular, some upstream Microduck 3D model assets are distributed under **CC BY-SA-NC**, while upstream software repositories use their stated software licenses. See the provenance documentation before copying or redistributing assets.

---

**Search topics:** Microduck, Microduck reverse engineering, Microduck hardware, Microduck BOM, Microduck teardown, Microduck CAD, Microduck simulation, Microduck reinforcement learning, Microduck RL, Dynamixel XL330, LSM6DSV16X, Radxa Zero 3W, Microduck robot model, Microduck sim-to-real.