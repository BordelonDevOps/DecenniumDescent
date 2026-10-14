import json,hashlib
from pathlib import Path
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';D=R/'data/playtest/spell_drafts'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
review='docs/audit/2026-10-08/full-game/GPT_ENCHANTMENT_RANK1_EXACT_REVIEW.md'
rt=(G/review).read_text(encoding='utf-8')
assert 'No functional text repairs are required' in rt
sub=read(A/'ENCHANTMENT_RANK1_EXACT_SUBMISSION.json');p=D/'candidate_enchantment_rank1.json';b=D/'batch_enchantment_rank1.json'
assert sha(p)==sub['candidateSha256BeforeReview']=='212687265c7f5de5653ad10d728512f0bf234f1c7c3e18a8a2668224d851687c'
assert not b.exists()
d=read(p);ids=[s['id'] for s in d['spells']];assert len(ids)==12
cat=read(R/'data/public/spell_playtests/catalog.json')['spells']
existing={s['id']:s['operational'] for s in cat if s['operational']}
assert len(existing)==210 and not set(ids).intersection(existing)
assert hashlib.sha256(json.dumps(existing,sort_keys=True,ensure_ascii=False).encode()).hexdigest()==sub['previousOperationalSha256']
d['status']='PLAYTEST — REVIEWED / MANUSCRIPT-APPROVED exactly as submitted; runtime/balance pending'
d['reviewEvidence']=[review]
for s in d['spells']:
 s['implementationStatus']='REVIEWED authored operational PLAYTEST manuscript; runtime, human balance and broader Enchantment/social-control integration pending'
 s['sourceReview'].append(review);s['reviewEvidence']=[review]
dump(p,d);b.write_bytes(p.read_bytes())
sel=read(D/'selected_sources.json');assert sum(map(len,sel.values()))==210
assert not set(ids).intersection(i for v in sel.values() for i in v)
sel['Enchantment'].extend(ids);dump(D/'selected_sources.json',sel)
sub.update(status='approved exactly as submitted; promoted; pipeline pending',reviewEvidence=review,reviewTurnId='c3d6ad40-d199-4f8b-9a3c-3d2e03fd12a3',requiredRepairsApplied=[],changesLimitedToReviewedRepairs=True,candidateSha256AfterPromotion=sha(p),batchSha256=sha(b),operationalAfter=222,unfinishedAfter=626)
dump(A/'ENCHANTMENT_RANK1_EXACT_SUBMISSION.json',sub)
cp=A/'ENCHANTMENT_RANK1_CONFERENCE_SUBMISSION.json';conf=read(cp);conf.update(status='source conference and exact review complete; promoted without functional repairs',exactReviewEvidence=review);dump(cp,conf)
sp=R/'docs/mechanics/ENCHANTMENT_RANK1_REVIEW_STATUS.json';st=read(sp)
st.update(status='REVIEWED / MANUSCRIPT-APPROVED exactly as submitted; promoted',exactManuscriptApproved=True,promoted=True,reviewEvidence=review,candidateSha256=sha(p),promotedBatchPath=b.relative_to(R).as_posix(),promotedBatchSha256=sha(b),submittedCandidateSha256=sub['candidateSha256BeforeReview'],requiredRepairsApplied=[],operationalCatalogCount=222,unfinishedIdentityCount=626,pipelineValidation='pending rebuild and validation',openBalanceQuestions=['Sleep no-save fixed24HP Unconscious, Mesmerize Stunned/unaware, reaction Distract cancellation, Command vocabulary and sustained Hideous Laughter need human table tests.','Canonical alignment overlays, overlapping social affinities and final RP-price modifiers are authored interfaces; runtime integration and numerical balance remain open.','Enthrall Enchantment rank2/Core349 remains preserved, unassigned and not selectable.'])
dump(sp,st)
vp=R/'tools/validate_spell_playtests.py';t=vp.read_text(encoding='utf-8')
for old,new in [('All210 individually reviewed selected IDs','All222 individually reviewed selected IDs'),('len(set(selected))==210','len(set(selected))==222'),('Remaining638 explicitly blocked','Remaining626 explicitly blocked'),("for s in spells.values())==638","for s in spells.values())==626")]:
 assert old in t;t=t.replace(old,new)
vp.write_text(t,encoding='utf-8')
p=R/'docs/mechanics/SPELL_INTEGRATION_RULES.md';t=p.read_text(encoding='utf-8')
t+="""

## Rank-one Enchantment: compulsion, alignment and final spell pricing

The [exact rank-one Enchantment review](../../../../docs/audit/2026-10-08/full-game/GPT_ENCHANTMENT_RANK1_EXACT_REVIEW.md) approves twelve cards without functional repairs. [Review status](ENCHANTMENT_RANK1_REVIEW_STATUS.json) records the manuscript scope and open runtime/balance work.

Mesmerize's Stunned package and unaware rider remain distinct. Sleep retains its no-save, ordered fixed24-current-HP budget; an attempted immune/guard-blocked target still spends its cost. A helper's physical rousing Action ends all ordinary Sleep applications on that creature, while unrelated Unconscious causes remain. Positive post-defense/pre-temp-HP damage wakes without undoing an already determined hit/critical. Confusing Flash and Command use actual existing Action/movement/interaction permissions, not added budgets, and replace their own pending same-spell applications rather than banking them. Their actual whole-Action components claim the shared source-character/target/encounter allowance when established; a blocked component receives no invented fallback.

Distract cancels a pending Action only after its commitment/beginning hooks and before its first main outcome, subject to its INT save and shared hard guard. Its independent opportunity-attack restriction ends with the current numbered round. If a nested effect already canceled the formerly valid parent, Distract cancels nothing and claims no hard allowance for that nonexistent cancellation. Costs/attempt history persist; Counterspell keeps its own reviewed scope. Hideous Laughter separately applies immediate Prone and maintained Incapacitated. Its repeat save occurs at every affected regular-turn END, including the current regular turn when affected; this is not its maximum-duration clock. Initially prevented hard control does not wait to activate later.

Pacify restricts voluntary attacks and selected damaging spell modes without a harm-ending clause. Voice of Peace snapshots its protected participating allies at application; actual recognition of the target's allies is checked when provocation occurs. Faction Charm keeps independent caster/target/faction affinity records, without stacked advantage or compelled allegiance. Enthrall affects all actual Perception checks of its up-to-three targets. Its separate Enchantment rank2/Core349 source remains preserved/unassigned, not an upcast or extra grant.

**Alignment Suggestion:** calculate each new one-step shift with all prior same-spell overlays ignored, retaining independent actual alignment changes. Only changed defined axes receive fixed overlay values. A no-change result creates no replacement; the caster's already-required concentration transition still occurs and never resurrects an old application. A valid changed-axis application replaces the previous same-spell application; replaced concentration maintains no remaining effect. Ending exposes the then-current underlying alignment, not a historical snapshot. No conduct, belief or oathbreaking is compelled.

**Resonance Influence:** compute ordinary legal spell price first, including mandatory extras, Dissonance, eligible source reductions/waivers and each feature's own minimum. Then apply final plus/minus1, minimum0. A feature's minimum1 reduction step is not a universal final-price floor. Ease can offset one RP of the resulting total, including a mandatory Resonance Shield extra. A genuine RP-priced spell reduced/waived to0 still qualifies; Burden makes it1. In Mage Spell Sharing, the Mage's earlier sharing payment is unchanged, while the ally's later actual shared spell is independently priced: Ease0/Burden1. An ally unable to pay cannot commit, leaves Influence pending, and still uses the original limited sharing window. Nonspell techniques and charge-only spells without an RP-price interface do not qualify merely because they have costs. Qualifying class discounts require their actual class/spell eligibility; examples do not reclassify nonspell techniques. No runtime implementation or numerical balance is certified by this manuscript ruling.
"""
p.write_text(t,encoding='utf-8')
p=R/'docs/mechanics/DEVELOPMENT_ROADMAP.md';t=p.read_text(encoding='utf-8');i=t.index('**Current conference:**');j=t.index('\n\n',i)
t=t[:i]+"""**Current conference:** twelve rank-one Enchantment identities are [jointly manuscript-approved exactly as submitted](../../../../docs/audit/2026-10-08/full-game/GPT_ENCHANTMENT_RANK1_EXACT_REVIEW.md). Exact compulsion, independent condition components, ceasefires, faction affinity, canonical alignment overlays and final RP-price modification are authored. [Review status](ENCHANTMENT_RANK1_REVIEW_STATUS.json) records preserved sources/access and open runtime/balance. Previous approvals retain their bounded scopes; 327 feats remain unfinished. The [spell index](SPELL_PLAYTEST_STARTER.md) has 222 reviewed drafts and 626 unfinished identities, preserving all 848 IDs and 936 placements. All currently unfinished Enchantment identities through rank1 and Abjuration, Conjuration and Divination identities through rank3 are authored. Continue rank-two Enchantment and other low-rank schools; higher ranks, [unassigned variants](SPELL_VARIANT_REVIEW_STATUS.json), broader systems, runtime, human balance and whole-game closure remain open."""+t[j:]
t=t.replace('203 unfinished identities','191 unfinished identities')
t=t.replace('210 individual drafts reviewed, including 72 starters, 6 healing/death additions, 5 transformation/buffer spells, 37 additional Abjuration identities, 39 additional Conjuration identities, 39 additional Divination identities and 12 additional Enchantment identities; 638 unfinished.','222 individual drafts reviewed, including 72 starters, 6 healing/death additions, 5 transformation/buffer spells, 37 additional Abjuration identities, 39 additional Conjuration identities, 39 additional Divination identities and 24 additional Enchantment identities; 626 unfinished.')
p.write_text(t,encoding='utf-8')
p=G/'START_HERE.md';t=p.read_text(encoding='utf-8');old='210 reviewed drafts; all 848 IDs and 936 placements preserved | 638 unfinished spell identities';assert old in t;p.write_text(t.replace(old,'222 reviewed drafts; all 848 IDs and 936 placements preserved | 626 unfinished spell identities'),encoding='utf-8')
p=A/'REVIEW_STATUS.md';t=p.read_text(encoding='utf-8').replace('210 reviewed; 638 unfinished identities','222 reviewed; 626 unfinished identities')
t+="""

## Twelve rank-one Enchantment identities completed

The [source conference](GPT_ENCHANTMENT_RANK1_SOURCE_CONFERENCE.md) and [exact review](GPT_ENCHANTMENT_RANK1_EXACT_REVIEW.md) approve all twelve cards without functional repairs. Alignment Suggestion ignores prior same-spell overlays when computing a new step, preserving independent underlying changes. Resonance Influence applies its final price adjustment after actual source reductions/waivers, including the ally's later Mage Spell Sharing cast; existing class records remain unchanged.

The catalog now has 222 reviewed identities and 626 unfinished; 191 unfinished have some actual class rank0–3. All thirteen source placements/Core blocks and exact access are retained. The Enchantment rank2 Enthrall source remains unassigned and not selectable. All 848 identities and 936 placements remain. [Status](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/ENCHANTMENT_RANK1_REVIEW_STATUS.json) records verification scope. Human balance, effect runtime, broader systems and whole-game closure remain open. No source was deleted and GitHub was not pushed.
"""
p.write_text(t,encoding='utf-8')
p=R/'data/playtest/game_development_coverage.json';cov=read(p)
scopes={
'DD-02':'Sleep and Hideous Laughter use positive post-defense/pre-temp-HP packets for waking/ending, preserving already determined hit/critical outcomes and unrelated Unconscious causes.',
'DD-03':'Rank-one Enchantment compulsion/cancellation uses existing action budgets and combined hard-denial history; pending commands do not bank extra Actions. Distract retains actual committed costs and LIFO interruption.',
'DD-11':'Twelve Enchantment rank-one identities retain all thirteen placements/Core blocks and actual class access;222 reviewed/626 unfinished. Enthrall rank2 remains unassigned, not an upcast or class grant.',
'DD-12':'Twelve rank-one Enchantment cards approved exactly; canonical alignment anti-ratcheting and final RP-price order explicitly resolved. Higher ranks, variants, runtime and numerical balance remain open.',
'DD-19':'Mesmerize unaware remains separate from Stunned; Enthrall modifies actual Perception without invented passive penalties, Hidden or automatic awareness deletion.',
'DD-49':'Faction Charm preserves one-hour affinity with independent caster/target/faction records and recognized-harm ending; no membership, standing or compelled allegiance.',
'DD-53':'Voice of Peace snapshots participating allies; Command supplies bounded actual compulsion using existing permissions, preserving source limits and target detail choices.',
'DD-54':'Hidden eligibility remains paid resolution without an oracle; alignment overlays do not disclose underlying axes, and unknown affiliation does not secretly trigger faction harm ending.'
}
for a in cov['aspects']:
 if a['id'] not in scopes:continue
 for key,path in [('reviewEvidence',review),('draftEvidence','DescentReviewChanges/ReviewBible/data/playtest/spell_drafts/batch_enchantment_rank1.json'),('validationEvidence','DescentReviewChanges/ReviewBible/docs/mechanics/ENCHANTMENT_RANK1_REVIEW_STATUS.json')]:
  if path not in a[key]:a[key].append(path)
 a.setdefault('completedScopes',[]).append(scopes[a['id']])
 if a['id'] in ['DD-11','DD-12']:a['openIssues']=[s.replace('210 individual spell drafts reviewed;638 unfinished','222 individual spell drafts reviewed;626 unfinished') for s in a['openIssues']]
 if a['id']=='DD-12':a['openIssues'].append('Human-balance questions remain for fixed24HP no-save Sleep, Mesmerize, reaction Distract, Command, Hideous Laughter, canonical alignment overlays and final RP-price manipulation; no runtime execution is certified.')
dump(p,cov)
print(json.dumps({'promoted':12,'selected':sum(map(len,sel.values())),'batchSha256':sha(b),'functionalRepairs':0,'pipeline':'pending'},indent=2))

