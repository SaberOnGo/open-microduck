# OpenMicroDuck

<p align="center"><strong>🌐 Language / 语言</strong></p>
<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/ENGLISH-1f6feb?style=for-the-badge" alt="English" height="44"></a>&nbsp;&nbsp;
  <a href="README.zh-CN.md"><img src="https://img.shields.io/badge/%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-d73a49?style=for-the-badge" alt="简体中文" height="44"></a>
</p>

**Independent, unofficial Microduck research, reverse-engineering, simulation, and documentation project.**

OpenMicroDuck turns public Microduck information into a practical reference: what the robot contains, how its software works, how the movement AI is trained and deployed, and which details are still unknown.

> OpenMicroDuck is not affiliated with or endorsed by Pollen Robotics or Hugging Face. It does not claim that Microduck is open-source hardware. Public evidence shows an open software stack, while complete production mechanical/electronic design files are not published as open-source hardware.

## Microduck in 20 seconds

```text
Camera ──► vision AI ──────────────┐
ToF ────► obstacle geometry ───────┼──► behavior decision
Other sensors ─────────────────────┘      “walk / look / kick”
                                              │
                                              ▼
                                      movement RL policy
                                      61 inputs → 14 actions
                                              │
                                              ▼
                                     safety + motor control
                                              │
                                              ▼
                                           15 motors
```

The standard walking policy does **not** directly consume camera images or the raw 8×8 ToF frame. Camera perception, ToF processing, high-level behavior, movement AI, and motor control are separate layers.

## Start here

| Goal | Read this |
|---|---|
| Understand the whole robot | [Start Here](docs/en/getting-started/README.md) |
| Understand the software architecture | [How the Microduck Software Fits Together](docs/en/software/runtime-architecture.md) |
| Run the virtual robot first | [Simulation First](docs/en/getting-started/simulation-first.md) |
| Follow a reproduction path | [Public Reproduction Roadmap](docs/en/getting-started/public-reproduction-roadmap.md) |
| Bring up real hardware safely | [Hardware Bring-up and Calibration](docs/en/getting-started/hardware-bringup-and-calibration.md) |
| Understand high-level behavior | [Autonomous Brain](docs/en/software/autonomous-brain.md) |
| Understand geometry and position estimation | [Kinematics and Odometry](docs/en/software/kinematics-and-odometry.md) |
| Find hardware-bus details | [`robotd` Hardware Protocol](docs/en/software/robotd-hardware-protocol.md) |
| Find hardware parameters | [Hardware Parameter Reference](docs/en/hardware/parameter-reference.md) |
| Understand assembly | [Structure and Assembly Map](docs/en/hardware/structure-and-assembly-map.md) |
| Find sim-to-real values | [Sim-to-Real Parameter Reference](docs/en/simulation/sim-to-real-parameter-reference.md) |

## Four numbers to remember

| Number | Meaning |
|---:|---|
| **15** | physical motor IDs in the current runtime |
| **14** | joints controlled by the locomotion policy |
| **61** | standard movement-policy input width |
| **50 Hz** | movement-control frequency |

## Documentation

### Hardware

- [Hardware Parameter Reference](docs/en/hardware/parameter-reference.md)
- [Structure and Assembly Map](docs/en/hardware/structure-and-assembly-map.md)
- [Public Hardware / BOM Status](docs/en/hardware/public-bom.md)
- [Electronics, Buses, Sensors, and Power](docs/en/hardware/electronics-and-buses.md)
- [Community BOM Reconstruction](docs/en/hardware/community-bom-reconstruction.md)

### Software

- [How the Microduck Software Fits Together](docs/en/software/runtime-architecture.md)
- [Control Loop: How the Robot Moves](docs/en/software/control-loop-and-sensor-dataflow.md)
- [Autonomous Brain and High-Level Behavior](docs/en/software/autonomous-brain.md)
- [Kinematics and Odometry](docs/en/software/kinematics-and-odometry.md)
- [`robotd` Hardware Protocol](docs/en/software/robotd-hardware-protocol.md)
- [Hardware Bring-up and Calibration](docs/en/getting-started/hardware-bringup-and-calibration.md)

### Simulation and learning

- [Simulation and Reinforcement Learning](docs/en/simulation/model-and-rl.md)
- [Policy Catalog and Switching](docs/en/simulation/policy-catalog-and-switching.md)
- [Reproducible Training and ONNX Export](docs/en/simulation/reproducible-training-and-export.md)
- [Sim-to-Real Parameter Reference](docs/en/simulation/sim-to-real-parameter-reference.md)

### Tools

- [Upstream Parameter Diff Tool](tools/upstream-diff/README.md)

### Sources and research status

- [Official Specification Baseline](docs/en/product/official-specifications.md)
- [Open Questions and Source Conflicts](docs/en/research/open-questions-and-conflicts.md)
- [Upstream Version Matrix](docs/en/upstream/version-matrix.md)
- [Sources and Evidence Map](docs/en/sources.md)
- [Full Documentation Index](docs/en/README.md)

## Evidence labels

OpenMicroDuck separates:

- **Official product spec** — public product-level statements;
- **Official source** — directly visible in official code/docs;
- **Official simulation model** — values from released simulation assets;
- **Community reconstruction** — public third-party derivation;
- **Measured** — reproducible physical measurement;
- **Unresolved** — not enough public evidence yet.

Unknown values stay unknown instead of being guessed.

## Public-only rule

Do not submit confidential, leaked, private, or otherwise non-public engineering information. Third-party assets must have compatible rights and attribution.

See [Research Guidelines](docs/en/research-guidelines.md), [Contributing](CONTRIBUTING.md), and [Provenance and Licensing](docs/en/legal/provenance-and-licenses.md).

## Primary upstream references

- https://github.com/pollen-robotics/microduck
- https://github.com/pollen-robotics/microduck_rl
- https://pollen-robotics.com/microduck/
- https://pollen-robotics.com/microduck/press-kit/
