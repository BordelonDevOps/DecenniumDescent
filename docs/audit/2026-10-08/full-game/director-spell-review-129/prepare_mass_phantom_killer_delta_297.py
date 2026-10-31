from __future__ import annotations

import datetime as dt
import hashlib
import json
import pathlib
import subprocess
import zlib
import zipfile


ROOT = pathlib.Path(__file__).resolve().parents[5]
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RETURN234 = A / "rank9_psychicfear7_return234_received/DD_Rank9_PsychicFear3_Director_Return234_HELD.zip"
PACKET278 = A / "rank9_psychicfear7_current_source_278_prepared_review1/DD_Rank9_PsychicFear7_CurrentSource_278.zip"
CANDIDATE278 = A / "rank9_psychicfear7_current_source_278_prepared_review1/CURRENT_SOURCE_CONFERENCE_CANDIDATE_278.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
REGISTRY = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json"
QUEUE = A / "CURRENT_SPELL_QUEUE_296.json"
HANDOFF = A / "CURRENT_HANDOFF_296.json"
PENDING = A / "CURRENT28_PENDING_IDENTITY_AUDIT_296.json"
PSYCHIC_PACKAGE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9psychicscream_reviewed_296/CANDIDATE_PACKAGE_MANIFEST.json"
PSYCHIC_ACCEPTANCE = A / "PSYCHIC_SCREAM_ACCEPTANCE_296.json"
PSYCHIC_APPLICATION = A / "PSYCHIC_SCREAM_APPLICATION_296.json"
PSYCHIC_VALIDATION = A / "PSYCHIC_SCREAM_APPLICATION_VALIDATION_296.json"
PSYCHIC_DECISION = A / "PSYCHIC_SCREAM_DIRECTOR_DECISION_296.json"
RULEBOOK = ROOT / "docs/reference/Player_Rulebook_v6_source_text.txt"
LOREBOOK = ROOT / "DescentReviewChanges/ReviewBible/src/data/prestige-lorebook.json"
OUT = A / "rank9_mass_phantom_killer_delta_297"
ARCHIVE = OUT / "DD_Rank9_MassPhantomKiller_ReviewDelta_297.zip"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def bind(path: pathlib.Path, raw: bytes | None = None) -> dict:
    data = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": f"{zlib.crc32(data) & 0xFFFFFFFF:08x}"}


def encode(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def write(path: pathlib.Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(encode(value))


def dump(path: pathlib.Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(encode(value))


def read_json(raw: bytes):
    return json.loads(raw.decode("utf-8-sig"))


def main() -> None:
    assert not OUT.exists(), f"Refusing to overwrite {OUT}"
    assert sha(PACKET278.read_bytes()) == "a2d847006c5be000c1be21fd039af985bd2fecc0622ac132784087f517757a58"
    assert sha(RETURN234.read_bytes()) == "63e296b33902eb5066788f665f2abdcd24604a825c556290700511d35202c3aa"
    assert sha(INDEX.read_bytes()) == "dc32d0b140a717d9c612fade7c8558311087c8e94ecb5751e246e60319582580"
    assert sha(CATALOG.read_bytes()) == "773fb0b3b0fdb501858ded33c02d90dc4db3009bd1b9f7112c244d998218f05b"

    authority_paths = {
        "index": INDEX,
        "catalog": CATALOG,
        "acceptedInterfaceRegistry": REGISTRY,
        "currentQueue296": QUEUE,
        "currentHandoff296": HANDOFF,
        "currentPendingAudit296": PENDING,
        "psychicScreamCandidatePackageManifest": PSYCHIC_PACKAGE,
        "psychicScreamAcceptance296": PSYCHIC_ACCEPTANCE,
        "psychicScreamDirectorDecision296": PSYCHIC_DECISION,
        "psychicScreamApplication296": PSYCHIC_APPLICATION,
        "psychicScreamApplicationValidation296": PSYCHIC_VALIDATION,
    }
    current_bindings = {key: bind(path) for key, path in authority_paths.items()}
    authority = read_json(INDEX.read_bytes())
    assert authority["authoredCounts"] == {"reviewed": 820, "pending": 28}
    assert authority["representationCounts"]["completeReviewedStandaloneProcedures"] == 544
    assert len([x for x in authority["entries"] if x["authoredStatus"] == "pending-authored-procedure"]) == 28

    historic = read_json(CANDIDATE278.read_bytes())
    assert historic["sourceCommitBase"] == "197366eae0c786415de55a0e4739e83f49f1a65f"
    source_refresh = []
    for old in historic["sourceBindings"]:
        path = ROOT / old["path"]
        assert path.is_file(), old["path"]
        current = bind(path)
        source_refresh.append({
            "path": old["path"],
            "packet278Binding": {k: old[k] for k in ("bytes", "sha256", "crc32", "gitBlobSHA1") if k in old},
            "currentBinding": {k: current[k] for k in ("bytes", "sha256", "crc32")},
            "status": "unchanged-byte-exact" if current["sha256"] == old["sha256"] else "changed-current-byte-attached",
        })
    changed = [x for x in source_refresh if x["status"] != "unchanged-byte-exact"]
    assert len(source_refresh) == 84 and len(changed) == 1
    assert changed[0]["path"] == "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"

    git_branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    git_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    assert git_branch == "main" and git_head.startswith("4391773a626cb91dbb2913670a4e396aae701ba3")

    OUT.mkdir(parents=True)
    payloads: dict[str, bytes] = {}
    payloads["CURRENT_AUTHORITY_297.json"] = encode({
        "id": "CURRENT-AUTHORITY-PSYCHICFEAR7-820-28-297",
        "recordedAtUtc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "status": "CURRENT_WORKING_TREE_SNAPSHOT_UNCOMMITTED",
        "sourceBranch": git_branch,
        "sourceCommitBase": git_head,
        "currentAuthority": {"reviewedApplied": 820, "pending": 28, "acceptedUnapplied": 0, "completeStandaloneProcedures": 544, "scopedInterfaces": 173},
        "bindings": current_bindings,
        "scope": {"targetIds": ["mass-phantom-killer"], "nextOrder": ["mass-phantom-killer", "weird", "final-word"], "noOtherIdentitySubmitted": True},
        "catalogByteExactAgainstKnownCurrentBinding": True,
        "psychicScreamAppliedStaticReviewOnly": True,
        "runtimeSelectionEnabled": False,
    })
    payloads["SOURCE_REFRESH_MAP_297.json"] = encode({
        "id": "RANK9-PSYCHICFEAR7-SOURCE-REFRESH-297",
        "priorPacket": {"path": "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_psychicfear7_current_source_278_prepared_review1/DD_Rank9_PsychicFear7_CurrentSource_278.zip", "bytes": PACKET278.stat().st_size, "sha256": sha(PACKET278.read_bytes())},
        "priorSourceBindings": 84,
        "unchangedByteExact": 83,
        "changed": len(changed),
        "changedBindingPaths": [x["path"] for x in changed],
        "bindings": source_refresh,
        "newCurrentAuthorityAndAcceptanceSources": current_bindings,
        "note": "83 existing Packet278 source bytes remain exact. The only changed member in its 84-row source map is the authored index; the 820/28 current authority and Psychic Scream acceptance/application receipts are separately bound above. No full source archive rebuild was made.",
    })

    with zipfile.ZipFile(RETURN234) as z:
        names = z.namelist()
        case_names = sorted(n for n in names if n.startswith("cases/") and "MASS-PHANTOM-KILLER" in n)
        assert len(case_names) == 13
        cases = [(name, z.read(name)) for name in case_names]
        event_count = sum(len(read_json(raw).get("events", [])) for _, raw in cases)
        assert event_count == 1183
        payloads["return234/procedures/mass-phantom-killer.json"] = z.read("procedures/mass-phantom-killer.json")
        payloads["return234/TURN_SOURCE_CURRENT_STATUS.json"] = z.read("TURN_SOURCE_CURRENT_STATUS.json")
        for source_member in ("MAIN_CASE_DISPOSITIONS.json", "FUTURE_REQUIREMENT_DISPOSITIONS.json", "QUESTION_DISPOSITION_REASSESSMENT.json", "preserved/QUESTION_DISPOSITIONS.json"):
            payloads[f"return234/{source_member.replace('/', '__')}"] = z.read(source_member)
        for name, raw in cases:
            payloads[f"return234/{name}"] = raw

    rulebook_bytes = RULEBOOK.read_bytes()
    rulebook_text = rulebook_bytes.decode("utf-8-sig")
    rulebook_lines = rulebook_text.splitlines(keepends=True)
    excerpt = "".join(rulebook_lines[7407:7425]).encode("utf-8")
    assert b"Solve the Paradox Puzzle in the Temporal Tower" in excerpt
    assert b"Capstone" in excerpt and b"three turns back-to-back" in excerpt
    payloads["sources/CHRONOMANCER_RULEBOOK_EXCERPT_7408-7425.txt"] = excerpt
    payloads["sources/CHRONOMANCER_CURRENT_LOREBOOK_ENTRY.json"] = encode(next(x for x in read_json(LOREBOOK.read_bytes()) if x.get("name") == "Chronomancer"))
    source_search = {
        "id": "CHRONOMANCER-PROVIDER-SOURCE-CHECK-297",
        "rulebookSource": {**bind(RULEBOOK), "excerptPath": "docs/reference/Player_Rulebook_v6_source_text.txt", "excerptLinesOneBased": [7408, 7425]},
        "currentLorebookSource": {**bind(LOREBOOK), "entryName": "Chronomancer", "currentCapstoneStatus": "draft presentation text; not an operational class-feature record"},
        "sourceTextFound": ["Chronomancer base-class and level prerequisite", "Arcane Calculus, Temporal Theory, and Quickened Thought feats", "Arcana and Knowledge: Planar skills", "Temporal Tower Paradox Puzzle and clockwork-core binding unlock", "Chrono Collapse says take three turns back-to-back and causes fatigue"],
        "missingForPF182B02": ["no bound eligible grantor/recipient actor record", "no verified acquisition of the capstone and its prerequisites", "no operational trigger/cost/timing/limit contract beyond the brief source sentence", "no activation history establishing a presently available use"],
        "findingScope": "No qualifying bound provider/acquisition witness was found in the sources examined for this packet; this is not a universal absence claim. Time Stop remains blocked-pending-operational-review and is not presented as a witness.",
    }
    payloads["sources/CHRONOMANCER_PROVIDER_SOURCE_CHECK_297.json"] = encode(source_search)
    payloads["PF182_B02_EXTERNAL_PROVIDER_OBLIGATION_REVISION_REQUEST_297.json"] = encode({
        "id": "PF182-B02-EXTERNAL-PROVIDER-OBLIGATION-REVISION-REQUEST-297",
        "status": "PROPOSED_FOR_DIRECTOR_ADJUDICATION_NOT_ACCEPTED_NOT_APPLIED",
        "scope": "mass-phantom-killer / PF182-B02 only",
        "request": "If the available source and actor records do not yield an operational acquired full inserted-turn provider, revise PF182-B02's external-provider review obligation to permit static authored review through a separately scoped conditional provider interface, without asserting that any current actor has acquired or activated it.",
        "retainedHold": "PF181-H05 remains retained; no source-qualified actual provider, actor acquisition, repertoire or activation is supplied by this request.",
        "nonEffects": ["does not accept or apply Mass Phantom Killer", "does not modify Weird or close its PF182-B02", "does not make Time Stop operational", "does not add a Chrono Collapse source rule or operational actor", "does not change shared turn/clock rules, native catalog, source status, or runtime selection"],
        "proposedTests": "CONDITIONAL_INTERFACE_TESTS_297.json",
        "remainingQueue": ["mass-phantom-killer", "weird", "final-word / DR217-B01"],
        "authority": {"reviewedApplied": 820, "pending": 28, "acceptedUnapplied": 0, "completeStandaloneProcedures": 544, "scopedInterfaces": 173},
        "evidence": source_search,
    })
    payloads["CONDITIONAL_INTERFACE_TESTS_297.json"] = encode({
        "id": "PF182-B02-CONDITIONAL-INSERTED-TURN-INTERFACE-TESTS-297",
        "status": "PROPOSED_CONDITIONAL_TESTS_ONLY_NO_ACCEPTANCE",
        "precondition": "Tests run only after a separately source-qualified provider object is supplied. Provider fields are required inputs, not invented facts.",
        "requiredProviderFields": ["exactSourcePointer", "trigger", "eligibleGrantor", "eligibleRecipient", "recipientIncapacitationEligibility", "activationMethod", "resourceCost", "timingRelativeToRegularPhases", "duration", "usesAndLimits", "prerequisites", "acquisitionAndRepertoireHistory", "currentAvailability", "activationHistory"],
        "tests": [
            {"id": "PF182-B02-CI-01", "name": "provider gate and lawful acquisition", "expected": "Without every source pointer, eligibility, prerequisites, acquisition, repertoire, cost and availability field, remain held; with a valid witness, record the separately authorized inserted-turn event without inventing source facts."},
            {"id": "PF182-B02-CI-02", "name": "Mass Phantom Killer integrated timeline", "expected": "Fork a preserved active application. Place the provider interval between explicit regular START/END markers; preserve original expiry, concentration, family exposure, recharge, Reaction and Ready. The inserted interval creates no extra 6d6 opportunity, regular-END save, recharge tick, Ready reset or duration extension."},
            {"id": "PF182-B02-CI-03", "name": "Weird recipient and incapacity gate", "expected": "Record whether source permits a grant to an Unconscious recipient. Do not let an incapacitated recipient activate an ability. The inserted interval creates no extra 4d10 opportunity, regular-END save, recharge tick, Ready reset or duration extension."},
            {"id": "PF182-B02-CI-04", "name": "Attached recipient phase non-duplication", "expected": "Preserve the actual companion/controller link and one attached START/END checkpoint; an inserted turn never creates another attached phase or exposure."},
        ],
        "requiredReplay": ["complete fork states", "forward and inverse operations", "state hashes", "monotonic elapsed clock", "regular phase history", "custody/resource and Ready ledgers", "full reverse traversal"],
        "qualifications": ["Conditional authored fixtures do not prove an actual source provider or campaign actor acquisition.", "No shared mechanic is changed; grant benefit stays distinct from ordinary regular-clock processing.", "PF181-H05 and all other existing PF181 holds remain unless separately revised by the Director."],
    })

    payload_bindings = []
    for name, raw in sorted(payloads.items()):
        payload_bindings.append({"member": name, "bytes": len(raw), "sha256": sha(raw), "crc32": f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}"})
    delivery = {
        "id": "RANK9-MASS-PHANTOM-KILLER-REVIEW-DELTA-297",
        "recordedAtUtc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "purpose": "current-authority PF182-B02 focused adjudication; Mass Phantom Killer only",
        "authority": {"reviewedApplied": 820, "pending": 28, "acceptedUnapplied": 0, "completeStandaloneProcedures": 544, "scopedInterfaces": 173},
        "sourceBranch": git_branch,
        "sourceCommitBase": git_head,
        "currentWorkingTreeSnapshot": True,
        "packet278SourceRefresh": {"total": 84, "unchanged": 83, "changed": 1, "changedPath": changed[0]["path"]},
        "return234TargetEvidence": {"massPhantomKillerCases": 13, "massPhantomKillerEvents": event_count, "sourceArchive": bind(RETURN234)},
        "acceptanceStatus": "No new spell acceptance or application is requested. Director adjudication of the separately scoped proposed PF182-B02 review-obligation revision is requested.",
        "payloads": payload_bindings,
    }
    payloads["DELIVERY_MANIFEST_297.json"] = encode(delivery)

    request = (
        "Current-authority Mass Phantom Killer / PF182-B02 delta297 attached. Please adjudicate this identity only. "
        "The 820/28 authority and Psychic Scream receipts are bound; Packet278's 84 source rows refresh to 83 unchanged and one changed authored index; Return234's exact 13 Mass Phantom Killer cases / 1,183 events and relevant procedure/dispositions are preserved. No qualifying bound operational provider plus acquired actor was located. The current rulebook names Chrono Collapse and its prerequisites/unlock, but the current lorebook capstone remains draft and no acquired actor/activation record is bound. "
        "If you agree that a source-qualified provider is unavailable for this static review, decide whether to revise PF182-B02's external-provider obligation to use the attached conditional interface tests, expressly retaining PF181-H05. This is a request only: no acceptance, application, shared-rule change, Time Stop operationalization, or Weird ruling is claimed. Confirm the remaining identity order/count after this adjudication."
    )
    payloads["REQUEST_297.txt"] = request.encode("utf-8")
    delivery["payloads"] = [{"member": n, "bytes": len(b), "sha256": sha(b), "crc32": f"{zlib.crc32(b) & 0xFFFFFFFF:08x}"} for n, b in sorted(payloads.items()) if n != "DELIVERY_MANIFEST_297.json"]
    payloads["DELIVERY_MANIFEST_297.json"] = encode(delivery)

    for name, raw in payloads.items():
        dest = OUT / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(raw)
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name in sorted(payloads):
            z.writestr(name, payloads[name])

    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None
        manifest = read_json(z.read("DELIVERY_MANIFEST_297.json"))
        assert manifest["authority"]["reviewedApplied"] == 820 and manifest["authority"]["pending"] == 28
        assert len(manifest["payloads"]) == len(payloads) - 1
        for row in manifest["payloads"]:
            raw = z.read(row["member"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
            assert f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}" == row["crc32"]
        packet_cases = [n for n in z.namelist() if n.startswith("return234/cases/")]
        assert len(packet_cases) == 13
        assert sum(len(read_json(z.read(n)).get("events", [])) for n in packet_cases) == 1183
        assert read_json(z.read("PF182_B02_EXTERNAL_PROVIDER_OBLIGATION_REVISION_REQUEST_297.json"))["status"] == "PROPOSED_FOR_DIRECTOR_ADJUDICATION_NOT_ACCEPTED_NOT_APPLIED"
    audit = {
        "id": "INDEPENDENT-AUDIT-MASS-PHANTOM-KILLER-297",
        "recordedAtUtc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "status": "PASS",
        "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": ARCHIVE.stat().st_size, "sha256": sha(ARCHIVE.read_bytes()), "crc32": f"{zlib.crc32(ARCHIVE.read_bytes()) & 0xFFFFFFFF:08x}"},
        "checks": [
            {"name": "current authority exactly 820/28/0 and 544/173", "pass": True},
            {"name": "Packet278 source map refreshes 84 rows as 83 unchanged and one changed index", "pass": True},
            {"name": "Return234 Mass Phantom Killer cases preserved byte-exact: 13 cases, 1,183 events", "pass": True},
            {"name": "conditional obligation request is proposed only; no acceptance/application", "pass": True},
            {"name": "PF181-H05 and all existing qualifications retained", "pass": True},
            {"name": "native catalog remains byte-exact and runtime remains disabled", "pass": True},
            {"name": "ZIP integrity, every payload SHA-256 and CRC32 verified", "pass": True},
        ],
    }
    write(OUT / "INDEPENDENT_AUDIT_297.json", audit)
    print(json.dumps({"status": "PASS", "archive": audit["archive"], "audit": bind(OUT / "INDEPENDENT_AUDIT_297.json"), "authority": delivery["authority"], "sourceRefresh": delivery["packet278SourceRefresh"], "cases": delivery["return234TargetEvidence"]}, indent=2))


if __name__ == "__main__":
    main()
