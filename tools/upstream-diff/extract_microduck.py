#!/usr/bin/env python3
"""Extract a small, reviewable Microduck parameter snapshot from public upstream checkouts.

This tool intentionally reads local source trees only. It does not download anything and it does
not infer a production BOM. Its purpose is to make version-sensitive public parameters easier to
compare across upstream revisions.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import sys
import tomllib
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


SCALAR_PATTERNS = {
    "imu_dxl_id": r"pub const IMU_DXL_ID:\s*u8\s*=\s*(\d+)\s*;",
    "baud_rate": r"pub const BAUD_RATE:\s*u32\s*=\s*([\d_]+)\s*;",
    "battery_full_v": r"pub const BATTERY_FULL_V:\s*f64\s*=\s*([\d.]+)\s*;",
    "battery_empty_v": r"pub const BATTERY_EMPTY_V:\s*f64\s*=\s*([\d.]+)\s*;",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_number_list(text: str, name: str, cast=float) -> list[Any]:
    match = re.search(rf"pub const {re.escape(name)}:[^=]+=\s*\[(.*?)\];", text, re.S)
    if not match:
        return []
    body = re.sub(r"//.*", "", match.group(1))
    values = []
    for token in body.split(","):
        token = token.strip().replace("_", "")
        if not token:
            continue
        try:
            values.append(cast(token))
        except ValueError:
            pass
    return values


def extract_model_rs(root: Path) -> dict[str, Any]:
    path = root / "duck-control" / "src" / "model.rs"
    if not path.exists():
        return {"missing": str(path)}
    text = path.read_text(encoding="utf-8")
    out: dict[str, Any] = {
        "path": str(path.relative_to(root)),
        "sha256": sha256(path),
        "joint_ids": parse_number_list(text, "JOINT_IDS", int),
        "default_position_rad": parse_number_list(text, "DEFAULT_POSITION", float),
    }
    for key, pattern in SCALAR_PATTERNS.items():
        match = re.search(pattern, text)
        if not match:
            continue
        raw = match.group(1).replace("_", "")
        out[key] = float(raw) if "." in raw else int(raw)

    regs = re.search(r"pub const EXPECTED_REGISTERS:[^=]+=\s*&\[(.*?)\];", text, re.S)
    if regs:
        out["expected_registers"] = {
            name: int(value)
            for name, value in re.findall(r'\("([^"]+)",\s*(\d+)\)', regs.group(1))
        }
    return out


def find_one(root: Path, filename: str) -> Path | None:
    matches = sorted(root.rglob(filename))
    return matches[0] if matches else None


def floats(value: str | None) -> list[float] | None:
    if value is None:
        return None
    try:
        return [float(x) for x in value.split()]
    except ValueError:
        return None


def extract_mjcf(root: Path) -> dict[str, Any]:
    path = find_one(root, "robot_allcollisions.xml")
    if path is None:
        return {"missing": "robot_allcollisions.xml"}
    tree = ET.parse(path)
    xml_root = tree.getroot()

    joints = []
    for joint in xml_root.iter("joint"):
        if not joint.get("name"):
            continue
        joints.append(
            {
                "name": joint.get("name"),
                "type": joint.get("type", "hinge"),
                "axis": floats(joint.get("axis")),
                "range": floats(joint.get("range")),
            }
        )

    bodies = []
    total_mass = 0.0
    for body in xml_root.iter("body"):
        inertial = body.find("inertial")
        if inertial is None:
            continue
        mass = float(inertial.get("mass", "0"))
        total_mass += mass
        bodies.append(
            {
                "name": body.get("name"),
                "mass_kg": mass,
                "com": floats(inertial.get("pos")),
                "diaginertia": floats(inertial.get("diaginertia")),
                "fullinertia": floats(inertial.get("fullinertia")),
            }
        )

    mesh_instances = collections.Counter()
    for geom in xml_root.iter("geom"):
        mesh = geom.get("mesh")
        if mesh:
            mesh_instances[mesh] += 1

    return {
        "path": str(path.relative_to(root)),
        "sha256": sha256(path),
        "joint_count": len(joints),
        "joints": joints,
        "body_inertials": bodies,
        "total_inertial_mass_kg": total_mass,
        "mesh_instance_counts": dict(sorted(mesh_instances.items())),
    }


def extract_robotd_toml(root: Path) -> dict[str, Any]:
    path = root / "deploy" / "robotd.toml"
    if not path.exists():
        return {"missing": str(path)}
    with path.open("rb") as f:
        data = tomllib.load(f)
    return {
        "path": str(path.relative_to(root)),
        "sha256": sha256(path),
        "config": data,
    }


def snapshot(microduck: Path | None, microduck_rl: Path | None) -> dict[str, Any]:
    out: dict[str, Any] = {"schema": 1}
    if microduck:
        out["microduck"] = {
            "model": extract_model_rs(microduck),
            "robotd_toml": extract_robotd_toml(microduck),
        }
    if microduck_rl:
        out["microduck_rl"] = {"mjcf": extract_mjcf(microduck_rl)}
    return out


def diff_values(a: Any, b: Any, path: str = "") -> list[dict[str, Any]]:
    changes: list[dict[str, Any]] = []
    if type(a) is not type(b):
        return [{"path": path or "/", "before": a, "after": b}]
    if isinstance(a, dict):
        for key in sorted(set(a) | set(b)):
            p = f"{path}/{key}"
            if key not in a:
                changes.append({"path": p, "before": None, "after": b[key]})
            elif key not in b:
                changes.append({"path": p, "before": a[key], "after": None})
            else:
                changes.extend(diff_values(a[key], b[key], p))
        return changes
    if isinstance(a, list):
        if a != b:
            changes.append({"path": path or "/", "before": a, "after": b})
        return changes
    if a != b:
        changes.append({"path": path or "/", "before": a, "after": b})
    return changes


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract/diff public Microduck source parameters")
    sub = parser.add_subparsers(dest="cmd", required=True)

    snap = sub.add_parser("snapshot", help="write a JSON parameter snapshot")
    snap.add_argument("--microduck", type=Path)
    snap.add_argument("--microduck-rl", type=Path)
    snap.add_argument("--out", type=Path, required=True)

    diff = sub.add_parser("diff", help="compare two JSON snapshots")
    diff.add_argument("before", type=Path)
    diff.add_argument("after", type=Path)

    args = parser.parse_args()
    if args.cmd == "snapshot":
        if args.microduck is None and args.microduck_rl is None:
            parser.error("snapshot needs --microduck and/or --microduck-rl")
        data = snapshot(args.microduck, args.microduck_rl)
        args.out.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(args.out)
        return 0

    before = json.loads(args.before.read_text(encoding="utf-8"))
    after = json.loads(args.after.read_text(encoding="utf-8"))
    changes = diff_values(before, after)
    print(json.dumps(changes, indent=2, sort_keys=True))
    return 1 if changes else 0


if __name__ == "__main__":
    sys.exit(main())
