# Research Guidelines

OpenMicroDuck is intended to produce useful, reproducible engineering knowledge. Reverse-engineering notes are most valuable when readers can tell what is known, what was measured, what was inferred, and what is still uncertain.

## Evidence labels

Use one of these labels when documenting technical claims:

- **Public source** — stated in publicly available documentation, source code, product pages, talks, papers, or other attributable material.
- **Measured** — obtained through a documented physical measurement or experiment.
- **Observed** — visible black-box behavior, teardown observation, protocol capture, or other direct observation.
- **Inferred** — derived from available evidence but not directly confirmed.
- **Assumed** — placeholder used for simulation or design until better evidence is available.

Whenever practical, include the date, equipment, software version, firmware version, sample count, test conditions, and raw data location.

## Reverse-engineering principles

1. Prefer public information and independently reproducible measurements.
2. Do not upload leaked, confidential, or unlawfully obtained proprietary material.
3. Do not present assumptions as confirmed specifications.
4. Keep raw measurements separate from interpretation.
5. Record uncertainty and variation rather than publishing a single false-precision value.
6. When testing commercial hardware, document the exact hardware and firmware revision.
7. Preserve attribution and licenses for upstream open-source code.
8. Prefer independently created diagrams, models, tables, and implementations.

## Simulation parameters

Every simulation parameter should ideally record:

- parameter name;
- nominal value;
- units;
- source/evidence label;
- uncertainty or expected range;
- hardware revision or test condition;
- last verification date.

Parameters likely to require randomization include:

- link mass and center of mass;
- joint friction;
- contact friction;
- backlash/deadband;
- actuator torque and speed;
- control latency and jitter;
- supply voltage;
- IMU bias/noise;
- encoder or joint-position error;
- sensor latency and packet loss.

## Hardware measurements

For actuator testing, avoid treating one servo as universal truth. Record the individual unit identifier where possible and distinguish unit-to-unit variation from measurement noise.

Start with one unit for basic protocol discovery and preliminary characterization. Multiple units become useful later when estimating manufacturing variation and robustness requirements.

## Documentation style

Research documents should be written for third-party readers, not as transcripts of private design discussions. Prefer neutral public-facing language, explicit assumptions, tables, diagrams, and links to evidence.
