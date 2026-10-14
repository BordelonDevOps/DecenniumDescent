"""Promote eight exact-approved cards without changing their functional text."""
import json,hashlib
from pathlib import Path
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
review='docs/audit/2026-10-08/full-game/GPT_CONJURATION_RANK2_EXACT_REVIEW.md'
assert 'Approved. No required functional repairs remain.' in (G/review).read_text(encoding='utf-8')
p=R/'data/playtest/spell_drafts/candidate_conjuration_rank2.json';sub=read(A/'CONJURATION_RANK2_EXACT_SUBMISSION.json');assert sha(p)==sub['candidateSha256BeforeReview']
d=read(p);ids=[s['id'] for s in d['spells']]
d['status']='PLAYTEST — REVIEWED / MANUSCRIPT-APPROVED; runtime, CR certification and numerical balance pending'
d['scope']='Eight rank-2 Conjuration identities; eight original placements/Core blocks and actual seven-class access retained. Provisional authored rules, not runtime, bestiary-CR or numerical-balance certification.'
d['reviewEvidence'].append(review)
for s in d['spells']:
 s['implementationStatus']='REVIEWED authored operational-playtest manuscript; runtime, CR certification and numerical balance pending';s['sourceReview'].append(review);s['reviewEvidence']=[review]
dump(p,d);batch=R/'data/playtest/spell_drafts/batch_conjuration_rank2.json';assert not batch.exists();batch.write_bytes(p.read_bytes())
sp=R/'data/playtest/spell_drafts/selected_sources.json';sel=read(sp);assert sum(map(len,sel.values()))==144 and not set(ids).intersection(x for a in sel.values() for x in a);sel['Conjuration'].extend(ids);dump(sp,sel)
sub.update({'status':'exact manuscript approved; no functional repairs; promoted; pipeline pending','reviewEvidence':review,'requiredRepairsApplied':[],'functionalManuscriptChangedAfterReview':False,'candidateSha256AfterMetadataPromotion':sha(p),'batchSha256':sha(batch),'operationalAfter':152,'unfinishedAfter':696});dump(A/'CONJURATION_RANK2_EXACT_SUBMISSION.json',sub)
conference=read(A/'CONJURATION_RANK2_CONFERENCE_SUBMISSION.json');conference.update({'status':'source conference completed; exact cards approved without functional repairs and promoted','sourceReviewEvidence':'docs/audit/2026-10-08/full-game/GPT_CONJURATION_RANK2_SOURCE_CONFERENCE.md','exactReviewEvidence':review});dump(A/'CONJURATION_RANK2_CONFERENCE_SUBMISSION.json',conference)
status={'status':'REVIEWED / MANUSCRIPT-APPROVED; no functional repairs required; promoted to operational playtest batch','ids':ids,'count':8,'sourcePlacements':8,'sourceCoreBlocks':8,'reviewEvidence':review,'candidatePath':p.relative_to(R).as_posix(),'candidateSha256':sha(p),'promotedBatchPath':batch.relative_to(R).as_posix(),'promotedBatchSha256':sha(batch),'submittedCandidateSha256':sub['candidateSha256BeforeReview'],'functionalManuscriptChangedAfterReview':False,'requiredRepairsApplied':[],'operationalCatalogCount':152,'unfinishedIdentityCount':696,'pipelineValidation':'pending rebuild and validation','runtimeImplemented':False,'bestiaryCrCertified':False,'balanceValidated':False,'wholeGameClosed':False,'githubPushed':False,'openBalanceQuestions':['Elemental Barrage rank-2 value versus rank-1 Elemental Bolt.','Minor Planar Ally is a new finite summon-only profile for the intended CR-1 role, not a certified bestiary CR-1 creature.','Fixed Air Pet AC/HP/two attacks relative to explicitly scaling other companion profiles.'],'sourceScanEvidence':'docs/audit/2026-10-08/full-game/PLANAR_ALLY_MINOR_PUBLIC_CR1_SOURCE_SCAN.json'}
dump(R/'docs/mechanics/CONJURATION_RANK2_REVIEW_STATUS.json',status)
vp=R/'tools/validate_spell_playtests.py';v=vp.read_text(encoding='utf-8')
for old,new in [('All144 individually reviewed selected IDs','All152 individually reviewed selected IDs'),('len(set(selected))==144','len(set(selected))==152'),('Remaining704 explicitly blocked','Remaining696 explicitly blocked'),('for s in spells.values())==704','for s in spells.values())==696')]:
 assert old in v,old
 v=v.replace(old,new)
vp.write_text(v,encoding='utf-8')

rules=R/'docs/mechanics/SPELL_INTEGRATION_RULES.md';t=rules.read_text(encoding='utf-8');marker='A replacement requires the full casting cost. No summon grants loot, a reusable corpse or resource-generating death trigger.'
assert marker in t
extra='''

The [rank-2 Conjuration review](../../../../docs/audit/2026-10-08/full-game/GPT_CONJURATION_RANK2_EXACT_REVIEW.md) approves this specific companion overlay: **when an exact companion source prints multiple attacks as one damaging action, those attacks are components of one commanded offensive action and consume the owner's single offensive-companion allowance unless that source expressly grants otherwise.** Summon Air Pet explicitly makes its two source attacks within that one action; no second command/action or remaining offense for another companion is created. Its fixed AC15/HP20/two 1d6 attacks do not inherit generic companion scaling.

Planar Ally (Minor) uses a finite NEW summon-only profile for the source's intended CR-1 role. The bounded public bestiary scan did not establish an eligible published exact-CR1 extraplanar creature; this card does not certify its CR or rewrite a bestiary entry. Summon Weaponry Satchel has finite conjured contents tied to one duration, with a narrow exception only for an already resolving immediate use. Alignment Weapon's suppression default applies only to that printed card.

Resonance Well rolls one 1d4 total reserve. Its separately named creation and receipt uses commit before prevention and reset only through each character's beneficial long rest. These limits neither share nor reset Kindle or Mod Rod records. Read the exact cards and [rank-2 status](CONJURATION_RANK2_REVIEW_STATUS.json); pricing/schema checks do not execute these effects or certify balance.
'''
rules.write_text(t.replace(marker,marker+extra),encoding='utf-8')

roadmap=R/'docs/mechanics/DEVELOPMENT_ROADMAP.md';t=roadmap.read_text(encoding='utf-8');i=t.index('**Current conference:**');j=t.index('\n\n',i)
t=t[:i]+"**Current conference:** eight rank-2 Conjuration spells are [jointly manuscript-approved without functional repairs](../../../../docs/audit/2026-10-08/full-game/GPT_CONJURATION_RANK2_EXACT_REVIEW.md) and selectable in the [spell index](SPELL_PLAYTEST_STARTER.md). Air Pet retains two attacks within one commanded offensive action; the packet also covers Elemental Barrage, Shield of Sparks, finite satchel contents, a provisional Minor Planar Ally, Resonance Well, Greater Faction Emblem and Alignment Weapon. [Review status](CONJURATION_RANK2_REVIEW_STATUS.json) records preserved sources and open CR/balance questions. The previous twenty-four Conjuration additions and thirty-seven Abjuration additions retain their approvals. The [body/equipment guide](BODY_EQUIPMENT_PLAYTEST.md), [five-spell transformation/buffer interface](TRANSFORMATION_SPELL_PLAYTEST.md) and eight [reviewed feats](FEAT_PLAYTEST_INDEX.md) retain their bounded scopes; 327 feats remain unfinished. The ordinary catalog has 152 reviewed drafts and 696 unfinished identities, preserving all 848 IDs and 936 placements. [Unassigned variants](SPELL_VARIANT_REVIEW_STATUS.json), wider catalogs, runtime, balance and the whole-game candidate remain open."+t[j:]
t=t.replace('twenty-four additional Conjuration identities are complete','thirty-two additional Conjuration identities are complete').replace('269 unfinished identities','261 unfinished identities')
t=t.replace('144 individual drafts reviewed, including 72 starters, 6 healing/death additions, 5 transformation/buffer spells, 37 additional Abjuration identities and 24 additional Conjuration identities; 704 unfinished.','152 individual drafts reviewed, including 72 starters, 6 healing/death additions, 5 transformation/buffer spells, 37 additional Abjuration identities and 32 additional Conjuration identities; 696 unfinished.')
roadmap.write_text(t,encoding='utf-8')
start=G/'START_HERE.md';t=start.read_text(encoding='utf-8');t=t.replace('144 reviewed drafts; all 848 IDs and 936 placements preserved | 704 unfinished spell identities','152 reviewed drafts; all 848 IDs and 936 placements preserved | 696 unfinished spell identities');start.write_text(t,encoding='utf-8')
rs=A/'REVIEW_STATUS.md';t=rs.read_text(encoding='utf-8');t=t.replace('144 reviewed; 704 unfinished identities','152 reviewed; 696 unfinished identities')
marker='retaining the Core/V6 Mod Rod conflict evidence.';assert marker in t;t=t.replace(marker,marker+' Eight rank-2 Conjuration cards are [approved without functional repairs](GPT_CONJURATION_RANK2_EXACT_REVIEW.md) and promoted, including the bounded Air Pet multiattack exception and provisional Planar Ally profile.',1)
t+='''

## Eight rank-2 Conjuration spells completed

The [source conference](GPT_CONJURATION_RANK2_SOURCE_CONFERENCE.md) and [exact approval](GPT_CONJURATION_RANK2_EXACT_REVIEW.md) close the authored scope for Summon Air Pet, Elemental Barrage, Conjure Shield of Sparks, Summon Weaponry Satchel, Planar Ally (Minor), Resonance Well, Faction Emblem (Greater) and Alignment Weapon. No functional repairs were required. Eight original placements/Core blocks and all class access remain unchanged. The shared companion overlay now explicitly treats the Air Pet's two attacks as one offensive action using its owner's whole companion allowance.

The catalog now has 152 reviewed operational identities and 696 unfinished; 261 unfinished identities have at least one actual class rank at 0–3. The [status record](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/CONJURATION_RANK2_REVIEW_STATUS.json) records verification scope. Planar Ally is a NEW finite summon-only CR-1-role profile, not a certified CR-1 bestiary creature. Elemental Barrage's relative rank value and companion numerical balance remain open. Runtime, all source variants and whole-game/GitHub completion are not established.
'''
rs.write_text(t,encoding='utf-8')
cp=R/'data/playtest/game_development_coverage.json';cov=read(cp)
for a in cov['aspects']:
 if a['id'] in ['DD-11','DD-12','DD-35','DD-41']:
  if review not in a['reviewEvidence']:a['reviewEvidence'].append(review)
  path='DescentReviewChanges/ReviewBible/data/playtest/spell_drafts/batch_conjuration_rank2.json'
  if path not in a['draftEvidence']:a['draftEvidence'].append(path)
  path='DescentReviewChanges/ReviewBible/docs/mechanics/CONJURATION_RANK2_REVIEW_STATUS.json'
  if path not in a['validationEvidence']:a['validationEvidence'].append(path)
  a.setdefault('completedScopes',[])
 if a['id'] in ['DD-11','DD-12']:
  a['openIssues']=[s.replace('144 individual spell drafts reviewed;704 unfinished','152 individual spell drafts reviewed;696 unfinished') for s in a['openIssues']]
  a['completedScopes'].append('Eight rank-2 Conjuration identities manuscript-approved without functional repairs: source-specific Air Pet two attacks in one owner-budgeted action, single-target Barrage, bounded Shield retaliation, finite satchel, new provisional Minor Planar Ally profile, finite Well, membership save aura and alignment weapon. Eight placements/Core blocks preserved; runtime/CR/balance remain open.')
 if a['id']=='DD-12':a['openIssues'].append('Balance-test Elemental Barrage versus Elemental Bolt and fixed versus scaling companion profiles; Minor Planar Ally has only provisional intended CR-1 role, not certified bestiary CR.')
 if a['id']=='DD-35':
  a['completedScopes'].append('Air Pet preserves its two attacks within one commanded offensive action consuming the full owner companion allowance. Minor Planar Ally gains one explicitly new finite profile with actual mass/carrying and mundane property conservation; no canonical creature or CR certification is implied.')
  a['openIssues'].append('Human/encounter validation of the new Minor Planar Ally intended CR-1 profile and comparative Air Pet power remain outstanding; authored approval is not runtime or bestiary-wide closure.')
 if a['id']=='DD-41':a['completedScopes'].append('Resonance Well has separate character-wide creation and receipt uses per beneficial long rest, one rolled total reserve and committed finite withdrawals. It neither resets nor merges the reviewed Kindle/Mod Rod ledgers; no whole-resource-recovery or runtime closure implied.')
dump(cp,cov)
print(json.dumps({'promoted':8,'selected':sum(map(len,sel.values())),'batchSha256':sha(batch),'functionalRepairs':0,'pipeline':'pending'},indent=2))
