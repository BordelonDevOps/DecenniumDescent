from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import pathlib
import zlib

ROOT = pathlib.Path.cwd()
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE = A / "CURRENT_SPELL_QUEUE_304.json"
HANDOFF = A / "CURRENT_HANDOFF_304.json"
PENDING = A / "CURRENT26_PENDING_IDENTITY_AUDIT_304.json"
AUTHORITY = {"reviewedApplied": 822, "pending": 26, "acceptedUnapplied": 0,
             "completeStandaloneProcedures": 546, "scopedInterfaces": 173}
NEXT = {"group": "rank9-defense-form8", "pendingIds": ["elemental-shell", "timeless-form", "invulnerable-sphere"],
        "pendingCount": 3, "status": "DIRECTOR_NEXT_ACTIONABLE_GROUP_AFTER_FINAL_WORD_HOLD_303",
        "freshPacketRequiredForCurrentAuthority": True,
        "blockerByIdentity": {"elemental-shell": ["DF218-B01", "DF218-B02"],
                              "timeless-form": ["DF218-B03"], "invulnerable-sphere": ["DF218-B04"]},
        "directorRequirement": "Prepare a fresh current-source packet for Elemental Shell alone, covering DF218-B01 and DF218-B02. Preserve Druid/Mage/Wizard Transmutation, rank 9, class level 17, base 26 RP routes, native card and selected rules; refresh 87-source inventory, current authority and relevant accepted-interface bindings; preserve 21 prior cases including both completed CH07 Null traces."}
DIRECTOR = {
    "scope": "Elemental Shell alone; blockers DF218-B01 and DF218-B02 only",
    "preserve": ["Druid/Mage/Wizard Transmutation", "rank 9", "class level 17", "base 26 RP routes", "native card", "existing selected rules", "prior 87-source inventory refreshed", "current authority records and relevant accepted-interface bindings", "21 prior cases, including both completed CH07 Null traces"],
    "DF218-B01": ["Source-established noncreature elemental damage source", "exact geometry, selected damage type, amount or roll, and timing", "Shell bearer occupancy, defenses, paid application, and deadline", "demonstrate selected component mitigation and Shell immunity", "where no responsible creature dealer exists, show no reflected recipient and no emitted reflection packet; do not invent an environmental owner"],
    "DF218-B02": ["Legally acquired and actually instantiated companion/proxy", "complete body/profile, HP/defenses, equipment or explicit absence", "native damaging attack with type/reach/range", "controller acquisition, command cost, attached-phase schedule", "trace attack into Shell and reflection back to actual creature dealer, never automatically to controller", "preserve damage/lifecycle, resources, custody, phase history"],
    "integratedTraceInvariants": ["reflection basis after other applicable defenses but before Shell immunity; reflected amount floor(basis/2)", "actual dealer within 120 feet and unobstructed line of effect; otherwise no reflection or deferred payment", "separate original/reflected roots, reflector-derived Null provenance, once-only causal keys, no reflection recursion", "actual cast/interruption accounting, regular clocks, command opportunities, suppression, original deadlines, complete reversible states"],
    "retainedQuestionsAndQualifications": ["DF9-Q01", "DF9-Q12", "DF9-Q13", "DF9-Q14", "DF9-Q15", "DF9-Q26", "DEF129-ADD01", "relevant future requirements", "all qualifications"],
    "selectedDuration": "60-second nonconcentration duration remains spell-local authorship, not recovered native text",
    "sourceLeads": ["accepted/index-bound envelope alone is not a demonstrated environmental packet", "Dominate Beast alone is not an instantiated companion", "Spectral Steed without a damaging Action cannot supply B02", "synthetic replacement needs an explicit scoped ruling before replacing these obligations"],
    "remainingOrder": ["elemental-shell", "timeless-form", "invulnerable-sphere", "nullification-wave", "reality-anchor", "time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy", "faction-omniscience-supreme", "banishment-gate", "conjure-demiplane-fortress", "summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay", "reverse-gravity-field", "alignment-ascension", "alignment-perfection", "faction-incarnate", "faction-perfection", "corruption-purification", "astral-projection", "imprisonment", "divine-intervention-greater", "wish"],
    "finalWord": "Remains separately held under DR217-B01. Total 26 pending closure identities; zero first-review tasks.",
    "decisionEffect": "No acceptance, application, or canonical change occurs in this scope clarification.",
}

def raw(path: pathlib.Path) -> bytes:
    return path.read_bytes()

def read(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def ref(path: pathlib.Path, data: bytes | None = None) -> dict:
    b = raw(path) if data is None else data
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(b),
            "sha256": hashlib.sha256(b).hexdigest(), "crc32": f"{zlib.crc32(b) & 0xffffffff:08x}"}

def write(path: pathlib.Path, value) -> bytes:
    b = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    path.write_bytes(b)
    return b

def main() -> None:
    q, h, p = read(QUEUE), read(HANDOFF), read(PENDING)
    old_next = copy.deepcopy(h["nextPendingGroup"])
    assert old_next["group"] == "rank9-memory-denial6" and old_next["directorReturn"] == 289
    assert h["currentPreparation"]["group"] == "rank9-defense-form8"
    assert q["currentAuthority"] == p["authority"] == h["currentAuthority"] == AUTHORITY
    assert q["next"]["group"] == p["nextPendingGroup"]["group"] == "rank9-defense-form8"
    index_raw, catalog_raw = raw(INDEX), raw(CATALOG)
    stamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")

    requirements = {"id": "ELEMENTAL-SHELL-DIRECTOR-SCOPE-305", "recordedAtUtc": stamp,
                    "source": {"service": "ChatGPT", "conversationTitle": "Calibration review part 6",
                               "url": "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"},
                    "currentAuthority": AUTHORITY, "acceptedIds": [], "appliedIds": [],
                    "directorRequirements": DIRECTOR}
    req_path = A / "ELEMENTAL_SHELL_DIRECTOR_REQUIREMENTS_305.json"
    req_ref = ref(req_path, write(req_path, requirements))

    fixed = copy.deepcopy(h)
    fixed.update({"id": "CURRENT-HANDOFF-305", "recordedAtUtc": stamp,
                  "supersedes": "CURRENT-HANDOFF-304", "status": "HANDOFF_CORRECTED_ELEMENTAL_SHELL_NEXT_822_26",
                  "nextPendingGroup": copy.deepcopy(NEXT),
                  "historicalNextPendingGroupPointer304": old_next,
                  "currentQueueBinding": copy.deepcopy(fixed["queueBinding"]),
                  "historicalCurrentQueueBinding304": copy.deepcopy(h.get("currentQueueBinding")),
                  "nextStep": copy.deepcopy(NEXT), "currentPreparation": copy.deepcopy(NEXT),
                  "nextGroup": "rank9-defense-form8", "nextPendingIds": NEXT["pendingIds"],
                  "nextPendingCount": 3, "nextStepText": NEXT["directorRequirement"],
                  "directorConnectionStatus": "Director reconfirmed Elemental Shell / DF218-B01/B02 as next actionable; Final Word stays held under DR217-B01. Handoff 304 stale Return289 pointer is preserved in historicalNextPendingGroupPointer304 and corrected here.",
                  "directorRequirements": req_ref, "canonicalFilesChangedByThisRuling": False})
    hand_path = A / "CURRENT_HANDOFF_305.json"
    hand_ref = ref(hand_path, write(hand_path, fixed))

    checks = [
        ("Director-confirmed queue and pending audit agree at 822/26/0", q["currentAuthority"] == p["authority"] == AUTHORITY),
        ("304 stale nextPendingGroup pointer is preserved as historical evidence", fixed["historicalNextPendingGroupPointer304"] == old_next),
        ("corrected nextPendingGroup matches current preparation", fixed["nextPendingGroup"] == fixed["currentPreparation"] and fixed["nextPendingGroup"]["group"] == "rank9-defense-form8"),
        ("current queue binding is corrected and original pointer is preserved", fixed["currentQueueBinding"] == fixed["queueBinding"] and fixed["historicalCurrentQueueBinding304"] == h["currentQueueBinding"]),
        ("Elemental Shell alone is submitted for DF218-B01/B02 with no acceptance", DIRECTOR["scope"] == "Elemental Shell alone; blockers DF218-B01 and DF218-B02 only" and requirements["acceptedIds"] == requirements["appliedIds"] == []),
        ("21 existing defense/form cases and integrated trace requirements are explicitly preserved", "21 prior cases, including both completed CH07 Null traces" in DIRECTOR["preserve"] and len(DIRECTOR["integratedTraceInvariants"]) == 4),
        ("canonical index and native catalog remain byte-exact", raw(INDEX) == index_raw and raw(CATALOG) == catalog_raw),
    ]
    assert all(ok for _, ok in checks), [name for name, ok in checks if not ok]
    validation = {"id": "ELEMENTAL-SHELL-HANDOFF-CORRECTION-VALIDATION-305", "recordedAtUtc": stamp,
                  "status": "PASS", "checkCount": len(checks), "passedChecks": len(checks), "failedChecks": 0,
                  "checks": [{"check": n, "passed": bool(ok)} for n, ok in checks],
                  "correctedHandoff": hand_ref, "directorRequirements": req_ref,
                  "currentAuthority": AUTHORITY, "acceptedIds": [], "appliedIds": [],
                  "indexAndCatalogByteExact": True}
    val_path = A / "ELEMENTAL_SHELL_HANDOFF_CORRECTION_VALIDATION_305.json"
    val_ref = ref(val_path, write(val_path, validation))
    snap = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_305.md"
    snap.write_text("# Spell Review Snapshot — Elemental Shell Scope (305)\n\n"
                    "Authority remains **822 applied / 26 pending / 0 accepted-unapplied; 546 procedures / 173 interfaces**. Final Word stays held under DR217-B01.\n\n"
                    "Director confirmed Elemental Shell alone is next, with DF218-B01/B02. The packet must refresh the prior 87-source inventory and relevant accepted-interface bindings, preserve all 21 prior cases, and provide source-established environmental damage and an acquired/instantiated companion or proxy. No synthetic substitute is authorized without a separate scoped ruling.\n\n"
                    "Handoff 304's stale Return289 pointer is retained as history and corrected in CURRENT_HANDOFF_305.json. Validation: " + val_ref["path"] + " (" + val_ref["sha256"] + ").\n",
                    encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "handoff": hand_ref, "requirements": req_ref,
                      "validation": val_ref, "snapshot": snap.relative_to(ROOT).as_posix(),
                      "authority": AUTHORITY, "next": NEXT["pendingIds"]}, indent=2))

if __name__ == "__main__":
    main()
