from pathlib import Path
import json,hashlib
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';D=R/'data/playtest/spell_drafts'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
compact=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':'),sort_keys=True)
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
review='docs/audit/2026-10-08/full-game/GPT_EVOCATION_CANTRIP_EXACT_REVIEW.md'
rt=(G/review).read_text(encoding='utf-8');assert 'APPROVE all twelve exact cards' in rt and 'No functional replacement text is required' in rt and 'provisional manuscript promotion' in rt
sub=read(A/'EVOCATION_CANTRIP_EXACT_SUBMISSION.json');p=D/'candidate_evocation_cantrips.json';b=D/'batch_evocation_cantrips.json'
assert not b.exists() and sha(p)==sub['candidateSha256BeforeReview']
assert len(sub['dispatch']['attachments'])==4 and all(x['matchesPreparedApartFromFinalWhitespace'] for x in sub['dispatch']['attachments'])
cat=read(R/'data/public/spell_playtests/catalog.json')['spells'];prior={s['id']:s['operational'] for s in cat if s['operational']}
assert len(prior)==237 and hashlib.sha256(compact(prior).encode()).hexdigest()==sub['previousOperationalSha256']
d=read(p);ids=[s['id'] for s in d['spells']];assert len(ids)==12 and not set(ids).intersection(prior)
d.update(status='PLAYTEST — REVIEWED / MANUSCRIPT-APPROVED; no functional repairs; runtime/balance pending',reviewEvidence=[review])
for s in d['spells']:
 s['implementationStatus']='REVIEWED authored operational PLAYTEST manuscript; runtime, human balance and broader integration pending'
 s['sourceReview'].append(review);s['reviewEvidence']=[review]
dump(p,d);b.write_bytes(p.read_bytes())
sel=read(D/'selected_sources.json');assert sum(map(len,sel.values()))==237 and not set(ids).intersection(i for v in sel.values() for i in v)
sel['Evocation'].extend(ids);dump(D/'selected_sources.json',sel)
dump(A/'EVOCATION_CANTRIP_EXACT_REPAIR_LOG.json',{'status':'No functional replacement fields/text required; approved candidate mechanics retained exactly','authority':review,'changes':[]})
sub.update(status='approved and promoted; rebuild/preservation verification pending',reviewEvidence=review,reviewTurnId='7829712c-d6e7-4c03-914b-94a646fe080c',reviewSha256=sha(G/review),requiredRepairsApplied=[],candidateSha256AfterPromotion=sha(p),batchSha256=sha(b),operationalAfter=249,unfinishedAfter=599);dump(A/'EVOCATION_CANTRIP_EXACT_SUBMISSION.json',sub)
cp=A/'EVOCATION_CANTRIP_CONFERENCE_SUBMISSION.json';c=read(cp);c.update(status='source conference, clarification and exact review complete; promoted without functional repairs',exactReviewEvidence=review);dump(cp,c)
sp=R/'docs/mechanics/EVOCATION_CANTRIP_REVIEW_STATUS.json';s=read(sp);s.update(status='REVIEWED / MANUSCRIPT-APPROVED; promoted; no functional repairs',exactManuscriptApproved=True,promoted=True,reviewEvidence=review,reviewTurnId=sub['reviewTurnId'],candidateSha256=sha(p),submittedCandidateSha256=sub['candidateSha256BeforeReview'],promotedBatchPath=b.relative_to(R).as_posix(),promotedBatchSha256=sha(b),requiredRepairsApplied=[],operationalCatalogCount=249,unfinishedIdentityCount=599,pipelineValidation='pending rebuild and validation',nextWork='Complete preservation verification, then continue rank-one Evocation.');dump(sp,s)
p=R/'tools/validate_spell_playtests.py';t=p.read_text(encoding='utf-8')
for old,new in [('All237 individually reviewed selected IDs','All249 individually reviewed selected IDs'),('len(set(selected))==237','len(set(selected))==249'),('Remaining611 explicitly blocked','Remaining599 explicitly blocked'),('for s in spells.values())==611','for s in spells.values())==599')]:
 assert old in t,old;t=t.replace(old,new)
p.write_text(t,encoding='utf-8')
p=R/'docs/mechanics/SPELL_INTEGRATION_RULES.md';t=p.read_text(encoding='utf-8');t+='''

## Evocation cantrips: actual casts, delayed riders and source-specific attacks

Twelve cantrips have [exact manuscript approval](../../../../docs/audit/2026-10-08/full-game/GPT_EVOCATION_CANTRIP_EXACT_REVIEW.md) without functional repairs. Read the full cards in [the spell reference](SPELL_PLAYTEST_STARTER.md); all fourteen source placements/Core blocks and actual class-access rows are retained. Their components remain V/S, with no added focus or automatic damage scaling.

Arcane Echo grants one genuine Bonus Action recast with the original actual class/school/rank-0 damaging-mode provenance, normal current eligibility/costs/hooks and chronological Refrain. Its arm and generated repeat keep separate finite records; a generated repeat never triggers another arm. Freezing Touch delays its Speed rider until the next regular target turn, with the expressly reviewed virtual-to-actual onset and original absolute cap. Flame Lash preserves the source conflict as a spell-local 30-foot melee attack. Shocking Grasp retains Reaction/30 feet and its prospective Reaction denial, without canceling a committed parent Action or stacked Reaction.

Dancing Lights has actual usable illumination for either generating school and bounded commanded movement. Chill Touch blocks broad current-HP gain, including direct recovery, while retaining independent non-HP effects and the existing resurrection life-transition exception. Its blocked natural20/Stable procedures use the existing healing-state rules. Soundburst and Thunderclap preserve distinct areas/riders; Thunderclap includes its caster. The object procedures never grant generic worn-item targeting. [Review status](EVOCATION_CANTRIP_REVIEW_STATUS.json) retains runtime, human balance and broader game integration as unfinished. Cosmology remains outside this mechanics batch.
''';p.write_text(t,encoding='utf-8')
p=R/'docs/mechanics/DEVELOPMENT_ROADMAP.md';t=p.read_text(encoding='utf-8');i=t.index('**Current conference:**');j=t.index('\n\n',i)
t=t[:i]+'''**Current conference:** twelve Evocation cantrips are [jointly manuscript-approved](../../../../docs/audit/2026-10-08/full-game/GPT_EVOCATION_CANTRIP_EXACT_REVIEW.md) without functional repairs. The [review status](EVOCATION_CANTRIP_REVIEW_STATUS.json) records source preservation and open runtime/balance questions. Arcane Echo, delayed Freezing Touch, source-specific Flame Lash/Shocking Grasp, light movement and broad Chill Touch recovery prevention now have explicit procedures. The [spell index](SPELL_PLAYTEST_STARTER.md) has 249 reviewed drafts and 599 unfinished identities, retaining all 848 IDs and 936 placements. Continue twelve rank-one Evocation sources, then the remaining low-rank schools and higher ranks. All previously completed Abjuration/Conjuration/Divination/Enchantment through actual rank3 remain intact; unassigned variants, broader systems, 327 unfinished feats, runtime, human balance and whole-game closure remain open.'''+t[j:]
t=t.replace('176 unfinished identities','164 unfinished identities')
old='237 individual drafts reviewed, including 72 starters, 6 healing/death additions, 5 transformation/buffer spells, 37 additional Abjuration identities, 39 additional Conjuration identities, 39 additional Divination identities and 39 additional Enchantment identities; 611 unfinished.'
assert old in t;t=t.replace(old,'249 individual drafts reviewed, including 72 starters, 6 healing/death additions, 5 transformation/buffer spells, 37 additional Abjuration identities, 39 additional Conjuration identities, 39 additional Divination identities, 39 additional Enchantment identities and 12 additional Evocation cantrips; 599 unfinished.');p.write_text(t,encoding='utf-8')
p=G/'START_HERE.md';t=p.read_text(encoding='utf-8');old='237 reviewed drafts; all 848 IDs and 936 placements preserved | 611 unfinished spell identities';assert old in t;t=t.replace(old,'249 reviewed drafts; all 848 IDs and 936 placements preserved | 599 unfinished spell identities')
i=t.index('The latest completed manuscript work is ');j=t.index('\n\n',i)
t=t[:i]+'''The latest completed manuscript work is [twelve Evocation cantrips](DescentReviewChanges/ReviewBible/docs/mechanics/EVOCATION_CANTRIP_REVIEW_STATUS.json), jointly approved without functional repairs. Their exact rules preserve both source schools where present, define Arcane Echo’s genuine recast and retain unusual source attacks rather than silently importing another game’s versions. Source preservation and catalog integration are being verified. The [development roadmap](DescentReviewChanges/ReviewBible/docs/mechanics/DEVELOPMENT_ROADMAP.md) moves next to twelve rank-one Evocation sources; the pending Time Loop work below remains a separate integration track.'''+t[j:];p.write_text(t,encoding='utf-8')
p=A/'REVIEW_STATUS.md';t=p.read_text(encoding='utf-8').replace('| Ordinary spells | 237 reviewed; 611 unfinished identities;','| Ordinary spells | 249 reviewed; 599 unfinished identities;');t+='''

## Twelve Evocation cantrips completed

The [source conference](GPT_EVOCATION_CANTRIP_SOURCE_CONFERENCE.md), [authoring clarification](GPT_EVOCATION_CANTRIP_AUTHORING_CLARIFICATION.md) and [exact review](GPT_EVOCATION_CANTRIP_EXACT_REVIEW.md) approve all twelve full cards without functional repairs. Four actually delivered exact attachments are preserved and match the prepared full text. All fourteen original placements/Core blocks, both dual-school access sets and all237 previous operational records remain unchanged.

Arcane Echo is a provenance-bound actual recast with independent finite arm/repeat records and no recursion. Freezing Touch has a delayed next-turn window, Flame Lash a spell-local30ft melee attack, Shocking Grasp a30ft Reaction interrupt, and Dancing Lights real bounded movable illumination. Chill Touch blocks broad current-HP gain using existing state-recovery rules without creating a resurrection seal. The catalog now has249 reviewed identities/599 unfinished;164 unfinished have actual class rank0–3. All848 IDs/936 placements remain. Runtime, human balance, variants and whole-game closure remain open. No source was deleted or GitHub pushed. Cosmology remains deferred until after successful authorized GitHub push and remote commit verification.
''';p.write_text(t,encoding='utf-8')
p=R/'data/playtest/game_development_coverage.json';c=read(p)
scopes={
 'DD-03':'Twelve Evocation cantrips exact-approved: delayed next-turn slow, independent Echo arm/repeat timing, legal Action-start Reaction interrupt and finite light commands. Runtime integration remains open.',
 'DD-11':'Twelve identities preserve fourteen placements/Core blocks, V/S-only components and exact access including dual-school Dancing Lights/Chill Touch; Echo repeats keep actual original class/school/rank0 mode.',
 'DD-12':'Twelve Evocation cantrips authored and reviewed without repairs;249 reviewed/599 unfinished,164 low-rank. Broad Reaction damage, recasting, illumination and HP-gain suppression need human testing.',
 'DD-17':'Source-local melee/ranged spell attacks, shared area damage/independent saves and prospective Reaction denial reviewed; old237 records unchanged.',
 'DD-19':'Dancing Lights real10bright/additional10dim illumination, bounded movement/tether, ordinary barriers and no automatic Hidden/Invisible revelation are authored, not runtime-certified.',
 'DD-53':'Finite point/target/ordinary-object procedures and source-conflict dispositions reviewed for twelve cantrips; no generic worn-item attack permission or imported game version.'
}
for a in c['aspects']:
 if a['id'] not in scopes:continue
 for key,path in [('reviewEvidence',review),('draftEvidence','DescentReviewChanges/ReviewBible/data/playtest/spell_drafts/batch_evocation_cantrips.json'),('validationEvidence','DescentReviewChanges/ReviewBible/docs/mechanics/EVOCATION_CANTRIP_REVIEW_STATUS.json')]:
  if path not in a[key]:a[key].append(path)
 a.setdefault('completedScopes',[]).append(scopes[a['id']])
 if a['id'] in ['DD-11','DD-12']:a['openIssues']=[v.replace('237 individual spell drafts reviewed;611 unfinished','249 individual spell drafts reviewed;599 unfinished') for v in a['openIssues']]
 if a['id']=='DD-12':a['openIssues'].append('Evocation cantrip balance: broad Shocking Grasp Reaction, Arcane Echo cast economy/hooks, four moving lights, broad Chill Touch HP prevention, delayed slow scheduling and self-inclusive Thunderclap remain human-test questions.')
dump(p,c)
print(json.dumps({'promoted':12,'selected':sum(map(len,sel.values())),'batchSha256':sha(b),'functionalRepairs':0,'pipeline':'pending'},indent=2))
