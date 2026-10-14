"""Windows MAX_PATH helpers for deep V7.2 lab extract paths."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


def win_long(path: Path | str) -> str:
    p = os.path.abspath(str(path))
    if os.name == "nt" and not p.startswith("\\\\?\\"):
        return "\\\\?\\" + p
    return p


def ensure_dir(path: Path | str) -> None:
    os.makedirs(win_long(path), exist_ok=True)


def write_json(path: Path | str, obj: Any) -> None:
    path = Path(path)
    ensure_dir(path.parent)
    with open(win_long(path), "w", encoding="utf-8") as f:
        f.write(json.dumps(obj, indent=2))


def write_text(path: Path | str, text: str) -> None:
    path = Path(path)
    ensure_dir(path.parent)
    with open(win_long(path), "w", encoding="utf-8") as f:
        f.write(text)
