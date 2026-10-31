from __future__ import annotations

from pathlib import Path


HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "prepare_defenseform8_current_236.py"
source = TEMPLATE.read_text(encoding="utf-8")

# Rebase the already-audited Packet236 build procedure onto the exact current
# authority checkpoint. The historical Return218 blocker evidence stays intact.
for old, new in (("236", "280"), ("811", "816"), ("37", "32"), ("535", "540")):
    if old not in source:
        raise RuntimeError(f"Expected template token is absent: {old}")
    source = source.replace(old, new)

source = source.replace(
    'q["status"] == "RETURN235_AUDITED_HELD_816_32_0_PACKET280_PREPARATION"',
    'q["status"] == "RETURN279_TEXT_HELD_816_32_NEXT_DEFENSEFORM8"',
)
source = source.replace(
    "and Return235's audited held decision.",
    "Return235's audited held decision and Return279's current text-only hold, crosscheck, Packet279 audit/receipt, and parent snapshots.",
)

marker = '    add(files, "current/RETURN235_RECEIPT.json", return235_receipt.read_bytes())\n'
addition = marker + '''    # Bind the immediately preceding Director decision and checkpoint so the
    # current-source review cannot reopen or lose Return279's hold.
    for member, local_name in [
        ("current/RETURN279_DIRECTOR_RULING.json", "DEATHRECOVERY7_DIRECTOR_RULING_279.json"),
        ("current/RETURN279_CROSSCHECK.json", "DEATHRECOVERY7_DIRECTOR_RULING_279_CROSSCHECK.json"),
        ("current/RETURN279_PACKET_AUDIT.json", "RANK9DEATHRECOVERY7_PACKET279_INDEPENDENT_AUDIT.json"),
        ("current/RETURN279_PACKET_RECEIPT.json", "RANK9DEATHRECOVERY7_PACKET279_RECEIPT.json"),
        ("history/Parent279/CURRENT_HANDOFF_279.json", "CURRENT_HANDOFF_279.json"),
        ("history/Parent279/CURRENT_SPELL_QUEUE_279.json", "CURRENT_SPELL_QUEUE_279.json"),
        ("history/Parent279/CURRENT32_PENDING_IDENTITY_AUDIT_279.json", "CURRENT32_PENDING_IDENTITY_AUDIT_279.json"),
        ("history/Parent279/CURRENT_SPELL_REVIEW_SNAPSHOT_279.md", "CURRENT_SPELL_REVIEW_SNAPSHOT_279.md"),
    ]:
        add(files, member, (BASE / local_name).read_bytes())
    latest_ruling = read(BASE / "DEATHRECOVERY7_DIRECTOR_RULING_279.json")
    latest_crosscheck = read(BASE / "DEATHRECOVERY7_DIRECTOR_RULING_279_CROSSCHECK.json")
    latest_packet_audit = read(BASE / "RANK9DEATHRECOVERY7_PACKET279_INDEPENDENT_AUDIT.json")
    latest_packet_receipt = read(BASE / "RANK9DEATHRECOVERY7_PACKET279_RECEIPT.json")
    assert latest_ruling["status"] == "DIRECTOR_TEXT_DECISION_COMPLETE_NOT_SEALED"
    assert latest_ruling["acceptedIds"] == latest_ruling["appliedIds"] == []
    assert latest_ruling["heldIds"] == ["final-word"] and latest_ruling["blockerIds"] == ["DR217-B01"]
    assert latest_crosscheck["status"] == "PASS" and latest_packet_audit["status"] == latest_packet_receipt["status"] == "PASS"
'''
if marker not in source:
    raise RuntimeError("Cannot locate packet member insertion point")
source = source.replace(marker, addition, 1)

marker = '    assert all(row["passed"] for row in checks), checks\n'
addition = '''    checks.append({
        "check": "Return279's exact text-only hold and passing Packet279 audit/receipt are carried forward",
        "passed": latest_ruling["authority"] == AUTHORITY
            and latest_ruling["heldIds"] == ["final-word"]
            and latest_ruling["acceptedIds"] == latest_ruling["appliedIds"] == []
            and latest_ruling["blockerIds"] == ["DR217-B01"]
            and latest_crosscheck["status"] == latest_packet_audit["status"] == latest_packet_receipt["status"] == "PASS"
            and latest_ruling["source"]["sealedReturnArchiveCreated"] is False,
    })
    assert all(row["passed"] for row in checks), checks
'''
if marker not in source:
    raise RuntimeError("Cannot locate independent preparation check block")
source = source.replace(marker, addition, 1)

# The template itself lives beside this wrapper, so its project-root resolution
# and all exact source-path rules remain unchanged.
namespace = {"__name__": "__main__", "__file__": str(TEMPLATE)}
exec(compile(source, str(TEMPLATE), "exec"), namespace)
