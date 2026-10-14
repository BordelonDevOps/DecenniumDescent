"""Find missing feats from all canon sources."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from ingest_canon_data import (  # noqa: E402
    docx_paragraphs,
    extract_named_objects,
    ingest_docx_feats,
    normalize_name,
    parse_feat_block,
)


def read_text(path: Path) -> str:
    buf = path.read_bytes()
    if buf[:2] == b"\xff\xfe":
        return buf.decode("utf-16le").lstrip("\ufeff")
    return buf.decode("utf-8", errors="replace")


def load_current() -> set[str]:
    text = (ROOT / "src/data/feats.js").read_text(encoding="utf-8")
    return {normalize_name(n) for n in re.findall(r'"name": "([^"]+)"', text)}


def docx_feat_names() -> dict[str, list[str]]:
    files = [
        ("Decennium_Descent_Feats.docx", "General", "Combat Feats", 20),
        ("Decennium_Descent_Combat_Feats.docx", "Combat", None, None),
        ("Decennium_Descent_Magic_Feats.docx", "Magic", None, None),
        ("Decennium_Descent_Skill_Feats.docx", "Skill", None, None),
        ("Decennium_Descent_330_Feat_Compendium.docx", "General", None, None),
    ]
    out: dict[str, list[str]] = {}
    for fname, ftype, stop, max_count in files:
        path = ROOT / fname
        if not path.is_file():
            continue
        feats = parse_feat_block(
            docx_paragraphs(str(path)), ftype, stop_at=stop, max_count=max_count
        )
        out[fname] = [f["name"] for f in feats]
    return out


def main() -> None:
    current = load_current()
    print(f"current={len(current)}")

    docx = docx_feat_names()
    for fname, names in docx.items():
        print(f"{fname}: {len(names)} parsed")

    gd = (ROOT / "game-data.js").read_text(encoding="utf-8")
    add = (ROOT / "additional-feats.js").read_text(encoding="utf-8")
    game = extract_named_objects(gd, "FEATS") + extract_named_objects(add, "ADDITIONAL_FEATS")
    game_names = {normalize_name(f["name"]) for f in game}
    print(f"game+additional unique={len(game_names)}")

    # prestige feat refs
    rb = read_text(ROOT / "rulebook_output.txt")
    refs: set[str] = set()
    for line in rb.splitlines():
        if "Feats:" in line:
            chunk = line.split("Feats:", 1)[1]
            for part in re.split(r",\s*", chunk):
                name = part.strip().strip("-").strip()
                if name and len(name) < 60:
                    refs.add(normalize_name(name))
    missing_refs = refs - current
    print(f"prestige_refs={len(refs)} missing={len(missing_refs)}")
    for n in sorted(missing_refs):
        print(f"  prestige_missing: {n}")

    # search rulebook for feat-like blocks: Name then Effect/Requirement
    paras = [p.strip() for p in rb.splitlines() if p.strip()]
    rb_feats: list[str] = []
    for i, line in enumerate(paras):
        if line.startswith("Effect:") and i >= 1:
            prev = paras[i - 1]
            if not prev.startswith(("Effect:", "Requirement:", "Prerequisite:", "#", "|", "-", "*")):
                if re.match(r"^[A-Z][\w '\-/]+$", prev) and len(prev) < 50:
                    rb_feats.append(prev)
    rb_set = {normalize_name(n) for n in rb_feats}
    print(f"rulebook_feat_blocks={len(rb_set)} missing={len(rb_set - current)}")

    # search for "Chapter" feat sections
    for i, line in enumerate(paras):
        if re.search(r"feat", line, re.I) and ("chapter" in line.lower() or line.startswith("#")):
            print(f"FEAT_SECTION @{i}: {line[:120]}")

    # compendium full text
    comp = read_text(ROOT / "feat_compendium_output.txt")
    comp_paras = [p.strip() for p in comp.splitlines() if p.strip()]
    for i, line in enumerate(comp_paras):
        if "330" in line or "Class-Specific" in line or "class-specific" in line.lower():
            print(f"COMP @{i}: {line[:120]}")

    # List game feats not matching docx (potential class-specific in game-data only)
    all_docx = {normalize_name(n) for names in docx.values() for n in names}
    game_only = game_names - current  # should be empty
    print(f"game_only_not_merged={len(game_only)}")

    # Count additional-feats separately
    add_only = extract_named_objects(add, "ADDITIONAL_FEATS")
    print(f"additional_feats={len(add_only)}")

    # Types in current
    text = (ROOT / "src/data/feats.js").read_text(encoding="utf-8")
    types = re.findall(r'"type": "([^"]+)"', text)
    from collections import Counter
    print("types", dict(Counter(types)))


if __name__ == "__main__":
    main()
