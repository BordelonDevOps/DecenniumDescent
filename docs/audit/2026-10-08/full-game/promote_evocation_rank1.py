from pathlib import Path
import json,hashlib
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';D=R/'data/playtest/spell_drafts'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
compact=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':'),sort_keys=True)
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

review='docs/audit/2026-10-08/full-game/GPT_EVOCATION_RANK1_EXACT_REVIEW.md'
rt=(G/review).read_text(encoding='utf-8')
assert 'APPROVE all twelve cards' in rt and 'No functional replacement text is required' in rt and 'provisional manuscript promotion' in rt
sub=read(A/'EVOCATION_RANK1_EXACT_SUBMISSION.json');p=D/'candidate_evocation_rank1.json';b=D/'batch_evocation_rank1.json'
assert not b.exists() and sha(p)==sub['candidateSha256BeforeReview']
assert len(sub['dispatch']['attachments'])==4 and all(x['matchesPreparedApartFromFinalWhitespace'] for x in sub['dispatch']['attachments'])
cat=read(R/'data/public/spell_playtests/catalog.json')['spells'];prior={s['id']:s['operational'] for s in cat if s['operational']}
assert len(prior)==249 and hashlib.sha256(compact(prior).encode()).hexdigest()==sub['previousOperationalSha256']
assert all(sha(R/k)==v for k,v in sub['frozenSourceAndClassFiles'].items())
d=read(p);ids=[s['id'] for s in d['spells']];assert ids==sub['ids'] and len(ids)==12 and not set(ids).intersection(prior)
sel=read(D/'selected_sources.json');assert sum(map(len,sel.values()))==249 and not set(ids).intersection(i for v in sel.values() for i in v)
validator=R/'tools/validate_spell_playtests.py';vt=validator.read_text(encoding='utf-8')
replacements=[('All249 individually reviewed selected IDs','All261 individually reviewed selected IDs'),('len(set(selected))==249','len(set(selected))==261'),('Remaining599 explicitly blocked','Remaining587 explicitly blocked'),('for s in spells.values())==599','for s in spells.values())==587')]
for old,new in replacements:
 assert old in vt,old
 vt=vt.replace(old,new)

d.update(status='PLAYTEST — REVIEWED / MANUSCRIPT-APPROVED; no functional repairs; runtime/balance pending',reviewEvidence=[review])
for s in d['spells']:
 s['implementationStatus']='REVIEWED authored operational PLAYTEST manuscript; runtime, human balance and broader integration pending'
 s['sourceReview'].append(review);s['reviewEvidence']=[review]
dump(p,d);b.write_bytes(p.read_bytes());sel['Evocation'].extend(ids);dump(D/'selected_sources.json',sel)
dump(A/'EVOCATION_RANK1_EXACT_REPAIR_LOG.json',{'status':'No functional replacements required; approved candidate mechanics retained exactly','authority':review,'changes':[]})
sub.update(status='approved and promoted; rebuild/preservation verification pending',reviewEvidence=review,reviewTurnId=sub['dispatch']['turnId'],reviewSha256=sha(G/review),requiredRepairsApplied=[],candidateSha256AfterPromotion=sha(p),batchSha256=sha(b),operationalAfter=261,unfinishedAfter=587);dump(A/'EVOCATION_RANK1_EXACT_SUBMISSION.json',sub)
cp=A/'EVOCATION_RANK1_CONFERENCE_SUBMISSION.json';c=read(cp);c.update(status='source conference, authoring/eligibility clarifications and exact review complete; promoted without functional repairs',exactReviewEvidence=review);dump(cp,c)
sp=R/'docs/mechanics/EVOCATION_RANK1_REVIEW_STATUS.json';s=read(sp);s.update(status='REVIEWED / MANUSCRIPT-APPROVED; promoted; no functional repairs',exactManuscriptApproved=True,promoted=True,reviewEvidence=review,reviewTurnId=sub['reviewTurnId'],candidateSha256=sha(p),submittedCandidateSha256=sub['candidateSha256BeforeReview'],promotedBatchPath=b.relative_to(R).as_posix(),promotedBatchSha256=sha(b),requiredRepairsApplied=[],operationalCatalogCount=261,unfinishedIdentityCount=587,pipelineValidation='pending rebuild and validation',nextWork='Complete preservation verification, then continue eight rank-two Evocation source identities.')
s['authoringAttention']=[v.replace('Clarification phrase equivalent defensive protective effect must be compared against firstconference explicitward/barrierrequirement; do not classify by substring. Ten comparisoncards preserved for this unresolved exact-authoring question.','The twelve-identity eligibility conference and exact review resolve the semantic protective-layer predicate; no substring classification or generic defensive-buff eligibility.') for v in s['authoringAttention']]
dump(sp,s);validator.write_text(vt,encoding='utf-8')

p=R/'docs/mechanics/SPELL_INTEGRATION_RULES.md';t=p.read_text(encoding='utf-8');t+='''

## Rank-one Evocation attacks and maintained effects

Twelve rank-one Evocation identities have [exact manuscript approval](../../../../docs/audit/2026-10-08/full-game/GPT_EVOCATION_RANK1_EXACT_REVIEW.md), preserving thirteen placements/Core blocks and actual class access. Their complete procedures are in [the spell reference](SPELL_PLAYTEST_STARTER.md); the existing spell cards remain unchanged.

Magic Missile Storm fixes three separately resolved missiles at commitment. Its card expressly applies ordinary Shield's named Magic Missile exception, with one targeting opportunity per recipient before that recipient's first missile damage. This does not alias Mage Arcane Missile. Arcane Shield Shatter requires an individually perceived rank-0/1 spell protective layer and a protected creature, with exact source-qualified eligibility. Its current Resonance Shield grant and whole Protective Sphere procedures prevent stripping unrelated temporary HP or inventing a hole in a boundary.

Witch Bolt's maintenance uses an ordinary Action to activate its existing effect. It is not another cast. Its pulse-use history survives initiative changes while preserving the Action for other uses when a pulse was already spent. Zephyr Strike grants no attack at casting; its first weapon-hit rider and continuing movement protection have separate consumption rules. Ignition Bolt and Ice Knife retain their short source ranges and captured impact positions; only attack damage dice critically double. Earth Tremor creates finite magical difficult terrain on one contiguous supporting surface. See [review status](EVOCATION_RANK1_REVIEW_STATUS.json) for the remaining runtime and human-balance questions.
''';p.write_text(t,encoding='utf-8')
p=R/'docs/mechanics/DEVELOPMENT_ROADMAP.md';t=p.read_text(encoding='utf-8');i=t.index('**Current conference:**');j=t.index('\n\n',i)
t=t[:i]+'''**Current conference:** twelve rank-one Evocation cards are [jointly manuscript-approved](../../../../docs/audit/2026-10-08/full-game/GPT_EVOCATION_RANK1_EXACT_REVIEW.md) without functional repairs. The [review status](EVOCATION_RANK1_REVIEW_STATUS.json) records source preservation and open runtime/balance questions. The Shield interaction, Shatter eligibility, individual missile packets, burst geometry, maintained Witch Bolt pulses and Zephyr Strike consumption now have explicit procedures. The [spell index](SPELL_PLAYTEST_STARTER.md) has 261 reviewed drafts and 587 unfinished identities, retaining all 848 IDs and 936 placements. Continue eight rank-two Evocation sources, then rank three, the remaining low-rank schools and higher ranks. Completed earlier spell batches remain intact; unassigned variants, broader systems, 327 unfinished feats, runtime, human balance and whole-game closure remain open.'''+t[j:]
t=t.replace('164 unfinished identities','152 unfinished identities')
old='249 individual drafts reviewed, including 72 starters, 6 healing/death additions, 5 transformation/buffer spells, 37 additional Abjuration identities, 39 additional Conjuration identities, 39 additional Divination identities, 39 additional Enchantment identities and 12 additional Evocation cantrips; 599 unfinished.'
assert old in t;t=t.replace(old,'261 individual drafts reviewed, including 72 starters, 6 healing/death additions, 5 transformation/buffer spells, 37 additional Abjuration identities, 39 additional Conjuration identities, 39 additional Divination identities, 39 additional Enchantment identities and 24 additional Evocation identities through rank one; 587 unfinished.');p.write_text(t,encoding='utf-8')
p=G/'START_HERE.md';t=p.read_text(encoding='utf-8');old='249 reviewed drafts; all 848 IDs and 936 placements preserved | 599 unfinished spell identities';assert old in t;t=t.replace(old,'261 reviewed drafts; all 848 IDs and 936 placements preserved | 587 unfinished spell identities')
i=t.index('The latest completed manuscript work is ');j=t.index('\n\n',i)
t=t[:i]+'''The latest completed manuscript work is [twelve rank-one Evocation cards](DescentReviewChanges/ReviewBible/docs/mechanics/EVOCATION_RANK1_REVIEW_STATUS.json), jointly approved without functional repairs. They resolve Shield and Arcane Shield Shatter interactions, separate missile and burst damage, and define maintained Witch Bolt and Zephyr Strike effects. Source preservation and catalog integration are being verified. The [development roadmap](DescentReviewChanges/ReviewBible/docs/mechanics/DEVELOPMENT_ROADMAP.md) moves next to eight rank-two Evocation sources; the pending Time Loop work below remains a separate integration track.'''+t[j:];p.write_text(t,encoding='utf-8')
p=A/'REVIEW_STATUS.md';t=p.read_text(encoding='utf-8').replace('| Ordinary spells | 249 reviewed; 599 unfinished identities;','| Ordinary spells | 261 reviewed; 587 unfinished identities;');t+='''

## Twelve rank-one Evocation cards completed

The [source conference](GPT_EVOCATION_RANK1_SOURCE_CONFERENCE.md), [authoring clarification](GPT_EVOCATION_RANK1_AUTHORING_CLARIFICATION.md), [Shatter eligibility conference](GPT_ARCANE_SHIELD_SHATTER_ELIGIBILITY_CONFERENCE.md) and [exact review](GPT_EVOCATION_RANK1_EXACT_REVIEW.md) approve all twelve full cards and their shared wording without functional repairs. All four delivered review parts match their prepared manuscripts. The thirteen original placements/Core blocks and every actual class-access row are retained.

Magic Missile Storm has an explicit ordinary Shield bridge without merging class features. Arcane Shield Shatter has source-qualified protective-layer eligibility and source-owned cleanup. Short-range bursts, independent Prone/push riders, finite Earth Tremor terrain, Witch Bolt maintenance and Zephyr Strike consumption are explicit. The catalog now has 261 reviewed identities and 587 unfinished; 152 unfinished identities have actual class rank 0–3. All 848 identities and 936 placements remain. Runtime, human balance, source variants and whole-game closure remain open. No source was deleted or GitHub pushed. Cosmology remains deferred until after successful authorized push and remote commit verification.
''';p.write_text(t,encoding='utf-8')
p=R/'data/playtest/game_development_coverage.json';c=read(p)
scopes={
 'DD-03':'Rank-one Evocation exact-approved: fixed multi-attack order, named Shield opportunity, existing-effect Witch Bolt activation and preserved pulse-use history; source-owned Zephyr consumption. Runtime remains open.',
 'DD-11':'Twelve rank-one identities preserve thirteen placements/Core blocks and exact access, including both Chromatic Orb schools; no class-feature alias created by the ordinary Shield interaction.',
 'DD-12':'Twelve rank-one Evocation manuscripts approved without repairs;261 reviewed/587 unfinished,152 with actual rank0–3. Eight rank-two sources are next.',
 'DD-17':'Separate auto-hit missile packets, automatic Force Spike damage with independent Prone, captured burst centers and mandatory Thunderwave displacement are exact-approved. Human balance remains open.',
 'DD-19':'Earth Tremor uses one contiguous supporting surface, independent initial damage and finite magical difficult terrain; no permanent material or entry damage.',
 'DD-53':'Arcane Shield Shatter source-qualified rank0–1 protective-layer predicate, twelve comparison identities, Resonance Shield current accepted grant and whole Protective Sphere cleanup are reviewed.'
}
for a in c['aspects']:
 if a['id'] not in scopes:continue
 for key,path in [('reviewEvidence',review),('draftEvidence','DescentReviewChanges/ReviewBible/data/playtest/spell_drafts/batch_evocation_rank1.json'),('validationEvidence','DescentReviewChanges/ReviewBible/docs/mechanics/EVOCATION_RANK1_REVIEW_STATUS.json')]:
  if path not in a[key]:a[key].append(path)
 a.setdefault('completedScopes',[]).append(scopes[a['id']])
 if a['id'] in ['DD-11','DD-12']:a['openIssues']=[v.replace('249 individual spell drafts reviewed;599 unfinished','261 individual spell drafts reviewed;587 unfinished') for v in a['openIssues']]
 if a['id']=='DD-12':a['openIssues'].append('Rank-one Evocation balance remains open: separate automatic missile packets, automatic Force Spike, Shatter eligibility, short-range/no-save bursts, Witch Bolt sustain and Zephyr movement protection need table testing.')
dump(p,c)
print(json.dumps({'promoted':12,'selected':sum(map(len,sel.values())),'batchSha256':sha(b),'functionalRepairs':0,'pipeline':'pending'},indent=2))
