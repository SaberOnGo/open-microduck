# Onboard Runtime Architecture

> This page summarizes the architecture exposed by the official `pollen-robotics/microduck` software repository. It documents the public software stack, not unpublished electronics.

## Overview

The official Microduck repository describes the onboard system as a Rust workspace running a small set of cooperating Linux daemons on an RK3566-class computer.

```text
                   clients
        app / gamepad / CLI / scripts
                     │
             shared JSON-RPC API
                     │
     ┌───────────────┼─────────────────┐
     │               │                 │
   robotd          configd           updaterd
 control/motors   Wi-Fi/identity    signed updates
     │
     ├──────── padd     gamepad input
     ├──────── btd      Bluetooth path
     ├──────── mediad   camera/WebRTC
     └──────── tofd     depth/ToF service
```

The daemons communicate locally through **JSON-RPC over Unix sockets**. The architecture deliberately keeps the transport separate from the owning service: Bluetooth, local CLI tools, and other clients can route the same API calls rather than implementing different robot-control protocols.

## Main services

| Service | Public role |
|---|---|
| `robotd` | Owns the 50 Hz control loop, motor bus, policy execution, robot state, skills, and safety/control decisions. |
| `updaterd` | Installs signed software releases and supports health-gated rollback. |
| `configd` | Owns Wi-Fi/network configuration, identity, and system configuration functions. |
| `btd` | Bluetooth transport used by phone/client provisioning paths; routes calls to the owning services. |
| `padd` | Reads the game controller and converts input into the common robot API. |
| `mediad` | Captures/encodes/streams camera media, including the current WebRTC path. |
| `tofd` | Owns the multi-zone ToF sensor and exposes depth frames/status. |

The exact service set can evolve; the official repository is the authoritative source for current binaries and APIs.

## Control loop

The current configuration uses a **50 Hz** control loop.

The official repository describes this loop as driving fifteen servo devices while neural policies output fourteen controlled joint commands. The mouth/beak motor is controlled separately.

Current alpha policies are validated at load time against a shared interface:

```text
observation: 61 floats
policy output: 14 actions
control rate: 50 Hz
```

The runtime can switch among policies/skills while keeping the same observation/action contract. This is why walking, recovery, sit/stand, kicking, rolling, ground-pick, and roller behaviors can share the onboard control infrastructure rather than requiring a different firmware image for every behavior.

## 61-dimensional observation contract

The official RL repository describes the current actor observation as:

```text
48 proprioception
+ 13 command values
= 61 total
```

The command block is shared across the policy family:

- twist: 3 values;
- head pose: 4 values;
- body pose: 6 values.

Tasks that do not use a command field zero-pad it instead of changing the network input width. That invariant enables runtime policy hot-swapping.

## ONNX deployment

Policies are trained in the separate `microduck_rl` project and exported to **ONNX**. The onboard runtime loads the exported networks through ONNX Runtime.

Upstream documentation emphasizes that observation normalization is baked into the exported graph; a manually converted checkpoint without the expected normalizer is not equivalent to the deployment artifact.

## Motor/IMU I/O

`robotd` reaches the current development motor bus through `duck-control` and the upstream Dynamixel-compatible Rust stack.

The public control sources expose:

- 15 motor IDs;
- one IMU bridge at ID 200;
- 1 Mbps serial configuration;
- current development port `/dev/ttyS2` on Radxa Zero 3W;
- position/velocity/voltage/status data used by the control loop.

The control IMU is read on the same transaction family as the servo state, reducing synchronization ambiguity between joint and orientation data.

## Policy filtering and actuator-facing control

The runtime does more than call a neural network. Public configuration/source includes actuator-facing behavior such as:

- action scaling;
- head and leg low-pass filtering;
- position gains;
- battery-voltage-aware options;
- joint travel handling;
- fall/limp/recovery logic;
- dropped-bus-transaction handling;
- watchdog/deadman behavior.

These details are important to sim-to-real reproducibility because the physical robot executes **policy + runtime control path**, not the ONNX network in isolation.

## Safety and health

The official runtime separates robot state from release health. A robot can report battery, motor temperature, loop statistics, and bus counters, while the updater uses a narrower health gate to decide whether a software release should be rolled back.

Public configuration includes thresholds for achieved control frequency, stalled loops, and consecutive bus errors. The update design therefore treats “process is running” and “robot control is operating correctly” as different conditions.

## Input and remote-control paths

The architecture is intentionally multi-client:

- game controller through `padd`;
- local administration through `robotctl` and Unix sockets;
- Bluetooth provisioning/control path through `btd`;
- application/network functions through the same service contracts.

This design keeps robot commands transport-independent: transports carry requests; the service owning the capability remains responsible for the behavior.

## Camera and depth services

### `mediad`

Current official hardware bring-up uses the RK3566/Rockchip media stack and hardware H.264 encoding through Rockchip MPP, with WebRTC integration in the software architecture.

### `tofd`

The ToF service owns multi-zone depth acquisition and makes the result available to other components instead of letting every client talk directly to the sensor.

## Updates

`updaterd` is designed around signed releases, installation, post-install validation, and rollback. This is particularly relevant on a walking robot: a software update that leaves Linux alive but degrades the real-time control loop must not be considered healthy merely because the daemon answers a socket.

## Primary sources

- https://github.com/pollen-robotics/microduck
- https://github.com/pollen-robotics/microduck/blob/main/README.md
- https://github.com/pollen-robotics/microduck/tree/main/docs/design
- https://github.com/pollen-robotics/microduck/blob/main/deploy/robotd.toml
- https://github.com/pollen-robotics/microduck/blob/main/duck-control/src/model.rs
- https://github.com/pollen-robotics/microduck_rl

For the public hardware side of this architecture, see [../hardware/electronics-and-buses.md](../hardware/electronics-and-buses.md).
