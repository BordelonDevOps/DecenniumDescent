#!/usr/bin/env python3
"""Record GPT Director's final closure order and prerequisites from Return289."""
from __future__ import annotations

import json
import pathlib
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
ORDER_PATH = BASE / "CURRENT_CLOSURE_PRIORITIES_290.json"
HANDOFF_PATH = BASE / "CURRENT_HANDOFF_290.json"
QUEUE_PATH = BASE / "CURRENT_SPELL_QUEUE_290.json"
SNAPSHOT_PATH = BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_290.md"

order = [
    {"priority": 1, "identities": ["mind-collapse"], "blockers": ["MD196-B01"], "remaining": "Authorized genuine inserted-full-turn grant; its legal acquisition and complete actor/grantor history; integrated paid Mind Collapse witness preserving regular ENDs, admission, concentration/Ready, recharge/Reaction and resource history."},
    {"priority": 2, "identities": ["absolute-domination"], "blockers": ["AG190-B01"], "remaining": "Independently demonstrate the inserted-turn grant in the control/turn branch; Mind Collapse evidence alone does not close this interaction."},
    {"priority": 3, "identities": ["puppetmaster-s-realm"], "blockers": ["AG190-B02", "H150-ROSTER"], "remaining": "Authorized creature profile with native Multiattack and constituent attack reaches; lawful admission, control, command payment and execution history."},
    {"priority": 4, "identities": ["psychic-scream", "mass-phantom-killer", "weird"], "blockersByIdentity": {"psychic-scream": ["PF182-B01"], "mass-phantom-killer": ["PF182-B02"], "weird": ["PF182-B02"]}, "remaining": "Psychic Scream: explicit head anatomy, final-death/head consequence and changed-form/remains settlement. Mass Phantom Killer and Weird: genuine acquired inserted-turn witnesses preserving regular and attached-phase clocks."},
    {"priority": 5, "identities": ["final-word"], "blockers": ["DR217-B01"], "remaining": "Actual eligible victim's current body/HP, available soul, final-death and custody/capture/Hunt facts, followed by lawful reserve expenditure."},
    {"priority": 6, "identities": ["elemental-shell", "timeless-form", "invulnerable-sphere"], "blockersByIdentity": {"elemental-shell": ["DF218-B01", "DF218-B02"], "timeless-form": ["DF218-B03"], "invulnerable-sphere": ["DF218-B04"]}, "remaining": "Shell: quantified noncreature elemental packet and instantiated companion/proxy history. Timeless Form: operational acquired Time Stop interaction. Sphere: lawful acquired planar crossing to an authorized destination against the closed partition, with full custody."},
    {"priority": 7, "identities": ["nullification-wave", "reality-anchor"], "blockersByIdentity": {"nullification-wave": ["WC188-B01"], "reality-anchor": ["WC188-B02"]}, "remaining": "Actual continuing unique/item/innate magical component with classification, acquisition and lifecycle. Demonstrate Wave terminal removal and Anchor deny/allow, expiry and surviving-source resumption without refill."},
    {"priority": 8, "identities": ["time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy"], "blockersByIdentity": {"time-stop": ["TF192-B01"], "fate-rewrite": ["TF192-B04"], "collapse-timeline": ["TF192-B05"], "eternal-prophecy": ["TF192-B02"]}, "remaining": "Time Stop: source-complete immune actor and independent-phase interaction. Eternal Prophecy: authorized finite guarantee mechanism under prevented delivery and changed facts. Fate Rewrite/Collapse Timeline: actual committed guarantee and compatible/conflicting histories with complete settlement; avoid circular acceptance."},
    {"priority": 9, "identities": ["faction-omniscience-supreme"], "blockers": ["KR198-B01"], "remaining": "Canonical faction past/present/distant-branch ledger and concrete forecast premises, with private/protected information and missing-record boundaries."},
    {"priority": 10, "identities": ["banishment-gate", "conjure-demiplane-fortress"], "blockersByIdentity": {"banishment-gate": ["PG200-B03", "PG200-B04"], "conjure-demiplane-fortress": ["PG200-B06"]}, "remaining": "Gate: legal non-Elemental participant plus crossing/cell/body/cargo lifecycle branches. Fortress: support/damage/work/companion histories and occupied removal, suppression, nested-space and terminal settlements."},
    {"priority": 11, "identities": ["summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay"], "blockersByIdentity": {"summon-elemental-avatar": ["SH202-B01"], "summon-herald-of-the-planes": ["SH202-B02"], "summon-avatar-of-decay": ["SH202-B03"]}, "remaining": "Elemental Avatar: inserted turn, mixed damage and control/aura branches. Herald: complete eligible unique CR15+ profile, availability, consent, arrival and return. Avatar of Decay: competing control, type change, relay/aura suppression and outstanding physical/reach facts."},
    {"priority": 12, "identities": ["reverse-gravity-field"], "blockers": ["IE204-B02"], "remaining": "Actual 20-lb crate material/durability and 60/120-ft impact/breakage/custody contract; rated tether/anchor strength and upward-force/load rule."},
    {"priority": 13, "identities": ["alignment-ascension", "alignment-perfection", "faction-incarnate", "faction-perfection", "corruption-purification"], "blockersByIdentity": {"alignment-ascension": ["AFP211-B01"], "alignment-perfection": ["AFP211-B02"], "faction-incarnate": ["AFP211-B03"], "faction-perfection": ["AFP211-B04"], "corruption-purification": ["AFP211-B05"]}, "remaining": "Authorized form/insight lifecycle; purification and axis benefits; Incarnate profile/actions/invocation; concrete finite faction benefit and permissions; cure matrix/geometry/permanent-versus-dispellable settlement, followed by integrated encounters. AFP211-E01 remains closed."},
    {"priority": 14, "identities": ["astral-projection", "imprisonment"], "blockersByIdentity": {"astral-projection": ["PC232-B01"], "imprisonment": ["PC232-B02"]}, "remaining": "Authorized Astral site and body/resource/return contract; complete confinement methods and physical/magical profiles; demonstrate useful travel/return or confinement/rescue with lifecycle and custody."},
    {"priority": 15, "identities": ["divine-intervention-greater", "wish"], "blockersByIdentity": {"divine-intervention-greater": ["MR233-B01"], "wish": ["MR233-B02"]}, "remaining": "Concrete Director-authored question/task and substantial reality-change outcomes, including a composite Wish, followed by lawful paid positive/adverse encounters. MR233-E01 remains closed."},
]

all_ids = [spell for row in order for spell in row["identities"]]
pending_path = BASE / "CURRENT32_PENDING_IDENTITY_AUDIT_290.json"
pending = json.loads(pending_path.read_text(encoding="utf-8-sig"))
if len(all_ids) != 32 or set(all_ids) != set(pending.get("pendingIds", [])):
    raise SystemExit("Director closure order does not reconcile to the 32 pending identities")

record = {
    "id": "DIRECTOR-CLOSURE-PRIORITIES-290",
    "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
    "source": "GPT Director response in Calibration review part 6 after Return289",
    "authority": {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0, "completeStandaloneProcedures": 540, "scopedInterfaces": 173},
    "reviewSweep": {"firstReviewTasksRemaining": 0, "allPendingIdentitiesReviewedAndHeld": True, "unreviewedIds": [], "noAcceptedIds": True, "noAppliedIds": True},
    "evidenceDeltaGuidance": {
        "doNot": "Do not repeat acceptance review on unchanged evidence or resend a full-source refresh just to repeat an old hold.",
        "nextUsefulSubmission": "A focused closure delta showing what changed: an authorized contract or newly recovered source fact, legal acquisition/actor history where required, missing integrated traces, and independent semantic/replay checks.",
        "authoringScope": "Some blockers need new or newly recovered source facts; others need spell-local authored outcomes or complete witnesses using existing sources.",
    },
    "mindCollapseSourceCheck": {
        "finding": "No new qualifying full-turn grant or legally acquired grant-bearing actor is established by the bound evidence.",
        "comparison": "The 65 source files shared by Packet276 and Packet289 are byte-identical.",
        "insufficientLeads": [
            {"anchor": "class_playtests/dragoon.json#/cards/35/effect", "establishes": "An extra full Action next turn."},
            {"anchor": "class_playtests/oracle.json#/cards/32/effect, /cards/34/effect, /cards/77/effect", "establishes": "Additional Actions, including restricted Actions."},
            {"anchor": "class_playtests/oracle.json#/cards/26/effect, /cards/218/effect", "establishes": "Duration/cost changes or initiative movement."},
            {"anchor": "class_playtests/wizard.json#/cards/53/effect", "establishes": "Control of the next normal turn, explicitly no extra turn."},
            {"anchor": "Time Stop Core entry 921, source paragraph 10122", "establishes": "Historical 'Take 3 turns uninterrupted' wording; TF192-B01 remains unresolved and is not an acquired operational grant witness."},
        ],
        "requiredEvidence": [
            "Authorized grant contract with exact source/hash/card, genuine inserted full turn, recipient eligibility, trigger, activation, timing, costs, limits and ending.",
            "Complete legal recipient and any separate grantor acquisition/history, prerequisites/selections, resources and actual activation; explain legality while the recipient is Stunned (granting a turn does not itself remove Stunned).",
            "Integrated witness preserving initial INT save, paid Mind Collapse, concentration/Ready effects, 6.205 admission, regular ENDs at 7.900/13.900/19.900, event :11 at 6.300 as a boundary rather than a turn, recharge, Reaction, Ready expiry and conserved resources.",
        ],
    },
    "priorityOrder": order,
    "identityCount": len(all_ids),
}
ORDER_PATH.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

for path, field in [(HANDOFF_PATH, "closureOrder"), (QUEUE_PATH, "closureOrder")]:
    doc = json.loads(path.read_text(encoding="utf-8-sig"))
    doc[field] = {"path": ORDER_PATH.relative_to(ROOT).as_posix(), "priorities": order, "priorityCount": len(order), "identityCount": len(all_ids)}
    if path == HANDOFF_PATH:
        doc["nextStep"] = "Prepare a focused closure delta for mind-collapse / MD196-B01. It must add an authorized or newly recovered full-turn grant source, legal acquisition and actor/grantor history, and the integrated witness. Do not repeat unchanged reviews. Later priorities and their closure prerequisites are listed in the linked Director order."
        doc["nextStepText"] = doc["nextStep"]
        doc["closureGuidance"] = record["evidenceDeltaGuidance"]
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

pending["closureOrder"] = {"path": ORDER_PATH.relative_to(ROOT).as_posix(), "priorities": order, "priorityCount": len(order), "identityCount": len(all_ids)}
pending_path.write_text(json.dumps(pending, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def bind(path: pathlib.Path):
    raw = path.read_bytes()
    import hashlib, zlib
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}

queue = json.loads(QUEUE_PATH.read_text(encoding="utf-8-sig"))
queue["pendingIdentityAudit"] = bind(pending_path)
queue["currentPendingAudit"] = queue["pendingIdentityAudit"]
QUEUE_PATH.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

handoff = json.loads(HANDOFF_PATH.read_text(encoding="utf-8-sig"))
handoff["queue"] = bind(QUEUE_PATH)
handoff["queueBinding"] = handoff["queue"]
handoff["currentQueueBinding"] = handoff["queue"]
handoff["pendingIdentityAudit"] = bind(pending_path)
handoff["closureOrder"] = {"path": ORDER_PATH.relative_to(ROOT).as_posix(), **bind(ORDER_PATH), "priorityCount": len(order), "identityCount": len(all_ids)}
HANDOFF_PATH.write_text(json.dumps(handoff, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

snapshot = SNAPSHOT_PATH.read_text(encoding="utf-8-sig")
if "[Director closure order](CURRENT_CLOSURE_PRIORITIES_290.json)" not in snapshot:
    snapshot = snapshot.replace("Next artifacts:", "Director closure order: [15 priorities and exact prerequisites](CURRENT_CLOSURE_PRIORITIES_290.json). The Director requests a focused evidence delta; spell-local authoring or complete witnesses using existing sources may resolve blockers without repeating an unchanged hold.\n\nNext artifacts:")
SNAPSHOT_PATH.write_text(snapshot, encoding="utf-8")
print(json.dumps({"status": "RECORDED", "path": ORDER_PATH.relative_to(ROOT).as_posix(), "priorityCount": len(order), "identityCount": len(all_ids), "next": order[0]}, ensure_ascii=False, indent=2))
