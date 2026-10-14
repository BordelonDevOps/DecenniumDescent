import json, hashlib
from pathlib import Path
G=Path(r'C:\Github\DecenniumDescent'); R=G/'DescentReviewChanges/ReviewBible'; A=G/'docs/audit/2026-10-08/full-game'; D=R/'data/playtest/spell_drafts'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
review='docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK2_EXACT_REVIEW.md'
final='docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK2_FINAL_CLARIFICATION.md'
assert (G/final).exists(), 'Actual final timing clarification required before promotion'
assert 'After those repairs, all eight may be promoted' in (G/review).read_text(encoding='utf-8')
p=D/'candidate_divination_rank2.json'; sub=read(A/'DIVINATION_RANK2_EXACT_SUBMISSION.json')
assert sha(p)==sub['candidateSha256AfterPreflightRepairs']
d=read(p); by={s['id']:s for s in d['spells']}; ids=list(by)
proposal=read(A/'DIVINATION_RANK2_TIMING_PROPOSAL.json')
old=by['vision-trap']['effect']
assert proposal['oldTiming'] in old
new=old.replace(proposal['oldTiming'],proposal['newTiming'])
assert new==proposal['proposedEffect']
by['vision-trap']['effect']=new
repairs=sub['requiredRepairsApplied']+[{'id':'vision-trap','field':'effect','before':old,'after':new,'reason':'Final GPT clarification: exclude the entire current target turn from the next-turn endpoint'}]
before=read(R/'data/public/spell_playtests/catalog.json')['spells']
existing={s['id']:s['operational'] for s in before if s['operational']}
assert len(existing)==182 and not set(ids).intersection(existing)
sub['previousOperationalSha256']=hashlib.sha256(json.dumps(existing,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
d['status']='PLAYTEST — REVIEWED / MANUSCRIPT-APPROVED after preflight and Vision Trap timing repairs; runtime/balance pending'
d['reviewEvidence'].extend([review,final])
for s in d['spells']:
    s['implementationStatus']='REVIEWED authored operational PLAYTEST manuscript; runtime, numerical balance and broader Divination/information-system validation pending'
    s['sourceReview'].extend([review,final]); s['reviewEvidence']=[review,final]
dump(p,d)
b=D/'batch_divination_rank2.json'; assert not b.exists(); b.write_bytes(p.read_bytes())
sel=read(D/'selected_sources.json'); assert sum(map(len,sel.values()))==182
assert not set(ids).intersection(i for v in sel.values() for i in v)
sel['Divination'].extend(ids); dump(D/'selected_sources.json',sel)
sub.update({'status':'approved preflight and timing repairs applied; promoted; pipeline pending','reviewEvidence':[review,final],'requiredRepairsApplied':repairs,'changesLimitedToReviewedRepairs':True,'candidateSha256AfterPromotion':sha(p),'batchSha256':sha(b),'operationalAfter':190,'unfinishedAfter':658})
dump(A/'DIVINATION_RANK2_EXACT_SUBMISSION.json',sub)
proposal.update({'status':'approved; exact timing repair applied','reviewEvidence':final}); dump(A/'DIVINATION_RANK2_TIMING_PROPOSAL.json',proposal)
conf=read(A/'DIVINATION_RANK2_CONFERENCE_SUBMISSION.json'); conf.update({'status':'source conference, exact review and timing clarification complete; promoted','exactReviewEvidence':[review,final]}); dump(A/'DIVINATION_RANK2_CONFERENCE_SUBMISSION.json',conf)
status={'status':'REVIEWED / MANUSCRIPT-APPROVED; preflight and timing repairs applied; promoted','ids':ids,'count':8,'sourcePlacements':8,'sourceCoreBlocks':8,'reviewEvidence':[review,final],'candidatePath':p.relative_to(R).as_posix(),'candidateSha256':sha(p),'promotedBatchPath':b.relative_to(R).as_posix(),'promotedBatchSha256':sha(b),'submittedCandidateSha256':sub['candidateSha256BeforeReview'],'requiredRepairsApplied':[{'id':x['id'],'field':x['field'],'reason':x['reason']} for x in repairs],'operationalCatalogCount':190,'unfinishedIdentityCount':658,'pipelineValidation':'pending rebuild and validation','runtimeImplemented':False,'balanceValidated':False,'wholeGameClosed':False,'githubPushed':False,'openBalanceQuestions':['Human adventure validation of one-mile and any-distance same-plane information; same-plane unknowns are resolved only after paid casting.','Forecast usefulness and stable equivalent inquiries need human adjudication and adventure tests.','Resonance Tracking has a bounded one-hour trace model; full provenance, protection and spatial runtime remain open.','Vision Trap damage/next-attack rider balance and broader interaction tests remain open.']}
dump(R/'docs/mechanics/DIVINATION_RANK2_REVIEW_STATUS.json',status)
vp=R/'tools/validate_spell_playtests.py'; t=vp.read_text(encoding='utf-8')
for old,new in [('All182 individually reviewed selected IDs','All190 individually reviewed selected IDs'),('len(set(selected))==182','len(set(selected))==190'),('Remaining666 explicitly blocked','Remaining658 explicitly blocked'),('for s in spells.values())==666','for s in spells.values())==658')]:
    assert old in t; t=t.replace(old,new)
vp.write_text(t,encoding='utf-8')
rules=R/'docs/mechanics/SPELL_INTEGRATION_RULES.md'
t=rules.read_text(encoding='utf-8')
t+='''

## Rank-two Divination: paid information and preserved turn timing

The [exact review](../../../../docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK2_EXACT_REVIEW.md) requires **Locate Person, Faction Spy and Resonance Tracking** to resolve hidden person eligibility, plane/range conditions and trace existence after casting costs commit. Their legal Self inquiry/search must not reveal those facts through a free target-legality check. No-result feeds/bearings/searches do not diagnose the hidden reason or refund committed costs. This clarification is scoped to these exact card interfaces; other spells retain their printed target rules.

The [final timing clarification](../../../../docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK2_FINAL_CLARIFICATION.md) keeps **Vision Trap** consistent with the existing hostile/next-turn convention: its pending rider ends at the end of the target's first future regular turn, excluding the entire current target turn even if its end is still upcoming. An attack earlier than that endpoint can consume the rider normally. Existing virtual markers, outside-initiative six-second timing and end-phase-before-cleanup ordering remain unchanged.

Augury and Alignment Prediction supply bounded useful likelihood forecasts without forcing choices. Divine Perception requires actual divine provenance. Clairvoyance and Faction Spy provide only their specified fixed remote senses. Resonance Tracking preserves the original cast-start age of actual origin/path/endpoint traces; observing them creates no copied trail, new resource or refreshed age. [Review status](DIVINATION_RANK2_REVIEW_STATUS.json) records manuscript scope; wider information, provenance, runtime and numerical balance remain open.
'''
rules.write_text(t,encoding='utf-8')
road=R/'docs/mechanics/DEVELOPMENT_ROADMAP.md'; t=road.read_text(encoding='utf-8'); i=t.index('**Current conference:**'); j=t.index('\n\n',i)
t=t[:i]+"""**Current conference:** eight rank-two Divination spells are [jointly manuscript-approved](../../../../docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK2_EXACT_REVIEW.md), with three hidden-information preflight repairs and the [Vision Trap next-turn clarification](../../../../docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK2_FINAL_CLARIFICATION.md) applied. Forecasts, divine provenance, remote senses, locating a person, disorientation and spell-trace tracking now have exact procedures. [Review status](DIVINATION_RANK2_REVIEW_STATUS.json) records unchanged source/access and open runtime/balance scope. Previous approvals retain their bounded scopes; 327 feats remain unfinished. The [spell index](SPELL_PLAYTEST_STARTER.md) has 190 reviewed drafts and 658 unfinished identities, preserving all 848 IDs and 936 placements. All currently unfinished Divination identities through rank 2 and Conjuration through rank 3 are authored. Higher ranks, other schools, [unassigned variants](SPELL_VARIANT_REVIEW_STATUS.json), broader systems, runtime, human balance and whole-game closure remain open."""+t[j:]
t=t.replace('231 unfinished identities','223 unfinished identities').replace('182 individual drafts reviewed, including 72 starters, 6 healing/death additions, 5 transformation/buffer spells, 37 additional Abjuration identities, 39 additional Conjuration identities and 23 additional Divination identities; 666 unfinished.','190 individual drafts reviewed, including 72 starters, 6 healing/death additions, 5 transformation/buffer spells, 37 additional Abjuration identities, 39 additional Conjuration identities and 31 additional Divination identities; 658 unfinished.')
road.write_text(t,encoding='utf-8')
sp=G/'START_HERE.md'; t=sp.read_text(encoding='utf-8'); old='182 reviewed drafts; all 848 IDs and 936 placements preserved | 666 unfinished spell identities'; assert old in t
sp.write_text(t.replace(old,'190 reviewed drafts; all 848 IDs and 936 placements preserved | 658 unfinished spell identities'),encoding='utf-8')
rp=A/'REVIEW_STATUS.md'; t=rp.read_text(encoding='utf-8').replace('182 reviewed; 666 unfinished identities','190 reviewed; 658 unfinished identities')
anchor='Twelve rank-1 Divination cards are [approved](GPT_DIVINATION_RANK1_EXACT_REVIEW.md) after requiring Fate Coin to wait for the complete roll.'
assert anchor in t
t=t.replace(anchor,anchor+' Eight rank-two Divination cards are [approved](GPT_DIVINATION_RANK2_EXACT_REVIEW.md) with paid-information preflight repairs and the [Vision Trap timing clarification](GPT_DIVINATION_RANK2_FINAL_CLARIFICATION.md).',1)
t+='''

## Eight rank-two Divination spells completed

The [source conference](GPT_DIVINATION_RANK2_SOURCE_CONFERENCE.md), [exact manuscript review](GPT_DIVINATION_RANK2_EXACT_REVIEW.md) and [final timing clarification](GPT_DIVINATION_RANK2_FINAL_CLARIFICATION.md) approve eight cards. Locate Person, Faction Spy and Resonance Tracking resolve hidden eligibility only after paid casting, preventing free information from target checks. Vision Trap excludes the entire current target turn from its next-turn expiry, retaining the existing shared rule.

The cards define goal-relative Augury, actual divine provenance, fixed remote sight/hearing, a single person bearing, brief attack disorientation, useful voluntary-response forecasting and one-hour origin/path/endpoint spell traces. The catalog has 190 reviewed identities and 658 unfinished; 223 unfinished have an actual class rank 0–3. Eight placements/Core blocks and exact access rows are preserved. Broader systems, source variants, runtime, numerical balance and whole-game review remain open. No source information was deleted and GitHub was not pushed. [Status](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/DIVINATION_RANK2_REVIEW_STATUS.json) records validation scope.
'''
rp.write_text(t,encoding='utf-8')
cp=R/'data/playtest/game_development_coverage.json'; cov=read(cp)
scopes={
'DD-02':'Augury and Alignment Prediction have bounded current-circumstances forecasts without guaranteed die outcomes or forced behavior. Broader resolution/adjudication remains open.',
'DD-03':'Vision Trap keeps the shared next-turn endpoint, excluding the entire current target turn. Remote-feed suppression and trace age preserve their existing deadlines; no general scheduler/runtime closure.',
'DD-11':'Eight rank-two Divination identities retain all eight source placements/Core blocks and exact six-class rank/access. Catalog: 190 reviewed / 658 unfinished; variants remain separately open.',
'DD-12':'Eight exact rank-two Divination cards approved after paid-information preflight repairs and Vision Trap timing clarification. Runtime and numerical balance remain open.',
'DD-19':'Clairvoyance and Faction Spy have fixed-point sense, lighting, cover, Blindness/Deafened and protection procedures; no general perception-system closure.',
'DD-39':'Locate Person provides a paid instantaneous one-mile bearing; Resonance Tracking follows actual one-hour spell traces through ordinary movement, without fabricating paths or remote planar travel.',
'DD-49':'Faction Spy observes a specific known institutional HQ without reputation/member gates; same-plane feed, fixed room selection and later institutional relocation are bounded.',
'DD-53':'Goal-relative forecasts, actual divine provenance and deterministic trace selection have exact Director procedures; undefined/protected facts are not invented.',
'DD-54':'Locate Person, Faction Spy and Resonance Tracking defer hidden eligibility to paid effect resolution, preventing target-legality information leakage. Wider secrecy/data separation remains open.'
}
for a in cov['aspects']:
    if a['id'] not in scopes:continue
    for key,path in [('reviewEvidence',review),('reviewEvidence',final),('draftEvidence','DescentReviewChanges/ReviewBible/data/playtest/spell_drafts/batch_divination_rank2.json'),('validationEvidence','DescentReviewChanges/ReviewBible/docs/mechanics/DIVINATION_RANK2_REVIEW_STATUS.json')]:
        if path not in a[key]:a[key].append(path)
    a.setdefault('completedScopes',[]).append(scopes[a['id']])
    if a['id'] in ['DD-11','DD-12']:
        a['openIssues']=[s.replace('182 individual spell drafts reviewed;666 unfinished','190 individual spell drafts reviewed;658 unfinished') for s in a['openIssues']]
dump(cp,cov)
print(json.dumps({'promoted':8,'selected':sum(map(len,sel.values())),'batchSha256':sha(b),'reviewedFunctionalFieldRepairs':len(repairs),'pipeline':'pending'},indent=2))
