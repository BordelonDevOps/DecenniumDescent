import json, hashlib
from pathlib import Path

G = Path('C:/Github/DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'
D = R / 'data/playtest/spell_drafts'
read = lambda p: json.loads(p.read_text(encoding='utf-8'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p, d):
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

review = 'docs/audit/2026-10-08/full-game/GPT_ENCHANTMENT_RANK2_EXACT_REVIEW.md'
rt = (G / review).read_text(encoding='utf-8')
assert 'No required functional repairs.' in rt
assert 'approved for provisional manuscript promotion' in rt
sub = read(A / 'ENCHANTMENT_RANK2_EXACT_SUBMISSION.json')
p = D / 'candidate_enchantment_rank2.json'
b = D / 'batch_enchantment_rank2.json'
shared_source = D / 'candidate_enchantment_rank2_shared_rules.md'
shared_dest = R / 'docs/mechanics/ENCHANTMENT_CONTROL_INTEGRATION_PLAYTEST.md'
assert not b.exists() and not shared_dest.exists()
assert sha(p) == sub['candidateSha256BeforeReview']
assert sha(shared_source) == sub['sharedCandidateSha256BeforeReview']
assert all(x['matchesPreparedApartFromFinalWhitespace'] for x in sub['dispatch']['attachments'])
d = read(p)
ids = [s['id'] for s in d['spells']]
cat = read(R / 'data/public/spell_playtests/catalog.json')['spells']
existing = {s['id']: s['operational'] for s in cat if s['operational']}
assert len(ids) == 7 and len(existing) == 222 and not set(ids).intersection(existing)
assert hashlib.sha256(json.dumps(existing, sort_keys=True, ensure_ascii=False).encode()).hexdigest() == sub['previousOperationalSha256']
d['status'] = 'PLAYTEST — REVIEWED / MANUSCRIPT-APPROVED exactly as submitted; runtime/balance pending'
d['reviewEvidence'] = [review]
for s in d['spells']:
    s['implementationStatus'] = 'REVIEWED authored operational PLAYTEST manuscript; runtime, human balance and broader Enchantment/social-control integration pending'
    s['sourceReview'].append(review)
    s['reviewEvidence'] = [review]
dump(p, d)
b.write_bytes(p.read_bytes())
sel = read(D / 'selected_sources.json')
assert sum(map(len, sel.values())) == 222
assert not set(ids).intersection(i for values in sel.values() for i in values)
sel['Enchantment'].extend(ids)
dump(D / 'selected_sources.json', sel)

# Publish the approved shared body. Only candidate-status labels change.
shared = shared_source.read_text(encoding='utf-8')
replacements = [
    ('# Enchantment control integration — exact-review candidate', '# Enchantment control integration — provisional playtest'),
    ('LOCAL CANDIDATE — NOT ACTIVE. Proposed publication path: docs/mechanics/ENCHANTMENT_CONTROL_INTEGRATION_PLAYTEST.md. These NEW integration rules accompany seven unselected rank-two Enchantment cards. Source conference and authoring clarification establish draftability, not exact manuscript approval. They grant no cosmology interpretation, source deletion, runtime certification or balance approval.',
     'REVIEWED PROVISIONAL MANUSCRIPT. These NEW integration rules accompany seven approved rank-two Enchantment cards. The [exact review](../../../../docs/audit/2026-10-08/full-game/GPT_ENCHANTMENT_RANK2_EXACT_REVIEW.md) approves the submitted body and records the binding interpretations below. Source originals remain preserved. This is not runtime certification, human balance approval, whole-game closure or GitHub delivery approval.'),
    ('EXACT-REVIEW COMPLETION: a target', 'Reviewed procedure: a target'),
    ('EXACT-REVIEW COMPLETION for entering initiative:', 'Reviewed procedure for entering initiative:'),
    ('The two marked cadence completions require explicit exact-review approval, especially concurrent outside-initiative applications and the first real turn\'s carried budget.',
     'Concurrent outside-initiative applications and the first real turn\'s carried budget have exact manuscript approval; executable runtime integration remains open.')
]
for old, new in replacements:
    assert shared.count(old) == 1, old
    shared = shared.replace(old, new)
clarifications = """
## Binding interpretations from the exact review

One-shot Command, Confusing Flash and Illusive Commands do not gain a new repeating cadence from this overlay. If their compelled behavior falls into the same current six-second/regular-turn opportunity, their demands compete for the same actual remaining behavior budget through Compelled Budget Arbitration.

Ordinary actual regular-start processing still happens at the first real regular turn: Reaction refresh, recharge, death-save and start effects follow their normal combat rules. Only the Enchantment control START/order opportunity and already-spent ordinary behavior budget are not replayed. The virtual START was not itself a combat turn or resource-refresh event.

For Illusive Commands, an independently valid soft movement/interaction component that survives a blocked hard Action component establishes a new instruction and replaces the prior pending same-spell record. A saved-against, wholly invalid or wholly blocked instruction establishes no replacement.

A Dire Charm application keeps its repeat saves while at least one of its original components remains. Once it has none, its save schedule stops; an old save never removes a later application's replacement component. No hard-control history is refunded.

Command's Grovel does not inherently consume the ordinary Action. Its required Prone posture can coexist with another legal Action. Confusing Flash's Attack branch continues to spend the ordinary Action on exactly one ordinary attack.
"""
shared_dest.write_text(shared.rstrip() + '\n\n' + clarifications.strip() + '\n', encoding='utf-8')
dump(A / 'ENCHANTMENT_RANK2_SHARED_PUBLICATION_CHANGES.json', {
    'status': 'approved body preserved apart from candidate-status labels and binding review interpretations',
    'sourcePath': str(shared_source), 'sourceSha256': sha(shared_source),
    'publicationPath': str(shared_dest), 'publicationSha256': sha(shared_dest),
    'statusLabelReplacements': [{'before': old, 'after': new} for old, new in replacements],
    'appendedBindingClarifications': clarifications.strip(),
    'authority': review,
    'functionalCardRepairs': []
})

sub.update(status='approved exactly as submitted; promoted; pipeline pending',
    requiredRepairsApplied=[], changesLimitedToReviewedRepairs=True,
    candidateSha256AfterPromotion=sha(p), batchSha256=sha(b),
    sharedPublishedPath=shared_dest.relative_to(R).as_posix(), sharedPublishedSha256=sha(shared_dest),
    operationalAfter=229, unfinishedAfter=619)
dump(A / 'ENCHANTMENT_RANK2_EXACT_SUBMISSION.json', sub)
cp = A / 'ENCHANTMENT_RANK2_CONFERENCE_SUBMISSION.json'
conf = read(cp)
conf.update(status='source conference and exact review complete; promoted without functional repairs', exactReviewEvidence=review)
dump(cp, conf)
sp = R / 'docs/mechanics/ENCHANTMENT_RANK2_REVIEW_STATUS.json'
st = read(sp)
st.update(status='REVIEWED / MANUSCRIPT-APPROVED exactly as submitted; promoted',
    exactManuscriptApproved=True, promoted=True, reviewEvidence=review,
    reviewTurnId=sub['reviewTurnId'], candidateSha256=sha(p),
    promotedBatchPath=b.relative_to(R).as_posix(), promotedBatchSha256=sha(b),
    submittedCandidateSha256=sub['candidateSha256BeforeReview'], requiredRepairsApplied=[],
    operationalCatalogCount=229, unfinishedIdentityCount=619,
    sharedPublishedPath=shared_dest.relative_to(R).as_posix(), sharedPublishedSha256=sha(shared_dest),
    sharedPublicationChanges='docs/audit/2026-10-08/full-game/ENCHANTMENT_RANK2_SHARED_PUBLICATION_CHANGES.json',
    pipelineValidation='pending rebuild and validation')
dump(sp, st)

vp = R / 'tools/validate_spell_playtests.py'
t = vp.read_text(encoding='utf-8')
for old, new in [('All222 individually reviewed selected IDs','All229 individually reviewed selected IDs'),
    ('len(set(selected))==222','len(set(selected))==229'),
    ('Remaining626 explicitly blocked','Remaining619 explicitly blocked'),
    ('for s in spells.values())==626','for s in spells.values())==619')]:
    assert old in t
    t = t.replace(old, new)
vp.write_text(t, encoding='utf-8')

p = R / 'docs/mechanics/SPELL_INTEGRATION_RULES.md'
t = p.read_text(encoding='utf-8')
t += """
## Rank-two Enchantment and shared control integration

Seven rank-two Enchantment identities have [exact manuscript approval](../../../../docs/audit/2026-10-08/full-game/GPT_ENCHANTMENT_RANK2_EXACT_REVIEW.md) with no functional card repairs. Their [shared control integration](ENCHANTMENT_CONTROL_INTEGRATION_PLAYTEST.md) is part of this provisional rules overlay and applies its specific arbitration interface to existing Command and Confusing Flash as well as Illusive Commands, Dire Charm and Crown of Madness. Their prior individual card texts remain unchanged.

The integration defines native ordinary Attack Actions and the explicit Confusing Flash single-attack exception; separately scoped Dire Charm components; chronological priority for conflicting instructions using the same ordinary budget; a shared six-second cycle for ongoing Dire Charm/Crown control outside initiative; and first-real-turn budget carry without replaying control orders. Ordinary real-turn start processing still occurs. One-shot commands keep their own timing while sharing actual remaining budgets.

Calm Emotions and Zone of Truth keep independent first-exposure save histories in fixed zones, with total-cover/outside suppression and return without rerolling. Calm Emotions suppresses actual Frightened effects while underlying clocks and saves continue. The five compared emotion-themed class cards acquire no new maintenance dependency. Zone of Truth preserves both actual class/rank/price modes without granting additional access or a truth-detection oracle. The [review status](ENCHANTMENT_RANK2_REVIEW_STATUS.json) retains open numerical balance, effect-runtime and broader social-control work.
"""
p.write_text(t, encoding='utf-8')

p = R / 'docs/mechanics/DEVELOPMENT_ROADMAP.md'
t = p.read_text(encoding='utf-8')
i = t.index('**Current conference:**')
j = t.index('\n\n', i)
t = t[:i] + """**Current conference:** seven rank-two Enchantment identities and their shared control integration are [jointly manuscript-approved exactly as submitted](../../../../docs/audit/2026-10-08/full-game/GPT_ENCHANTMENT_RANK2_EXACT_REVIEW.md). [Shared procedures](ENCHANTMENT_CONTROL_INTEGRATION_PLAYTEST.md) cover conflicting instructions, ordinary attacks, split components, outside-initiative control cadence and fixed-zone histories. [Review status](ENCHANTMENT_RANK2_REVIEW_STATUS.json) records preserved sources/access and open runtime/balance. The [spell index](SPELL_PLAYTEST_STARTER.md) has 229 reviewed drafts and 619 unfinished identities, preserving all 848 IDs and 936 placements. All currently unfinished Enchantment identities through rank2 and Abjuration, Conjuration and Divination identities through rank3 are authored. Continue rank-three Enchantment and other low-rank schools; higher ranks, [unassigned variants](SPELL_VARIANT_REVIEW_STATUS.json), broader systems, 327 unfinished feats, runtime, human balance and whole-game closure remain open.""" + t[j:]
t = t.replace('191 unfinished identities', '184 unfinished identities')
old = '222 individual drafts reviewed, including 72 starters, 6 healing/death additions, 5 transformation/buffer spells, 37 additional Abjuration identities, 39 additional Conjuration identities, 39 additional Divination identities and 24 additional Enchantment identities; 626 unfinished.'
assert old in t
t = t.replace(old, '229 individual drafts reviewed, including 72 starters, 6 healing/death additions, 5 transformation/buffer spells, 37 additional Abjuration identities, 39 additional Conjuration identities, 39 additional Divination identities and 31 additional Enchantment identities; 619 unfinished.')
p.write_text(t, encoding='utf-8')

p = G / 'START_HERE.md'
t = p.read_text(encoding='utf-8')
old = '222 reviewed drafts; all 848 IDs and 936 placements preserved | 626 unfinished spell identities'
assert old in t
t = t.replace(old, '229 reviewed drafts; all 848 IDs and 936 placements preserved | 619 unfinished spell identities')
i = t.index('The latest completed work is ')
j = t.index('\n\n', i)
t = t[:i] + """The latest completed manuscript work is [seven rank-two Enchantment spells](DescentReviewChanges/ReviewBible/docs/mechanics/ENCHANTMENT_RANK2_REVIEW_STATUS.json), jointly approved without functional repairs. Their [shared control rules](DescentReviewChanges/ReviewBible/docs/mechanics/ENCHANTMENT_CONTROL_INTEGRATION_PLAYTEST.md) settle overlapping orders, ordinary attack budgets, control outside initiative and zone histories. Source preservation and catalog integration are being verified. The [development roadmap](DescentReviewChanges/ReviewBible/docs/mechanics/DEVELOPMENT_ROADMAP.md) identifies rank-three Enchantment as the next content priority; the pending Time Loop work below remains a separate integration track.""" + t[j:]
p.write_text(t, encoding='utf-8')

p = A / 'REVIEW_STATUS.md'
t = p.read_text(encoding='utf-8').replace('| Ordinary spells | 222 reviewed; 626 unfinished identities;', '| Ordinary spells | 229 reviewed; 619 unfinished identities;')
t += """
## Seven rank-two Enchantment identities completed

The [source conference](GPT_ENCHANTMENT_RANK2_SOURCE_CONFERENCE.md), [authoring clarification](GPT_ENCHANTMENT_RANK2_AUTHORING_CLARIFICATION.md) and [exact review](GPT_ENCHANTMENT_RANK2_EXACT_REVIEW.md) approve all seven cards and the shared Enchantment-control manuscript without functional card repairs. All three actual delivered attachments are preserved and match the locally prepared exact text.

The [shared integration](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/ENCHANTMENT_CONTROL_INTEGRATION_PLAYTEST.md) includes the binding clarification that normal real-turn start events still occur during the virtual-to-initiative transition. Control orders and already-spent behavior budgets do not repeat. One-shot instructions retain their own timing, competing for the same actual remaining budget. No previous operational spell or class card is rewritten.

The catalog now targets 229 reviewed identities and 619 unfinished; 184 unfinished have actual class rank0–3 access. All eight source placements/Core blocks and exact class access remain. The catalog retains 848 identities and 936 placements. Runtime, human balance, variants and whole-game closure remain open. No original source was deleted and GitHub was not pushed. Cosmology remains deferred until the authorized push and remote verification.
"""
p.write_text(t, encoding='utf-8')

p = R / 'data/playtest/game_development_coverage.json'
cov = read(p)
scopes = {
    'DD-02': 'Deep Mesmerize uses actual Stunned and positive post-defense/pre-temp-HP damage ending, preserving already-resolved attacks and unrelated condition sources.',
    'DD-03': 'Seven rank-two Enchantment cards and shared control-budget arbitration approved. Outside-initiative Dire/Crown share one cycle; first-real-turn control orders/budgets do not replay while ordinary actual start events still occur.',
    'DD-11': 'Seven rank-two Enchantment identities preserve eight placements/Core blocks and exact access. Zone of Truth retains actual Enchantment2/3RP and Divination4/7RP modes.229 reviewed/619 unfinished.',
    'DD-12': 'Rank-two Enchantment manuscripts and shared native Attack Action/component/zone-history procedures approved exactly;184 low-rank identities remain unfinished, plus higher ranks/variants/runtime/balance.',
    'DD-53': 'Dire/Crown orders and short Illusive Commands use existing permissions and resource/conduct limits. Group Pacify uses actual enemy snapshot and recognized-ally commitment provocation. No extra Actions are created.',
    'DD-54': 'Zone of Truth blocks deliberate false assertions without forced disclosure, objective truth or save-result diagnostics. Crown grants no remote sensory feed. Hidden eligibility remains paid resolution.'
}
for a in cov['aspects']:
    if a['id'] not in scopes:
        continue
    for key, path in [('reviewEvidence', review),
        ('draftEvidence', 'DescentReviewChanges/ReviewBible/data/playtest/spell_drafts/batch_enchantment_rank2.json'),
        ('draftEvidence', 'DescentReviewChanges/ReviewBible/docs/mechanics/ENCHANTMENT_CONTROL_INTEGRATION_PLAYTEST.md'),
        ('validationEvidence', 'DescentReviewChanges/ReviewBible/docs/mechanics/ENCHANTMENT_RANK2_REVIEW_STATUS.json')]:
        if path not in a[key]:
            a[key].append(path)
    a.setdefault('completedScopes', []).append(scopes[a['id']])
    if a['id'] in ['DD-11', 'DD-12']:
        a['openIssues'] = [s.replace('222 individual spell drafts reviewed;626 unfinished', '229 individual spell drafts reviewed;619 unfinished') for s in a['openIssues']]
    if a['id'] == 'DD-12':
        a['openIssues'].append('Dire Charm/Crown multiple attacks, non-concentration servant control, Deep Mesmerize, group pacification, fear suppression and Zone of Truth class-price discrepancy need human balance tests. Shared order/zone histories remain authored procedures, not certified runtime.')
dump(p, cov)
print(json.dumps({'promoted': 7, 'selected': sum(map(len, sel.values())), 'batchSha256': sha(b), 'sharedSha256': sha(shared_dest), 'functionalCardRepairs': 0, 'pipeline': 'pending'}, indent=2))

