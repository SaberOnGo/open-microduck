# OpenMicroDuck

<p align="center"><strong>🌐 Language / 语言</strong></p>
<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/ENGLISH-1f6feb?style=for-the-badge" alt="English" height="44"></a>&nbsp;&nbsp;
  <a href="README.zh-CN.md"><img src="https://img.shields.io/badge/%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-d73a49?style=for-the-badge" alt="简体中文" height="44"></a>
</p>

**Independent, unofficial Microduck research, reverse-engineering, simulation, and documentation project.**

OpenMicroDuck organizes publicly available information about **Microduck** into a readable, source-driven technical reference. It covers public hardware information, BOM research, mechanical structure, electronics, onboard software, simulation, reinforcement learning, sim-to-real parameters, and reproducible community reverse engineering.

**简体中文简介：** OpenMicroDuck 是一个独立、非官方的 **Microduck 逆向分析与技术资料整理项目**。完整中文内容请点击上方 **「简体中文」** 按钮。

> OpenMicroDuck is not affiliated with, endorsed by, sponsored by, or officially connected with Pollen Robotics or Hugging Face. Microduck and related names, logos, trademarks, and branding belong to their respective owners.

The repository does **not** claim that Microduck is open-source hardware. Pollen Robotics states that the open-source commitment covers the software stack; the mechanical and electronic design files are not published as open-source hardware.

## New to Microduck? Start here

The project is intentionally organized so a reader does not need to understand robotics, RL and electronics all at once.

| If you want to… | Start with… |
|---|---|
| Understand the whole project in a few minutes | [Start Here](docs/en/getting-started/README.md) |
| See Microduck move before buying hardware | [Simulation First](docs/en/getting-started/simulation-first.md) |
| Follow a staged public reproduction path | [Public Reproduction Roadmap](docs/en/getting-started/public-reproduction-roadmap.md) |
| Find motor IDs, home pose, masses, bus/IMU/battery parameters | [Hardware Parameter Reference](docs/en/hardware/parameter-reference.md) |
| Understand how the structure is assembled | [Structure and Assembly Map](docs/en/hardware/structure-and-assembly-map.md) |
| Find BAM, delay, backlash, voltage and domain-randomization values | [Sim-to-Real Parameter Reference](docs/en/simulation/sim-to-real-parameter-reference.md) |

A practical research sequence is:

```text
official model + existing ONNX in simulation
              ↓
understand joints / mass / structure
              ↓
reproduce one training task
              ↓
understand the 50 Hz bus + IMU dataflow
              ↓
small hardware benches
              ↓
mechanical subassemblies
              ↓
full research assembly and sim-to-real comparison
```

## Four numbers that explain much of the architecture

| Number | Meaning |
|---:|---|
| **15** | physical motor IDs in the current runtime, including the mouth/beak |
| **14** | joints controlled by the locomotion RL policy |
| **61** | shared actor-observation width of the current policy family |
| **50 Hz** | locomotion policy/runtime control frequency |

## Confirmed components at a glance

The table names concrete parts whenever public sources allow it. “Development/reference” means the part is directly visible in the current official source tree but is not necessarily guaranteed to be the final production BOM item.

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

## Documentation map

### Getting started / public reproduction

- [Start Here](docs/en/getting-started/README.md)
- [Simulation First](docs/en/getting-started/simulation-first.md)
- [Public Reproduction Roadmap](docs/en/getting-started/public-reproduction-roadmap.md)

### Hardware and mechanics

- [Hardware parameter reference](docs/en/hardware/parameter-reference.md)
- [Structure and assembly map](docs/en/hardware/structure-and-assembly-map.md)
- [Public hardware inventory and BOM status](docs/en/hardware/public-bom.md)
- [Community-derived BOM, fasteners, bearings, and assembly reconstruction](docs/en/hardware/community-bom-reconstruction.md)
- [Mechanical structure and kinematics](docs/en/hardware/mechanical-structure.md)
- [Electronics, buses, sensors, and power](docs/en/hardware/electronics-and-buses.md)
- [Public component datasheet index](docs/en/hardware/component-datasheets.md)

### Software, control, simulation and learning

- [Control loop and sensor dataflow](docs/en/software/control-loop-and-sensor-dataflow.md)
- [Onboard runtime architecture](docs/en/software/runtime-architecture.md)
- [Simulation and reinforcement learning](docs/en/simulation/model-and-rl.md)
- [Policy catalog and runtime switching](docs/en/simulation/policy-catalog-and-switching.md)
- [Reproducible training and ONNX export](docs/en/simulation/reproducible-training-and-export.md)
- [Simulation model assets reference](docs/en/simulation/model-assets-reference.md)
- [Sim-to-real parameter reference](docs/en/simulation/sim-to-real-parameter-reference.md)

### Research status, ecosystem and provenance

- [Official specification baseline](docs/en/product/official-specifications.md)
- [Open questions and source conflicts](docs/en/research/open-questions-and-conflicts.md)
- [Upstream version matrix](docs/en/upstream/version-matrix.md)
- [Reviewed reverse-engineering and community projects](docs/en/ecosystem/reverse-engineering-projects.md)
- [Sources and evidence map](docs/en/sources.md)
- [Research guidelines](docs/en/research-guidelines.md)
- [Provenance and licensing](docs/en/legal/provenance-and-licenses.md)
- [Full documentation index](docs/en/README.md)

## Evidence policy

Technical statements should distinguish:

- **Official product spec** — published product/press/store information;
- **Official source** — directly visible in upstream source code or design documentation;
- **Official simulation model** — values/geometry from released simulation assets, not automatically a production measurement;
- **Community reconstruction** — independently derived from public assets or observation;
- **Measured** — reproducible real-hardware measurements with test conditions;
- **Unresolved / provisional** — not established well enough to present as final production fact.

When sources disagree, the discrepancy is recorded instead of silently turning an inference into an official specification.

## Language and documentation structure

English is the default repository language. Simplified Chinese is a first-class documentation language rather than a summary translation.

```text
open-microduck/
├── README.md
├── README.zh-CN.md
└── docs/
    ├── en/
    │   ├── getting-started/   beginner/public-reproduction path
    │   ├── product/           official product baseline
    │   ├── hardware/          parts, mechanics, buses, parameters
    │   ├── software/          runtime and control
    │   ├── simulation/        models, RL, sim-to-real
    │   ├── research/          unresolved questions
    │   ├── ecosystem/         community projects
    │   ├── upstream/          version snapshots
    │   └── legal/             provenance/licenses
    └── zh-CN/                 matching Simplified Chinese tree
```

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

**Search topics:** Microduck, Microduck reverse engineering, Microduck hardware, Microduck BOM, Microduck teardown, Microduck CAD, Microduck electronics, Microduck components, Microduck simulation, Microduck reinforcement learning, Microduck RL, Dynamixel XL330, LSM6DSV16X, Radxa Zero 3W, Microduck robot model, Microduck sim-to-real, Microduck 逆向, Microduck 硬件, Microduck BOM, Microduck 仿真, Microduck 强化学习.
