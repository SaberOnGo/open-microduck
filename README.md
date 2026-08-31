# OpenMicroDuck

**Independent Microduck reverse engineering, hardware research, simulation, reinforcement learning, and sim-to-real robotics project.**

> **Unofficial and independent project.** OpenMicroDuck is not affiliated with, endorsed by, sponsored by, or officially connected with Pollen Robotics or Hugging Face. `Microduck` and related names, marks, and branding belong to their respective owners.

OpenMicroDuck is a community-oriented research project focused on understanding the architecture and behavior of **Microduck**, building reproducible simulation models, studying compact biped robot hardware, and developing independently designed robotics systems.

The project aims to turn scattered research into reproducible engineering knowledge: from servos, sensors, buses, and control electronics to physics simulation, reinforcement learning, domain randomization, and sim-to-real deployment.

## Goals

- Study and document the observable hardware and software architecture of Microduck.
- Build reproducible Microduck-oriented simulation models.
- Research servo dynamics, latency, backlash, friction, power behavior, and communication buses.
- Model sensors such as IMUs, cameras, ranging sensors, and joint feedback.
- Develop reinforcement-learning workflows for locomotion, recovery, manipulation, and other embodied behaviors.
- Develop practical sim-to-real methods, including domain randomization and system identification.
- Design and validate independently developed mechanical, electronic, firmware, and control solutions.
- Make compact embodied-robotics research easier to reproduce for developers, students, researchers, and hobbyists.

## Project Scope

```text
OpenMicroDuck
├── hardware/       Mechanical, electronic, servo, sensor, and power research
├── simulation/     Robot models, physics parameters, environments, and validation
├── control/        MCU, servo bus, low-level control, timing, and robot I/O
├── learning/       RL policies, locomotion, recovery, manipulation, and sim-to-real
└── docs/           Research notes, methodology, architecture, roadmap, and references
```

The project may study Microduck as a reference system, but the long-term goal is **independent engineering and reproducible research**, not redistribution of proprietary mechanical or electronic design files.

## Research Areas

### Hardware

- Servo characterization and actuator modeling
- Joint layout and kinematics
- Main controller and auxiliary MCU architecture
- Servo-bus topology and timing
- IMU and other sensor integration
- Power distribution and battery behavior
- Mechanical mass, inertia, friction, and backlash estimation

### Simulation

- Robot description and rigid-body model
- Joint limits and actuator constraints
- Contact and friction modeling
- Sensor noise and latency
- Voltage and torque variation
- Parameter identification
- Domain randomization
- Simulation-to-real validation

### Reinforcement Learning

- Standing and balancing
- Walking and turning
- Fall recovery
- Dynamic locomotion
- Manipulation
- Multi-skill policies
- Policy deployment on physical hardware

## Research Method

OpenMicroDuck favors reproducible, evidence-based engineering. Parameters should be derived from one or more of:

1. Publicly available documentation and software.
2. Direct measurements on legally obtained hardware.
3. Black-box behavioral testing and system identification.
4. Independent mechanical/electronic design and prototyping.
5. Simulation-to-real comparison and iterative calibration.

Measured values, inferred values, assumptions, and placeholders should be clearly distinguished in project documentation.

## Current Status

The repository is in its **initial research and architecture phase**. Early work focuses on:

- establishing the project documentation structure;
- collecting verifiable Microduck architecture information;
- characterizing candidate servos and sensors;
- defining the simulation parameter set;
- designing the control architecture needed for simulation and future physical prototypes.

See [`docs/ROADMAP.md`](docs/ROADMAP.md) for the working roadmap.

## Relationship to Microduck

Microduck is used here as a research reference and search term because this project studies that robot and related compact embodied-robotics techniques.

OpenMicroDuck is an **independent, unofficial project**. It does not claim to be an official Microduck repository, an authorized derivative product, or a Pollen Robotics / Hugging Face project.

Where upstream open-source software is used or modified, its original license and attribution requirements must be preserved.

## Contributing

Research contributions are welcome, especially reproducible measurements, simulation validation, actuator characterization, control experiments, and clearly sourced technical documentation.

Before contributing reverse-engineering results, please read [`docs/RESEARCH_GUIDELINES.md`](docs/RESEARCH_GUIDELINES.md).

## License

A repository-wide license has **not yet been selected**. Until a license is added, do not assume that repository contents are licensed for unrestricted reuse.

Third-party components retain their original licenses and copyrights.

## Disclaimer

This repository is provided for independent research, interoperability study, education, experimentation, and development. Contributors are responsible for ensuring that their contributions do not include confidential information, unlawfully obtained material, or proprietary files copied from third parties.

See [`DISCLAIMER.md`](DISCLAIMER.md) for details.

---

**Search topics:** Microduck, Microduck reverse engineering, Microduck hardware, Microduck simulation, Microduck reinforcement learning, Microduck RL, Microduck servo, Microduck DIY, sim-to-real robotics, compact biped robot, embodied robotics.
