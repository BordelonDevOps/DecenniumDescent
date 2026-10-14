"""Record actual scoped feat closure and prepare the next exact conference."""
from pathlib import Path
import json
AUDIT=Path(__file__).resolve().parent;GAME=AUDIT.parents[3];ROOT=GAME/'DescentReviewChanges/ReviewBible'
closure='docs/audit/2026-10-08/full-game/GPT_BUFFER_FEAT_FINAL_CLOSURE.md'
assert (ROOT/'data/playtest/feat_drafts/batch_buffers.json').exists()
path=ROOT/'data/playtest/game_development_coverage.json';data=json.loads(path.read_text(encoding='utf-8'))
snapshot=AUDIT/'COVERAGE_BEFORE_BUFFER_FEAT_CLOSURE.json'
assert not snapshot.exists(),'Closure already recorded'
snapshot.write_bytes(path.read_bytes())
for row in data['aspects']:
    if row['id'] in ('DD-14','DD-24','DD-28','DD-35','DD-41','DD-50','DD-69','DD-70'):
        row['reviewEvidence']=list(dict.fromkeys(row['reviewEvidence']+[closure]))
        note='Eight complete feat interfaces reviewed and provisionally promoted: Chef, Inspiring Leader, Empowered Summoning, Field Medic, Blood Ritual, Necrotic Affinity, Lifeleech and Soul Cage;131 targeted checks/2,520 funding boundary cases. All335 original objects preserved. Remaining327 feats, full economy/recipes/soul taxonomy/runtime and human balance remain open.'
        row.setdefault('completedScopes',[]).append(note)
    if row['id']=='DD-14':
        row['status']='eight-full-feats-reviewed-remainder-open'
        row['openIssues']=[i for i in row['openIssues'] if not i.startswith('Eight full feat candidates now have')]
        row['openIssues'].append('Complete the remaining327 feat source objects; current full-feat overlay8/335 reviewed. Keep class selections, ordinary Soul Cage spell and Soulrender whole-soul ritual distinct.')
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name in ('README.md','REVIEW_STATUS.md'):
    path=AUDIT/name;text=path.read_text(encoding='utf-8')
    text+='\n## Eight-feat bounded closure and provisional promotion\n\nThe [actual completed GPT audit](GPT_BUFFER_FEAT_FINAL_CLOSURE.md) found no remaining reproducible blocker and explicitly closed all printed clauses plus the labeled operational bridges for the eight feats. The [active feat index](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/FEAT_PLAYTEST_INDEX.md) now preserves335 source objects and distinguishes8 reviewed/327 unfinished. Validation passes131 targeted checks and2,520 funding boundary cases. Source/legacy records remain unchanged. The previously deferred Chef, Inspiring Leader and Soul Cage form/buffer roles are closed; Time Loop world conservation remains the single original deferred component. Human balance and broad systems remain open.\n'
    path.write_text(text,encoding='utf-8')
path=ROOT/'docs/mechanics/FORM_TEMP_HP_PLAYTEST.md';text=path.read_text(encoding='utf-8')
text=text.replace('Four originally named components still require completion: Time Loop and the full Chef, Inspiring Leader and Soul Cage feat clauses; the latter belong to the eight-feat development batch.',
 'The full Chef, Inspiring Leader and Soul Cage clauses are now [separately reviewed and provisionally promoted](BUFFER_FEAT_PLAYTEST.md) within the complete eight-feat package. Time Loop world conservation is the single remaining originally deferred component.')
path.write_text(text,encoding='utf-8')
for rel in ('START_HERE.md','DescentReviewChanges/ReviewBible/docs/mechanics/DEVELOPMENT_ROADMAP.md'):
    path=GAME/rel;text=path.read_text(encoding='utf-8')
    text+='\n### Eight-feat reviewed playtest overlay\n\nChef, Inspiring Leader, Empowered Summoning, Field Medic, Blood Ritual, Necrotic Affinity, Lifeleech and the Soul Cage feat are reviewed in full with131 targeted checks and2,520 funding cases. All335 original records are preserved:8 reviewed/327 unfinished. '
    link='DescentReviewChanges/ReviewBible/docs/mechanics/FEAT_PLAYTEST_INDEX.md' if rel=='START_HERE.md' else 'FEAT_PLAYTEST_INDEX.md'
    text+='[Current feat index]('+link+'). The next source conference addresses Time Loop world/body/inventory/clock conservation; this is not whole-game completion.\n'
    path.write_text(text,encoding='utf-8')
for name in ('FEAT_REGISTRY_STATUS.md','FEAT_REGISTRY_PLAN.md'):
    path=ROOT/'docs/feats'/name;text=path.read_text(encoding='utf-8')
    text+='\n## Current full-clause review overlay\n\nThe eight-feat authored scope is now REVIEWED / reference-VALIDATED and provisionally promoted. [Active index](../mechanics/FEAT_PLAYTEST_INDEX.md):8 full feats reviewed,327 unfinished,335 original objects preserved. [Rules](../mechanics/BUFFER_FEAT_PLAYTEST.md) and [validation](../mechanics/BUFFER_FEAT_PLAYTEST_VALIDATION.json) record131 checks/2,520 cases. Historical registry flags and earlier pending-review notes are superseded only for these eight IDs; no global completion is implied.\n'
    path.write_text(text,encoding='utf-8')
prepared=(AUDIT/'CODEX_TEMPORAL_WORLD_CONFERENCE_PREPARED.md').read_text(encoding='utf-8')
prepared=prepared.replace('— PREPARED, not yet sent','— exact source conference')
prepared=prepared.replace('The eight feats are in a separate implementation review. Do not infer their approval here.',
 'Your completed eight-feat audit found no remaining reproducible blocker and explicitly closed their bounded authored scope (131 checks/2,520 cases). They are now in the provisional playtest overlay; all335 original feat objects remain unchanged. The exact closure is GPT_BUFFER_FEAT_FINAL_CLOSURE.md.')
prepared=prepared.replace('These eight-feat candidate interactions must eventually match the actual final review; no review status is assumed.',
 'The reviewed eight-feat scope now supplies these interactions; preserve its finite resources and event identities.')
prepared+='\n## Exact completed eight-feat disposition\n\n'+(AUDIT/'GPT_BUFFER_FEAT_FINAL_CLOSURE.md').read_text(encoding='utf-8')
(AUDIT/'CODEX_TEMPORAL_WORLD_CONFERENCE.md').write_text(prepared,encoding='utf-8')
print('Recorded scoped closure and prepared actual next conference; every broader area remains visible.')
