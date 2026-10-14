"""Search canon sources for prestige stub feat definitions."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.parent

STUBS = [
    "Anatomy Lore", "Arcane Adaptation", "Arcane Calculus", "Arcane Momentum",
    "Beast Lore", "Blood Ritual", "Combat Engineering", "Companion Training",
    "Conjure Flora", "Core Infusion", "Curse Channeling", "Curse Weaving",
    "Cursebound Flesh", "Dark Affinity", "Dark Binding", "Dark Fortitude",
    "Eldritch Combat", "Eldritch Echo", "Favored Enemy (Dragon)", "Forbidden Pact",
    "Frenzied Rage", "Giant Slayer", "Hardened Grip", "Hemocraft", "Life Drinker",
    "Lifeleech", "Lightning Affinity", "Master Smithing", "Mimicry", "Necrotic Affinity",
    "Precision Strike", "Primal Instinct", "Quickened Thought", "Siege Savant",
    "Slayer's Resolve", "Soul Cage", "Spell Reflection", "Stormcaller",
    "Temporal Theory", "Trapcasting", "Trapsetter", "Undying Flesh", "Verdant Bond",
    "Voltyros Pact", "Wounding Magic",
]

SOURCES: list[Path] = [
    ROOT / "feat_compendium_output.txt",
    ROOT / "rulebook_output.txt",
    ROOT / "game-data.js",
    ROOT / "additional-feats.js",
    ROOT / "src/data/prestige-lorebook.json",
    ROOT / "src/data/prestige.js",
    ROOT / "ENHANCED-FEATURES.JS",
]

for p in PARENT.rglob("*"):
    if p.is_file() and "node_modules" not in p.parts:
        low = p.name.lower()
        if "feat" in low and p.suffix in {".txt", ".js", ".json", ".md", ".docx"}:
            if p not in SOURCES:
                SOURCES.append(p)


def extract_feat_block(text: str, name: str) -> str | None:
    """Try to extract a feat definition block near the name."""
    patterns = [
        rf"(?i)(?:^|\n)\s*{re.escape(name)}\s*\n(?:Requirement|Prerequisite|Effect|Description|Type)[^\n]*(?:\n[^\n]+){{0,8}}",
        rf"(?i){re.escape(name)}[^\n]{{0,80}}\n(?:Requirement|Prerequisite|Effect|Description)[^\n]+(?:\n[^\n]+){{0,6}}",
        rf'(?i)"name":\s*"{re.escape(name)}"[^\}}]{{0,500}}',
        rf"(?i){re.escape(name)}\s*[-–—]\s*[^\n]+",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.MULTILINE)
        if m:
            return m.group(0).strip()
    idx = text.find(name)
    if idx >= 0:
        return text[max(0, idx - 80) : idx + 300].replace("\n", " ").strip()
    return None


def main() -> None:
    loaded: dict[Path, str] = {}
    for src in SOURCES:
        if not src.exists():
            continue
        try:
            if src.suffix == ".docx":
                continue  # skip binary for now
            loaded[src] = src.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            pass

    print(f"sources={len(loaded)}")
    for stub in STUBS:
        hits: list[tuple[str, str]] = []
        for src, text in loaded.items():
            if stub in text:
                block = extract_feat_block(text, stub)
                rel = src.relative_to(ROOT) if src.is_relative_to(ROOT) else src
                hits.append((str(rel), block or "(name only)"))
        if hits:
            print(f"\n=== {stub} ({len(hits)} hits) ===")
            for rel, block in hits[:3]:
                print(f"  [{rel}]")
                print(f"    {block[:400]}")
        else:
            print(f"\n=== {stub} NOT FOUND ===")


if __name__ == "__main__":
    main()
