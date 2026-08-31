# Discovered Microduck Repositories

> GitHub discovery snapshot: 2026-08-31. This is a **discovery index**, not a quality ranking and not a technical endorsement.

Microduck is new and the GitHub ecosystem is changing quickly. This page preserves meaningful repository names found in a broad `microduck` repository search while separating discovery from technical verification.

For projects that have already been inspected and summarized, see [Reverse-engineering and community project index](reverse-engineering-projects.md).

## Official Pollen Robotics repositories

- `pollen-robotics/microduck` — onboard runtime / system software
- `pollen-robotics/microduck_rl` — official simulation and reinforcement-learning stack
- `pollen-robotics/microduck-gst-plugins` — media/GStreamer-related repository

## Mechanical / reconstruction / model work

- `fanhao375/microduck-replica` — inspected; assembly/BOM/fastener/hardware reconstruction
- `boris721/microduck-3d` — inspected; public 3D model organization/transforms
- `poboll/microduck-replica` — appears to track/fork the reconstruction project; verify provenance before treating it as independent work
- `XWT985/microduck_robot` — discovered; not yet audited

## Simulation and RL

- `IronSpiderMan/MicroDuckModels` — inspected; browser simulator
- `nickoenig37/mjlab_microduck_waddle` — discovered; mjlab walking work
- `kabilankb/isaaclab-microduck` — inspected; Isaac Lab/Newton port
- `Macmachi/microduck-rl-genesis` — inspected; Genesis/ROCm port
- `APX103/mjx_microduck` — inspected; MJX/JAX/Brax implementation
- `jvpflum/microduck-simulator` — discovered; simulator
- `Arvmor/microduck-simulator` — discovered; simulator/skill branch
- `lgtkgtv/microduck_sim` — discovered; simulator
- `littlejohntj/microduck-sim` — discovered; simulator
- `SAMBAS123/microduck-sandbox` — discovered; sandbox/simulation work
- `jvpflum/microduck-lab` — discovered; lab/experimentation repository
- `AlexandreEDMOND/microduck-rl-lab` — discovered; RL lab
- `Xuexue-Jiang/microduck-rl` — discovered; RL repository
- `x10zyn/microduck-sim-playground` — discovered; simulation playground
- `Liyucheng1997/318_lab-microduck-simulator` — discovered; simulator
- `AmanPriyanshu/toodoom-the-mlx-metal-microduck` — discovered; MLX/Metal-related experiment

## Policies / skills / behavior experiments

- `Lulzx/microduck-backflip` — discovered; backflip-related policy/experiment
- `bihaokun/microduck-step-up-policy` — discovered; step-up policy
- `bentedesco/microduck-parkour` — discovered; parkour-named experiment
- `selinayfilizp/microduck-courier` — discovered; courier/application experiment
- `pezzonovante7/microduck-sidekick-dance` — discovered; dance/behavior experiment
- `DollhouseRobotics/microduck-miniverse` — discovered; environment/application experiment

## Runtime / control / protocol / language work

- `TommyZihao/microduck_runtime` — inspected at README level; documents an earlier/prototype-style Raspberry Pi Zero 2W + BNO055 runtime path and should not be confused with the current official RK3566 runtime
- `craigm26/duckkit` — inspected; Swift model/policy/protocol implementation
- `rokbenko/quackd` — discovered; control/runtime-related project
- `agentculture/microduck-cli` — discovered; CLI tooling
- `joeynyc/microduck-mcp` — discovered; MCP integration
- `aj-dev-smith/microduck-mcp` — discovered; MCP integration
- `apirrone/microduck_kinematics_rs` — discovered; Rust kinematics work
- `apirrone/microduck_maploc_rs` — discovered; mapping/localization work

## App / media / perception / interaction

- `apirrone/microduck_app` — discovered; application work
- `apirrone/microduck_pet_detect` — discovered; pet/touch/audio classification-related work
- `apirrone/microduck_sounds` — discovered; sound/voice-related work
- `kgediya/specs-microduck` — inspected; Spectacles/AR gesture teleoperation
- `ThousandsOfTies/GarTalkableDuck` — discovered; interaction/application project

## Registries / curated lists

- `joeynyc/awesome-microduck` — discovered; curated resources
- `ob1-s/awesome-microduck` — discovered; curated resources
- `ob1-s/uduck-registry` — discovered; registry

## Plain forks and low-information matches

A broad GitHub search also returns many repositories named simply `microduck` whose size/history strongly suggests they are forks or mirrors of the official repository, plus unrelated historical repositories that happen to contain the same word. They are intentionally not listed individually here because doing so would add noise rather than research value.

## Status labels

- **inspected** — at least the README/source relevant to this index was reviewed during the current source sweep;
- **discovered** — found by repository search, but not yet technically audited;
- **official** — owned by Pollen Robotics;
- **fork/mirror** — should not be credited as an independent technical source unless it contains meaningful divergent work.

A discovered repository should only be promoted into technical documentation after checking what it actually implements, which upstream revision it uses, whether results are reproduced, and what license/provenance applies.
