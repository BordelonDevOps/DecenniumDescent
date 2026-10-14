from pathlib import Path
import json,hashlib
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';D=R/'data/playtest/spell_drafts'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
compact=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':'),sort_keys=True)
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sub=read(A/'EVOCATION_RANK2_EXACT_SUBMISSION.json');review=sub['reviewEvidence'];rt=(G/review).read_text(encoding='utf-8')
assert 'APPROVE — all eight cards and the shared wording' in rt and 'No exact manuscript repairs required' in rt
p=D/'candidate_evocation_rank2.json';b=D/'batch_evocation_rank2.json';assert not b.exists() and sha(p)==sub['candidateSha256BeforeReview']
assert sub['dispatch']['serviceAccepted'] and sub['dispatch']['sentMatchesPreparedApartFromOuterWhitespace'] and sub['dispatch']['turnId']=='174b2eda-9e1c-4f1a-b342-b082f21e4586'
assert Path(sub['dispatch']['sentPromptPath']).read_text(encoding='utf-8').strip()==Path(sub['dispatch']['preparedCombinedPath']).read_text(encoding='utf-8').strip()
cat=read(R/'data/public/spell_playtests/catalog.json')['spells'];prior={s['id']:s['operational'] for s in cat if s['operational']}
assert len(prior)==261 and hashlib.sha256(compact(prior).encode()).hexdigest()==sub['previousOperationalSha256']
assert all(sha(R/k)==v for k,v in sub['frozenSourceAndClassFiles'].items())
d=read(p);ids=[s['id'] for s in d['spells']];assert ids==sub['ids'] and len(ids)==8 and not set(ids).intersection(prior)
sel=read(D/'selected_sources.json');assert sum(map(len,sel.values()))==261 and not set(ids).intersection(i for v in sel.values() for i in v)
vp=R/'tools/validate_spell_playtests.py';vt=vp.read_text(encoding='utf-8')
for old,new in [('All261 individually reviewed selected IDs','All269 individually reviewed selected IDs'),('len(set(selected))==261','len(set(selected))==269'),('Remaining587 explicitly blocked','Remaining579 explicitly blocked'),('for s in spells.values())==587','for s in spells.values())==579')]:
 assert old in vt,old;vt=vt.replace(old,new)
d.update(status='PLAYTEST — REVIEWED / MANUSCRIPT-APPROVED; no functional repairs; runtime/balance pending',reviewEvidence=[review])
for s in d['spells']:
 s['implementationStatus']='REVIEWED authored operational PLAYTEST manuscript; runtime, human balance and broader integration pending';s['sourceReview'].append(review);s['reviewEvidence']=[review]
dump(p,d);b.write_bytes(p.read_bytes());sel['Evocation'].extend(ids);dump(D/'selected_sources.json',sel);vp.write_text(vt,encoding='utf-8')
dump(A/'EVOCATION_RANK2_EXACT_REPAIR_LOG.json',{'status':'No functional replacements required; approved candidate mechanics retained exactly','authority':review,'changes':[]})
sub.update(status='approved and promoted; rebuild/preservation verification pending',reviewTurnId=sub['dispatch']['turnId'],candidateSha256AfterPromotion=sha(p),batchSha256=sha(b),requiredRepairsApplied=[],operationalAfter=269,unfinishedAfter=579)
control=R/'docs/mechanics/CONTROL_STATES_PLAYTEST.md';sub['controlGuidePrefixSha256']=sha(control);sub['controlGuidePrefixBytes']=control.stat().st_size
old_control_bytes=control.read_bytes();backup=A/'CONTROL_STATES_BEFORE_FROST_NOVA.md';assert not backup.exists();backup.write_bytes(old_control_bytes)
control.write_bytes(old_control_bytes+'''

## Frost Nova elemental Speed control

The [rank-two Evocation exact review](../../../../docs/audit/2026-10-08/full-game/GPT_EVOCATION_RANK2_EXACT_AND_DELIVERY_REVIEW.md) adds Frost Nova's specific source-owned Speed 0 rider to the individually reviewed elemental Speed-control components for Balanced Elements. Use the complete [spell card](SPELL_PLAYTEST_STARTER.md#spell-frost-nova). Same owner/target/group/exact profile uses the existing refresh policy, while different owners retain independent records. The nominal one-round endpoint is a base deadline that the existing Balanced Elements formula may extend; actual express maximums still apply. This classification does not add the Core Frozen, Root or Restrained condition. Runtime registration and execution remain separate work.
'''.encode('utf-8'))
dump(A/'EVOCATION_RANK2_EXACT_SUBMISSION.json',sub)
sp=R/'docs/mechanics/EVOCATION_RANK2_REVIEW_STATUS.json';s=read(sp);s.update(status='REVIEWED / MANUSCRIPT-APPROVED; promoted; no functional repairs',exactManuscriptApproved=True,promoted=True,reviewEvidence=review,reviewTurnId=sub['reviewTurnId'],candidateSha256=sha(p),submittedCandidateSha256=sub['candidateSha256BeforeReview'],promotedBatchPath=b.relative_to(R).as_posix(),promotedBatchSha256=sha(b),requiredRepairsApplied=[],operationalCatalogCount=269,unfinishedIdentityCount=579,pipelineValidation='pending rebuild and validation',nextWork='Complete preservation verification; continue dependency-ordered player/Director flow, with larger catalog batches.');dump(sp,s)
cp=A/'EVOCATION_RANK2_CONFERENCE_SUBMISSION.json';c=read(cp);c.update(status='source conference, clarification and exact review complete; promoted without functional repairs',exactReviewEvidence=review);dump(cp,c)
p=R/'docs/mechanics/SPELL_INTEGRATION_RULES.md';p.write_text(p.read_text(encoding='utf-8')+'''

## Rank-two Evocation areas and delayed damage

Eight rank-two Evocation identities have [exact manuscript approval](../../../../docs/audit/2026-10-08/full-game/GPT_EVOCATION_RANK2_EXACT_AND_DELIVERY_REVIEW.md). Their [complete cards](SPELL_PLAYTEST_STARTER.md) preserve five exact Core blocks and three separate possible historical-name blocks; matching metadata adoption does not merge identities or class access. Scorching Raystorm uses three independent attacks; line and burst spells keep their printed ranges. Shatter uses one fixed pre-damage snapshot and bounded structural sections. Frost Nova's specific elemental Speed 0 rider uses the existing refresh policy and reviewed Balanced Elements bridge. Acid Arrow's independently owned delayed packets keep their original one-shot markers and are not new casts. See [review status](EVOCATION_RANK2_REVIEW_STATUS.json) for remaining runtime and balance work.
''',encoding='utf-8')
p=G/'START_HERE.md';t=p.read_text(encoding='utf-8');old='261 reviewed drafts; all 848 IDs and 936 placements preserved | 587 unfinished spell identities';assert old in t;t=t.replace(old,'269 reviewed drafts; all 848 IDs and 936 placements preserved | 579 unfinished spell identities');i=t.index('The latest completed manuscript work is ');j=t.index('\n\n',i);t=t[:i]+'''The latest completed manuscript work is [eight rank-two Evocation cards](DescentReviewChanges/ReviewBible/docs/mechanics/EVOCATION_RANK2_REVIEW_STATUS.json), jointly approved without functional repairs. They preserve historical-name evidence and resolve Frost Nova, Shatter and Acid Arrow alongside the simpler attack/area spells. Promotion verification is in progress. The [agreed delivery priorities](docs/audit/2026-10-08/full-game/GPT_EVOCATION_RANK2_EXACT_AND_DELIVERY_REVIEW.md) now put character creation and advancement, equipment and the expedition-to-Haven flow alongside larger spell/feat batches. The quickstart roll summary and legacy builder guide now point to the current candidate rules. Full Time Loop execution remains a separate unfinished integration.'''+t[j:];p.write_text(t,encoding='utf-8')
p=R/'docs/mechanics/DEVELOPMENT_ROADMAP.md';t=p.read_text(encoding='utf-8');i=t.index('**Current conference:**');j=t.index('\n\n',i);t=t[:i]+'''**Current conference:** eight rank-two Evocation cards are [jointly manuscript-approved](../../../../docs/audit/2026-10-08/full-game/GPT_EVOCATION_RANK2_EXACT_AND_DELIVERY_REVIEW.md) without repairs. The [spell index](SPELL_PLAYTEST_STARTER.md) has 269 reviewed drafts and 579 unfinished identities, retaining all 848 IDs and 936 placements. The same conference agrees to dependency-ordered game-flow work: character creation/advancement, equipment/acquisition, expedition/encounter/reward/extraction/Haven, Director interfaces and packaging. Continue the remaining catalogs in larger batches using already reviewed shared procedures; reserve further source conferences for substantive conflicts. Human balance, runtime and publication remain separate gates. This is a change in workflow, not a reduction of the full objective or final flow approval.'''+t[j:];t=t.replace('152 unfinished identities','144 unfinished identities').replace('261 individual drafts reviewed','269 individual drafts reviewed').replace('24 additional Evocation identities through rank one; 587 unfinished.','32 additional Evocation identities through rank two; 579 unfinished.');p.write_text(t,encoding='utf-8')
p=A/'REVIEW_STATUS.md';t=p.read_text(encoding='utf-8').replace('| Ordinary spells | 261 reviewed; 587 unfinished identities;','| Ordinary spells | 269 reviewed; 579 unfinished identities;');t+='''

## Rank-two Evocation and delivery priorities

[Eight exact rank-two cards](GPT_EVOCATION_RANK2_EXACT_AND_DELIVERY_REVIEW.md) are approved and promoted without functional repairs. The three historical-name records remain evidence, not identity mergers. Frost Nova uses the existing refresh policy and explicit elemental classification; Shatter fixes its target/structure snapshot before damage; Acid Arrow has independent source-owned one-shot riders. Catalog:269 reviewed/579 unfinished;144 unfinished with actual rank0–3. Preservation verification follows the rebuild.

The same notebook conference agrees to larger catalog batches and dependency-ordered whole-game work. Begin with character creation/advancement, equipment/acquisition and the expedition-to-Haven loop, using existing sources before inventing replacements. [Initial character-flow findings](CHARACTER_FLOW_INITIAL_FINDINGS.md) record two corrected entry-document mismatches. Full scope, source preservation, final joint flow review, conditional GitHub delivery and post-push-only cosmology review remain unchanged.
''';p.write_text(t,encoding='utf-8')
p=R/'data/playtest/game_development_coverage.json';c=read(p)
for a in c['aspects']:
 if a['id'] in ['DD-11','DD-12','DD-13']:a['openIssues']=[v.replace('261 individual spell drafts reviewed;587 unfinished','269 individual spell drafts reviewed;579 unfinished') for v in a['openIssues']]
 if a['id'] in ['DD-03','DD-11','DD-12','DD-16','DD-17','DD-21','DD-53']:
  for key,path in [('reviewEvidence',review),('draftEvidence','DescentReviewChanges/ReviewBible/data/playtest/spell_drafts/batch_evocation_rank2.json'),('validationEvidence','DescentReviewChanges/ReviewBible/docs/mechanics/EVOCATION_RANK2_REVIEW_STATUS.json')]:
   if path not in a[key]:a[key].append(path)
  a.setdefault('completedScopes',[]).append('Eight rank-two Evocation manuscripts approved: three historical metadata adoptions preserve separate aliases; Frost Nova refresh/elemental control, fixed Shatter structural snapshot and Acid Arrow one-shot packets are explicit. Runtime and human balance remain open.')
 if a['id']=='DD-12':a['openIssues'].append('Rank-two Evocation needs table testing for self-inclusive Frost Nova, automatic Arcane Implosion, bounded structural Shatter damage, independent Acid Arrow riders and three-ray attack packets.')
c['workingMethod']='Dependency-ordered player/Director flow plus larger catalog batches; reuse approved shared procedures and confer over substantive conflicts. Full objective unchanged; cosmology post-push only.';dump(p,c)
print(json.dumps({'promoted':8,'selected':269,'batchSha256':sha(b),'functionalRepairs':0,'pipeline':'pending'},indent=2))
