from __future__ import annotations

from pathlib import Path


HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "verify_defenseform8_packet236_independent.py"
source = TEMPLATE.read_text(encoding="utf-8")
for old, new in (("236", "280"), ("811", "816"), ("37", "32"), ("535", "540")):
    if old not in source:
        raise RuntimeError(f"Expected verifier token is absent: {old}")
    source = source.replace(old, new)

marker = 'failures = [row for row in checks if not row["passed"]]\n'
addition = '''    latest_ruling = read_json(z.read("current/RETURN279_DIRECTOR_RULING.json"))
    latest_crosscheck = read_json(z.read("current/RETURN279_CROSSCHECK.json"))
    latest_packet_audit = read_json(z.read("current/RETURN279_PACKET_AUDIT.json"))
    latest_packet_receipt = read_json(z.read("current/RETURN279_PACKET_RECEIPT.json"))
    check(
        "Return279 text-only hold and Packet279 audit/receipt are preserved without reopening Final Word",
        latest_ruling.get("authority") == AUTHORITY
        and latest_ruling.get("heldIds") == ["final-word"]
        and latest_ruling.get("acceptedIds") == latest_ruling.get("appliedIds") == []
        and latest_ruling.get("blockerIds") == ["DR217-B01"]
        and latest_ruling.get("source", {}).get("sealedReturnArchiveCreated") is False
        and latest_crosscheck.get("status") == latest_packet_audit.get("status") == latest_packet_receipt.get("status") == "PASS",
        {"heldIds": latest_ruling.get("heldIds"), "blockers": latest_ruling.get("blockerIds"),
         "crosscheck": latest_crosscheck.get("status"), "packetAudit": latest_packet_audit.get("status"),
         "packetReceipt": latest_packet_receipt.get("status")},
    )
    for member in (
        "history/Parent279/CURRENT_HANDOFF_279.json",
        "history/Parent279/CURRENT_SPELL_QUEUE_279.json",
        "history/Parent279/CURRENT32_PENDING_IDENTITY_AUDIT_279.json",
        "history/Parent279/CURRENT_SPELL_REVIEW_SNAPSHOT_279.md",
    ):
        check(f"Parent279 checkpoint artifact is present: {member}", member in name_set)

'''
if marker not in source:
    raise RuntimeError("Cannot locate verifier report block")
source = source.replace(marker, addition + marker, 1)
namespace = {"__name__": "__main__", "__file__": str(TEMPLATE)}
exec(compile(source, str(TEMPLATE), "exec"), namespace)
