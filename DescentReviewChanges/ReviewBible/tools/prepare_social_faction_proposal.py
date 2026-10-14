"""Preserve an unsent social/faction proposal and its authored review scenarios."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
from urllib.parse import unquote, urlsplit

G = Path(__file__).resolve().parents[3]
A = G / "docs/audit/2026-10-08/full-game"
PROPOSAL = A / "SOCIAL_FACTION_OPERATING_PROPOSAL.md"


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


SCENARIOS = [
    ("SO-01", "An authorized clerk already agrees to show an available ledger.", "No check is required; record any actual viewing time and conditions. A roll does not create an extra benefit."),
    ("SO-01", "A natural 20 is proposed for asking a clerk to transfer property they cannot authorize.", "Identify the missing authority before rolling; no total grants the transfer. A changed request can be considered separately."),
    ("SO-02", "Fixed DC12, modifier+4, natural8; no additional critical benefits declared.", "Total12 is Success and obtains exactly the promised success on stated terms. The Director cannot add an unannounced price by reserving success for22."),
    ("SO-02", "Fixed DC12, modifier+4, natural7, declared alternative costs5gp; compare opposed14 versus14.", "The fixed task fails at11. The player may accept the recorded5gp alternative or keep the money and refusal. The distinct opposed tie leaves the existing state unchanged; do not convert natural task shifts into tie modifiers."),
    ("SO-03", "An Insight approach has observable hesitation but no access to the hidden document being discussed.", "Resolve only the declared obtainable inference. Success does not read the document or reveal cosmic alignment; failure does not force belief in a fabricated fact."),
    ("SO-03", "A character succeeds at entertaining a crowd with Performance and asks for an automatic license and a second free Persuasion roll.", "Honor the declared audience response. The other requested outcomes need actual authority and distinct unresolved approaches; Performance does not grant them."),
    ("SO-04", "A known companion-schema score+2 and a legacy Loop-schema score+2 appear on separate imported characters.", "Preserve both originals and their formats. Only the known companion integer carries forward automatically; the Loop number needs a recorded interpretation because its meaning differs."),
    ("SO-04", "A new Medic background has been applied once; earned standing, an unknown faction key, explicit zero and a malformed source value now exist.", "Reapplying the background cannot reset earned scores. Keep unknown keys, explicit zero and the unresolved malformed value. Do not normalize them away or claim absence equals recorded zero."),
    ("SO-05", "The preserved Player alignment paragraph is encountered during the ordinary social conference.", "Retain the whole original as a deferred receipt. The proposal recommends no automatic alignment modifier pending review, but grants no authority to adopt that boundary or interpret cosmology before GPT's explicit disposition."),
    ("SO-05", "Two characters openly share a stated civic objective but their cosmic alignment is unknown.", "Their communicated objective can supply ordinary scene leverage; it does not establish identical cosmic alignment or grant the legacy automatic advantage."),
    ("SO-06", "Three participants and an interpreter complete a declared ten-minute exchange concurrently.", "Advance the shared clock by ten minutes, plus only actual separately required time. Do not charge forty minutes or count translation as an unrelated spell component."),
    ("SO-06", "A character tries to finish a minute-long bargain during one six-second combat round with a blocked communication channel.", "The bargain does not complete for free and the channel must actually work. Preserve initiative costs, effect deadlines and threats; a social skill cannot erase the missing channel."),
    ("SO-07", "A helper in initiative spends Help; the ally waits until after the helper's next regular start to check.", "The existing Help benefit has expired. Social rules do not extend its reviewed deadline."),
    ("SO-07", "After refusal, four allies repeat the same approach; later one supplies a genuine authorization letter.", "Speaker rotation alone grants no new resolutions. The new letter may establish a new approach with fresh disclosed stakes and time; earlier costs and refusal remain recorded."),
    ("SO-08", "A target is Charmed by the speaker, who requests a concession outside the target's authority.", "Preserve the charmer's social advantage where a legal check exists. Charmed supplies neither authority nor obedience, so it cannot make this concession possible."),
    ("SO-08", "Ordinary Intimidation succeeds; a separate actual Frightened source is no longer visible.", "Intimidation does not itself apply Frightened. Under the actual condition, loss of source visibility ends only its visibility-dependent disadvantage; the willing-approach restriction follows the source's existing duration."),
    ("SO-09", "An NPC accepts a bargain about property belonging to an absent owner they do not represent.", "Their agreement cannot transfer the absent owner's property. The speaker's success remains limited to the authority stated before the roll."),
    ("SO-09", "A player invokes a character's social feature to override another player's Session Zero boundary.", "The feature does not provide table agreement. Pause or revise under the existing table contract; do not impose a character penalty for using that procedure."),
    ("SO-10", "A confirmed major scene event proposes+2 standing from+2 under the recommended−3..+3 policy.", "Record original+2, attempted+2, applied+1, resulting+3 and overflow+1. Replaying the same institution/scene event adds nothing; the overflow is history, not banked future credit."),
    ("SO-10", "A private rescue changes one NPC's relationship; another institution learns of it through a later report.", "Do not grant omniscient global standing. Record the actual information event and the receiving institution's own attributable reaction, keeping report versus established fact distinct."),
    ("SO-11", "A faction's interview runs10:00–12:00; a return occurs11:00 and the same expedition crosses the threshold again11:05.", "The interview remains incomplete at11:00; the repeat crossing is not another return checkpoint and grants no work, tick or substitute completion."),
    ("SO-11", "A return and a proposed completed24-hour Haven checkpoint coincide while one actor has two incompatible assignments.", "The proposal processes one checkpoint, never duplicated hours or actions. The actor cannot complete both assignments with the same interval. The24-hour cadence still requires FL-03/FL-24 joint review."),
    ("SO-12", "A Claim clock at2/4 receives one new witness event, then two reports of that same event.", "Advance once to3/4. Preserve the report records without creating more segments. A distinct later qualifying document can advance the clock again."),
    ("SO-12", "A Depth clock reaches its threshold before the real route can be traversed; a Grudge clock fills during conversation.", "Record the Depth project's missing prerequisite instead of teleporting the rival. Grudge schedules its stated response through a real action, without a free immediate attack. Each objective's consequence resolves at most once."),
]


def main():
    text = PROPOSAL.read_text(encoding="utf-8")
    source = read(A / "SOCIAL_FACTION_SOURCE_PREPARATION.json")
    sources = source["fullSourceFiles"]
    for rel, meta in sources.items():
        expected = meta["sha256"] if isinstance(meta, dict) else meta
        assert sha(G / rel) == expected, rel
    frozen = read(A / "TEACHING_NAVIGATION_EXACT_V1_PREPARATION.json")["manifest"]
    protected = []
    for rel, meta in frozen.items():
        if rel == "README_TEACHING_EXACT_V1.md":
            continue
        assert sha(G / rel) == meta["sha256"], rel
        protected.append(rel)
    assert len(protected) == 217
    questions = sorted(set(re.findall(r"SO-\d{2}", text)))
    assert questions == [f"SO-{i:02d}" for i in range(1, 13)]
    references = []
    for href in re.findall(r"\]\(([^)]+)\)", text):
        parts = urlsplit(href)
        assert not parts.scheme and not parts.netloc
        p = (PROPOSAL.parent / unquote(parts.path)).resolve()
        assert p.is_relative_to(G.resolve()) and p.is_file(), href
        if parts.fragment:
            headings = [re.sub(r"[^\w -]", "", h.lower()).replace(" ", "-") for h in re.findall(r"^#{1,6}\s+(.+)$", p.read_text(encoding="utf-8-sig"), re.M)]
            assert parts.fragment in headings, href
        references.append({"href": href, "resolvedPath": p.relative_to(G).as_posix(), "sha256": sha(p)})
    scenarios = [{"id": f"SO-P-{i:02d}", "question": q, "premise": premise, "expectedUnderUnadoptedProposal": expected, "executionStatus": "authored-review-scenario-not-a-runtime-test"} for i, (q, premise, expected) in enumerate(SCENARIOS, 1)]
    assert len(scenarios) == 24 and all(sum(x["question"] == q for x in scenarios) == 2 for q in questions)
    receipt = {
        "status": "unadopted-proposal-prepared-unsent",
        "preparedAtUtc": datetime.now(timezone.utc).isoformat(),
        "manuscript": {"path": PROPOSAL.relative_to(G).as_posix(), "bytes": PROPOSAL.stat().st_size, "sha256": sha(PROPOSAL)},
        "questions": questions,
        "sharedDecision": "FL-23; no independent duplicate standing ruling",
        "fullSourceFiles": sources,
        "sourceFilesUnchanged": len(sources),
        "activeTeachingDiskPayloadsUnchanged": len(protected),
        "resolvedReferences": references,
        "authoredScenarios": scenarios,
        "exampleScope": "Two synthetic authored sequences; not campaign lore, runtime output or human test results",
        "newDecisionsRequiringJointReview": ["DC success remains the promised result; costly agreement is a separate offer", "Canonical−3..+3 recommendation and five existing companion bands", "Retirement of legacy automatic standing modifiers", "Explicit deferred-alignment boundary without cosmic interpretation", "Lossless original standing records and nonautomatic ambiguous conversions", "One signed institution/scene change with source-sized caps and preserved overflow", "Outside-initiative assistance duration", "Stable return/action IDs and real faction action clocks", "Proposed24-hour Haven checkpoint reconciled with FL-03/24", "Distinct-event rival clock ticks and real completion prerequisites"],
        "governingRulesModified": 0,
        "newApprovals": 0,
        "runtimeImplemented": False,
        "realSavesReadOrChanged": False,
        "humanTested": False,
        "cosmologyInterpreted": False,
        "submissionStatus": "UNSENT; confer after live teaching review"
    }
    out = A / "SOCIAL_FACTION_PROPOSAL_PREPARATION.json"
    assert not out.exists(), "Preserve prior receipt before preparing another revision"
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": receipt["status"], "questions": len(questions), "authoredScenarios": len(scenarios), "resolvedReferences": len(references), "unchangedSourceFiles": len(sources), "unchangedTeachingPayloads": len(protected), "manuscript": receipt["manuscript"]}, indent=2))


if __name__ == "__main__":
    main()
