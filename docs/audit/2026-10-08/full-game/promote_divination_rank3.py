import json,hashlib
from pathlib import Path
G=Path(r'C:\Github\DecenniumDescent'); R=G/'DescentReviewChanges/ReviewBible'; A=G/'docs/audit/2026-10-08/full-game'; D=R/'data/playtest/spell_drafts'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
review='docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK3_EXACT_REVIEW.md'
assert 'All eight are approved as authored.' in (G/review).read_text(encoding='utf-8')
p=D/'candidate_divination_rank3.json'; sub=read(A/'DIVINATION_RANK3_EXACT_SUBMISSION.json')
assert sha(p)==sub['candidateSha256BeforeReview']
d=read(p); ids=[s['id'] for s in d['spells']]
existing={s['id']:s['operational'] for s in read(R/'data/public/spell_playtests/catalog.json')['spells'] if s['operational']}
assert len(existing)==190 and not set(ids).intersection(existing)
sub['previousOperationalSha256']=hashlib.sha256(json.dumps(existing,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
d['status']='PLAYTEST — REVIEWED / MANUSCRIPT-APPROVED exactly as submitted; runtime/balance pending'
d['reviewEvidence'].append(review)
for s in d['spells']:
    s['implementationStatus']='REVIEWED authored operational PLAYTEST manuscript; runtime, numerical balance and broader system validation pending'
    s['sourceReview'].append(review); s['reviewEvidence']=[review]
dump(p,d)
b=D/'batch_divination_rank3.json'; assert not b.exists(); b.write_bytes(p.read_bytes())
sel=read(D/'selected_sources.json'); assert sum(map(len,sel.values()))==190
assert not set(ids).intersection(i for v in sel.values() for i in v)
sel['Divination'].extend(ids); dump(D/'selected_sources.json',sel)
sub.update({'status':'approved without functional repairs; promoted; pipeline pending','reviewEvidence':review,'requiredRepairsApplied':[],'functionalManuscriptChangedAfterReview':False,'candidateSha256AfterPromotion':sha(p),'batchSha256':sha(b),'operationalAfter':198,'unfinishedAfter':650})
dump(A/'DIVINATION_RANK3_EXACT_SUBMISSION.json',sub)
conf=read(A/'DIVINATION_RANK3_CONFERENCE_SUBMISSION.json');conf.update({'status':'source conference and exact review complete; promoted without functional repairs','exactReviewEvidence':review});dump(A/'DIVINATION_RANK3_CONFERENCE_SUBMISSION.json',conf)
status={'status':'REVIEWED / MANUSCRIPT-APPROVED; promoted exactly as submitted','ids':ids,'count':8,'sourcePlacements':9,'sourceCoreBlocks':9,'reviewEvidence':review,'candidatePath':p.relative_to(R).as_posix(),'candidateSha256':sha(p),'promotedBatchPath':b.relative_to(R).as_posix(),'promotedBatchSha256':sha(b),'submittedCandidateSha256':sub['candidateSha256BeforeReview'],'requiredRepairsApplied':[],'operationalCatalogCount':198,'unfinishedIdentityCount':650,'pipelineValidation':'pending rebuild and validation','runtimeImplemented':False,'balanceValidated':False,'wholeGameClosed':False,'githubPushed':False,'openBalanceQuestions':['Future Echo has a reviewed bounded tabletop permutation, not a completed runtime scheduler adapter.','Speak with Dead identity/remains memory bindings and information protections require wider runtime and adventure validation.','Public planar observation and native detection need human adventure balance testing.','Alignment Revelation retains source rank/save cost despite overlap with lower-rank private readers.','Broader provenance, faction information, active-magic and secrecy systems remain open.']}
dump(R/'docs/mechanics/DIVINATION_RANK3_REVIEW_STATUS.json',status)
vp=R/'tools/validate_spell_playtests.py';t=vp.read_text(encoding='utf-8')
for old,new in [('All190 individually reviewed selected IDs','All198 individually reviewed selected IDs'),('len(set(selected))==190','len(set(selected))==198'),('Remaining658 explicitly blocked','Remaining650 explicitly blocked'),('for s in spells.values())==658','for s in spells.values())==650')]:
    assert old in t;t=t.replace(old,new)
vp.write_text(t,encoding='utf-8')
rules=R/'docs/mechanics/SPELL_INTEGRATION_RULES.md';t=rules.read_text(encoding='utf-8')
t+='''

## Rank-three Divination: initiative, remains and information

The [exact review](../../../../docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK3_EXACT_REVIEW.md) approves all eight cards without functional repairs. [Review status](DIVINATION_RANK3_REVIEW_STATUS.json) records their bounded manuscript scope.

**Future Echo** records a willing allied participant order and, at the next numbered round boundary, permutes surviving participants only among their existing regular baseline slots. Finish current end-round events, restore any prior Echo permutation while retaining legitimate other initiative changes, then apply pending schedules in stable application order. Earlier applications claim their eligible participants, including a singleton; later schedules skip those participants. Enemy/unselected slots stay fixed. A pending schedule suppressed or unavailable at its one execution boundary expires without makeup. Its execution commits a fixed one-round assignment rather than a state that can be dispelled midround to duplicate or skip turns. The baseline returns at the following boundary before another Echo is applied. Each participant still receives exactly one actual regular turn and its ordinary start/end procedure. Existing virtual duration, periodic, falling and absolute clocks do not migrate or replay. Outside initiative the spell has no scheduling effect. This is a tabletop procedure; the broader scheduler adapter and full Time Loop remain unimplemented/disabled as previously recorded.

**Speak with Dead** retains both school placements. Cast through Cleric, Mirrorsage, Ranger, Shaman, Wizard or Paladin as Divination; through Crimson Agent, Druid or Thief as Necromancy, under the actual selected class access. A Divination-only protection therefore does not automatically block its Necromancy placement. The spell uses a retained memory echo associated with actual remains/death context, not a summoned soul or resurrection. Old fragments do not automatically acquire memories from a later resurrected life. Hidden identity eligibility resolves after paid casting; currently living identities are ineligible. Five separate Action/question exchanges follow the casting Action within its one-minute window. Actual return to life or loss of the qualifying physical anchor ends the interview.

Eyes of the Divine inspects readable appearance/form layers without reverting the body. Reveal Weakness affects the next actual save event, including an automatic-result save without overriding its result. Planar Window separates public ordinary vision from the caster's private native-presence detection. Faction Divination reads a genuine institutional objective, Alignment Revelation supplies public visible sigils after a failed CHA save, and Resonance Sight (Greater) identifies readable local effects and recorded proximate provenance without remote current-location omniscience. Wider runtime, source variants, secrecy, information completeness and human balance remain open.
'''
rules.write_text(t,encoding='utf-8')
road=R/'docs/mechanics/DEVELOPMENT_ROADMAP.md';t=road.read_text(encoding='utf-8');i=t.index('**Current conference:**');j=t.index('\n\n',i)
t=t[:i]+"""**Current conference:** eight rank-three Divination identities are [jointly manuscript-approved exactly as submitted](../../../../docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK3_EXACT_REVIEW.md). This includes Future Echo's bounded next-round initiative permutation and both actual Speak with Dead school placements. [Review status](DIVINATION_RANK3_REVIEW_STATUS.json) preserves all nine source placements/Core blocks and exact class access. Previous approvals retain their bounded scopes; 327 feats remain unfinished. The [spell index](SPELL_PLAYTEST_STARTER.md) has 198 reviewed drafts and 650 unfinished identities, preserving all 848 IDs and 936 placements. All currently unfinished Divination and Conjuration identities through rank 3 are authored. Continue the remaining low-rank schools; higher ranks, [unassigned variants](SPELL_VARIANT_REVIEW_STATUS.json), broader systems, runtime, human balance and whole-game closure remain open."""+t[j:]
t=t.replace('223 unfinished identities','215 unfinished identities').replace('190 individual drafts reviewed, including 72 starters, 6 healing/death additions, 5 transformation/buffer spells, 37 additional Abjuration identities, 39 additional Conjuration identities and 31 additional Divination identities; 658 unfinished.','198 individual drafts reviewed, including 72 starters, 6 healing/death additions, 5 transformation/buffer spells, 37 additional Abjuration identities, 39 additional Conjuration identities and 39 additional Divination identities; 650 unfinished.')
road.write_text(t,encoding='utf-8')
sp=G/'START_HERE.md';t=sp.read_text(encoding='utf-8');old='190 reviewed drafts; all 848 IDs and 936 placements preserved | 658 unfinished spell identities';assert old in t
sp.write_text(t.replace(old,'198 reviewed drafts; all 848 IDs and 936 placements preserved | 650 unfinished spell identities'),encoding='utf-8')
rp=A/'REVIEW_STATUS.md';t=rp.read_text(encoding='utf-8').replace('190 reviewed; 658 unfinished identities','198 reviewed; 650 unfinished identities')
anchor='Eight rank-two Divination cards are [approved](GPT_DIVINATION_RANK2_EXACT_REVIEW.md) with paid-information preflight repairs and the [Vision Trap timing clarification](GPT_DIVINATION_RANK2_FINAL_CLARIFICATION.md).';assert anchor in t
t=t.replace(anchor,anchor+' Eight rank-three Divination cards are [approved exactly as submitted](GPT_DIVINATION_RANK3_EXACT_REVIEW.md), including Future Echo and both Speak with Dead placements.',1)
t+='''

## Eight rank-three Divination identities completed

The [source conference](GPT_DIVINATION_RANK3_SOURCE_CONFERENCE.md) and [exact review](GPT_DIVINATION_RANK3_EXACT_REVIEW.md) approve all eight cards without functional repairs. Future Echo permutes willing allies among their existing slots for one numbered round while retaining fixed clocks. Speak with Dead preserves both actual school placements, uses five separate paid question exchanges and binds memories to actual remains/death context. The other cards define disguise inspection, next-save disadvantage, public planar observation/private native detection, institutional objectives, public alignment revelation and local magical-effect provenance.

The catalog has 198 reviewed identities and 650 unfinished; 215 unfinished have an actual class rank 0–3. Nine original placements/Core blocks and exact class access are retained. No currently unfinished Divination identity through rank three remains, but higher ranks, source variants, broader systems, runtime, human balance and whole-game review remain open. No source information was deleted and GitHub was not pushed. [Status](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/DIVINATION_RANK3_REVIEW_STATUS.json) records validation scope.
'''
rp.write_text(t,encoding='utf-8')
cp=R/'data/playtest/game_development_coverage.json';cov=read(cp)
scopes={
'DD-03':'Future Echo exact tabletop schedule approved: selected-slot permutation, boundary restoration, stable competing claims, no extra turns/clock duplication. Runtime scheduler remains open.',
'DD-11':'Eight rank-three Divination identities and nine source placements/Core blocks preserved, including Speak with Dead’s actual Divination/Necromancy class modes. 198 reviewed / 650 unfinished; source variants remain open.',
'DD-12':'Eight rank-three Divination cards approved exactly as submitted. All Divination identities through rank3 now authored; higher ranks, variants, runtime and numerical balance remain open.',
'DD-19':'Eyes of the Divine separates disguise/form presence from readable underlying appearance; Planar Window and Greater Resonance Sight retain exact sensory/protection limits.',
'DD-39':'Planar Window supplies public remote vision and private bounded native detection with no travel/remote-casting permission; actual location/plane provenance remains source-defined.',
'DD-49':'Faction Divination reads one stable actual institutional objective without member/reputation gates or fabricating private plans as institution-wide facts.',
'DD-53':'Speak with Dead uses truthful subjective memory echoes, five actual exchanges and remains/death-context knowledge; alignment and magic-source reports preserve independent unknown/protected fields.',
'DD-54':'Speak with Dead uses its actual casting-class school for protection; currently living identity/remains truth resolves only after payment. Broader secrecy/data separation remains open.'
}
for a in cov['aspects']:
    if a['id'] not in scopes:continue
    for key,path in [('reviewEvidence',review),('draftEvidence','DescentReviewChanges/ReviewBible/data/playtest/spell_drafts/batch_divination_rank3.json'),('validationEvidence','DescentReviewChanges/ReviewBible/docs/mechanics/DIVINATION_RANK3_REVIEW_STATUS.json')]:
        if path not in a[key]:a[key].append(path)
    a.setdefault('completedScopes',[]).append(scopes[a['id']])
    if a['id'] in ['DD-11','DD-12']:a['openIssues']=[s.replace('190 individual spell drafts reviewed;658 unfinished','198 individual spell drafts reviewed;650 unfinished') for s in a['openIssues']]
dump(cp,cov)
print(json.dumps({'promoted':8,'sourcePlacements':9,'selected':sum(map(len,sel.values())),'batchSha256':sha(b),'functionalRepairs':0,'pipeline':'pending'},indent=2))
