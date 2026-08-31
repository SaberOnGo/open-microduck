# Start Here: Microduck in Plain Language

**English** | [简体中文](../../zh-CN/getting-started/README.md)

> Public, source-backed information only. This page is for readers who do not already know robotics.

## Microduck in one picture

A useful way to understand the whole robot is:

```text
                THE PHYSICAL ROBOT
 structure + motors + battery + sensors
                         │
                         ▼
                    SENSING
        Camera / ToF / IMU / joint state
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
      understand the world      understand the body
      vision / ToF geometry     joints / IMU
             │                       │
             └───────────┬───────────┘
                         ▼
                  BEHAVIOR DECISION
              “walk there / look left / kick”
                         │
                         ▼
                    MOVEMENT AI
             61 inputs → ONNX → 14 actions
                         │
                         ▼
                 SAFETY + MOTOR CODE
                         │
                         ▼
                      15 motors
```

Simulation mirrors the movement side of this system before real hardware is added.

## Which parts are AI?

Not everything is AI:

- **Camera detection:** AI model.
- **ToF depth processing:** normal geometry/filtering code.
- **High-level autonomous behavior:** mainly rules/state-machine logic in the older runtime; the new daemon architecture has not fully ported it yet.
- **Walking and movement skills:** reinforcement-learning policies exported to ONNX.
- **Motor bus, safety, updates and networking:** normal software.

This distinction prevents a common misunderstanding: the camera and ToF do not directly feed the standard 61-D walking policy.

## Four numbers explain most of the movement architecture

| Number | Meaning |
|---:|---|
| **15** | physical motor IDs in the current runtime, including the mouth/beak |
| **14** | joints controlled by the locomotion policies |
| **61** | input width shared by the current movement-policy family |
| **50 Hz** | movement control rate: one cycle every 20 ms |

## Where to start

| Goal | Read this |
|---|---|
| Make the virtual robot move first | [Simulation First](simulation-first.md) |
| Understand the complete software flow | [How the Microduck software fits together](../software/runtime-architecture.md) |
| Understand the 50 Hz movement loop | [Control Loop: How the Robot Moves](../software/control-loop-and-sensor-dataflow.md) |
| Find hardware parameters | [Hardware Parameter Reference](../hardware/parameter-reference.md) |
| Understand how the structure is assembled | [Structure and Assembly Map](../hardware/structure-and-assembly-map.md) |
| Follow a staged public reproduction path | [Public Reproduction Roadmap](public-reproduction-roadmap.md) |
| Train or change a movement policy | [Reproducible Training and ONNX Export](../simulation/reproducible-training-and-export.md) |
| Check sim-to-real values | [Sim-to-Real Parameter Reference](../simulation/sim-to-real-parameter-reference.md) |

## Recommended reproduction order

Do not treat “build Microduck” as one task. A safer public research sequence is:

```text
1. Run the official robot model and an existing ONNX policy in simulation
2. Understand the joints, masses and structure
3. Reproduce one training task
4. Understand the real 50 Hz motor + IMU loop
5. Test small hardware pieces separately
6. Validate mechanical subassemblies
7. Build a complete research assembly
8. Compare simulation with real measurements
```

Simulation comes first because it lets a researcher verify the model, joint order, policy interface and control assumptions before mechanical and electrical uncertainty are added.

## What is already fairly clear from public sources?

Public material is strong enough to document:

- the current 14 policy-controlled joints and 15 runtime motor IDs;
- home pose and simulation joint limits;
- the 50 Hz control path and 1 Mbps motor bus;
- the control IMU data path;
- the 61-D movement-policy interface;
- official MuJoCo models, RL tasks and many sim-to-real parameters;
- Camera, ToF, kinematics and current onboard software architecture;
- many public meshes, body masses and assembly transforms.

## What is still not a complete production-hardware package?

Public evidence is still incomplete for items such as:

- full production schematics and PCB BOM;
- final production wiring harnesses and connector details;
- exact final camera/lens/FOV if the upstream product is still changing;
- final production ToF part if multiple supported parts remain possible;
- complete production fastener list, materials and manufacturing tolerances;
- full production assembly process.

Unknown values stay marked as unknown instead of being guessed.

## Evidence labels

| Label | Meaning |
|---|---|
| **Official product spec** | published as a product-level fact by Pollen Robotics |
| **Official source** | directly visible in official code or documentation |
| **Official simulation model** | present in official simulation assets, not automatically a physical production measurement |
| **Community reconstruction** | derived by a public third party from public evidence |
| **Measured** | reproducible physical measurement with conditions recorded |
| **Unresolved** | not enough public evidence yet |

## Upstream snapshot used for the current parameter sweep

- `pollen-robotics/microduck` main: `590b986bd8c0d50ae02cb3ea2f59c463b6828168`
- `pollen-robotics/microduck_rl` develop: `d424a0c899f6b33cbd3daeb279913134349c0b63`
- `Rhoban/bam` main: `620a64fe67c1afe94fca81da73b128c7aed17c5f`

See [Upstream Version Matrix](../upstream/version-matrix.md) for version-sensitive details.
