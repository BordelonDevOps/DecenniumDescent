"""Record the bounded notebook disposition; preserve all broader open gates."""
from pathlib import Path
import json

GAME=Path(__file__).resolve().parents[4]
ROOT=GAME/'DescentReviewChanges/ReviewBible'
AUDIT=Path(__file__).resolve().parent
EVIDENCE='docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md'

p=ROOT/'data/playtest/custom_condition_bindings.json'
data=json.loads(p.read_text(encoding='utf-8'))
scope={'id':'periodic-family-2026-10-08', 'name':'Periodic family integration',
       'status':'REVIEWED / reference-VALIDATED',
       'scope':'The 32 registered periodic profiles and their shared family, cure, immunity, refresh and source-qualified hook interfaces. The registry as a whole, full-engine application and human balance remain open.',
       'reviewEvidence':EVIDENCE}
scopes=data.setdefault('completedScopes',[])
scopes[:]=[s for s in scopes if s['id']!=scope['id']]+[scope]
for d in data['definitions']:
    if 'periodic' in d:
        d['status']='REVIEWED / reference-VALIDATED within periodic-family scope; broader registry IN_PROGRESS'
        if EVIDENCE not in d['reviewEvidence']:
            d['reviewEvidence'].append(EVIDENCE)
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

p=ROOT/'data/playtest/game_development_coverage.json'
data=json.loads(p.read_text(encoding='utf-8'))
for row in data['aspects']:
    if row['number']==16:
        row['openIssues'][0]='Complete root/slow/mark and curse/disease metadata, Strain namespace reconciliation and exhaustive semantic coverage across active class/spell effects. The bounded periodic-family package is reviewed and reference-validated; DD16 remains open.'
        s='The 32 registered periodic profiles and their shared family/cure/immunity/refresh interfaces reviewed with GPT and reference-validated (84 selected checks; 114 exact source references across the current registry).'
        if s not in row['completedScopes']:
            row['completedScopes'].append(s)
        if EVIDENCE not in row['reviewEvidence']:
            row['reviewEvidence'].append(EVIDENCE)
    if row['number'] in (3,17,18,19,20,21):
        for e in (EVIDENCE,'docs/audit/2026-10-08/full-game/CODEX_COMBAT_COUNTEREXAMPLES.md'):
            if e not in row['reviewEvidence']:
                row['reviewEvidence'].append(e)
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

p=AUDIT/'REVIEW_STATUS.md'
text=p.read_text(encoding='utf-8').replace('Final bounded confirmation is pending; this does not close all DD16.', 'The [bounded GPT disposition](GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md) confirms this periodic package as REVIEWED / reference-VALIDATED. This does not close all DD16.')
text += '\nThe [first combat proposal](GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md) is preserved. The [counterexample conference](CODEX_COMBAT_COUNTEREXAMPLES.md) challenges movement-cost refunds, free Pin/Silence riders, start-turn death-save ordering, Hide ties, Ready costs and duration anchors before implementation.\n'
p.write_text(text,encoding='utf-8')
p=AUDIT/'CUSTOM_RIDER_WORKING_DECISIONS.md'
text=p.read_text(encoding='utf-8')
text+='\n## Bounded periodic closure\n\nThe [GPT disposition](GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md) confirms the periodic-family package as REVIEWED / reference-VALIDATED after the two material fixes. The overall registry remains IN_PROGRESS, with roots/slows/marks, curse/disease metadata, Strain namespacing and semantic completeness outstanding.\n'
p.write_text(text,encoding='utf-8')
print('Recorded bounded periodic closure; registry and whole-game gates remain open.')
