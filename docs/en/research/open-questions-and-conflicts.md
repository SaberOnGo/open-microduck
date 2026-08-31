# Open Questions and Source Conflicts

**English** | [简体中文](../../zh-CN/research/open-questions-and-conflicts.md)

> This page records what public sources **do not yet establish**. “Unknown” here means “not confirmed from public evidence,” not “missing from the robot.”

A public research project becomes less reliable when every blank is filled with a guess. This page does the opposite: it keeps unresolved items visible until a stronger source appears.

## Current unresolved hardware details

| Topic | What is publicly known | What is still unresolved |
|---|---|---|
| XL330 actuator sub-variant | Official source identifies Dynamixel XL330 family | Exact production sub-variant is not yet fixed by a clear official Microduck BOM |
| Main carrier board | Current official source shows Radxa Zero 3W as a development/reference platform; product spec confirms RK3566 | Whether every production revision uses exactly the same carrier board |
| Camera | Current development path includes IMX219 / Raspberry Pi Camera v2-style bring-up | Final production module, lens, resolution, and FOV; the press kit still marks resolution/FOV provisional |
| ToF sensor | Official source supports VL53L5CX/VL53L8CX family paths; product spec confirms an 8×8 ToF matrix | Final production sensor model and final range; range is still provisional |
| Second IMU | Product spec confirms two IMUs, one in body and one in head; source exposes LSM6DSV16X control IMU and a BMI088 on current HAT description | Exact final mapping and production implementation of both IMUs |
| Robot HAT | Official source identifies a Pollen Robotics RPI Robot HAT and several attached devices | Full production schematic and BOM |
| `imu_to_dxl` v2 | Official source confirms the board and its protocol role | Complete schematic, MCU/transceiver/passive BOM |
| NFC | Product spec confirms two antennas | Exact controller/transceiver IC and final implementation |
| Audio | Product spec confirms microphones and speaker; development source exposes TLV320AIC3104 codec path | Final microphone/speaker part numbers and exact production audio BOM |
| Fasteners / bearings | Public meshes and community analysis provide useful geometry-derived clues | Final production lengths, quantities, material/grade, supplier parts |
| Wiring | Public architecture shows connectivity and bus relationships | Final production harnesses, connector families, and cable lengths |

## Important source conflicts / moving targets

### Product battery vs simulation naming

The official product specification identifies a removable **NP-F550, 2600 mAh** battery.

Some simulation/model assets have contained `NP-F970`-named geometry. OpenMicroDuck therefore treats:

- NP-F550 / 2600 mAh as the current **official product specification**;
- F970-named model geometry as **simulation/development evidence**, not a product BOM statement.

### Press-kit weight vs store weight

The press kit says **under 800 g**, while the current official store lists **780 g**.

These are not necessarily contradictory. The store value is more specific; the press-kit value is a broader launch specification. Both can be preserved with their source context.

### Product specification vs development hardware

A development source can be more specific than the product page without becoming a permanent production commitment.

Examples include:

- Radxa Zero 3W;
- IMX219 camera path;
- VL53L5CX / VL53L8CX support;
- TLV320AIC3104 codec;
- BMI088 on the development HAT description.

OpenMicroDuck should label these as **official-source development implementation** unless Pollen Robotics explicitly promotes them to final product specification.

## Questions about the policy stack that should remain versioned

Some software facts are public but can still move quickly:

- exactly which policies ship with the robot;
- task IDs and task variants;
- whether a behavior is implemented inside one combined policy or as a separate policy;
- domain-randomization ranges;
- filter/gain defaults;
- observation-command layout in future policy generations.

These should be tied to the upstream version matrix instead of described as timeless robot facts.

## How to resolve an open question

Use the strongest available public evidence in roughly this order:

1. official final product specification;
2. official source code / documentation;
3. official simulation assets;
4. reproducible observation or measurement on publicly obtained hardware;
5. well-documented community reconstruction;
6. secondary reporting.

When a new source appears, update both language trees and preserve meaningful historical context if an old and new value describe different revisions.

## What should not be used to “fill the gap”

Do not resolve an unknown item using:

- private research notes;
- confidential BOMs or supplier information;
- unpublished purchasing data;
- leaked design files;
- unrelated proprietary project information;
- guesses derived from private knowledge and then rewritten as if public.

The correct public value for an unresolved item is sometimes simply **unknown**.

## Related pages

- [Public hardware inventory / BOM status](../hardware/public-bom.md)
- [Sources and evidence map](../sources.md)
- [Upstream version matrix](../upstream/version-matrix.md)
- [Research guidelines](../research-guidelines.md)
