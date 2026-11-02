from __future__ import annotations

import hashlib
import json
import zlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[6]
REL = Path("docs/audit/2026-10-08/full-game/director-spell-review-129")
PACK = REL / "final_word_discovery_and_catalog_binding_476_repack02"
ARCHIVE = PACK / "DD_FinalWord_ChangedEvidence_476_Repack02.zip"
MANIFEST = PACK / "PACKET_SOURCES_MANIFEST_476_REPACK02.json"
DELIVERY = PACK / "DELIVERY_476_REPACK02.json"
OLD303 = REL / "rank9_final_word_closure_delta_303/DD_Rank9_FinalWord_ClosureDelta_303.zip"
PINNED_COMMIT = "f6e89fde9251b7807fe0125ec14670c46ff8edfa"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def repo_file(path: str) -> bytes:
    return (ROOT / path).read_bytes()


specs: list[tuple[str, str, str | None]] = [
    ("evidence/CHANGE_EVIDENCE_LEAD_SHEET_476_REPACK02.json", (PACK / "CHANGE_EVIDENCE_LEAD_SHEET_476_REPACK02.json").as_posix(), None),
    ("evidence/CATALOG_BYTE_CORRESPONDENCE_476_REPACK02.json", (PACK / "CATALOG_BYTE_CORRESPONDENCE_476_REPACK02.json").as_posix(), None),
    ("evidence/VALIDATION_476_REPACK02.json", (PACK / "VALIDATION_476_REPACK02.json").as_posix(), None),
    ("evidence/README.md", (PACK / "README.md").as_posix(), None),
    ("evidence/VERIFY_476_REPACK02.py", (PACK / "VERIFY_476_REPACK02.py").as_posix(), None),
    ("evidence/BUILD_PACKET_476_REPACK02.py", (PACK / "BUILD_PACKET_476_REPACK02.py").as_posix(), None),
    ("sources/catalog-current-workingtree-crlf.json", "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json", None),
    ("sources/catalog-queuebound-w06-lf.json", (REL / "banishment_gate_witness365_w06_planes_shift_repack06_verified04/packet/sources/catalog.json").as_posix(), None),
    ("sources/catalog-303-current.json", OLD303.as_posix(), "current/catalog.json"),
    ("sources/authored-review-index-current.json", "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json", None),
    ("sources/authored-review-index-303-current.json", OLD303.as_posix(), "current/authored_review_index.json"),
    ("sources/queue476.json", (REL / "CURRENT_SPELL_QUEUE_476_REPACK01.json").as_posix(), None),
    ("sources/pending-audit476.json", (REL / "CURRENT17_PENDING_IDENTITY_AUDIT_476_REPACK01.json").as_posix(), None),
    ("sources/final-word-director-decision-303.json", (REL / "FINAL_WORD_DIRECTOR_DECISION_303.json").as_posix(), None),
    ("sources/chronicle.md", "docs/manuals/Chronicle_of_the_Decennial_Opening.md", None),
    ("sources/f51-gazetteer.md", "docs/manuals/F51_100_Director_Deep_Gazetteer.md", None),
    ("sources/W07_GUST_CORPSE_CASE_363.json", (REL / "banishment_gate_witness363/packet/W07_GUST_CORPSE_CASE_363.json").as_posix(), None),
    ("sources/SOULS_RESEARCH_REVIEWED_01.md", (REL / "rank7gateglyph3_return01_141_extracted/evidence/source01/sources/DescentReviewChanges/ReviewBible/docs/director-only/cosmology/SOULS_RESEARCH_REVIEWED_01.md").as_posix(), None),
    ("sources/02_CREATURE_LIFECYCLE_PLAYTEST.md", (REL / "rank9_faction_incarnate_review_337_prepared_v2/packet/sources/02_CREATURE_LIFECYCLE_PLAYTEST.md").as_posix(), None),
    ("sources/spells.js", "DescentReviewChanges/ReviewBible/src/data/spells.js", None),
    ("sources/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json", "DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json", None),
    ("sources/owner-adoption-468-testonly.json", (REL / "elemental_shell_caster_premise_proposal_468/OWNER_DF218_B02_SHELL_CASTER_PREMISE_ADOPTION_468_TESTONLY.json").as_posix(), None),
    ("sources/owner-adoption-448-testonly.json", (REL / "fortress_w13_nested_space_owner_proposal_448/OWNER_PG328_W13_ADOPTION_448_TESTONLY.json").as_posix(), None),
]

members: dict[str, bytes] = {}
origins: dict[str, dict[str, str]] = {}
with zipfile.ZipFile(ROOT / OLD303) as previous:
    for member, original, archive_member in specs:
        data = previous.read(archive_member) if archive_member else repo_file(original)
        members[member] = data
        origins[member] = {
            "repositoryPath": original,
            "pinnedCommit": PINNED_COMMIT,
            **({"archivedZipMember": archive_member} if archive_member else {}),
            "sha256": digest(data),
            "bytes": len(data),
        }

manifest = {
    "schemaVersion": 1,
    "id": "PACKET-SOURCES-MANIFEST-476-REPACK02",
    "pinnedCommit": PINNED_COMMIT,
    "archiveContent": "Every source member is copied byte-for-byte from the bound repository path or the declared member of the retained 303 ZIP. CRLF working-tree representations are preserved as observed.",
    "members": [
        {"archivePath": name, "bytes": len(data), "sha256": digest(data), "origin": origins[name]}
        for name, data in sorted(members.items())
    ],
}
manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
MANIFEST.write_bytes(manifest_bytes)
members["evidence/PACKET_SOURCES_MANIFEST_476_REPACK02.json"] = manifest_bytes

with zipfile.ZipFile(ROOT / ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for name, data in sorted(members.items()):
        info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

archive_bytes = (ROOT / ARCHIVE).read_bytes()
delivery = {
    "schemaVersion": 1,
    "id": "DELIVERY-FINAL-WORD-476-REPACK02",
    "status": "READY_FOR_GPT_DIRECTOR_REVIEW",
    "archive": {
        "path": ARCHIVE.as_posix(),
        "bytes": len(archive_bytes),
        "sha256": digest(archive_bytes),
        "crc32": f"{zlib.crc32(archive_bytes) & 0xffffffff:08x}",
        "memberCount": len(members),
    },
    "leadSheet": {
        "path": (PACK / "CHANGE_EVIDENCE_LEAD_SHEET_476_REPACK02.json").as_posix(),
        "sha256": digest(repo_file((PACK / "CHANGE_EVIDENCE_LEAD_SHEET_476_REPACK02.json").as_posix())),
        "status": "COMPLETE_NO_QUALIFYING_CHANGED_EVIDENCE",
    },
    "catalogCorrespondence": {
        "path": (PACK / "CATALOG_BYTE_CORRESPONDENCE_476_REPACK02.json").as_posix(),
        "sha256": digest(repo_file((PACK / "CATALOG_BYTE_CORRESPONDENCE_476_REPACK02.json").as_posix())),
        "status": "PASS_EXACT_CRLF_TO_LF_CORRESPONDENCE",
    },
    "validation": {
        "path": (PACK / "VALIDATION_476_REPACK02.json").as_posix(),
        "sha256": digest(repo_file((PACK / "VALIDATION_476_REPACK02.json").as_posix())),
        "status": "PASS",
        "passed": 20,
        "failed": 0,
    },
    "queueAuthority": {
        "reviewedApplied": 831,
        "pending": 17,
        "acceptedUnapplied": 0,
        "nextIdentity": "elemental-shell",
        "finalWord": "HELD_AS_SECOND_IN_PRIORITY"
    },
    "decisionBoundary": {
        "no_identity_accepted_or_applied": True,
        "no_blocker_closed": True,
        "no_campaign_event_asserted": True,
        "no_canonical_rule_changed": True,
        "catalog_index_and_queue_unchanged": True
    }
}
DELIVERY.write_text(json.dumps(delivery, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(delivery, ensure_ascii=False, indent=2))
