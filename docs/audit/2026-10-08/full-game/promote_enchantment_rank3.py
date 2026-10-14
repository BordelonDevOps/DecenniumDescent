import json,hashlib
from pathlib import Path
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';D=R/'data/playtest/spell_drafts'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
review='docs/audit/2026-10-08/full-game/GPT_ENCHANTMENT_RANK3_EXACT_REVIEW.md'
rt=(G/review).read_text(encoding='utf-8')
assert 'NO REQUIRED FUNCTIONAL REPAIRS.' in rt and 'provisional manuscript promotion' in rt
sub=read(A/'ENCHANTMENT_RANK3_EXACT_SUBMISSION.json')
p=D/'candidate_enchantment_rank3.json';b=D/'batch_enchantment_rank3.json';q=D/'candidate_enchantment_rank3_shared_rules.md'
pub=R/'docs/mechanics/ENCHANTMENT_RANK3_INTEGRATION_PLAYTEST.md'
assert not b.exists() and not pub.exists()
assert sha(p)==sub['candidateSha256BeforeReview'] and sha(q)==sub['sharedCandidateSha256BeforeReview']
assert all(x['matchesPreparedApartFromFinalWhitespace'] for x in sub['dispatch']['attachments'])
d=read(p);ids=[s['id'] for s in d['spells']]
cat=read(R/'data/public/spell_playtests/catalog.json')['spells']
existing={s['id']:s['operational'] for s in cat if s['operational']}
assert len(ids)==8 and len(existing)==229 and not set(ids).intersection(existing)
assert hashlib.sha256(json.dumps(existing,sort_keys=True,ensure_ascii=False).encode()).hexdigest()==sub['previousOperationalSha256']
# Resolve authoring-status labels only, keeping approved mechanical wording.
editorial=[
('dominate-beast','limitations',' This independent-source completion requires exact review.',''),
('dominate-beast','designNotes','Exact review must approve concurrent independent same-spell records and the shared manuscript’s queued-command/absent-phase completions.','Exact review approved concurrent independent same-spell records and the shared manuscript’s queued-command/absent-phase completions.'),
('mental-chains','effect','It cannot choose voluntary transport away from the anchor’s plane; this explicit completion needs exact review.','It cannot choose voluntary transport away from the anchor’s plane.')
]
changes=[]
for ident,field,old,new in editorial:
    s=next(s for s in d['spells'] if s['id']==ident)
    assert s[field].count(old)==1
    before=s[field];s[field]=before.replace(old,new)
    changes.append({'id':ident,'field':field,'before':before,'after':s[field],'removedStatusText':old,'replacementStatusText':new,'kind':'resolved exact-review status label only; no mechanical change'})
d['status']='PLAYTEST — REVIEWED / MANUSCRIPT-APPROVED; no functional repairs; runtime/balance pending'
d['reviewEvidence']=[review]
for s in d['spells']:
    s['implementationStatus']='REVIEWED authored operational PLAYTEST manuscript; runtime, human balance and broader integration pending'
    s['sourceReview'].append(review);s['reviewEvidence']=[review]
dump(p,d);b.write_bytes(p.read_bytes())
sel=read(D/'selected_sources.json')
assert sum(map(len,sel.values()))==229
assert not set(ids).intersection(i for vals in sel.values() for i in vals)
sel['Enchantment'].extend(ids);dump(D/'selected_sources.json',sel)
dump(A/'ENCHANTMENT_RANK3_EDITORIAL_STATUS_CHANGES.json',{'status':'three exact-review status labels resolved after approval; no functional repairs','authority':review,'changes':changes})

shared=q.read_text(encoding='utf-8')
replacements=[
('# Rank-three Enchantment integration — exact-review candidate','# Rank-three Enchantment integration — provisional playtest'),
('LOCAL CANDIDATE — NOT ACTIVE. Proposed publication path: docs/mechanics/ENCHANTMENT_RANK3_INTEGRATION_PLAYTEST.md. This accompanies eight unselected full cards; source conference and authoring clarification establish draftability, not exact approval. The existing ENCHANTMENT_CONTROL_INTEGRATION_PLAYTEST.md remains authoritative in its approved scope. These additions require joint exact review and do not approve runtime, balance, whole-game closure or GitHub delivery. Cosmology remains outside this work.',
 'REVIEWED PROVISIONAL MANUSCRIPT. This accompanies eight approved rank-three Enchantment cards. The [exact review](../../../../docs/audit/2026-10-08/full-game/GPT_ENCHANTMENT_RANK3_EXACT_REVIEW.md) approves the submitted mechanics and marked completions. The existing [Enchantment control integration](ENCHANTMENT_CONTROL_INTEGRATION_PLAYTEST.md) remains authoritative in its approved scope. This approval does not certify runtime, human balance, whole-game closure or GitHub delivery. Cosmology remains outside this work.'),
('EXACT-REVIEW COMPLETION — pending commands:','Reviewed completion — pending commands:'),
('EXACT-REVIEW COMPLETION — phase availability:','Reviewed completion — phase availability:'),
('These bounded completions explicitly require exact approval.','These bounded completions have exact manuscript approval.'),
('EXACT-REVIEW COMPLETION — shared END-only cadence:','Reviewed completion — shared END-only cadence:'),
('This is the explicit narrow transition for these new END-only schedules and requires exact approval.','This is the explicitly reviewed narrow transition for these new END-only schedules.'),
('## Scope and explicit exact-review questions','## Scope and open validation'),
('The companion pending-command/phase completions, independent Dominate Beast same-spell records, END-only transition, and Mental Chains voluntary-transport/plane completions on its card require explicit review.',
 'The companion pending-command/phase completions, independent Dominate Beast same-spell records, END-only transition, and Mental Chains voluntary-transport/plane completions on its card have exact manuscript approval.')
]
for old,new in replacements:
    assert shared.count(old)==1,old
    shared=shared.replace(old,new)
binding="""
## Mental Chains: binding separated-plane interpretation

If a creature is involuntarily moved away from an application's anchor plane, that application's voluntary-distance/plane restriction has no effect while the creature remains separated. Ordinary rules govern further travel from that other plane, including voluntary travel elsewhere or return to the anchor plane. Concentration and the original deadline continue. On return, that application's original fixed anchor and boundary resume immediately. Another independent Mental Chains application on the creature's current plane still retains its own actual restrictions. This is the exact review's interpretation of the approved separation/resumption procedure, not a cosmology ruling.
"""
pub.write_text(shared.rstrip()+'\n\n'+binding.strip()+'\n',encoding='utf-8')
# Preserve the entire former companion guide before adding a discovery link.
companion=R/'docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md'
baseline=A/'CREATURE_LIFECYCLE_BEFORE_ENCHANTMENT_RANK3.md'
assert not baseline.exists()
baseline.write_bytes(companion.read_bytes())
append="""

## Dominate Beast integration

The [reviewed rank-three Enchantment supplement](ENCHANTMENT_RANK3_INTEGRATION_PLAYTEST.md) adds the source-qualified Dominate Beast bridge for actual Beast companions. It redirects only an existing owner-attached execution opportunity, preserves original profile/source-owner stats, reuses a same-companion/same-phase pending reservation where applicable, and occupies the original owner's structural command/offense caps without charging that owner's Bonus Action. It grants no independent companion turn, duplicate phase or new resource pool. The prior lifecycle text above remains intact; the new bridge is an authored manuscript addition whose stateful runtime integration remains open.
"""
companion.write_bytes(baseline.read_bytes()+append.encode('utf-8'))
dump(A/'ENCHANTMENT_RANK3_SHARED_PUBLICATION_CHANGES.json',{'status':'approved shared mechanics preserved; pending labels resolved; exact-review interpretation and discovery link added','sourcePath':str(q),'sourceSha256':sha(q),'publicationPath':str(pub),'publicationSha256':sha(pub),'statusLabelReplacements':[{'before':a,'after':z} for a,z in replacements],'appendedBindingClarification':binding.strip(),'companionBaselinePath':str(baseline),'companionBaselineSha256':sha(baseline),'companionPath':str(companion),'companionAppendedLink':append,'authority':review})

sub.update(status='approved; promoted; pipeline pending',reviewTurnId='d15faf7f-6690-45c3-bc49-3235411fded0',reviewEvidence=review,requiredRepairsApplied=[],editorialStatusChanges='docs/audit/2026-10-08/full-game/ENCHANTMENT_RANK3_EDITORIAL_STATUS_CHANGES.json',candidateSha256AfterPromotion=sha(p),batchSha256=sha(b),sharedPublishedPath=pub.relative_to(R).as_posix(),sharedPublishedSha256=sha(pub),operationalAfter=237,unfinishedAfter=611)
dump(A/'ENCHANTMENT_RANK3_EXACT_SUBMISSION.json',sub)
cp=A/'ENCHANTMENT_RANK3_CONFERENCE_SUBMISSION.json';c=read(cp);c.update(status='source conference, authoring clarification and exact review complete; promoted with no functional repairs',exactReviewEvidence=review);dump(cp,c)
sp=R/'docs/mechanics/ENCHANTMENT_RANK3_REVIEW_STATUS.json';s=read(sp)
s.update(status='REVIEWED / MANUSCRIPT-APPROVED; promoted; no functional repairs',exactManuscriptApproved=True,promoted=True,reviewEvidence=review,reviewTurnId=sub['reviewTurnId'],candidateSha256=sha(p),submittedCandidateSha256=sub['candidateSha256BeforeReview'],promotedBatchPath=b.relative_to(R).as_posix(),promotedBatchSha256=sha(b),sharedPublishedPath=pub.relative_to(R).as_posix(),sharedPublishedSha256=sha(pub),requiredRepairsApplied=[],editorialStatusChanges=sub['editorialStatusChanges'],operationalCatalogCount=237,unfinishedIdentityCount=611,pipelineValidation='pending rebuild and validation',nextWork='Complete preservation checks; continue unfinished Evocation/other schools. Runtime/human balance and whole-game gates remain open.')
dump(sp,s)
p=R/'tools/validate_spell_playtests.py';t=p.read_text(encoding='utf-8')
for old,new in [('All229 individually reviewed selected IDs','All237 individually reviewed selected IDs'),('len(set(selected))==229','len(set(selected))==237'),('Remaining619 explicitly blocked','Remaining611 explicitly blocked'),('for s in spells.values())==619','for s in spells.values())==611')]:
    assert old in t;t=t.replace(old,new)
p.write_text(t,encoding='utf-8')
p=R/'docs/mechanics/SPELL_INTEGRATION_RULES.md';t=p.read_text(encoding='utf-8')
t+="""

## Rank-three Enchantment: companion control, source modes and task scope

Eight further identities have [exact manuscript approval](../../../../docs/audit/2026-10-08/full-game/GPT_ENCHANTMENT_RANK3_EXACT_REVIEW.md) with no functional repairs. Their [rank-three integration supplement](ENCHANTMENT_RANK3_INTEGRATION_PLAYTEST.md) is part of this provisional overlay. It explicitly binds Dominate Beast and Suggestion to existing instruction arbitration, supplies the owner-attached Beast-companion bridge and prevents duplicate commands/turns. Hypnotic Pattern retains Enchantment60ft versus Illusion30ft casting range, and its initial self-concentration collapse uses only the reviewed spell-specific atomic batch.

Terrifying Gaze and both Slow modes use the reviewed ending-save transition without generating action budgets. Slow preserves Action/WIS Enchantment and Reaction/CON Transmutation as separate source packages; its selected trigger creature, distinct movement segments, future-Reaction restriction and prospective Action ceiling are explicit. Mental Chains uses the actual voluntary boundary and original anchor with separated-plane suppression, without universal involuntary-transport immunity. Suggestion reserves necessary hard control at establishment, including conditional future tasks, and never dynamically acquires a new hard component. The [review status](ENCHANTMENT_RANK3_REVIEW_STATUS.json) retains human balance, effect-runtime and broader-system work as open.
"""
p.write_text(t,encoding='utf-8')
p=R/'docs/mechanics/DEVELOPMENT_ROADMAP.md';t=p.read_text(encoding='utf-8');i=t.index('**Current conference:**');j=t.index('\n\n',i)
t=t[:i]+"""**Current conference:** eight rank-three Enchantment identities and their companion/control supplement are [jointly manuscript-approved](../../../../docs/audit/2026-10-08/full-game/GPT_ENCHANTMENT_RANK3_EXACT_REVIEW.md) with no functional repairs. The [shared supplement](ENCHANTMENT_RANK3_INTEGRATION_PLAYTEST.md) preserves school-specific Hypnotic Pattern/Slow modes, existing companion budgets, finite task scope and explicit timing. [Review status](ENCHANTMENT_RANK3_REVIEW_STATUS.json) records preservation and open runtime/balance. The [spell index](SPELL_PLAYTEST_STARTER.md) has 237 reviewed drafts and 611 unfinished identities, retaining all 848 IDs and 936 placements. All currently unfinished Abjuration, Conjuration, Divination and Enchantment identities through actual rank3 are authored. Continue Evocation and the other low-rank schools; higher ranks, [unassigned variants](SPELL_VARIANT_REVIEW_STATUS.json), broader systems, 327 unfinished feats, runtime, human balance and whole-game closure remain open."""+t[j:]
t=t.replace('184 unfinished identities','176 unfinished identities')
old='229 individual drafts reviewed, including 72 starters, 6 healing/death additions, 5 transformation/buffer spells, 37 additional Abjuration identities, 39 additional Conjuration identities, 39 additional Divination identities and 31 additional Enchantment identities; 619 unfinished.'
assert old in t
t=t.replace(old,'237 individual drafts reviewed, including 72 starters, 6 healing/death additions, 5 transformation/buffer spells, 37 additional Abjuration identities, 39 additional Conjuration identities, 39 additional Divination identities and 39 additional Enchantment identities; 611 unfinished.')
p.write_text(t,encoding='utf-8')
p=G/'START_HERE.md';t=p.read_text(encoding='utf-8');old='229 reviewed drafts; all 848 IDs and 936 placements preserved | 619 unfinished spell identities';assert old in t;t=t.replace(old,'237 reviewed drafts; all 848 IDs and 936 placements preserved | 611 unfinished spell identities')
i=t.index('The latest completed manuscript work is ');j=t.index('\n\n',i)
t=t[:i]+"""The latest completed manuscript work is [eight rank-three Enchantment spells](DescentReviewChanges/ReviewBible/docs/mechanics/ENCHANTMENT_RANK3_REVIEW_STATUS.json), jointly approved without functional repairs. Their [companion and control supplement](DescentReviewChanges/ReviewBible/docs/mechanics/ENCHANTMENT_RANK3_INTEGRATION_PLAYTEST.md) preserves existing command budgets, school-specific spell modes and exact timing. Source preservation and catalog integration are being verified. The [development roadmap](DescentReviewChanges/ReviewBible/docs/mechanics/DEVELOPMENT_ROADMAP.md) moves next to Evocation and the remaining low-rank schools; the pending Time Loop work below remains a separate integration track."""+t[j:];p.write_text(t,encoding='utf-8')
p=A/'REVIEW_STATUS.md';t=p.read_text(encoding='utf-8').replace('| Ordinary spells | 229 reviewed; 619 unfinished identities;','| Ordinary spells | 237 reviewed; 611 unfinished identities;')
t+="""

## Eight rank-three Enchantment identities completed

The [exact review](GPT_ENCHANTMENT_RANK3_EXACT_REVIEW.md) approves all eight full cards and the companion/control integration with no functional repairs. Four actual delivered attachments are preserved and match the prepared packet. Three obsolete exact-review status labels were resolved in the new cards; their approved mechanics remain unchanged. The shared supplement records the binding Mental Chains separated-plane interpretation and is linked from the existing companion guide, whose prior content is preserved verbatim.

The catalog now targets 237 reviewed identities and 611 unfinished;176 unfinished have actual class rank0–3 access. All eleven source placements/Core blocks, exact class access,848 IDs and936 placements remain. All formerly unfinished Enchantment identities through rank3 are authored; variants, higher ranks, other schools, runtime, human balance and whole-game closure remain open. Forty future low-rank Evocation source identities are inventoried only, including three preserved historical alias Core blocks. No source deletion or GitHub push occurred. Cosmology remains deferred until the verified authorized push.
"""
p.write_text(t,encoding='utf-8')
p=R/'data/playtest/game_development_coverage.json';c=read(p)
scopes={
'DD-03':'Eight rank-three Enchantment cards and supplement approved: companion phase/budget conservation, END-only save timing, Hypnotic Pattern atomic batch and prospective Slow commitments.237/611 catalog.',
'DD-11':'Eight identities preserve eleven source placements/Core blocks and actual class access, including Hypnotic Pattern school ranges and distinct Slow activation/save/rider packages.',
'DD-12':'All unfinished Enchantment identities through rank3 now authored;237 reviewed/611 unfinished,176 low-rank. Human balance and effect runtime remain open.',
'DD-17':'Source-qualified Dominate Beast bridge uses existing Beast companion phase/profile and original-owner structural caps; same pending command can redirect without new turn, BA refund or duplicate allowance. Runtime integration remains open.',
'DD-53':'Suggestion finite-task scope, initial hard reservation and no later hard escalation; Pattern one-source rousing and control/companion arbitration explicitly reviewed.',
'DD-54':'Paid hidden eligibility/reasonableness supplies no diagnostic. Pattern rousing uses stable source order without disclosing metadata; Dominate Beast gives no remote sensory feed.'
}
for a in c['aspects']:
    if a['id'] not in scopes:continue
    for key,path in [('reviewEvidence',review),('draftEvidence','DescentReviewChanges/ReviewBible/data/playtest/spell_drafts/batch_enchantment_rank3.json'),('draftEvidence','DescentReviewChanges/ReviewBible/docs/mechanics/ENCHANTMENT_RANK3_INTEGRATION_PLAYTEST.md'),('validationEvidence','DescentReviewChanges/ReviewBible/docs/mechanics/ENCHANTMENT_RANK3_REVIEW_STATUS.json')]:
        if path not in a[key]:a[key].append(path)
    a.setdefault('completedScopes',[]).append(scopes[a['id']])
    if a['id'] in ['DD-11','DD-12']:a['openIssues']=[x.replace('229 individual spell drafts reviewed;619 unfinished','237 individual spell drafts reviewed;611 unfinished') for x in a['openIssues']]
    if a['id']=='DD-12':a['openIssues'].append('Rank-three Enchantment large-area Stunned/Inc, eight-hour Suggestion, sustained Beast attacks, no-repeat Fear and six-target Reaction Slow need human balance tests. Companion/condition/order schedulers are not certified by authored manuscripts.')
dump(p,c)
print(json.dumps({'promoted':8,'selected':sum(map(len,sel.values())),'batchSha256':sha(b),'sharedSha256':sha(pub),'functionalRepairs':0,'editorialStatusFields':len(changes),'pipeline':'pending'},indent=2))

