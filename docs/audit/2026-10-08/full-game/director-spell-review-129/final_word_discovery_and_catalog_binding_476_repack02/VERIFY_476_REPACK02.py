from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[6]
REL = Path("docs/audit/2026-10-08/full-game/director-spell-review-129")
PACK = REL / "final_word_discovery_and_catalog_binding_476_repack02"
CATALOG = Path("DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json")
INDEX = Path("DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json")
QUEUE = REL / "CURRENT_SPELL_QUEUE_476_REPACK01.json"
PENDING = REL / "CURRENT17_PENDING_IDENTITY_AUDIT_476_REPACK01.json"
DECISION = REL / "FINAL_WORD_DIRECTOR_DECISION_303.json"
CHRONICLE = Path("docs/manuals/Chronicle_of_the_Decennial_Opening.md")
GAZETTEER = Path("docs/manuals/F51_100_Director_Deep_Gazetteer.md")
W07 = REL / "banishment_gate_witness363/packet/W07_GUST_CORPSE_CASE_363.json"
SOULS = REL / "rank7gateglyph3_return01_141_extracted/evidence/source01/sources/DescentReviewChanges/ReviewBible/docs/director-only/cosmology/SOULS_RESEARCH_REVIEWED_01.md"
LIFECYCLE = REL / "rank9_faction_incarnate_review_337_prepared_v2/packet/sources/02_CREATURE_LIFECYCLE_PLAYTEST.md"
SNAPSHOT = REL / "banishment_gate_witness365_w06_planes_shift_repack06_verified04/packet/sources/catalog.json"
SPELLS_SOURCE = Path("DescentReviewChanges/ReviewBible/src/data/spells.js")
CORE_SOURCE = Path("DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json")
OLD303 = REL / "rank9_final_word_closure_delta_303/DD_Rank9_FinalWord_ClosureDelta_303.zip"
EXPECTED_COMMIT = "f6e89fde9251b7807fe0125ec14670c46ff8edfa"
EXPECTED_CATALOG_BLOB = "2d243b311cded8484630c12b6fcc2ae7f70cfddf"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


checks: list[dict[str, object]] = []


def check(name: str, passed: bool, detail: str | None = None) -> None:
    checks.append({"name": name, "passed": bool(passed), **({"detail": detail} if detail else {})})


lead = read_json(PACK / "CHANGE_EVIDENCE_LEAD_SHEET_476_REPACK02.json")
correspondence = read_json(PACK / "CATALOG_BYTE_CORRESPONDENCE_476_REPACK02.json")
queue = read_json(QUEUE)
pending = read_json(PENDING)
decision = read_json(DECISION)
catalog_raw = (ROOT / CATALOG).read_bytes()
snapshot_raw = (ROOT / SNAPSHOT).read_bytes()
catalog = json.loads(catalog_raw.decode("utf-8"))
snapshot = json.loads(snapshot_raw.decode("utf-8"))
index = read_json(INDEX)
current_row = index["entries"][675]
with zipfile.ZipFile(ROOT / OLD303) as archive:
    old_catalog_raw = archive.read("current/catalog.json")
    old_index_raw = archive.read("current/authored_review_index.json")
old_index = json.loads(old_index_raw.decode("utf-8"))
old_row = next(row for row in old_index["entries"] if row.get("id") == "final-word")

expected_catalog_hash = "f52cf6a4a4673897615a74c7c67dcba798c431362d4357e71ee552cc7c5d31f8"
normalized_catalog = catalog_raw.replace(b"\r\n", b"\n")
check("pinned main source commit is available", git("cat-file", "-e", f"{EXPECTED_COMMIT}^{{commit}}") == "")
root_blob = git("rev-parse", f"{EXPECTED_COMMIT}:{CATALOG.as_posix()}")
snapshot_blob = git("rev-parse", f"{EXPECTED_COMMIT}:{SNAPSHOT.as_posix()}")
check("tracked catalog and archived snapshot bind to the recorded Git blob", root_blob == EXPECTED_CATALOG_BLOB and snapshot_blob == EXPECTED_CATALOG_BLOB)
check("CRLF-to-LF transformation exactly reproduces Queue476 snapshot", normalized_catalog == snapshot_raw and sha256(normalized_catalog) == expected_catalog_hash)
check("observed Windows checkout representation matches the recorded raw bytes", len(catalog_raw) == 5085187 and sha256(catalog_raw) == "773fb0b3b0fdb501858ded33c02d90dc4db3009bd1b9f7112c244d998218f05b" and catalog_raw.count(b"\r\n") == 139868)
spells_bytes = (ROOT / SPELLS_SOURCE).read_bytes()
core_bytes = (ROOT / CORE_SOURCE).read_bytes()
check("Final Word spells.js declared hash matches exact LF-normalized bytes", len(spells_bytes) == 1305184 and spells_bytes.count(b"\r\n") == 52725 and sha256(spells_bytes.replace(b"\r\n", b"\n")) == "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078")
check("Final Word core JSON declared hash matches exact LF-normalized bytes", len(core_bytes) == 450543 and core_bytes.count(b"\r\n") == 15851 and sha256(core_bytes.replace(b"\r\n", b"\n")) == "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f")
check("all 848 parsed catalog spell objects are equal", catalog == snapshot and len(catalog["spells"]) == 848)
check("Final Word catalog card at /spells/675 matches the W06 snapshot and archived 303 member", catalog["spells"][675] == snapshot["spells"][675] and catalog["spells"][675]["id"] == "final-word" and catalog_raw == old_catalog_raw)
check("current Final Word index row at /entries/675 equals archived 303 row", current_row == old_row and current_row["id"] == "final-word")
check("Queue476 pins the archived LF snapshot and remains 831/17/0", queue["currentCatalogBinding"]["bytes"] == 4945319 and queue["currentCatalogBinding"]["sha256"] == expected_catalog_hash and queue["currentAuthority"] == {"reviewedApplied": 831, "pending": 17, "acceptedUnapplied": 0, "completeStandaloneProcedures": 555, "scopedInterfaces": 173})
check("queue priority remains Elemental Shell first and Final Word second", queue["continuingPriorityOrder"][0] == "elemental-shell" and queue["continuingPriorityOrder"][1] == "final-word" and queue["nextIdentity"] == "elemental-shell")
check("retained Director decision holds Final Word and preserves minimum witness", decision["decision"] == "HOLD_FINAL_WORD_PENDING_POSITIVE_SOURCE_QUALIFIED_CAPTURE_WITNESS" and decision["accepted"] is False and decision["applied"] is False and len(decision["minimumMissingWitness"]) == 2)
check("current pending audit still lists Final Word", "final-word" in pending["pendingIds"] if "pendingIds" in pending else any(x.get("id") == "final-word" for x in pending.get("pending", [])))

chronicle_lines = (ROOT / CHRONICLE).read_text(encoding="utf-8").splitlines()
gazetteer_lines = (ROOT / GAZETTEER).read_text(encoding="utf-8").splitlines()
check("Chronicle historical soulbinding and adventure-seed anchors resolve", "Archpriest Gorthan" in chronicle_lines[144] and "Archpriest Gorthan" in chronicle_lines[331] and "Gorthan's Letter" in chronicle_lines[548])
check("F51 Gorthan name-recovery hook resolves at line 233", "Vaskurhollow name-recovery contracts (Archpriest Gorthan)" in gazetteer_lines[232])

w07 = read_json(W07)
guard = w07["initial"]["actors"]["Guard-W07-TESTONLY"]
check("W07 Guard is only a TEST_ONLY fixture and is HP 0/dying", guard["HP"] == 0 and guard["death"]["status"] == "dying" and "TEST_ONLY" in guard["custodyStatus"] and "not a campaign fact" in guard["custodyStatus"])
check("general Hunt and creature lifecycle sources match recorded hashes", sha256((ROOT / SOULS).read_bytes()) == "01e141c7b4c1d63f2ee1e82169d869378571428269500df749e3188a31545121" and sha256((ROOT / LIFECYCLE).read_bytes()) == "eae68470d4dba14aa74334e22270e35a8aea022d3c5013aa75a96c15d8e93b08")

unchanged_paths = [CATALOG.as_posix(), INDEX.as_posix(), QUEUE.as_posix()]
diff_clean = all(subprocess.run(["git", "diff", "--quiet", "--", path], cwd=ROOT).returncode == 0 for path in unchanged_paths)
staged_clean = all(subprocess.run(["git", "diff", "--cached", "--quiet", "--", path], cwd=ROOT).returncode == 0 for path in unchanged_paths)
check("catalog, index and Queue476 have no staged or unstaged edits", diff_clean and staged_clean)
check("lead sheet records no qualifying changed evidence and no identity/queue effects", lead["status"] == "COMPLETE_NO_QUALIFYING_CHANGED_EVIDENCE" and lead["conclusion"]["identityAccepted"] is False and lead["conclusion"]["identityApplied"] is False and lead["conclusion"]["queueChanged"] is False)
check("byte-correspondence record states no silent normalization or rule/queue effects", correspondence["status"] == "PASS_EXACT_CRLF_TO_LF_CORRESPONDENCE" and correspondence["effects"]["catalogSilentlyNormalized"] is False and correspondence["effects"]["queue476Modified"] is False)

passed = sum(item["passed"] for item in checks)
packet_paths = [PACK / "CHANGE_EVIDENCE_LEAD_SHEET_476_REPACK02.json", PACK / "CATALOG_BYTE_CORRESPONDENCE_476_REPACK02.json"]
validation = {
    "status": "PASS" if passed == len(checks) else "FAIL",
    "passed": passed,
    "failed": len(checks) - passed,
    "packetFiles": [
        {"path": path.as_posix(), "bytes": (ROOT / path).stat().st_size, "sha256": sha256((ROOT / path).read_bytes())}
        for path in packet_paths
    ],
    "checks": checks,
}
validation_path = ROOT / PACK / "VALIDATION_476_REPACK02.json"
validation_path.write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(validation, ensure_ascii=False, indent=2))
raise SystemExit(0 if passed == len(checks) else 1)
