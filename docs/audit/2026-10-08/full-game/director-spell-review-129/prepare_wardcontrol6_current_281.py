from __future__ import annotations

from pathlib import Path


HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "prepare_wardcontrol6_current_237.py"
source = TEMPLATE.read_text(encoding="utf-8")
for old, new in (("237", "281"), ("236", "280"), ("811", "816"), ("37", "32"), ("535", "540")):
    if old not in source:
        raise RuntimeError(f"Expected template token is absent: {old}")
    source = source.replace(old, new)

source = source.replace(
    'rank9_defenseform8_return280_received/DD_Rank9_DefenseForm3_Director_Return280_HELD.zip',
    'rank9_defenseform8_return280_received/DD_Rank9_DefenseForm8_Director_Return280_HELD.zip',
)
source = source.replace(
    'rank9_defenseform8_return280_received/DD_Rank9_DefenseForm3_Director_Return280_HELD_DELIVERY.json',
    'rank9_defenseform8_return280_received/DD_Rank9_DefenseForm8_Director_Return280_HELD_DELIVERY.json',
)
source = source.replace(
    "the independently verified held Return280 and its next-group binding.",
    "the independently verified held Return280, the Return279 final-word hold under DR217-B01, and both next-group bindings.",
)

marker = '        files = {}\n'
addition = '''        # Carry the exact latest Return279 and corrected Return280 decisions,
        # audits, receipts, archives and external manifests into this handoff.
        latest_context_paths = [
            BASE / "DEATHRECOVERY7_DIRECTOR_RULING_279.json",
            BASE / "DEATHRECOVERY7_DIRECTOR_RULING_279_CROSSCHECK.json",
            BASE / "RANK9_DEFENSEFORM8_PACKET280_INDEPENDENT_AUDIT.json",
            BASE / "RANK9_DEFENSEFORM8_PACKET280_RECEIPT.json",
            BASE / "RANK9_DEFENSEFORM8_DIRECTOR_RULING_280.json",
            BASE / "RANK9_DEFENSEFORM8_RETURN280_CROSSCHECK.json",
            BASE / "RANK9DEFENSEFORM8_RETURN280_INDEPENDENT_AUDIT.json",
            BASE / "RANK9DEFENSEFORM8_RETURN280_RECEIPT.json",
            BASE / "rank9_defenseform8_return280_received/DD_Rank9_DefenseForm8_Director_Return280_HELD.zip",
            BASE / "rank9_defenseform8_return280_received/DD_Rank9_DefenseForm8_Director_Return280_HELD_DELIVERY.json",
        ]
        current_files.update({"current/" + path.relative_to(ROOT).as_posix(): path.read_bytes() for path in latest_context_paths})
        context["previousFinalWordReturn279"] = {"heldIds": ["final-word"], "blockerIds": ["DR217-B01"], "acceptedIds": [], "appliedIds": [], "authority": AUTH, "ruling": bind(BASE / "DEATHRECOVERY7_DIRECTOR_RULING_279.json"), "crosscheck": bind(BASE / "DEATHRECOVERY7_DIRECTOR_RULING_279_CROSSCHECK.json")}
        context["previousDefenseFormReturn280"] = {"heldIds": ["elemental-shell", "timeless-form", "invulnerable-sphere"], "blockerIds": {"elemental-shell": ["DF218-B01", "DF218-B02"], "timeless-form": ["DF218-B03"], "invulnerable-sphere": ["DF218-B04"]}, "acceptedIds": [], "appliedIds": [], "authority": AUTH, "ruling": bind(BASE / "RANK9_DEFENSEFORM8_DIRECTOR_RULING_280.json"), "independentAudit": bind(BASE / "RANK9DEFENSEFORM8_RETURN280_INDEPENDENT_AUDIT.json"), "nextGroup": GROUP, "nextPendingIds": IDS}
'''
if marker not in source:
    raise RuntimeError("Cannot locate Ward/Control6 member construction block")
source = source.replace(marker, addition + marker, 1)

namespace = {"__name__": "__main__", "__file__": str(TEMPLATE)}
exec(compile(source, str(TEMPLATE), "exec"), namespace)
