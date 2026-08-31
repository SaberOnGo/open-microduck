# Provenance and Licensing Notes

> This page is a project-maintenance summary, not legal advice. Always inspect the current upstream license files before copying, modifying, or redistributing third-party content.

## Project identity

OpenMicroDuck is an independent, unofficial research project. It is not affiliated with, endorsed by, sponsored by, or officially connected with Pollen Robotics or Hugging Face.

The Microduck name and related trademarks/branding remain the property of their respective owners. References to Microduck in this repository identify the subject of research and interoperability/documentation work; they do not imply official status.

## Official software

The official `pollen-robotics/microduck` repository currently carries an **Apache License 2.0** software license.

Repository:

https://github.com/pollen-robotics/microduck

Apache-2.0 permission for software does not by itself grant rights to third-party trademarks or unpublished mechanical/electronic design files.

## Official RL repository and 3D assets

The official `pollen-robotics/microduck_rl` README currently states:

- project software: **Apache License 2.0**;
- 3D model files: **Creative Commons BY-SA-NC**.

Repository:

https://github.com/pollen-robotics/microduck_rl

Because asset licensing can vary by file, revision, or upstream source, users should inspect the current repository license/notice information before copying meshes, transformed models, screenshots, or derivatives.

The **NC (NonCommercial)** condition is particularly important for 3D assets and derivatives when it applies.

## Hardware is not published as open-source hardware

The official Microduck press kit explicitly says that “open source” refers to the **software stack** and asks media not to describe the mechanical/electronic design files as open-source hardware.

Source:

https://pollen-robotics.com/microduck/press-kit/

OpenMicroDuck therefore distinguishes:

- documentation and analysis of publicly visible facts;
- independently derived measurements/reconstructions;
- upstream software under its software license;
- upstream/derivative 3D assets under their applicable asset license;
- unpublished proprietary manufacturing files, which are not part of this repository.

## Community-derived CAD and images

A third-party reconstruction can inherit restrictions from the source assets it transforms.

For example, `fanhao375/microduck-replica` states that its scripts are Apache-2.0 while its assembly-drawing/CAD derivatives of upstream Microduck 3D models are CC BY-SA-NC 4.0.

Repository:

https://github.com/fanhao375/microduck-replica

OpenMicroDuck currently links to and summarizes those results rather than copying the derived CAD/images into this repository.

## Attribution and quotations

When using upstream code or assets:

1. preserve required copyright and license notices;
2. identify the upstream project and source path;
3. do not remove attribution required by the license;
4. avoid presenting a community transformation as an official Pollen Robotics file;
5. prefer short technical summaries and independently created diagrams where possible.

## Repository-wide license status

OpenMicroDuck currently has **no repository-wide license** selected. That is deliberate while the project separates original documentation/code from referenced and potentially differently licensed third-party material.

Until a license is added, do not assume unrestricted reuse of OpenMicroDuck-original material merely because the repository is public.

Third-party material always retains its own license/copyright terms regardless of any future OpenMicroDuck license.

## Trademark / affiliation wording

Public pages should retain a clear non-affiliation statement and should not copy the official Microduck logo/visual identity in a way that could make this repository look official.

A descriptive link such as “Microduck reverse-engineering research” is different from claiming to be the official Microduck project.

## Private or confidential material

Confidential, leaked, unlawfully obtained, or unrelated private engineering material is outside the scope of this public repository and must not be contributed.

See [../research-guidelines.md](../research-guidelines.md) and the root [DISCLAIMER.md](../../../DISCLAIMER.md).
