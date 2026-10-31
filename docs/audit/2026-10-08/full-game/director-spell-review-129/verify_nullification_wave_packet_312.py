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
OUT = A / "rank9_wardcontrol6_source_packet_312_prepared"
PACKET = OUT / "DD_Rank9_WardControl6_CurrentSource_312.zip"
DELIVERY = OUT / "DD_Rank9_WardControl6_CurrentSource_312_DELIVERY.json"
OLD_PACKET = A / "rank9_wardcontrol6_source_packet_281_refreshed/DD_Rank9_WardControl6_CurrentSource_281.zip"
OLD_RETURN = A / "rank9_wardcontrol6_return281_received/DD_Rank9_WardControl6_Director_Return281_HELD.zip"
RETURN310 = A / "rank9_defenseform8_return310_received/DD_Rank9_DefenseForm8_Director_Return310_HELD.zip"
AUTH = {"reviewedApplied": 822, "pending": 26, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 546, "scopedInterfaces": 173}
TARGET = "nullification-wave"
BLOCKER = "WC188-B01"


def read(raw: bytes):
    return json.loads(raw.decode("utf-8-sig"))


def digest(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
            "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def main() -> None:
    delivery = json.loads(DELIVERY.read_text(encoding="utf-8-sig"))
    packet_raw = PACKET.read_bytes()
    results: list[dict] = []

    def check(name: str, passed: bool, detail: str = "") -> None:
        results.append({"check": name, "passed": bool(passed), "detail": detail})

    check("outer Packet312 hash matches delivery", digest(packet_raw) == {k: delivery["archive"][k] for k in digest(packet_raw)},
          f"{len(packet_raw)} bytes; SHA-256 {hashlib.sha256(packet_raw).hexdigest()}")
    check("target scope, authority and queue are precise", delivery["targetIds"] == [TARGET]
          and delivery["blockerIds"] == [BLOCKER] and delivery["authority"] == AUTH
          and delivery["acceptedIds"] == delivery["appliedIds"] == []
          and delivery["nextPendingGroup"]["nextIdentity"] == TARGET
          and delivery["nextPendingGroup"]["thenIdentity"] == "reality-anchor"
          and delivery["closureTasksRemaining"] == 26 and delivery["firstReviewTasksRemaining"] == 0,
          "Wave only; Reality Anchor is next but not jointly adjudicated")

    with zipfile.ZipFile(PACKET) as z, zipfile.ZipFile(OLD_PACKET) as old_source, zipfile.ZipFile(OLD_RETURN) as old_return:
        names = z.namelist()
        name_set = set(names)
        check("archive integrity, safe names and exact member count",
              z.testzip() is None and len(names) == len(name_set) == delivery["memberCount"] == 240
              and all(not pathlib.PurePosixPath(n).is_absolute()
                      and ".." not in pathlib.PurePosixPath(n).parts for n in names),
              f"{len(names)} unique safe members")
        manifest_raw = z.read("MEMBER_MANIFEST.json")
        manifest = read(manifest_raw)
        internal = {r["path"]: r for r in manifest["members"]}
        external = {r["path"]: r for r in delivery["members"]}
        payload_names = name_set - {"MEMBER_MANIFEST.json"}
        check("self-excluding internal manifest and external allowlist agree",
              manifest["selfExcluded"] is True and manifest["memberCountExcludingSelf"] == len(payload_names)
              and set(internal) == payload_names and set(external) == name_set
              and set(delivery["exactAllowlist"]) == name_set
              and digest(manifest_raw) == {k: delivery["memberManifest"][k] for k in digest(manifest_raw)},
              f"{len(payload_names)} payload members plus manifest")
        member_hashes_ok = True
        for name in names:
            actual = digest(z.read(name))
            member_hashes_ok &= actual == {k: external[name][k] for k in actual}
            if name != "MEMBER_MANIFEST.json":
                member_hashes_ok &= actual == {k: internal[name][k] for k in actual}
        check("all internal and external member hashes/CRCs", member_hashes_ok,
              f"{len(names)} archive members independently hashed")

        refresh = read(z.read("SOURCE_REFRESH_312.json"))
        previous = {r["path"]: r for r in refresh["previousBindings"]}
        current = {r["path"]: r for r in refresh["currentBindings"]}
        source_ok = len(previous) == len(current) == 91 == refresh["sourceCount"]
        changed = []
        for path, row in current.items():
            member = "sources_current/" + path
            live_path = ROOT / pathlib.Path(path)
            live = live_path.read_bytes() if live_path.is_file() else b""
            now = digest(live)
            source_ok &= member in name_set and now == {k: row[k] for k in now}
            old_raw = old_source.read("sources_current/" + path)
            old_d = digest(old_raw)
            source_ok &= old_d == {k: previous[path][k] for k in old_d}
            saved_old = read(z.read("old_source_bindings/" + path + ".json"))
            source_ok &= saved_old == old_d
            if old_raw != live:
                changed.append(path)
        check("all 91 Ward/Control source files refreshed and prior hashes retained",
              source_ok and sorted(changed) == sorted(r["path"] for r in refresh["changedSincePacket281"])
              and len(changed) == delivery["sourceBindingRefresh"]["changedCount"],
              f"91 current files match worktree; {len(changed)} changed from Packet281")

        requirements = read(z.read("NULLIFICATION_WAVE_DIRECTOR_REQUIREMENTS_312.json"))
        queue = read(z.read("CURRENT_SPELL_QUEUE_312.json"))
        handoff = read(z.read("CURRENT_HANDOFF_312.json"))
        pending = read(z.read("CURRENT26_PENDING_IDENTITY_AUDIT_311.json"))
        check("queue and handoff contain fresh current authority without stale Sphere/Timeless next pointers",
              queue["currentAuthority"] == handoff["authority"] == pending["authority"] == AUTH
              and queue["activeReview"]["scopeIds"] == [TARGET]
              and handoff["currentBlocker"] == {"identity": TARGET, "group": "rank9-ward-control6", "blockerIds": [BLOCKER]}
              and handoff["currentPreparation"]["scopeIds"] == [TARGET]
              and pending["pendingCount"] == 26 and len(pending["pendingIds"]) == 26
              and pending["nextGroup"] == "rank9-ward-control6"
              and queue["next"]["then"]["identity"] == "reality-anchor",
              "The four previous holds remain separate; current preparation is Wave only")
        check("Director scope guidance is preparation-only and Wave-only",
              requirements["status"] == "DIRECTOR_PREPARATION_GUIDANCE_ONLY_NOT_ADJUDICATION"
              and requirements["scopeIds"] == [TARGET] and requirements["blockerIds"] == [BLOCKER]
              and requirements["separateNextIdentity"]["jointPacketRequired"] is False
              and requirements["closureTasksRemaining"] == 26
              and requirements["firstReviewTasksRemaining"] == 0,
              "No blocker revision or acceptance requested in the scope ping")

        with zipfile.ZipFile(OLD_RETURN) as old:
            exact_files = [
                "ACTOR_PROFILES.json", "BLOCKERS.json", "QUALIFICATIONS.json", "SOURCE_PAIR_TABLE.json",
                "ORIGINAL_OBLIGATIONS.json", "QUESTION_DISPOSITIONS.json", "HOLD_REGISTER.json",
                "REMAINING_QUEUE.json", "procedures/nullification-wave.json",
            ]
            preserve_ok = all(z.read("history/Return281/" + name) == old.read(name) for name in exact_files)
            idx = read(z.read("history/Return281/WAVE_CASE_INDEX_312.json"))
            rows = idx["cases"]
            preserve_ok &= idx["scopeIds"] == [TARGET] and idx["caseCount"] == len(rows) == 18
            for row in rows:
                path = row["path"]
                out_name = "history/Return281/" + path
                preserve_ok &= z.read(out_name) == old.read(path)
                preserve_ok &= digest(z.read(out_name))["sha256"] == row["sha256"]
            ids = {r["id"] for r in rows}
            preserve_ok &= {"WC237-NW-HELPER", "WC237-NW-COUNTER", "WC219-NW-HELPER", "WC219-NW-COUNTER"}.issubset(ids)
            check("exact Return281 Wave procedure, blocker, qualifications, pair table, actors, obligations and 18 cases preserved",
                  preserve_ok, "Corrected Return237 helper/counter and superseded Return219 predecessors retained")

        et_data = read(z.read("ETERNAL_FORGE_ACCEPTED_ENVELOPE_AND_W2_CONTEXT_312.json"))
        lead_bindings = read(z.read("WAVE_SOURCE_EXTRA_BINDINGS_312.json"))["records"]
        lead_ok = len(lead_bindings) == 11 and "does not prove WC188-B01" in et_data["limitations"]
        for row in lead_bindings:
            raw = (ROOT / pathlib.Path(row["path"])).read_bytes()
            member = row["member"]
            lead_ok &= digest(raw) == {k: row[k] for k in digest(raw)} and z.read(member) == raw
        lead_ok &= et_data["w2CurrentStatus"].startswith("DRAFT_WITH_FORWARD_INVERSE_REPLAY")
        check("Glove and Eternal Forge evidence bindings are exact, leads remain non-findings", lead_ok,
              "Forge W2 remains a draft pending Director review")

        return310_matches = z.read("RETURN310_DIRECTOR_RETURN.zip") == RETURN310.read_bytes()
        check("prior Return310 Sphere HOLD is carried as separate exact context", return310_matches
              and read(z.read("RETURN310_HOLD_RECEIPT.json"))["heldIds"] == ["invulnerable-sphere"]
              and read(z.read("RETURN310_INDEPENDENT_AUDIT.json"))["status"] == "PASS",
              "Sphere remains held under DF218-B04; it is not the active Wave target")

    failures = [r for r in results if not r["passed"]]
    report = {
        "id": "NULLIFICATION-WAVE-PACKET312-INDEPENDENT-AUDIT",
        "recordedAtUtc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "status": "PASS" if not failures else "FAIL",
        "checkCount": len(results), "passedChecks": len(results) - len(failures), "failedChecks": len(failures),
        "checks": results,
        "packet": {"path": PACKET.relative_to(ROOT).as_posix(), **digest(packet_raw)},
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), **digest(DELIVERY.read_bytes())},
        "scopeIds": [TARGET], "blockerIds": [BLOCKER], "authority": AUTH,
        "interpretiveLimit": "This audit checks source/package bindings, historical preservation, and the Director-provided scope metadata. It does not establish a qualifying item enhancement or supply a new paid Nullification Wave encounter.",
    }
    out = A / "NULLIFICATION_WAVE_PACKET_312_INDEPENDENT_AUDIT.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "checkCount": report["checkCount"],
                      "failedChecks": report["failedChecks"], "failures": failures}, indent=2))
    if failures:
        raise SystemExit("Packet312 independent audit failed")


if __name__ == "__main__":
    main()
