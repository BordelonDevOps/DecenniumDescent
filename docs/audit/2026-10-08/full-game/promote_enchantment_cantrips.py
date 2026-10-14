import json,hashlib
from pathlib import Path
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';D=R/'data/playtest/spell_drafts'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
review='docs/audit/2026-10-08/full-game/GPT_ENCHANTMENT_CANTRIP_EXACT_REVIEW.md'
assert 'After those changes, all twelve Enchantment cantrips may be promoted' in (G/review).read_text(encoding='utf-8')
p=D/'candidate_enchantment_cantrips.json';sub=read(A/'ENCHANTMENT_CANTRIP_EXACT_SUBMISSION.json')
assert sha(p)==sub['candidateSha256BeforeReview']
d=read(p);by={s['id']:s for s in d['spells']};ids=list(by);repairs=[]
def repair(id,field,old,new,reason):
    before=by[id][field];assert old in before
    after=before.replace(old,new);assert after!=before
    by[id][field]=after;repairs.append({'id':id,'field':field,'before':before,'after':after,'reason':reason})
repair('mental-tap','effect',
    'Finish this spell’s damage packet and its immediately due damage/concentration consequences before establishing the new benefit. It cannot change the target’s already-resolved initial INT save or a save already resolved as part of that damage sequence, even if you targeted yourself.',
    'After defenses and actual HP handling determine actualDamageDealt. If it is greater than zero, establish the +1 benefit immediately at that point. It cannot modify the target’s already-resolved initial Intelligence save or any saving throw that resolved before actualDamageDealt became known. A saving throw subsequently caused by that damage, including your own concentration save if you targeted yourself, can be the next qualifying save and may consume the benefit.',
    'Exact review: benefit begins as soon as positive numeric actual damage is established, before later qualifying concentration saves')
repair('mental-tap','designNotes',
    'Exact completion orders the new grant after this damage sequence, including immediate concentration consequences, rather than retroactively modifying the same packet.',
    'Exact-review timing repair establishes the benefit immediately when positive actualDamageDealt is known; a subsequently triggered concentration save can consume it, while already-resolved saves cannot change.',
    'Conform the timing explanation to the exact approved effect repair')
repair('soothe-animal','limitations',
    'Losing the qualifying Beast/animal classification ends the calm; the record does not follow a later return to that classification.',
    'The Beast/animal predicate is checked when the spell resolves. A later transformation or classification change does not by itself end an already-applied calm on the same continuing creature unless that transformation’s actual rules expressly end or suppress the effect.',
    'Exact review: target classification is an application gate, not an unprinted ongoing tether')
repair('soothe-animal','designNotes',
    'Exact completions place hidden classification after payment, distinguish positive damage packets from zero prevention, and end the effect on actual loss of the required classification.',
    'Exact completions place hidden classification after payment and distinguish positive damage packets from zero prevention. The exact-review repair keeps classification as an application-only predicate; later changes do not themselves dispel the calm.',
    'Conform the target-classification explanation to the approved limitation repair')
repair('beguiling-gaze','resolution',
    'While locked, it cannot voluntarily avert its primary gaze from you or voluntarily close/cover its visual organs to break or evade that gaze. In particular, it cannot evade an independently actual gaze rule by claiming that voluntary eye closure has a different intended benefit. Ordinary involuntary blinking or another actual involuntary loss of sight is not a compelled harmful action.',
    'While locked, the target cannot voluntarily avert its primary gaze from you or deliberately close, cover or otherwise block its relevant visual organs in a manner that would meaningfully break or evade the maintained gaze, regardless of the stated reason for doing so. Ordinary momentary blinking that does not meaningfully break mutual visual contact remains possible. An actual involuntary loss of sight or visual contact can end the lock normally.',
    'Exact review: objective meaningful-gaze-break rule permits ordinary blinking without an intent loophole')
existing={s['id']:s['operational'] for s in read(R/'data/public/spell_playtests/catalog.json')['spells'] if s['operational']}
assert len(existing)==198 and not set(ids).intersection(existing)
sub['previousOperationalSha256']=hashlib.sha256(json.dumps(existing,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
d['status']='PLAYTEST — REVIEWED / MANUSCRIPT-APPROVED after three exact repairs; runtime/balance pending'
d['reviewEvidence'].append(review)
for s in d['spells']:
    s['implementationStatus']='REVIEWED authored operational PLAYTEST manuscript; runtime, human balance and broader Enchantment/social-control integration pending'
    s['sourceReview'].append(review);s['reviewEvidence']=[review]
dump(p,d)
b=D/'batch_enchantment_cantrips.json';assert not b.exists();b.write_bytes(p.read_bytes())
sel=read(D/'selected_sources.json');assert sum(map(len,sel.values()))==198
assert not set(ids).intersection(i for v in sel.values() for i in v)
sel['Enchantment'].extend(ids);dump(D/'selected_sources.json',sel)
sub.update({'status':'three exact repairs and corresponding design explanations applied; promoted; pipeline pending','reviewEvidence':review,'requiredRepairsApplied':repairs,'changesLimitedToReviewedRepairs':True,'candidateSha256AfterPromotion':sha(p),'batchSha256':sha(b),'operationalAfter':210,'unfinishedAfter':638})
dump(A/'ENCHANTMENT_CANTRIP_EXACT_SUBMISSION.json',sub)
conf=read(A/'ENCHANTMENT_CANTRIP_CONFERENCE_SUBMISSION.json');conf.update({'status':'source conference and exact review complete; three repairs applied; promoted','exactReviewEvidence':review});dump(A/'ENCHANTMENT_CANTRIP_CONFERENCE_SUBMISSION.json',conf)
status={'status':'REVIEWED / MANUSCRIPT-APPROVED; three repairs applied; promoted','ids':ids,'count':12,'sourcePlacements':12,'sourceCoreBlocks':12,'reviewEvidence':review,'candidatePath':p.relative_to(R).as_posix(),'candidateSha256':sha(p),'promotedBatchPath':b.relative_to(R).as_posix(),'promotedBatchSha256':sha(b),'submittedCandidateSha256':sub['candidateSha256BeforeReview'],'requiredRepairsApplied':[{'id':x['id'],'field':x['field'],'reason':x['reason']} for x in repairs],'operationalCatalogCount':210,'unfinishedIdentityCount':638,'pipelineValidation':'pending rebuild and validation','runtimeImplemented':False,'balanceValidated':False,'wholeGameClosed':False,'githubPushed':False,'openBalanceQuestions':['Disrupt Memory retains source cantrip concentration ending, including actual linked/tethered class exceptions; strong low-cost disruption requires human balance testing.','Social modifier overlaps, pacification and independent gaze-effect combinations require adventure and table validation.','Memory recall, information protections and multi-concentration ending callbacks are authored interfaces, not completed runtime integrations.']}
dump(R/'docs/mechanics/ENCHANTMENT_CANTRIP_REVIEW_STATUS.json',status)
vp=R/'tools/validate_spell_playtests.py';t=vp.read_text(encoding='utf-8')
for old,new in [('All198 individually reviewed selected IDs','All210 individually reviewed selected IDs'),('len(set(selected))==198','len(set(selected))==210'),('Remaining650 explicitly blocked','Remaining638 explicitly blocked'),('for s in spells.values())==650','for s in spells.values())==638')]:
    assert old in t;t=t.replace(old,new)
vp.write_text(t,encoding='utf-8')
rules=R/'docs/mechanics/SPELL_INTEGRATION_RULES.md';t=rules.read_text(encoding='utf-8')
t+='''

## Enchantment cantrips: memory, concentration and bounded influence

The [exact Enchantment-cantrip review](../../../../docs/audit/2026-10-08/full-game/GPT_ENCHANTMENT_CANTRIP_EXACT_REVIEW.md) approves twelve cards after three repairs. [Review status](ENCHANTMENT_CANTRIP_REVIEW_STATUS.json) records the manuscript scope and open runtime/balance work.

**Disrupt Memory** removes the target's own episodic recall of the six elapsed seconds immediately before resolution after a failed WIS save. It does not undo world events, resource histories, mechanical choices, physical records or other observers' memories. It ends all actual Concentration the target personally maintains, including both spells in reviewed Wizard Spell Tether, both Crimson Harmony Veinweaves, and Wizard Tethered Cast's separately sustained concentration spell. The current reviewed class cards govern those interactions; older historical wording is preserved as evidence. Unrelated non-concentration sustained effects are unaffected. Memory-only immunity does not automatically prevent the independently applicable concentration ending.

**Mental Tap** establishes its next-save +1 immediately when defenses and HP handling establish positive numeric actualDamageDealt (temp HP absorbed plus ordinary HP lost, excluding overkill). A subsequent concentration save caused by that damage may consume it, including on self-targeting; an already-resolved initial INT save cannot change. **Soothe Animal** checks actual Beast/animal eligibility at application, not continuously; later transformation on the same creature does not automatically dispel calm. Its harm-ending rule still applies on another creature's hostile commitment or a positive resolved damage packet. **Beguiling Gaze** prevents voluntary meaningful aversion/eye blocking while permitting ordinary momentary blinking; it grants no gaze attack or facing engine and does not prevent ordinary movement out of range.

False Comfort and Enthralling Tune modify actual Perception checks without an invented passive -5. Friends is a caster-side Charisma benefit, not Charmed. Faction Sympathy retains its printed concentration and F component, actual affiliation and recognized-harm ending. Alignment Empathy snapshots orientation without changing/disclosing canonical axes. Resonance Whisper uses the reviewed actual-task bridge: failed target WIS save applies Disturb; successful save leaves an existing valid Whisper intact. Minor Suggestion supplies a harmless salient option and one social-check benefit without commanding action. These rules do not certify full social-control, memory or concentration runtime, numerical balance or broader-system closure.
'''
rules.write_text(t,encoding='utf-8')
road=R/'docs/mechanics/DEVELOPMENT_ROADMAP.md';t=road.read_text(encoding='utf-8');i=t.index('**Current conference:**');j=t.index('\n\n',i)
t=t[:i]+"""**Current conference:** twelve Enchantment cantrips are [jointly manuscript-approved after three exact repairs](../../../../docs/audit/2026-10-08/full-game/GPT_ENCHANTMENT_CANTRIP_EXACT_REVIEW.md). Memory/concentration, distraction, social bonuses, pacification, harmless ideas and gaze lock now have exact procedures. [Review status](ENCHANTMENT_CANTRIP_REVIEW_STATUS.json) records preserved sources/access and open runtime/balance. Previous approvals retain their bounded scopes; 327 feats remain unfinished. The [spell index](SPELL_PLAYTEST_STARTER.md) has 210 reviewed drafts and 638 unfinished identities, preserving all 848 IDs and 936 placements. Enchantment cantrip identities and all currently unfinished Abjuration, Conjuration and Divination identities through rank 3 are authored. Continue ranked Enchantment and other low-rank schools; higher ranks, [unassigned variants](SPELL_VARIANT_REVIEW_STATUS.json), broader systems, runtime, human balance and whole-game closure remain open."""+t[j:]
t=t.replace('215 unfinished identities','203 unfinished identities').replace('198 individual drafts reviewed, including 72 starters, 6 healing/death additions, 5 transformation/buffer spells, 37 additional Abjuration identities, 39 additional Conjuration identities and 39 additional Divination identities; 650 unfinished.','210 individual drafts reviewed, including 72 starters, 6 healing/death additions, 5 transformation/buffer spells, 37 additional Abjuration identities, 39 additional Conjuration identities, 39 additional Divination identities and 12 additional Enchantment identities; 638 unfinished.')
road.write_text(t,encoding='utf-8')
sp=G/'START_HERE.md';t=sp.read_text(encoding='utf-8');old='198 reviewed drafts; all 848 IDs and 936 placements preserved | 650 unfinished spell identities';assert old in t
sp.write_text(t.replace(old,'210 reviewed drafts; all 848 IDs and 936 placements preserved | 638 unfinished spell identities'),encoding='utf-8')
rp=A/'REVIEW_STATUS.md';t=rp.read_text(encoding='utf-8').replace('198 reviewed; 650 unfinished identities','210 reviewed; 638 unfinished identities')
anchor='Eight rank-three Divination cards are [approved exactly as submitted](GPT_DIVINATION_RANK3_EXACT_REVIEW.md), including Future Echo and both Speak with Dead placements.';assert anchor in t
t=t.replace(anchor,anchor+' Twelve Enchantment cantrips are [approved after three repairs](GPT_ENCHANTMENT_CANTRIP_EXACT_REVIEW.md), including exact class concentration interactions.',1)
t+='''

## Twelve Enchantment cantrips completed

The [source conference](GPT_ENCHANTMENT_CANTRIP_SOURCE_CONFERENCE.md) and [exact review](GPT_ENCHANTMENT_CANTRIP_EXACT_REVIEW.md) approve twelve cards after Mental Tap timing, Soothe Animal application-only eligibility and Beguiling Gaze blinking repairs. Disrupt Memory's all-maintained-concentration scope explicitly includes current Spell Tether, Tethered Cast and Crimson Harmony. Source and reviewed class files remain unchanged.

The catalog now has 210 reviewed identities and 638 unfinished; 203 unfinished have an actual class rank 0–3. All twelve source placements/Core blocks and exact access are retained. Enchantment cantrip identities are authored; ranked spells, broader social/control/concentration integration, source variants, runtime and human balance remain open. [Status](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/ENCHANTMENT_CANTRIP_REVIEW_STATUS.json) records verification scope. No source was deleted and GitHub was not pushed.

The parallel [placement/access audit at 198 reviewed identities](SPELL_PLACEMENT_ACCESS_AUDIT_198.json) accounts for all 936 placements: 906 match actual class school/rank access and 30 do not, including six attached to operational identities at that snapshot. The [variant register](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_VARIANT_REVIEW_STATUS.json) retains that inventory alongside prior curated decisions. This structural finding grants or retires nothing; prior substantive dispositions still require review.
'''
rp.write_text(t,encoding='utf-8')
cp=R/'data/playtest/game_development_coverage.json';cov=read(cp)
scopes={
'DD-02':'Mental Tap distinguishes numeric damage dealt from positive damage packets and establishes its next-save benefit immediately after positive HP/temp-HP settlement; broader damage integration remains open.',
'DD-03':'Disrupt Memory keeps real mechanical histories and budgets; exact next-turn and minute clocks remain fixed. Gaze and soft influence grant no whole-Action denial.',
'DD-11':'Twelve Enchantment cantrip identities retain all twelve placements/Core blocks and exact class access;210 reviewed/638 unfinished. No source variant is silently granted.',
'DD-12':'Twelve Enchantment cantrips approved after three exact repairs; no unfinished Enchantment cantrip identity remains. Ranked spells, variants, runtime and numerical balance remain open.',
'DD-19':'False Comfort/Enthralling Tune modify actual Perception checks without passive -5; Beguiling Gaze permits ordinary blinking and creates no universal facing engine.',
'DD-49':'Faction Sympathy uses actual affiliation, initial membership snapshot and target-recognized faction harm without granting numeric standing, membership or rights.',
'DD-53':'Friends and Minor Suggestion defer hidden eligibility to paid resolution; limited social benefits retain task legality and agency. Memory loss changes recall, not world history.',
'DD-54':'Disrupt Memory preserves other observers/records and actual spent-state histories; hidden language/hostility/harmlessness checks are not free preflight oracles. Broader data separation remains open.'
}
for a in cov['aspects']:
    if a['id'] not in scopes:continue
    for key,path in [('reviewEvidence',review),('draftEvidence','DescentReviewChanges/ReviewBible/data/playtest/spell_drafts/batch_enchantment_cantrips.json'),('validationEvidence','DescentReviewChanges/ReviewBible/docs/mechanics/ENCHANTMENT_CANTRIP_REVIEW_STATUS.json')]:
        if path not in a[key]:a[key].append(path)
    a.setdefault('completedScopes',[]).append(scopes[a['id']])
    if a['id'] in ['DD-11','DD-12']:a['openIssues']=[s.replace('198 individual spell drafts reviewed;650 unfinished','210 individual spell drafts reviewed;638 unfinished') for s in a['openIssues']]
    if a['id']=='DD-12':a['openIssues'].append('Human-balance question: Disrupt Memory retains cantrip all-maintained-concentration ending, including actual class-linked exceptions. No unreviewed weakening was applied to hide that source power.')
dump(cp,cov)
print(json.dumps({'promoted':12,'selected':sum(map(len,sel.values())),'batchSha256':sha(b),'reviewedFunctionalFieldRepairs':len(repairs),'pipeline':'pending'},indent=2))
