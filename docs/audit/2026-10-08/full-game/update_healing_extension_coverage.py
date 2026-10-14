"""Historical coverage update for extension closure / redirection review stage."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
path=ROOT/'data/playtest/game_development_coverage.json'
data=json.loads(path.read_text(encoding='utf-8'))
row=next(r for r in data['aspects'] if r['id']=='DD-24')
row['status']='selected-interfaces-closed-remainder-integrating'
for field,values in {
 'reviewEvidence':['GPT_HEALING_REMAINING_CORRECTIONS.md','GPT_HEALING_EXTENSIONS_CLOSURE.md','GPT_REDIRECTION_BOUNDARIES.md','GPT_REDIRECTION_IMPLEMENTATION_FINDINGS.md'],
 'sourceEvidence':['REDIRECTION_SOURCE_CANDIDATES.json','MAXIMUM_HP_SOURCE_CANDIDATES.json'],
 'draftEvidence':['HEALING_SOURCE_EXTENSIONS.md','HEALING_REMAINING_SOURCE_BINDINGS.md','DAMAGE_SHARING_PLAYTEST.md','REDIRECTION_SOURCE_BINDINGS.md'],
 'validationEvidence':['HEALING_EXTENSION_VALIDATION.json','HEALING_REMAINING_SOURCE_VALIDATION.json','REDIRECTION_PLAYTEST_VALIDATION.json','REDIRECTION_SOURCE_VALIDATION.json']
}.items():
    prefix='docs/audit/2026-10-08/full-game/' if field in ('reviewEvidence','sourceEvidence') else 'DescentReviewChanges/ReviewBible/docs/mechanics/'
    for v in values:
        v=prefix+v
        if v not in row[field]:row[field].append(v)
row['openIssues']=[
 'All131 remaining class passages discussed; implement remaining paid pulse/zone schedule, maximum-HP composition, companion/device/tempHP and complete copy/provenance interfaces.',
 'Obtain final bounded disposition for corrected39-source redirection candidate;94 checks/186 conservation states currently PASS.',
 'Audit healing content in other domains; complete broader body/soul/affliction procedures.',
 'Complete temporal topology/equipment/clock package; selected participant field checks are not complete Time Loop execution.']
for scope in (
 'Selected153-source healing/death interface jointly reviewed:164 targeted checks plus120 unchanged Core damage states; six reviewed ordinary spells promoted.',
 'Three selected primitives from131-source remainder reviewed: Zealot backlash, locked-recipient Crown Burn shared healing and Dual Echo two-Mend components;21 checks.'):
    if scope not in row['completedScopes']:row['completedScopes'].append(scope)
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Recorded scoped closures; DD24 and whole-game closure remain open.')
