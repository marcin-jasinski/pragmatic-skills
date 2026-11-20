#!/usr/bin/env python3
"""Keep the shared blocks in every SKILL.md identical.

Skills install one at a time (`npx skills` lets the user pick), so they can't
share a file at runtime. Rules that must behave the same everywhere are copied
into each skill between markers:

    <!-- shared:NAME ... -->
    ...
    <!-- /shared:NAME -->

The copy in CANONICAL is the source of truth.

    scripts/check-shared-blocks.py          # exit 1 if any copy has drifted
    scripts/check-shared-blocks.py --write  # overwrite copies from the canonical one
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "skills" / "socratic-design" / "SKILL.md"
BLOCK = re.compile(
    r"(<!-- shared:(?P<name>[\w-]+)[^>]*-->\n)(?P<body>.*?)(<!-- /shared:(?P=name) -->)",
    re.S,
)


def blocks(text):
    return {m["name"]: m["body"] for m in BLOCK.finditer(text)}


def main():
    write = "--write" in sys.argv[1:]
    canonical = blocks(CANONICAL.read_text(encoding="utf-8"))
    if not canonical:
        sys.exit(f"no shared blocks found in {CANONICAL.relative_to(ROOT)}")

    drifted = []
    for path in sorted((ROOT / "skills").glob("*/SKILL.md")):
        if path == CANONICAL:
            continue
        text = path.read_text(encoding="utf-8")
        for m in BLOCK.finditer(text):
            name = m["name"]
            if name not in canonical:
                drifted.append(f"{path.relative_to(ROOT)}: unknown block '{name}'")
            elif m["body"] != canonical[name]:
                drifted.append(f"{path.relative_to(ROOT)}: block '{name}' differs")
        if write:
            new = BLOCK.sub(
                lambda m: m.group(1) + canonical.get(m["name"], m["body"]) + m.group(4),
                text,
            )
            if new != text:
                path.write_text(new, encoding="utf-8")

    if write:
        print("shared blocks synced from", CANONICAL.relative_to(ROOT))
        return
    if drifted:
        print("\n".join(drifted))
        print(f"\nThe canonical copies live in {CANONICAL.relative_to(ROOT)}. "
              "Edit there, then run: scripts/check-shared-blocks.py --write")
        sys.exit(1)
    print("shared blocks in sync")


if __name__ == "__main__":
    main()
