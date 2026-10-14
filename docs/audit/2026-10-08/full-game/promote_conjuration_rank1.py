"""Apply the three exact notebook repairs and promote their approved manuscript."""
import json,hashlib
from pathlib import Path
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
review='docs/audit/2026-10-08/full-game/GPT_CONJURATION_RANK1_EXACT_REVIEW.md'
assert 'After those repairs, I approve all twelve' in (G/review).read_text(encoding='utf-8')
p=R/'data/playtest/spell_drafts/candidate_conjuration_rank1.json'
sub=read(A/'CONJURATION_RANK1_EXACT_SUBMISSION.json')
assert sha(p)==sub['candidateSha256BeforeReview']
d=read(p);by={c['id']:c for c in d['spells']}
repairs={
 'heat-metal-conjured':{
  'field':'effect',
  'text':' Whenever this spell deals a pulse, record a next-pulse-not-before deadline 6 elapsed seconds after that pulse. No later pulse from this spell on this physical item can occur before that deadline, even if initiative begins, ends or is reordered. In initiative, after that deadline, the first otherwise eligible current-user regular-start in a numbered round may pulse, subject to the shared item/round guard. Leaving initiative preserves the same deadline; the first outside-initiative pulse cannot occur before it. Entering or leaving initiative never resets either the deadline or a spent item/round allowance. The physical item retains this deadline across replacement applications/casters just as it retains the shared round allowance. For a newly cast application with no preserved deadline, the first-future-user-start rule controls in initiative; outside initiative the initial deadline is application +6 seconds.'},
 'faction-messenger':{
  'field':'limitations',
  'text':' A description must identify one intended creature well enough that an ordinary observer using only the supplied description and currently perceivable facts could distinguish that creature from other creatures at the destination. If multiple creatures fit the description equally and the courier has no ordinary basis to distinguish the intended recipient, it delivers to none; the spell provides no magical tie-breaker or identity revelation.'},
 'corruption-sensor':{
  'field':'effect',
  'text':' When the detection predicate changes from false to true, the sensor emits one beep immediately, then one brief beep each elapsed second while the predicate remains true. It stops immediately when the predicate becomes false. The cadence is fixed and conveys no additional information. These are informational sounds, not separate mechanical actions or damage events.'}
}
for id,repair in repairs.items():by[id][repair['field']]+=repair['text']
d['status']='PLAYTEST — REVIEWED / MANUSCRIPT-APPROVED; three required textual repairs applied; runtime and balance validation pending'
d['scope']='Twelve ordinary rank-1 Conjuration identities; twelve placements/Core blocks and all seven source class-access rows retained. Authored tabletop procedures; no runtime/balance/whole-game approval.'
d['reviewEvidence'].append(review)
for c in d['spells']:
 c['implementationStatus']='REVIEWED authored operational-playtest manuscript; runtime and balance validation pending'
 c['sourceReview'].append(review);c['reviewEvidence']=[review]
dump(p,d)
batch=R/'data/playtest/spell_drafts/batch_conjuration_rank1.json';assert not batch.exists();batch.write_bytes(p.read_bytes())
ids=list(by)
selection=R/'data/playtest/spell_drafts/selected_sources.json';sel=read(selection)
assert sum(map(len,sel.values()))==132 and not set(ids).intersection(x for a in sel.values() for x in a)
sel['Conjuration'].extend(ids);dump(selection,sel)
names=['Heat Metal: explicit 6-second next-pulse-not-before deadline after every pulse, retained on physical item across initiative transitions and replacements','Faction Messenger: uniquely distinguishable ordinary description, otherwise no delivery or magical tie-breaker','Corruption Sensor: immediate first beep, then one fixed beep per elapsed second while predicate true']
sub.update({'status':'exact manuscript approved conditionally; three repairs applied; promoted; pipeline pending','reviewEvidence':review,'requiredRepairsApplied':names,'repairDetails':repairs,'candidateSha256AfterRepairs':sha(p),'batchSha256':sha(batch),'operationalAfter':144,'unfinishedAfter':704})
dump(A/'CONJURATION_RANK1_EXACT_SUBMISSION.json',sub)
conference=read(A/'CONJURATION_RANK1_CONFERENCE_SUBMISSION.json');conference.update({'status':'source conference completed; exact cards subsequently approved after three textual repairs and promoted','sourceReviewEvidence':'docs/audit/2026-10-08/full-game/GPT_CONJURATION_RANK1_SOURCE_CONFERENCE.md','exactReviewEvidence':review});dump(A/'CONJURATION_RANK1_CONFERENCE_SUBMISSION.json',conference)
status={'status':'REVIEWED / MANUSCRIPT-APPROVED; three required textual repairs applied; promoted to operational playtest batch','ids':ids,'count':12,'sourcePlacements':12,'sourceCoreBlocks':12,'reviewEvidence':review,'candidatePath':p.relative_to(R).as_posix(),'candidateSha256':sha(p),'promotedBatchPath':batch.relative_to(R).as_posix(),'promotedBatchSha256':sha(batch),'submittedCandidateSha256':sub['candidateSha256BeforeReview'],'requiredRepairsApplied':names,'sourceConflictDecision':'Summon Mod Rod restores Core V2 2 RP under spellcasting-domain precedence; V6/catalog 1-RP wording remains preserved as conflict evidence.','operationalCatalogCount':144,'unfinishedIdentityCount':704,'pipelineValidation':'pending rebuild and validation','runtimeImplemented':False,'balanceValidated':False,'wholeGameClosed':False,'githubPushed':False}
dump(R/'docs/mechanics/CONJURATION_RANK1_REVIEW_STATUS.json',status)

vpath=R/'tools/validate_spell_playtests.py';v=vpath.read_text(encoding='utf-8')
for old,new in [('All132 individually reviewed selected IDs','All144 individually reviewed selected IDs'),('len(set(selected))==132','len(set(selected))==144'),('Remaining716 explicitly blocked','Remaining704 explicitly blocked'),('for s in spells.values())==716','for s in spells.values())==704')]:
 assert old in v,old
 v=v.replace(old,new)
vpath.write_text(v,encoding='utf-8')

rules=R/'docs/mechanics/SPELL_INTEGRATION_RULES.md';t=rules.read_text(encoding='utf-8')
marker='## Components, summons and ongoing effects'
addition='''## Reviewed finite conjurations

The [rank-1 Conjuration review](../../../../docs/audit/2026-10-08/full-game/GPT_CONJURATION_RANK1_EXACT_REVIEW.md) selects **2 RP** for Summon Mod Rod under the manifest's Core V2 spellcasting precedence; the conflicting V6/catalog 1-RP wording remains preserved. Its charge and separate character-wide caster supply/recipient receipt uses commit at activation start, including prevented or zero recovery, and refresh only on each character's beneficial completed long rest. Replacing rods never resets those records.

Read the [exact cards](SPELL_PLAYTEST_STARTER.md) for each created object's weight, native HP, duration, custody, load and ending. Summon Minor Weapon is wielded through ordinary weapon actions; it grants no attack on casting. Conjure Rope and Resonance Bridge require real support and apply ordinary Falling on failure. Alignment Essence preserves its empty result-vial for one minute after full consumption. Faction Messenger conserves supplied mundane paper and cannot resolve an ambiguous recipient description magically. Heat Metal keeps its physical-item round record and six-second next-pulse deadline through recasting, handoff and initiative changes. These are authored procedures; [review status](CONJURATION_RANK1_REVIEW_STATUS.json) does not certify runtime or balance.

'''
assert marker in t;rules.write_text(t.replace(marker,addition+marker),encoding='utf-8')

roadmap=R/'docs/mechanics/DEVELOPMENT_ROADMAP.md';t=roadmap.read_text(encoding='utf-8');i=t.index('**Current conference:**');j=t.index('\n\n',i)
t=t[:i]+"**Current conference:** twelve rank-1 Conjuration spells are [jointly manuscript-approved after three exact repairs](../../../../docs/audit/2026-10-08/full-game/GPT_CONJURATION_RANK1_EXACT_REVIEW.md) and selectable in the [spell index](SPELL_PLAYTEST_STARTER.md). They cover direct attacks, summoned gear/companions, wards, heated metal, rope/bridge support, a faction courier, alignment revelation and Corruption detection. Core V2's 2-RP Mod Rod value controls while the 1-RP variant remains preserved. [Review status](CONJURATION_RANK1_REVIEW_STATUS.json) records the pulse-clock, recipient-description and beep-cadence repairs. The twelve Conjuration cantrips and thirty-seven added Abjuration identities retain their prior approvals. The [body/equipment guide](BODY_EQUIPMENT_PLAYTEST.md), [five-spell transformation/buffer interface](TRANSFORMATION_SPELL_PLAYTEST.md) and eight [reviewed feats](FEAT_PLAYTEST_INDEX.md) retain their bounded scopes; 327 feats remain unfinished. The ordinary catalog has 144 reviewed drafts and 704 unfinished identities, preserving all 848 IDs and 936 placements. [Unassigned source variants](SPELL_VARIANT_REVIEW_STATUS.json), wider catalogs, runtime, balance and the whole-game candidate remain open."+t[j:]
t=t.replace('twelve additional Conjuration cantrips are complete','twenty-four additional Conjuration identities are complete')
t=t.replace('281 unfinished identities','269 unfinished identities')
t=t.replace('132 individual drafts reviewed, including 72 starters, 6 healing/death additions, 5 transformation/buffer spells, 37 additional Abjuration identities and 12 additional Conjuration cantrips; 716 unfinished.','144 individual drafts reviewed, including 72 starters, 6 healing/death additions, 5 transformation/buffer spells, 37 additional Abjuration identities and 24 additional Conjuration identities; 704 unfinished.')
roadmap.write_text(t,encoding='utf-8')
start=G/'START_HERE.md';t=start.read_text(encoding='utf-8');t=t.replace('132 reviewed drafts; all 848 IDs and 936 placements preserved | 716 unfinished spell identities','144 reviewed drafts; all 848 IDs and 936 placements preserved | 704 unfinished spell identities');start.write_text(t,encoding='utf-8')
rs=A/'REVIEW_STATUS.md';t=rs.read_text(encoding='utf-8');t=t.replace('132 reviewed; 716 unfinished identities','144 reviewed; 704 unfinished identities')
marker='the Kindle alias remains separately preserved and Phantom Key balance remains open.'
assert marker in t;t=t.replace(marker,marker+' Twelve rank-1 Conjuration spells are [approved after three repairs](GPT_CONJURATION_RANK1_EXACT_REVIEW.md) and promoted, retaining the Core/V6 Mod Rod conflict evidence.',1)
t+='''

## Twelve rank-1 Conjuration spells completed

The [source conference](GPT_CONJURATION_RANK1_SOURCE_CONFERENCE.md) and [exact review](GPT_CONJURATION_RANK1_EXACT_REVIEW.md) approve Burning Sands, Shockwave, Summon Mod Rod, Summon Minor Weapon, Flame Armor, Heat Metal (Conjured), Conjure Rope, Summon Familiar, Resonance Bridge, Faction Messenger, Alignment Essence and Corruption Sensor. The three required repairs explicitly preserve Heat Metal's pulse deadline, reject ambiguous descriptive courier recipients and fix the sensor's beep cadence. Core's 2-RP rod recovery controls; both conflicting original values remain in source evidence.

The catalog now has 144 reviewed operational spell identities and 704 unfinished; 269 unfinished identities have at least one actual class rank at 0–3. Twelve source placements/Core blocks and all actual class access rows are unchanged. [Status](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/CONJURATION_RANK1_REVIEW_STATUS.json) records validation scope. Authored spell rules do not certify runtime, numerical balance, all source variants or whole-game/GitHub completion.
'''
rs.write_text(t,encoding='utf-8')
cp=R/'data/playtest/game_development_coverage.json';cov=read(cp)
for a in cov['aspects']:
 if a['id'] in ['DD-11','DD-12']:
  a['reviewEvidence'].append(review);a['draftEvidence'].append('DescentReviewChanges/ReviewBible/data/playtest/spell_drafts/batch_conjuration_rank1.json');a['validationEvidence'].append('DescentReviewChanges/ReviewBible/docs/mechanics/CONJURATION_RANK1_REVIEW_STATUS.json')
  a['openIssues']=[s.replace('132 individual spell drafts reviewed;716 unfinished','144 individual spell drafts reviewed;704 unfinished') for s in a['openIssues']]
  a['completedScopes'].append('Twelve rank-1 Conjuration identities manuscript-approved after pulse-transition, recipient-disambiguation and sensor-cadence repairs; bounded summoned gear/companions/structures, wards, detection and alignment vial. Core2RP Mod Rod authority chosen with V6/catalog1RP preserved. Twelve original placements/Core blocks retained; runtime and balance remain open.')
dump(cp,cov)
print(json.dumps({'promoted':12,'selected':sum(map(len,sel.values())),'batchSha256':sha(batch),'requiredRepairsApplied':names,'pipeline':'pending'},indent=2))
