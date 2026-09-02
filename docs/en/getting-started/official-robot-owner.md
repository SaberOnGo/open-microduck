# I Own an Official Microduck: Where to Start

**English** | [简体中文](../../zh-CN/getting-started/official-robot-owner.md)

> This page is for owners of an official Microduck. It is not a first-power-on guide for a research replica.

## Pick the correct hardware path

| Situation | Correct guide |
|---|---|
| You bought an official Microduck and want to start, pair a gamepad, check health, or update | This page and the official `docs/robot/` user documentation |
| You are building a controller, harness, mechanics, or a complete research replica | [Hardware Bring-up and Calibration](hardware-bringup-and-calibration.md) |

Do not apply research-replica serial, servo EEPROM, initialization, or development-board provisioning steps to a customer robot.

## Recommended first-use order

1. Read the official [Robot Cheat Sheet](https://github.com/pollen-robotics/microduck/blob/main/docs/robot/cheatsheet.md).
2. Complete one-time setup using the official [gamepad pairing guide](https://github.com/pollen-robotics/microduck/blob/main/docs/robot/pair-a-gamepad.md).
3. Start with read-only status commands on the robot:

```bash
robotctl version
robotctl health
robotctl monitor
```

4. For laptop control over Bluetooth, read the official [`duckctl` guide](https://github.com/pollen-robotics/microduck/blob/main/docs/robot/duckctl.md).
5. Follow the official [Updates section in the Cheat Sheet](https://github.com/pollen-robotics/microduck/blob/main/docs/robot/cheatsheet.md#updates-updaterd) for updates, rollback, and version pinning.

OpenMicroDuck provides navigation and plain-language context here. The official repository at the relevant revision owns the current commands and behavior.

## Two safety boundaries

- The official cheat sheet says that `relax` removes servo holding power, so the robot can collapse. Support it by hand or place it on a safe padded surface first.
- The official `duckctl` guide says that the browser console's `stop` only zeros motion intents. It is **not a servo-power emergency stop**.

Clear the area for the first test and keep the robot away from table edges, faces, fingers, pets, and fragile objects. Roller and roll skills need more space.

## What to save before reporting a problem

- `robotctl version`;
- `robotctl health --json` after checking it for device/personal information;
- the command run before the problem;
- whether an update or automatic rollback just occurred;
- battery, gamepad, and current drive mode.

Never publish device secrets, private keys, tokens, Wi-Fi passwords, or logs containing them.

## Official sources

- https://github.com/pollen-robotics/microduck
- https://github.com/pollen-robotics/microduck/tree/main/docs/robot
- https://pollen-robotics.com/microduck/
