"""Record completed bounded spell promotion and preserve wider open work."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent;GAME=HERE.parents[3];ROOT=GAME/'DescentReviewChanges/ReviewBible'
closure='docs/audit/2026-10-08/full-game/GPT_TRANSFORMATION_SPELL_FINAL_CLOSURE.md'
assert 'Eligible for provisional catalog promotion' in (GAME/closure).read_text(encoding='utf-8')
manifest=json.loads((ROOT/'data/public/spell_playtests/manifest.json').read_text(encoding='utf-8'))
assert manifest['operationalDrafts']==83 and manifest['blocked']==765
path=ROOT/'data/playtest/game_development_coverage.json';coverage=json.loads(path.read_text(encoding='utf-8'))
for r in coverage['aspects']:
    if r['id'] not in ('DD-08','DD-09','DD-11','DD-12','DD-21','DD-24','DD-26','DD-27','DD-35'):continue
    assert r['closure']=='open'
    r['reviewEvidence']=list(dict.fromkeys(r['reviewEvidence']+[closure]))
    r['openIssues']=[v for v in r['openIssues'] if not v.startswith('Five-spell candidate implemented')]
    r['openIssues']=[v.replace('Five named transformation/buffer spell source conference is in progress.','Five named transformation/buffer spells are now reviewed and promoted; broader catalog work remains.') for v in r['openIssues']]
    note='Five ordinary spell interfaces closed and promoted: Harmonic Bulwark, Polymorph, Shapechange, True Polymorph and Mass Polymorph;12 profiles,216 checks and729 spatial scenarios. Original848 IDs/936 placements preserved;83 operational/765 unfinished. Geometry/item/attack-taxonomy/runtime/balance remain bounded exclusions.'
    if note not in r.setdefault('completedScopes',[]):r['completedScopes'].append(note)
    r['status']='selected-interfaces-closed-remainder-integrating'
for r in coverage['aspects']:
    if r['id']=='DD-14':
        evidence='docs/audit/2026-10-08/full-game/GPT_BUFFER_FEAT_FIRST_REVIEW.md'
        r['reviewEvidence']=list(dict.fromkeys(r['reviewEvidence']+[evidence]))
        note='Eight complete source-discussed feat proposals exist: Chef, Inspiring Leader, Empowered Summoning, Field Medic, Blood Ritual, Necrotic Affinity, Lifeleech and Soul Cage. External dependency audit, implementation and independent validation remain pending; no feat promoted.'
        if note not in r['openIssues']:r['openIssues'].append(note)
path.write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name in ('README.md','REVIEW_STATUS.md'):
    path=HERE/name;text=path.read_text(encoding='utf-8');marker='## Five-spell bounded closure and provisional promotion'
    if marker not in text:
        text+='\n'+marker+'\n\n[Actual GPT closure](GPT_TRANSFORMATION_SPELL_FINAL_CLOSURE.md) approved the corrected216-check/729-scenario package. Five spells and12 finite profiles are promoted provisionally: active catalog83, unfinished765, all848 IDs/936 placements preserved. The catalog passes42 checks/89,040 access boundaries; historical175-source form integrity passes with five exact reviewed overlay-evolution records. Original spell/Core/class files are unchanged. Wider geometry, item/anatomy matrix, attack taxonomy, full runtime, balance and human playtests remain open.\n\nThe [eight-feat first proposals](GPT_BUFFER_FEAT_FIRST_REVIEW.md) are now source-discussed candidate designs. Read external dependencies before implementation; no feat is promoted. The [exact Soul Bind support](BUFFER_FEAT_SOUL_DEPENDENCY.json) is prepared to reconcile the proposed residue resource with existing resurrection restrictions.\n'
        path.write_text(text,encoding='utf-8')
path=ROOT/'docs/mechanics/FORM_TEMP_HP_PLAYTEST.md';text=path.read_text(encoding='utf-8')
text+='\nThe five originally deferred ordinary spells now have a [separately reviewed and promoted interface](TRANSFORMATION_SPELL_PLAYTEST.md), with216 checks and729 spatial scenarios. Their historical source snapshots remain unchanged and exact approved overlay evolution is validated. Four originally named components still require completion: Time Loop and the full Chef, Inspiring Leader and Soul Cage feat clauses; the latter belong to the eight-feat development batch.\n'
path.write_text(text,encoding='utf-8')
print('Recorded actual five-spell closure/promotion and eight-feat source discussion; no whole domain falsely closed.')
