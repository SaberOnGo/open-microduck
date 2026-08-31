# Sources and Evidence Map

> Last source sweep: 2026-08-31.

OpenMicroDuck is a source-driven public research project. A technical statement should be traceable to an authoritative source, reproducible observation, or clearly labeled community derivation.

## Source priority

For claims about Microduck itself, use this order whenever possible:

1. **Official product specification / press kit** — best source for launch/product facts and final public positioning.
2. **Official Pollen Robotics source code and documentation** — best source for runtime behavior, current interfaces, development hardware, model constants, and implementation details.
3. **Official RL/simulation assets** — best source for the training model, kinematics, inertial parameters, collision assets, policies, and sim-to-real recipe.
4. **Reproducible measurements on publicly obtained hardware** — best source for real-unit behavior not formally specified upstream.
5. **Community reconstruction** — useful for derived geometry, transformed assets, alternative implementations, and hypotheses; must remain labeled.
6. **Media/secondary reporting** — useful for context, but should not override an official technical source.

## Official product sources

### Product page

https://pollen-robotics.com/microduck/

Useful for:

- public launch/product positioning;
- headline technical specifications;
- accessories;
- open-source software statement;
- 50 Hz policy loop;
- current commercial availability information.

### Press kit

https://pollen-robotics.com/microduck/press-kit/

Preferred source for current product-level specifications, including:

- 15 motors;
- 25 cm height / 14 cm width;
- under 800 g;
- RK3566 / 1 GB / 32 GB;
- camera, 8×8 ToF, two IMUs;
- articulated beak, audio, NFC, connectivity;
- removable NP-F550 2600 mAh battery;
- explicit statement that “open source” refers to software, not mechanical/electronic design files;
- explicit list of specifications that are still provisional.

## Official onboard software

Repository:

https://github.com/pollen-robotics/microduck

Key paths:

| Path | Evidence provided |
|---|---|
| `README.md` | system-level daemon architecture and public runtime overview |
| `duck-control/src/model.rs` | 15 joint IDs, mouth index, IMU bus ID, baud rate, battery mapping, home pose |
| `duck-control/src/imu.rs` | LSM6DSV16X `imu_to_dxl` v2 data format and decoding |
| `deploy/robotd.toml` | current motor-bus port, 50 Hz loop, policy contract/configuration, safety/runtime defaults |
| `docs/design/robotd-design.md` | control-loop design and hardware/runtime reasoning |
| `docs/design/architecture.md` | service boundaries and system architecture |
| `docs/design/app-path-design.md` | local/Bluetooth/API routing architecture |
| `docs/project/media-bringup.md` | hardware-observed RK3566/Radxa media path and current camera/encoder bring-up |
| `tof/` | ST multi-zone ToF integration |
| `deploy/audio/` | current audio codec/device-tree bring-up |

Because this repository is active development, file-level claims should ideally record the relevant commit when exact reproducibility matters.

## Official RL / simulation stack

Repository:

https://github.com/pollen-robotics/microduck_rl

Key areas:

| Path / area | Evidence provided |
|---|---|
| `README.md` | official training stack, task registry summary, 61-D/14-action contract, BAM/backlash overview |
| `src/mjlab_microduck/robot/microduck/` | MJCF robot models, mesh assets, collision geometry, inertial parameters, joint tree |
| `src/mjlab_microduck/robot/microduck_constants.py` | model/config constants and actuator configuration |
| `src/mjlab_microduck/actuator/` | BAM/friction/randomization integration |
| `src/mjlab_microduck/tasks/` | observations, rewards, events, domain randomization and task families |
| `scripts/export.py` | official deployment export path |
| `scripts/infer_policy.py` | CPU MuJoCo inference / sim-to-real comparison workflow |

Upstream README states the software license is Apache-2.0 and the 3D model files are under Creative Commons BY-SA-NC. Always inspect the exact upstream file/license state before redistribution.

## Actuator model

https://github.com/Rhoban/bam

Used by the official Microduck RL stack for higher-fidelity Dynamixel actuator behavior.

## Reviewed community sources

| Repository | Main use in OpenMicroDuck |
|---|---|
| https://github.com/fanhao375/microduck-replica | mechanical assembly reconstruction, transformed meshes, fastener/bearing inference, source-driven electronics analysis |
| https://github.com/boris721/microduck-3d | public model/mesh catalog, kinematic/combined-model tooling |
| https://github.com/IronSpiderMan/MicroDuckModels | browser MuJoCo/WASM + ONNX simulator |
| https://github.com/kabilankb/isaaclab-microduck | Isaac Lab/Newton research port and parity work |
| https://github.com/Macmachi/microduck-rl-genesis | Genesis/ROCm research port and numerical validation work |
| https://github.com/APX103/mjx_microduck | MJX/JAX/Brax independent RL implementation |
| https://github.com/craigm26/duckkit | Swift model/policy/protocol implementation |
| https://github.com/kgediya/specs-microduck | AR gesture/teleoperation experiment |

See [ecosystem/reverse-engineering-projects.md](ecosystem/reverse-engineering-projects.md) for caveats.

## Evidence labels used by OpenMicroDuck

- **Official product spec** — current official public product statement.
- **Official source** — directly verifiable in official code/docs/models.
- **Measured** — reproducible physical measurement with test conditions.
- **Observed** — direct black-box/teardown/protocol observation.
- **Community reconstruction** / **Inferred** — derived from public evidence but not officially confirmed.
- **Assumed** — temporary model/research placeholder.
- **Provisional** — officially or technically visible but explicitly not finalized.

## Handling conflicts

When two sources disagree:

1. identify whether they describe different revisions;
2. check whether one is a product spec and the other a development/simulation artifact;
3. check dates/commits;
4. preserve the disagreement in documentation if it cannot be resolved;
5. never silently promote a community-derived value to “official”.

Examples already documented in this repository include product NP-F550 battery specification versus F970-named simulation geometry, and provisional camera/ToF details versus concrete current development drivers.

## Reproducibility note

URLs identify the human-readable source, but research that depends on exact code/model values should also record a Git commit SHA. Microduck is under active development, so `main`/`develop` can change after a document is written.
