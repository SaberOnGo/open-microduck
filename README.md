# OpenMicroDuck

[English](README.md) | [简体中文](README.zh-CN.md)

**Independent, unofficial Microduck research, reverse-engineering, simulation, and documentation project.**

> OpenMicroDuck is not affiliated with, endorsed by, sponsored by, or officially connected with Pollen Robotics or Hugging Face. Microduck and related names, logos, trademarks, and branding belong to their respective owners.

OpenMicroDuck organizes publicly available information about **Microduck** into a source-driven technical reference. The project focuses on public hardware information, mechanical structure, software architecture, simulation, reinforcement learning, interoperability research, and reproducible community reverse engineering.

The repository does **not** claim that Microduck is open-source hardware. Pollen Robotics currently states that the open-source commitment covers the software stack, while the mechanical and electronic design files are not published as open-source hardware.

## What is documented here

- public and source-code-derived hardware inventory;
- motors, joint layout, sensors, compute, battery, buses, and control-loop information;
- mechanical and kinematic structure derived from publicly released simulation assets;
- official runtime and reinforcement-learning architecture;
- community reverse-engineering, simulation, CAD reconstruction, and tooling projects;
- provenance, confidence labels, licensing notes, and known inconsistencies between sources.

## Start here

| Topic | English | 中文 |
|---|---|---|
| Documentation index | [docs/en/README.md](docs/en/README.md) | [docs/zh-CN/README.md](docs/zh-CN/README.md) |
| Public hardware inventory / BOM status | [docs/en/hardware/public-bom.md](docs/en/hardware/public-bom.md) | [docs/zh-CN/hardware/public-bom.md](docs/zh-CN/hardware/public-bom.md) |
| Mechanical structure | [docs/en/hardware/mechanical-structure.md](docs/en/hardware/mechanical-structure.md) | [docs/zh-CN/hardware/mechanical-structure.md](docs/zh-CN/hardware/mechanical-structure.md) |
| Electronics and buses | [docs/en/hardware/electronics-and-buses.md](docs/en/hardware/electronics-and-buses.md) | [docs/zh-CN/hardware/electronics-and-buses.md](docs/zh-CN/hardware/electronics-and-buses.md) |
| Runtime architecture | [docs/en/software/runtime-architecture.md](docs/en/software/runtime-architecture.md) | [docs/zh-CN/software/runtime-architecture.md](docs/zh-CN/software/runtime-architecture.md) |
| Simulation and RL | [docs/en/simulation/model-and-rl.md](docs/en/simulation/model-and-rl.md) | [docs/zh-CN/simulation/model-and-rl.md](docs/zh-CN/simulation/model-and-rl.md) |
| Reverse-engineering ecosystem | [docs/en/ecosystem/reverse-engineering-projects.md](docs/en/ecosystem/reverse-engineering-projects.md) | [docs/zh-CN/ecosystem/reverse-engineering-projects.md](docs/zh-CN/ecosystem/reverse-engineering-projects.md) |
| Sources and evidence | [docs/en/sources.md](docs/en/sources.md) | [docs/zh-CN/sources.md](docs/zh-CN/sources.md) |
| Licensing and provenance | [docs/en/legal/provenance-and-licenses.md](docs/en/legal/provenance-and-licenses.md) | [docs/zh-CN/legal/provenance-and-licenses.md](docs/zh-CN/legal/provenance-and-licenses.md) |

## Evidence policy

Technical statements should be labeled or written so readers can distinguish:

- **Official product spec** — published by Pollen Robotics / Hugging Face;
- **Official source** — visible in the upstream software, simulation model, configuration, or hardware bring-up notes;
- **Community reconstruction** — independently derived from public assets or observation;
- **Unverified / provisional** — plausible or present in a development branch, but not established as a final production specification.

When official product documentation and a community reconstruction disagree, the official source takes precedence and the discrepancy should be recorded rather than silently resolved.

## Repository structure

```text
open-microduck/
├── README.md
├── README.zh-CN.md
├── docs/
│   ├── en/                 English documentation
│   └── zh-CN/              Simplified Chinese documentation
├── hardware/               Project-owned hardware research outputs
├── simulation/             Project-owned simulation research outputs
├── control/                Project-owned control/interoperability research
└── learning/               Project-owned learning/reproducibility research
```

Additional languages can be added as sibling documentation trees such as `docs/ja/`, `docs/fr/`, or `docs/de/` without changing the English canonical paths.

## Upstream projects

The primary upstream references are:

- Pollen Robotics Microduck: https://github.com/pollen-robotics/microduck
- Microduck RL: https://github.com/pollen-robotics/microduck_rl
- Product page: https://pollen-robotics.com/microduck/
- Press kit / public specifications: https://pollen-robotics.com/microduck/press-kit/

Community projects are indexed separately in the reverse-engineering ecosystem documents; inclusion there does not imply endorsement or verification.

## Contributions

Corrections, source-backed technical notes, reproducible measurements, independent reconstructions, simulation validation, and links to relevant public projects are welcome.

Please read [CONTRIBUTING.md](CONTRIBUTING.md), [DISCLAIMER.md](DISCLAIMER.md), and the research guidelines before submitting material.

Do not submit leaked or confidential information, unlawfully obtained proprietary files, private credentials, or third-party material without compatible rights and attribution.

## License status

No repository-wide license has been selected yet. Third-party materials retain their original licenses and restrictions. In particular, some upstream Microduck 3D model assets are distributed under **CC BY-SA-NC**, while upstream software repositories use their stated software licenses. See the provenance documentation before copying or redistributing assets.

---

**Search topics:** Microduck, Microduck reverse engineering, Microduck hardware, Microduck BOM, Microduck teardown, Microduck CAD, Microduck simulation, Microduck reinforcement learning, Microduck RL, Dynamixel XL330, Microduck robot model, Microduck sim-to-real.