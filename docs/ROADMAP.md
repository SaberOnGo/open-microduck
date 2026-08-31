# OpenMicroDuck Roadmap

This roadmap is intentionally research-first. Items move from observation and measurement to simulation, control, physical validation, and finally independent hardware refinement.

## Phase 0 — Repository foundation

- Define project scope and contribution rules.
- Separate measured facts, public-source facts, inferred values, and assumptions.
- Establish hardware, simulation, control, learning, and documentation areas.
- Record upstream software licenses and third-party references.

## Phase 1 — Microduck architecture study

- Collect verifiable public information about the robot architecture.
- Document joint count, kinematic layout, sensors, compute, communication buses, and power architecture where observable or publicly documented.
- Build a component inventory with confidence levels and sources.
- Identify parameters that require direct measurement.

## Phase 2 — Actuator and sensor characterization

- Characterize candidate servos and their communication protocol.
- Measure or estimate speed, torque, deadband, backlash, friction, latency, current draw, and voltage sensitivity.
- Characterize IMU and other relevant sensor noise, latency, range, and update rate.
- Record test rigs and repeatable measurement procedures.

## Phase 3 — First simulation model

- Build the initial rigid-body and joint model.
- Add actuator limits and approximate dynamics.
- Add contact, friction, mass, inertia, and sensor models.
- Validate basic standing and commanded joint trajectories.

## Phase 4 — Low-level control architecture

- Define the main-compute to MCU boundary.
- Define servo-bus timing and update loops.
- Implement deterministic robot I/O abstractions.
- Establish logging, timestamping, calibration, and safety mechanisms.

## Phase 5 — Reinforcement learning

- Standing and balancing.
- Basic walking and turning.
- Disturbance recovery and fall recovery.
- Dynamic behaviors and manipulation as hardware permits.
- Evaluate single-policy and multi-skill approaches.

## Phase 6 — Sim-to-real

- Build system-identification procedures.
- Add domain randomization for mass, friction, backlash, latency, voltage, sensor noise, and actuator variation.
- Compare simulated trajectories with physical measurements.
- Iterate until policy transfer is reliable enough for repeatable experiments.

## Phase 7 — Independent hardware

- Replace research assumptions with independently engineered mechanical and electronic designs.
- Optimize actuator count, structure, cost, serviceability, and manufacturability.
- Validate the new hardware against the same simulation and learning stack.
- Keep research compatibility and product branding clearly separated.

## Near-term priorities

1. Establish a verified Microduck architecture notes document.
2. Finalize the first servo test plan.
3. Define the simulation parameter table and confidence labels.
4. Decide the first physics simulator workflow.
5. Define the low-level MCU/servo communication architecture for future prototypes.
