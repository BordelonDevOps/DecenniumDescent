"""Promote the exact approved manuscript; preserve source records and past evidence."""
import hashlib
import json
from pathlib import Path

GAME = Path(r"C:\Github\DecenniumDescent")
ROOT = GAME / "DescentReviewChanges/ReviewBible"
AUDIT = GAME / "docs/audit/2026-10-08/full-game"
def read(p): return json.loads(p.read_text(encoding="utf-8-sig"))
def dump(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
review = "docs/audit/2026-10-08/full-game/GPT_CONJURATION_CANTRIP_EXACT_REVIEW.md"
assert "Approved. No required textual repairs remain." in (GAME/review).read_text(encoding="utf-8")
p = ROOT/"data/playtest/spell_drafts/candidate_conjuration_cantrips.json"
submission = read(AUDIT/"CONJURATION_CANTRIP_EXACT_SUBMISSION.json")
assert sha(p)==submission["candidateSha256BeforeReview"], "Candidate differs from submitted manuscript"
candidate=read(p)
candidate["status"]="PLAYTEST — REVIEWED / MANUSCRIPT-APPROVED; runtime and balance validation pending"
candidate["scope"]="Twelve ordinary rank-0 Conjuration identities; twelve placements, eleven exact-name Core blocks and one separately preserved comparative Mana Kindle block. No runtime/balance/whole-game approval."
candidate["reviewEvidence"].append(review)
for c in candidate["spells"]:
    c["implementationStatus"]="REVIEWED authored operational-playtest manuscript; runtime and balance validation pending"
    c["sourceReview"].append(review)
    c["reviewEvidence"]=[review]
dump(p,candidate)
batch=ROOT/"data/playtest/spell_drafts/batch_conjuration_cantrips.json"
assert not batch.exists(), "Batch already exists"
batch.write_bytes(p.read_bytes())
ids=[c["id"] for c in candidate["spells"]]
selected_path=ROOT/"data/playtest/spell_drafts/selected_sources.json"
selected=read(selected_path)
assert sum(map(len,selected.values()))==120
assert not set(ids).intersection(i for values in selected.values() for i in values)
selected["Conjuration"].extend(ids)
dump(selected_path,selected)

status={
 "status":"REVIEWED / MANUSCRIPT-APPROVED; no textual repairs required; promoted to operational playtest batch",
 "ids":ids,"count":12,"sourcePlacements":12,"exactNameCoreBlocks":11,"comparativeHistoricalCoreBlocks":1,
 "reviewEvidence":review,"candidatePath":p.relative_to(ROOT).as_posix(),"candidateSha256":sha(p),
 "promotedBatchPath":batch.relative_to(ROOT).as_posix(),"promotedBatchSha256":sha(batch),
 "submittedCandidateSha256":submission["candidateSha256BeforeReview"],
 "functionalManuscriptChangedAfterReview":False,"requiredRepairsApplied":[],
 "sourceAliasDecision":"Resonance Kindle uses the exact catalog/V6 self-cast 1-RP recovery; Mana Kindle remains a separately preserved comparative Core block, not an exact-name block, extra operational identity or every-cantrip trigger.",
 "operationalCatalogCount":132,"unfinishedIdentityCount":716,
 "pipelineValidation":"pending rebuild and validation",
 "runtimeImplemented":False,"balanceValidated":False,"wholeGameClosed":False,"githubPushed":False,
 "openBalanceQuestions":["Phantom Key's source-promised mundane key-operated lock bypass versus Thief Lockpick Mastery and exploration challenge design."],
 "limits":["Authored card approval does not execute spell effects in the pricing helper or companion app.","Unassigned variants and other spell identities retain their separate unfinished status."]
}
dump(ROOT/"docs/mechanics/CONJURATION_CANTRIP_REVIEW_STATUS.json",status)
submission.update({"status":"exact manuscript approved; promoted; pipeline validation pending","reviewEvidence":review,"requiredRepairsApplied":[],"candidateSha256AfterMetadataPromotion":sha(p),"batchSha256":sha(batch),"functionalManuscriptChangedAfterReview":False,"operationalAfter":132,"unfinishedAfter":716})
dump(AUDIT/"CONJURATION_CANTRIP_EXACT_SUBMISSION.json",submission)
conference=read(AUDIT/"CONJURATION_CANTRIP_CONFERENCE_SUBMISSION.json")
conference.update({"status":"source conference completed; exact cards subsequently approved and promoted","sourceReviewEvidence":"docs/audit/2026-10-08/full-game/GPT_CONJURATION_CANTRIP_SOURCE_CONFERENCE.md","exactReviewEvidence":review})
dump(AUDIT/"CONJURATION_CANTRIP_CONFERENCE_SUBMISSION.json",conference)

validator=ROOT/"tools/validate_spell_playtests.py"
v=validator.read_text(encoding="utf-8")
for old,new in [("All120 individually reviewed selected IDs", "All132 individually reviewed selected IDs"),("len(set(selected))==120", "len(set(selected))==132"),("Remaining728 explicitly blocked", "Remaining716 explicitly blocked"),("for s in spells.values())==728", "for s in spells.values())==716")]:
    assert old in v, old
    v=v.replace(old,new)
validator.write_text(v,encoding="utf-8")

# Show comparative aliases beside exact source blocks, keeping the labels distinct.
builder=ROOT/"tools/build_spell_playtests.py"
b=builder.read_text(encoding="utf-8")
old="'coreEntries':spell['source']['coreEntries']},ensure_ascii=False,indent=2),"
new="'coreEntries':spell['source']['coreEntries'],\n                                  'possibleHistoricalAliases':spell['source']['possibleHistoricalAliases']},ensure_ascii=False,indent=2),"
assert old in b
builder.write_text(b.replace(old,new),encoding="utf-8")

rules=ROOT/"docs/mechanics/SPELL_INTEGRATION_RULES.md"
t=rules.read_text(encoding="utf-8")
marker="Other unresolved aliases stay pending their own review; matching names never silently merge effects."
addition="\n\nResonance Kindle now has [exact manuscript approval](../../../../docs/audit/2026-10-08/full-game/GPT_CONJURATION_CANTRIP_EXACT_REVIEW.md): Action/Self/V/S, recover 1 RP only when this spell reaches resolution. Its one character-wide use is spent at legal cast start and refreshes only on a beneficial completed long rest. The comparative Mana Kindle block remains separately preserved; its broader wording does not trigger recovery from other cantrips and its historical range grants no remote recipient. The [Conjuration cantrip status](CONJURATION_CANTRIP_REVIEW_STATUS.json) records this bounded decision and the other eleven approved cards."
assert marker in t
rules.write_text(t.replace(marker,marker+addition),encoding="utf-8")

roadmap=ROOT/"docs/mechanics/DEVELOPMENT_ROADMAP.md"
t=roadmap.read_text(encoding="utf-8")
start=t.index("**Current conference:**")
end=t.index("\n\n",start)
t=t[:start]+"**Current conference:** twelve remaining Conjuration cantrips are [jointly manuscript-approved without further repairs](../../../../docs/audit/2026-10-08/full-game/GPT_CONJURATION_CANTRIP_EXACT_REVIEW.md) and selectable in the [spell index](SPELL_PLAYTEST_STARTER.md). The cards reconcile temporary objects, light and mist, the Mana Kindle comparison, Resonance task checks and faction emblems; [review status](CONJURATION_CANTRIP_REVIEW_STATUS.json) states the exact scope. Phantom Key's strong mundane-lock bypass remains an explicit balance question. The previous thirty-seven added Abjuration identities and the [body, equipment and carrying guide](BODY_EQUIPMENT_PLAYTEST.md) retain their bounded approvals. Eight feats are [jointly reviewed](FEAT_PLAYTEST_INDEX.md), with 327 unfinished. The [five-spell transformation/buffer interface](TRANSFORMATION_SPELL_PLAYTEST.md) remains promoted provisionally. The ordinary catalog has 132 reviewed drafts and 716 unfinished spell identities, with all 848 IDs and 936 placements retained. [Unassigned source variants](SPELL_VARIANT_REVIEW_STATUS.json), wider catalogs, runtime integration, balance and the whole-game candidate remain open."+t[end:]
t=t.replace("The thirty-seven added Abjuration identities are complete in their stated authored scope;", "The thirty-seven added Abjuration identities and twelve additional Conjuration cantrips are complete in their stated authored scope;")
t=t.replace("293 unfinished identities", "281 unfinished identities")
t=t.replace("120 individual drafts reviewed, including 72 starters, 6 healing/death additions, 5 transformation/buffer spells, 12 Abjuration cantrips, 12 rank-1-access additions and 13 further Abjuration identities; 728 unfinished.", "132 individual drafts reviewed, including 72 starters, 6 healing/death additions, 5 transformation/buffer spells, 37 additional Abjuration identities and 12 additional Conjuration cantrips; 716 unfinished.")
roadmap.write_text(t,encoding="utf-8")

start=GAME/"START_HERE.md"
t=start.read_text(encoding="utf-8")
t=t.replace("120 reviewed drafts; all 848 IDs and 936 placements preserved | 728 unfinished spell identities", "132 reviewed drafts; all 848 IDs and 936 placements preserved | 716 unfinished spell identities")
start.write_text(t,encoding="utf-8")

review_status=AUDIT/"REVIEW_STATUS.md"
t=review_status.read_text(encoding="utf-8")
t=t.replace("120 reviewed; 728 unfinished identities", "132 reviewed; 716 unfinished identities")
marker="Counterspell timing and Core check semantics are integrated into the shared manuscript."
assert marker in t
t=t.replace(marker,marker+" Twelve Conjuration cantrips are now [approved without further repairs](GPT_CONJURATION_CANTRIP_EXACT_REVIEW.md) and promoted; the Kindle alias remains separately preserved and Phantom Key balance remains open.",1)
t+="\n\n## Twelve Conjuration cantrips completed\n\nThe [source conference](GPT_CONJURATION_CANTRIP_SOURCE_CONFERENCE.md) and [exact approval](GPT_CONJURATION_CANTRIP_EXACT_REVIEW.md) close the authored scope for Dust Gust, Lodestone Pull, Minor Elemental Ward, Flicker Flame, Stone Skin Sliver, Resonance Kindle, Pebble Swarm, Elemental Touch, Mist Veil, Phantom Key, Resonance Mote and Faction Emblem. Twelve placements, eleven exact-name Core blocks and the separate Mana Kindle comparison are preserved. No functional text required repair after exact review.\n\nThe catalog now has 132 reviewed operational identities and 716 unfinished; 281 unfinished identities have an actual class rank at 0–3. The [status record](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/CONJURATION_CANTRIP_REVIEW_STATUS.json) and promotion check record the validation result. These are authored tabletop rules; runtime, numerical balance, unresolved source variants and the final whole-game/GitHub gates remain open.\n"
review_status.write_text(t,encoding="utf-8")

coverage_path=ROOT/"data/playtest/game_development_coverage.json"
coverage=read(coverage_path)
for a in coverage["aspects"]:
    if a["id"] in ["DD-11","DD-12"]:
        a["reviewEvidence"].append(review)
        a["draftEvidence"].append("DescentReviewChanges/ReviewBible/data/playtest/spell_drafts/batch_conjuration_cantrips.json")
        a["validationEvidence"].append("DescentReviewChanges/ReviewBible/docs/mechanics/CONJURATION_CANTRIP_REVIEW_STATUS.json")
        a["openIssues"]=[x.replace("120 individual spell drafts reviewed;728 unfinished", "132 individual spell drafts reviewed;716 unfinished") for x in a["openIssues"]]
        a["completedScopes"].append("Twelve remaining Conjuration cantrips manuscript-approved without repairs: bounded movement, elemental wards/touch, light/mist, temporary key, character-wide Kindle recovery, Resonance-task bonus and reputation-gated emblem. Twelve placements, eleven exact-name Core blocks and one separately adjudicated comparative Mana Kindle block preserved. Runtime and balance remain open.")
        if a["id"]=="DD-12":a["openIssues"].append("Balance-test Phantom Key's correct-key bypass of one mundane key-operated lock against Thief Lockpick Mastery and exploration challenge design; do not silently weaken the source-promised effect.")
dump(coverage_path,coverage)
print(json.dumps({"promoted":len(ids),"batchSha256":sha(batch),"selected":sum(map(len,selected.values())),"sourceDeletion":False,"pipeline":"pending"},indent=2))
