# Simulation

This directory contains OpenMicroDuck simulation models, parameter sets, environments, validation data, and simulator-specific tooling.

Planned work includes:

- rigid-body and joint models;
- mass, inertia, center-of-mass, and joint-limit parameters;
- actuator torque/speed limits and response dynamics;
- friction, backlash, deadband, and contact models;
- sensor noise and latency models;
- domain randomization;
- system identification;
- simulation-to-real trajectory comparison.

Simulation parameters should identify whether each value is **public-source**, **measured**, **observed**, **inferred**, or **assumed**. See [`../docs/RESEARCH_GUIDELINES.md`](../docs/RESEARCH_GUIDELINES.md).
