from __future__ import annotations

import datetime as dt
import hashlib
import json
import pathlib
import subprocess
import zipfile
import zlib

ROOT = pathlib.Path(__file__).resolve().parents[5]
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = A / "rank9_summon_herald_w01_content_reconciliation_358"
COMMIT = "33c12135dcdf21a089a4ec962ca7d8935db3f9eb"
ARCHIVE = OUT / "DD_Rank9_SummonHerald_SH202B02_W01_Content_Reconciliation_358.zip"

SOURCES = {
    "structuredRoot": "src/bestiary_data_full.json",
    "structuredReviewBibleMirror": "DescentReviewChanges/ReviewBible/src/bestiary_data_full.json",
    "directorSealedSource": "docs/bestiary/Decennium_Descent_Monster_Manual_Canon_Rewrite_Source_Pack/Directors_Sealed_Bestiary_Source/entries/lumen-of-the-shattered-thread.md",
    "publicHistoricalRecord": "docs/bestiary/Decennium_Descent_Monster_Manual_Canon_Rewrite_Source_Pack/Monster_Manual_of_the_Known_Descent_Source/entries/lumen-sixth-gate-disaster-record.md",
    "canonManifest": "docs/canon/CANON_MANIFEST.json",
}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def crc(b: bytes) -> str:
    return f"{zlib.crc32(b) & 0xffffffff:08x}"


def git_bytes(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{COMMIT}:{path}"], cwd=ROOT)


def write_json(path: pathlib.Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    if OUT.exists() or ARCHIVE.exists():
        raise SystemExit(f"Refusing to overwrite prior W01 packet: {OUT}")
    OUT.mkdir(parents=True)
    stamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    blobs = {key: git_bytes(path) for key, path in SOURCES.items()}
    structured = json.loads(blobs["structuredRoot"])
    lumen_index = next(i for i, row in enumerate(structured) if row.get("name") == "Lumen of the Shattered Thread")
    structured_entry = structured[lumen_index]
    mirror_bytes = blobs["structuredReviewBibleMirror"]
    assert sha(blobs["structuredRoot"]) == sha(mirror_bytes)
    assert sha(blobs["directorSealedSource"]) == "7c48f180f467638943fd138a837f61caebef300b8ee055d67e7935a5771dee66"
    assert sha(blobs["publicHistoricalRecord"]) == "7881166850db75979572e1c6532449d05e942ee4aac404e9f617de63478bc47e"
    canon = json.loads(blobs["canonManifest"])
    authority_rows = [row for row in canon["domains"] if row["domain"] in ("monster-manual-director", "monster-manual-public")]
    assert {row["domain"] for row in authority_rows} == {"monster-manual-director", "monster-manual-public"}

    source_bindings = {
        key: {"path": path, "sourceCommit": COMMIT, "bytes": len(blobs[key]), "sha256": sha(blobs[key]),
              "gitBlobSHA1": subprocess.check_output(["git", "rev-parse", f"{COMMIT}:{path}"], cwd=ROOT, text=True).strip()}
        for key, path in SOURCES.items()
    }
    write_json(OUT / "02_SOURCE_BINDINGS.json", {"id": "SH202-W01-SOURCE-BINDINGS-358", "sourceBindings": source_bindings})
    write_json(OUT / "03_CANON_AUTHORITY_ENTRIES.json", {"id": "SH202-W01-CANON-AUTHORITY-358", "sourceCommit": COMMIT, "domains": authority_rows})
    write_json(OUT / "04_STRUCTURED_LUMEN_ENTRY.json", {
        "id": "SH202-W01-STRUCTURED-LUMEN-ENTRY-358", "sourcePath": SOURCES["structuredRoot"],
        "sourceCommit": COMMIT, "sourceBinding": source_bindings["structuredRoot"],
        "entryIndex": lumen_index, "record": structured_entry,
    })
    (OUT / "05_DIRECTOR_SEALED_LUMEN_SOURCE.md").write_bytes(blobs["directorSealedSource"])
    (OUT / "06_PUBLIC_HISTORICAL_LUMEN_RECORD.md").write_bytes(blobs["publicHistoricalRecord"])
    write_json(OUT / "07_W01_TEMPLATE_354.json", json.loads((A / "LUMEN_W01_CONTENT_AUTHORITY_RECONCILIATION_TEMPLATE_354.json").read_text(encoding="utf-8-sig")))
    hold = {
        "id": "SH202-B02-RETURN332-HOLD-EXCERPT-358",
        "return": json.loads((A / "rank9_summon_herald_of_the_planes_return332_received/payload/DIRECTOR_DECISION.json").read_text(encoding="utf-8-sig")),
        "conditionalEvidence": json.loads((A / "rank9_summon_herald_of_the_planes_return332_received/payload/CONDITIONAL_EVIDENCE_RULING.json").read_text(encoding="utf-8-sig")),
        "semanticAudit": json.loads((A / "rank9_summon_herald_of_the_planes_return332_received/payload/INDEPENDENT_SEMANTIC_FAILURE_CHECK.json").read_text(encoding="utf-8-sig")),
    }
    write_json(OUT / "08_PRIOR_HOLD_AND_OPEN_FINDINGS.json", hold)
    write_json(OUT / "09_OWNER_W02_TEST_AUTHORIZATION.json", json.loads((A / "OWNER_LUMEN_W02_TEST_AUTHORIZATION_358.json").read_text(encoding="utf-8-sig")))

    source_proposal = {
        "id": "SH202-W01-CONTENT-RECONCILIATION-SUBMISSION-358",
        "recordedAtUtc": stamp,
        "status": "SOURCE_BOUND_PROPOSAL_SUBMITTED_FOR_DIRECTOR_RULING_NOT_APPROVED",
        "spellId": "summon-herald-of-the-planes", "blockerId": "SH202-B02",
        "minimumWitnessId": "SH332-W01", "targetIdentity": "Lumen of the Shattered Thread",
        "authorityRequested": "GPT serving as Director-integration authority; GPT confirmed in the live conversation that it can serve in this role, and this submission requests its explicit W01 ruling.",
        "sourceBindingRefs": source_bindings,
        "conflictResolutionProposal": {
            "governingAbilities": {"STR": 19, "DEX": 16, "CON": 22, "INT": 9, "WIS": 12, "CHA": 11},
            "governingResistances": ["poison"],
            "governingConditionImmunities": ["poisoned"],
            "reason": "The canon manifest names Directors_Sealed_Bestiary_Source as the canonical Director-domain authority. Preserve the structured entry unchanged as a non-authoritative conflicting ingest record; its gate-guardian-trusted/non-draft metadata is provenance, not a supersession decision.",
            "structuredConflictsPreserved": {"abilities": structured_entry["abilities"], "resistances": structured_entry["combat"]["defenses"]["resistances"], "conditionImmunities": structured_entry["combat"]["defenses"]["conditionImmunities"]},
        },
        "sourceFactsAndUnresolvedFields": {
            "threadLance": {"sourceAttack": structured_entry["combat"]["attacks"][0], "sealedDescription": "One target; +11 to hit; 4d10+10 radiant; reach/range absent."},
            "threadBind": {"sourceAttack": structured_entry["combat"]["attacks"][1], "sealedDescription": "One target; +11 to hit; 3d10+8 force; reach/range absent."},
            "threadShatter": {"sourceAttack": structured_entry["combat"]["attacks"][2], "sourcedRadiusFt": 20, "authorityQuestion": "Adopt the source-bound 20-foot radius? The exact origin/placement is not specified by either record."},
            "body": {"sourceSize": "Large", "preciseOccupiedDimensions": None, "authorityQuestion": "Specify the occupied spatial envelope/fit rule without silently treating the size label as exact dimensions."},
            "seal": {"sourceRule": "Gate-Bound: cannot be permanently displaced from its arena while the Seal remains active.", "authorityQuestion": "Define whether and under what bounded call/return rule a temporary call can coexist with this constraint; no second Lumen/body/projection may be created."},
            "arena": {"sourceRule": "The Guardian's body, Seal, and terrain operate as one examination.", "authorityQuestion": "Bound the test call so it cannot transport/move the Seal or arena, open the Gate, or assert a campaign event."},
            "phase": {"sourceRules": ["Escalation Pulse; Thread Shatter recharges on 5–6; visible signs precede its first use.", "The entry says the Guardian escalates by phase and uses a Seal Pulse."], "authorityQuestion": "Specify state/phase/uses preservation and any phase boundary while called; do not invent an unrecorded phase schedule."},
        },
        "proposedNewRulesRequiringExplicitDirectorAuthorship": [
            "Exact Thread Lance and Thread Bind reach/range values, since neither bound profile supplies them.",
            "Thread Shatter origin and placement, if the 20-foot radius is adopted.",
            "Lumen occupied geometry/body-fit semantics required for arrival and return.",
            "The temporary call's interaction with Gate-Bound, unique-body custody, and blocked return.",
            "Phase, use/recharge, Seal, arena, and return-state preservation needed for W03/W04.",
        ],
        "w02Boundary": "Owner has authorized a hypothetical TEST_ONLY W02 state only after W01 approval. No W02 state has been created in this packet; no campaign consent, availability, resources, or permissions are asserted.",
        "requestedDirectorDisposition": "Please complete the exact SH332-W01 source reconciliation with explicit choices for every requiredRulings field, identify which values are source facts versus new Director-authored spell-local rules, and issue W01 APPROVED or list the remaining exact null paths. W01 approval is a separate decision from W02, W03, W04, and whole-identity acceptance.",
    }
    write_json(OUT / "10_CONTENT_RECONCILIATION_SUBMISSION.json", source_proposal)
    (OUT / "01_DIRECTOR_REQUEST.md").write_text(
        "# Director request — Summon Herald W01 source/content reconciliation\n\n"
        "This packet is a source-bound W01 submission for `summon-herald-of-the-planes` / `SH202-B02`; it is not approved evidence and does not request whole-identity acceptance. GPT confirmed it can serve as Director-integration authority and W01 can be ruled before W02 is built.\n\n"
        "Please issue an explicit W01 ruling after reviewing the binding set, resolving all known source conflicts, and filling every required reconciliation field. The structured record provides a source-bound 20-foot Thread Shatter radius but conflicts with the canonical Director profile on abilities and defenses; the two attack ranges and the Shatter origin are not stated. The packet identifies the remaining body-fit, Seal, arena, and phase rulings that a positive call/return witness must obey. Mark every new rule as Director-authored and spell-local.\n\n"
        "The owner has authorized a hypothetical TEST_ONLY Lumen call-state record scoped to SH332-W03/W04, with consent, resources, and permissions stated as test premises, only after W01 approval. The authorization is attached for context; this packet does not instantiate W02 or assert campaign facts.\n\n"
        "Requested response: completed W01 reconciliation, explicit source-versus-new-rule provenance, and `W01 APPROVED` or exact remaining defect paths. Preserve the prior HOLD and all unrelated identity dispositions until separate authorized application.\n",
        encoding="utf-8", newline="\n",
    )

    rows = []
    for path in sorted((p for p in OUT.iterdir() if p.is_file() and p.name != "MEMBER_MANIFEST.json"), key=lambda p: p.name):
        b = path.read_bytes()
        rows.append({"path": path.name, "bytes": len(b), "sha256": sha(b), "crc32": crc(b)})
    write_json(OUT / "MEMBER_MANIFEST.json", {"id": "SH202-W01-RECONCILIATION-358-MANIFEST", "selfExcluded": True, "memberCountExcludingSelf": len(rows), "members": rows})
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(OUT.iterdir(), key=lambda p: p.name):
            if path.is_file():
                zf.write(path, path.name)
    print(json.dumps({"status": "PREPARED_NOT_APPROVED", "archive": str(ARCHIVE), "sha256": sha(ARCHIVE.read_bytes()), "bytes": ARCHIVE.stat().st_size, "memberCount": len(rows)}, indent=2))


if __name__ == "__main__":
    main()
