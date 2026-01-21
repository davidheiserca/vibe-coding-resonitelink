#!/usr/bin/env python3
"""Extract component type names from a FrooxEngine decompile tree."""

import argparse
import json
import re
from pathlib import Path


CLASS_RE = re.compile(r"\bclass\s+([A-Za-z_][A-Za-z0-9_]*)\b")
NAMESPACE_RE = re.compile(r"^\s*namespace\s+([A-Za-z0-9_.]+)\s*$")


def is_component_class(line: str) -> bool:
    if " class " not in line or ":" not in line:
        return False
    if "abstract class" in line:
        return False
    if "<" in line and "class" in line:
        return False
    return re.search(r"\bComponent\b", line) is not None


def extract_components(root: Path) -> list[str]:
    components = set()
    for path in root.rglob("*.cs"):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        namespace = None
        for line in text:
            ns_match = NAMESPACE_RE.match(line)
            if ns_match:
                namespace = ns_match.group(1)
                break
        if not namespace:
            continue
        for line in text:
            if not is_component_class(line):
                continue
            class_match = CLASS_RE.search(line)
            if not class_match:
                continue
            class_name = class_match.group(1)
            full_name = f"[FrooxEngine]{namespace}.{class_name}"
            components.add(full_name)
    return sorted(components)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        required=True,
        help="Path to FrooxEngine decompile folder",
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Output JSON path",
    )
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()

    components = extract_components(root)
    payload = {
        "source_root": str(root),
        "count": len(components),
        "components": components,
    }
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
