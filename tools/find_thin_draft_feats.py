"""Find all draft feats with short effect text."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    text = (ROOT / "src/data/feats.js").read_text(encoding="utf-8")
    thin: list[tuple[str, int, str]] = []
    for block in re.split(r"\n  \{", text):
        if '"draft": true' not in block:
            continue
        name_m = re.search(r'"name":\s*"([^"]+)"', block)
        effect_m = re.search(r'"effect":\s*"((?:[^"\\]|\\.)*)"', block, re.DOTALL)
        if not name_m or not effect_m:
            continue
        effect = effect_m.group(1)
        if len(effect) < 80:
            thin.append((name_m.group(1), len(effect), effect))
    thin.sort(key=lambda x: x[1])
    print(f"thin_draft_count={len(thin)}")
    for name, ln, eff in thin:
        print(f"{ln:3d} | {name!r} | {eff[:120]}")


if __name__ == "__main__":
    main()
