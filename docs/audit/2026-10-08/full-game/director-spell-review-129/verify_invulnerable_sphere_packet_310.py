from __future__ import annotations

import datetime as dt
import hashlib
import json
import pathlib
import subprocess
import zlib
import zipfile

ROOT = pathlib.Path.cwd()
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = A / "rank9_defenseform8_current_source_310_prepared"
PACKET = OUT / "DD_Rank9_DefenseForm8_CurrentSource_310.zip"
DELIVERY = OUT / "DD_Rank9_DefenseForm8_CurrentSource_310_DELIVERY.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
AUTH = {"reviewedApplied": 822, "pending": 26, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 546, "scopedInterfaces": 173}
SPHERE_CASES = [
    "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-A", "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-B",
    "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-B1-TELEPORT", "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-B2-CONSENT-END",
    "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-B3-HIDDEN-OCCUPANCY", "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-B4-PLANAR",
    "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-B5-CONTROL", "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-COUNTER",
    "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-GATE-access", "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-GATE-components",
    "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-GATE-range", "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-GATE-resource",
    "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-READY-EXPIRES", "DF218-SPHERE-ACTUAL-CROWN-COMMAND",
]


def read(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def digest(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
            "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def check(name: str, passed: bool, detail: str = "") -> dict:
    return {"check": name, "passed": bool(passed), "detail": detail}


def main() -> None:
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    packet_raw = PACKET.read_bytes()
    delivery = read(DELIVERY)
    archive = digest(packet_raw)
    results: list[dict] = []
    results.append(check("outer archive binding", archive == {k: delivery["archive"][k] for k in archive},
                         f"{archive['bytes']} bytes; SHA-256 {archive['sha256']}; CRC32 {archive['crc32']}"))
    with zipfile.ZipFile(PACKET) as z:
        names = z.namelist()
        name_set = set(names)
        results.append(check("ZIP integrity, safe unique names and exact member count",
                             z.testzip() is None and len(names) == len(name_set) == delivery["memberCount"]
                             and all(not pathlib.PurePosixPath(n).is_absolute() and ".." not in pathlib.PurePosixPath(n).parts for n in names),
                             f"{len(names)} unique members"))
        manifest_raw = z.read("MEMBER_MANIFEST.json")
        manifest = json.loads(manifest_raw)
        results.append(check("exact payload allowlist and self-excluding manifest",
                             "MEMBER_MANIFEST.json" not in {r["path"] for r in manifest["members"]}
                             and manifest["memberCountExcludingSelf"] == len(names) - 1
                             and set(delivery["exactAllowlist"]) == name_set
                             and {r["path"] for r in delivery["members"]} == name_set
                             and digest(manifest_raw) == {k: delivery["memberManifest"][k] for k in digest(manifest_raw)},
                             f"{len(manifest['members'])} internal payload rows"))
        external_rows = {r["path"]: r for r in delivery["members"]}
        internal_rows = {r["path"]: r for r in manifest["members"]}
        member_ok = set(external_rows) == name_set and set(internal_rows) == name_set - {"MEMBER_MANIFEST.json"}
        for path in name_set:
            actual = digest(z.read(path))
            member_ok &= actual == {k: external_rows[path][k] for k in actual}
            if path != "MEMBER_MANIFEST.json":
                member_ok &= actual == {k: internal_rows[path][k] for k in actual}
        results.append(check("all external and internal member hashes/CRCs", member_ok,
                             f"{len(external_rows)} external rows; {len(internal_rows)} internal rows"))

        current_authority = json.loads(z.read("current/CURRENT_AUTHORITY_310.json"))
        candidate = json.loads(z.read("current/CURRENT_SOURCE_CONFERENCE_CANDIDATE_310.json"))
        leads = json.loads(z.read("current/SOURCE_SEARCH_LEADS_310.json"))
        requirements = json.loads(z.read("current/INVULNERABLE_SPHERE_DIRECTOR_REQUIREMENTS_310.json"))
        q_in = json.loads(z.read("current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_309.json"))
        h_in = json.loads(z.read("current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_309.json"))
        p_in = json.loads(z.read("current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT26_PENDING_IDENTITY_AUDIT_308.json"))
        index = json.loads(z.read("current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"))
        catalog = json.loads(z.read("current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"))
        by_index = {r["id"]: r for r in index["entries"]}
        by_catalog = {r["id"]: r for r in catalog["spells"]}
        results.append(check("exact current scope and unchanged authority",
                             delivery["targetIds"] == ["invulnerable-sphere"]
                             and delivery["authority"] == current_authority["authority"] == AUTH
                             and candidate["currentPendingGroup"]["spellIds"] == ["invulnerable-sphere"]
                             and q_in["currentAuthority"] == h_in["currentAuthority"] == p_in["authority"] == AUTH,
                             "Sphere / DF218-B04 only at 822/26/0, 546/173"))
        results.append(check("Sphere and Time Stop remain pending/non-operational",
                             by_index["invulnerable-sphere"]["authoredStatus"] == "pending-authored-procedure"
                             and by_catalog["invulnerable-sphere"].get("operational") is None
                             and by_index["time-stop"]["authoredStatus"] == "pending-authored-procedure"
                             and by_catalog["time-stop"].get("operational") is None,
                             "no operational card or acceptance is inferred"))
        results.append(check("current queue selects Sphere first and preserves parent bindings",
                             q_in["next"]["pendingIds"] == ["invulnerable-sphere"]
                             and q_in["next"]["blockerByIdentity"] == {"invulnerable-sphere": ["DF218-B04"]}
                             and q_in["next"]["status"] == "DIRECTOR_NEXT_AFTER_TIMELESS_FORM_HOLD_308",
                             "queue309 and handoff309 are the packet inputs"))
        results.append(check("source-search leads are explicitly non-findings",
                             leads["scopeIds"] == ["invulnerable-sphere"] and leads["leadsAreNotFindings"] is True
                             and len(leads["leads"]) == 5
                             and requirements["scopeIds"] == ["invulnerable-sphere"]
                             and requirements["blockerIds"] == ["DF218-B04"],
                             "no route, actor, or positive encounter is invented"))

        # The packet binds 87 current source files and these exact bytes match both
        # the current repository and the preexisting Packet308 source snapshot.
        source_rows = delivery["sourceBindings"]
        sources_ok = len(source_rows) == 87
        packet308 = A / "rank9_defenseform8_current_source_308_prepared/DD_Rank9_DefenseForm8_CurrentSource_308.zip"
        with zipfile.ZipFile(packet308) as old_source:
            old_names = set(old_source.namelist())
            for row in source_rows:
                path = row["path"]
                actual_path = "sources_current/" + path
                live = ROOT / pathlib.Path(path)
                row_digest = {k: row[k] for k in ("bytes", "sha256", "crc32")}
                current_bytes = z.read(actual_path) if actual_path in name_set else b""
                old_bytes = old_source.read(actual_path) if actual_path in old_names else b""
                live_bytes = live.read_bytes() if live.exists() else b""
                sources_ok &= digest(current_bytes) == row_digest and digest(old_bytes) == row_digest and digest(live_bytes) == row_digest
        results.append(check("87 current sources match Packet310, Packet308 and the worktree", sources_ok,
                             "byte length, SHA-256 and CRC32 checked on each path"))

        # Exact Return218 history and all 14 preserved case files.
        old_return = A / "rank9_defenseform8_return218_received/DD_Rank9_DefenseForm5_Director_Return218.zip"
        old_delivery = read(A / "rank9_defenseform8_return218_received/DD_Rank9_DefenseForm5_Director_Return218_DELIVERY.json")
        excerpt_bindings = json.loads(z.read("history/Return218_EXCERPT_BINDINGS_310.json"))
        excerpt_rows = {r["originalPath"]: r for r in excerpt_bindings["excerpts"]}
        history_ok = set(SPHERE_CASES).issubset(requirements["preserve"]["return218CaseIds"])
        with zipfile.ZipFile(old_return) as hist:
            index218 = json.loads(hist.read("CASE_INDEX.json"))
            case_rows218 = [r for r in index218["cases"] if r.get("spellId") == "invulnerable-sphere"]
            case_names218 = {r["id"]: r["path"] for r in case_rows218}
            for case_id in SPHERE_CASES:
                original_path = case_names218[case_id]
                output_path = "history/Return218/" + original_path
                history_ok &= output_path in name_set and z.read(output_path) == hist.read(original_path)
                ext = next(r for r in old_delivery["members"] if r["path"] == original_path)
                actual = digest(hist.read(original_path))
                history_ok &= actual == {k: ext[k] for k in actual}
                history_ok &= excerpt_rows[original_path]["sha256"] == actual["sha256"]
            procedure_raw = hist.read("procedures/invulnerable-sphere.json")
            history_ok &= z.read("history/Return218/procedures/invulnerable-sphere.json") == procedure_raw
            for filename in ["QUESTION_DISPOSITIONS.json", "FUTURE_OBLIGATION_DISPOSITIONS.json"]:
                history_ok &= z.read("history/Return218/" + filename) == hist.read(filename)
            blocker218 = json.loads(hist.read("BLOCKER_REASSESSMENT.json"))
            b04_218 = next(r for r in blocker218["records"] if r.get("currentId") == "DF218-B04")
        results.append(check("Return218 Sphere procedure, all 14 case IDs and selected dispositions are byte-preserved",
                             history_ok and len(case_rows218) == 14
                             and requirements["preserve"]["selectedDispositions"] == ["DF9-Q01", "DF9-Q23", "DF9-Q24", "DF9-Q25", "DF9-Q26", "DEF129-ADD02"],
                             "Crown-command case included; exact Return218 internal/external bindings checked"))

        # Return280 B04 context is bound to its archive; Return308 stays a held prior.
        return280_path = A / "rank9_defenseform8_return280_received/DD_Rank9_DefenseForm8_Director_Return280_HELD.zip"
        return280_delivery_path = A / "rank9_defenseform8_return280_received/DD_Rank9_DefenseForm8_Director_Return280_HELD_DELIVERY.json"
        return280_context = json.loads(z.read("current/PRIOR_RETURN280_B04_CONTEXT_310.json"))
        return280_raw = return280_path.read_bytes()
        results.append(check("Return280 B04 blocker context is exact",
                             return280_context["blocker"]["id"] == "DF218-B04"
                             and return280_context["blocker"]["spellId"] == "invulnerable-sphere"
                             and return280_context["archive"]["sha256"] == hashlib.sha256(return280_raw).hexdigest()
                             and return280_context["delivery"]["sha256"] == hashlib.sha256(return280_delivery_path.read_bytes()).hexdigest()
                             and return280_context["blocker"]["minimumMissingWitness"].startswith("A legal acquired planar crossing"),
                             "historical B04 evidence is context, not a new ruling"))
        return308_path = A / "rank9_defenseform8_return308_received/DD_Rank9_DefenseForm8_Director_Return308_HELD.zip"
        return308_audit = read(A / "TIMELESS_FORM_RETURN308_INDEPENDENT_AUDIT.json")
        return308_decision = read(A / "TIMELESS_FORM_DIRECTOR_DECISION_308.json")
        results.append(check("Return308 held context is bound and audit passed",
                             z.read("history/Return308_DIRECTOR_RETURN.zip") == return308_path.read_bytes()
                             and return308_audit["status"] == "PASS" and return308_audit["failedChecks"] == 0
                             and return308_decision["heldIds"] == ["timeless-form"]
                             and return308_decision["acceptedIds"] == return308_decision["appliedIds"] == []
                             and return308_decision["blockerIds"] == ["DF218-B03"],
                             "prior Timeless Form hold preserved without widening scope"))

        # Compare the committed index blob with the current working-tree bytes.
        overlay = candidate["workingTreeOverlay"]
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        base_raw = subprocess.check_output(["git", "show", f"{commit}:DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"], cwd=ROOT)
        current_index_raw = INDEX.read_bytes()
        results.append(check("base commit and working-tree overlay are explicitly separated",
                             overlay["baseCommit"] == commit
                             and overlay["baseAuthoredIndex"]["sha256"] == hashlib.sha256(base_raw).hexdigest()
                             and overlay["workingTreeAuthoredIndex"]["sha256"] == hashlib.sha256(current_index_raw).hexdigest()
                             and z.read("current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json") == current_index_raw,
                             f"base {commit}; current index SHA-256 {hashlib.sha256(current_index_raw).hexdigest()}"))

    failures = [r for r in results if not r["passed"]]
    report = {
        "id": "INVULNERABLE-SPHERE-PACKET310-INDEPENDENT-AUDIT",
        "recordedAtUtc": now,
        "status": "PASS" if not failures else "FAIL",
        "checkCount": len(results), "passedChecks": len(results) - len(failures), "failedChecks": len(failures),
        "checks": results, "packet": {"path": PACKET.relative_to(ROOT).as_posix(), **archive},
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), **digest(DELIVERY.read_bytes())},
        "scopeIds": ["invulnerable-sphere"], "blockerIds": ["DF218-B04"],
        "authority": AUTH, "acceptedIds": [], "appliedIds": [], "canonicalChanges": False,
        "note": "Preparation packet only. No acceptance, application, new crossing route, or positive encounter is claimed.",
    }
    out = A / "INVULNERABLE_SPHERE_PACKET_310_INDEPENDENT_AUDIT.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit(json.dumps(failures, indent=2))
    print(json.dumps({"status": report["status"], "checkCount": report["checkCount"],
                      "failedChecks": report["failedChecks"], "packet": report["packet"]}, indent=2))


if __name__ == "__main__":
    main()
