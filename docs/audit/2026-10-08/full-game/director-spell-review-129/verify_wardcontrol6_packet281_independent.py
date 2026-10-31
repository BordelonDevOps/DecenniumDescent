from __future__ import annotations

from pathlib import Path


HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "verify_wardcontrol6_packet237_independent.py"
source = TEMPLATE.read_text(encoding="utf-8")
for old, new in (("237", "281"), ("236", "280"), ("811", "816"), ("37", "32"), ("535", "540")):
    if old not in source:
        raise RuntimeError(f"Expected verifier token is absent: {old}")
    source = source.replace(old, new)
source = source.replace("df248b3dd6bd7bf36dd9bb7bbfb4d89d877814fb8fb7ab752d35d1f16d7784d5",
                        "1a49741bc259e2a64dca7a3bb87a1057af8ca4269b246714652119e3edaeed81")
source = source.replace(
    'rank9_defenseform8_return280_received/DD_Rank9_DefenseForm3_Director_Return280_HELD_DELIVERY.json',
    'rank9_defenseform8_return280_received/DD_Rank9_DefenseForm8_Director_Return280_HELD_DELIVERY.json',
)

marker = '    check("preparation declares ten passing checks and no canonical or GitHub application",'
addition = '''    latest279 = read_json(archive.read("current/docs/audit/2026-10-08/full-game/director-spell-review-129/DEATHRECOVERY7_DIRECTOR_RULING_279.json"))
    latest279_audit = read_json(archive.read("current/docs/audit/2026-10-08/full-game/director-spell-review-129/DEATHRECOVERY7_DIRECTOR_RULING_279_CROSSCHECK.json"))
    return280_audit = read_json(archive.read("current/docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9DEFENSEFORM8_RETURN280_INDEPENDENT_AUDIT.json"))
    return280_receipt = read_json(archive.read("current/docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9DEFENSEFORM8_RETURN280_RECEIPT.json"))
    return280_crosscheck = read_json(archive.read("current/docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_DEFENSEFORM8_RETURN280_CROSSCHECK.json"))
    check("Return279 Final Word hold remains preserved and crosschecked", latest279.get("heldIds") == ["final-word"] and latest279.get("blockerIds") == ["DR217-B01"] and latest279.get("acceptedIds") == latest279.get("appliedIds") == [] and latest279_audit.get("status") == "PASS", {"held": latest279.get("heldIds"), "blockers": latest279.get("blockerIds"), "crosscheck": latest279_audit.get("status")})
    check("Return280 Defense/Form8 hold is sealed, independently audited and crosschecked", return280_audit.get("status") == return280_receipt.get("status") == return280_crosscheck.get("status") == "PASS" and return280_audit.get("failedChecks") == 0 and return_delivery.get("heldIds") == ["elemental-shell", "timeless-form", "invulnerable-sphere"] and return_delivery.get("acceptedIds") == return_delivery.get("appliedIds") == [], {"audit": return280_audit.get("status"), "receipt": return280_receipt.get("status"), "crosscheck": return280_crosscheck.get("status"), "held": return_delivery.get("heldIds")})
    check("Packet281 keeps authority at 816/32/0 and requests only Ward/Control6", context.get("previousFinalWordReturn279", {}).get("blockerIds") == ["DR217-B01"] and context.get("previousDefenseFormReturn280", {}).get("heldIds") == ["elemental-shell", "timeless-form", "invulnerable-sphere"] and context.get("sourceAuthority") == AUTHORITY and set(candidate.get("currentPendingGroup", {}).get("spellIds", [])) == set(TARGETS), {"authority": context.get("sourceAuthority"), "wardTargets": candidate.get("currentPendingGroup"), "previousDefenseHolds": context.get("previousDefenseFormReturn280", {}).get("heldIds")})
'''
if marker not in source:
    raise RuntimeError("Cannot locate Ward/Control6 verifier extension point")
source = source.replace(marker, addition + marker, 1)
namespace = {"__name__": "__main__", "__file__": str(TEMPLATE)}
exec(compile(source, str(TEMPLATE), "exec"), namespace)
