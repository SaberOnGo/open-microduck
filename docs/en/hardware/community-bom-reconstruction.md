# Community-Derived BOM and Fastener Reconstruction

> **Not an official Microduck BOM.** This page records reproducible third-party conclusions derived from public MJCF/STL/source assets. Production hardware may differ.

Primary community source: https://github.com/fanhao375/microduck-replica

## Why this page is separate

Pollen Robotics has not published a production mechanical/electronic BOM. The independent `microduck-replica` project analyzes the public simulation meshes and official software to infer assembly and purchasing information. These results are useful for research, but OpenMicroDuck keeps them separate from [the public-source inventory](public-bom.md) so model-derived estimates are not mistaken for official manufacturing data.

## Model-derived assembly snapshot

For the upstream model snapshot analyzed by `microduck-replica`, the project reports approximately:

| Property | Community-derived result |
|---|---:|
| Model mass | ~737.2 g |
| Model envelope | ~144 × 141 × 264 mm |
| Motor count represented/identified | 15 Dynamixel XL330 |
| Policy-controlled motor joints | 14 |
| Additional motor | beak/mouth |

These numbers describe that analyzed model snapshot, not a scale measurement of a retail production unit. Official product wording remains **25 cm tall, 14 cm wide, under 800 g**.

## Inferred fastener geometry

The community project scans cylindrical hole features in the public mesh set and reports strong clusters consistent with an M2-based assembly system.

Selected reported feature counts:

| Mesh feature | Reported count | Community interpretation |
|---|---:|---|
| ~Ø2.2 mm holes | 77 | M2 clearance holes |
| ~Ø4.4 mm recesses/holes | 28 | head/counterbore features associated with M2 fasteners |
| ~Ø1.6 mm holes | 20 | M2 tapping-drill-sized features |
| ~Ø2.4 mm holes | 22 | looser M2 clearance candidates |
| ~Ø2.0 mm holes | 12 | tighter M2-class features |
| ~Ø2.7–2.8 mm holes | 20 | possible M2.5-class clearance features |

The analysis also estimates roughly **146 structural M2-class through-hole instances** after excluding motor/external-component features.

### Important limitation

A hole in a simulation/visual mesh does not prove the production screw type, length, insert method, tolerance, or even that the feature survives into the final manufactured revision. The mesh may simplify threads, hide inserts, or represent a development revision.

## Community purchase estimate

The same project publishes a conservative trial-assembly purchase estimate based on its measured hole-depth distribution:

| Item | Community estimate |
|---|---:|
| M2×4 socket-head screws | ~60 |
| M2×6 socket-head screws | ~80 |
| M2×8 socket-head screws | ~40 |
| M2×12 socket-head screws | ~15 |
| M2 nuts | ~50 |
| M2 heat-set inserts | ~60 |
| M2.5×6 screws | ~20 |

These quantities are **not a count of screws used by a production Microduck**. They are a third-party purchasing estimate intended to include trial assembly and losses.

## Bearing geometry inferred from meshes

The community analysis identifies public bearing-shaped mesh geometry approximately corresponding to:

| Model-derived geometry | Notes |
|---|---|
| 22 mm OD × 16 mm ID × 4 mm width | directly reflected by one asset name/geometry |
| ~15 mm OD × ~10 mm ID × 3 mm width | smaller bearing geometry in the model |

Public meshes do not establish supplier, tolerance class, material, seal type, load rating, or final production quantity.

## Publicly identified electronics/components

Combining facts that can be checked in official source with the community reconstruction produces the following research inventory:

| Area | Publicly identifiable item | Status |
|---|---|---|
| Compute | RK3566; current source bring-up on Radxa Zero 3/3W | official product/source; board revision may be provisional |
| Actuation | Dynamixel XL330 family, 15 motor IDs in runtime | official source |
| Control IMU | LSM6DSV16X on `imu_to_dxl` v2, DXL ID 200 | official source |
| Camera development path | IMX219 / Raspberry Pi Camera v2 on current Radxa bring-up | official source, development path |
| ToF software support | VL53L5CX and VL53L8CX | official source; final production part unresolved |
| Audio development path | TLV320AIC3104 | official source, development path |
| Battery product spec | removable NP-F550, 2600 mAh | official product spec |
| Custom board interfaces | bus bridge / Pi-HAT-style functions can be inferred from runtime and model assets | public-source/community reconstruction; no official production schematic/BOM |

## Board and model geometry notes

Third-party reconstruction has measured PCB-like geometry embedded in the public model and has inferred how current development modules fit together. Those measurements are useful for understanding the released simulation assets, but they are intentionally **not reproduced here as production PCB drawings**.

No unpublished schematic, PCB design file, manufacturing Gerber, or proprietary CAD is included in OpenMicroDuck.

## Reproducing the community analysis

The upstream community repository publishes analysis scripts rather than only screenshots. Its documented workflow fetches the public upstream Microduck RL assets, applies MJCF transforms to meshes, renders assembly views, exports transformed STL assemblies, and scans hole geometry.

Researchers should prefer rerunning those scripts against a pinned upstream commit when exact model-derived values matter. This avoids treating a result from one snapshot as timeless.

## Licensing / provenance

The community repository states that its analysis scripts and its derived CAD/image outputs have different licenses; its CAD/assembly derivatives inherit non-commercial/share-alike restrictions from upstream 3D assets. OpenMicroDuck therefore summarizes the technical results and links to the source rather than importing those derived assets.

See:

- https://github.com/fanhao375/microduck-replica
- [Provenance and licensing](../legal/provenance-and-licenses.md)
- [Mechanical structure](mechanical-structure.md)
