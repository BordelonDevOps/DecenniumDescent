"""Historical candidate-stage record; do not rerun after a later disposition."""
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
path=ROOT/'data/playtest/redirection_bindings.json'
data=json.loads(path.read_text(encoding='utf-8'))
tinker=json.loads((ROOT/'data/public/class_playtests/tinker.json').read_text(encoding='utf-8'))
data['supportingSources']=[{'sourcePath':'data/public/class_playtests/tinker.json','engineIndex':i,
                          'text':tinker['engine'][i],'sha256':hashlib.sha256(tinker['engine'][i].encode()).hexdigest()}
                         for i in (1,2)]
data['status']='IN_REVIEW'
data['implementationEvidence']=['tools/redirection_playtest_rules.py','docs/mechanics/REDIRECTION_PLAYTEST_VALIDATION.json']
for b in data['bindings']:
    b['status']='SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface'
    b['reviewEvidence'].append('GPT_REDIRECTION_BOUNDARIES.md')
    b['operationalOverrides']=['Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.']
    b['openIssues']=['Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface.']
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Mark exactly three reviewed primitives within the much larger131 discussion.
path=ROOT/'data/playtest/healing_remaining_bindings.json'
data=json.loads(path.read_text(encoding='utf-8'))
ids={'oracle.supplement.flame.crown-s-burn':'pooled/shared healing with locked activation recipients',
     'oracle.supplement.flame.zealot-s-renewal':'minimum resolved backlash damage',
     'mirrorsage.arch.dual-echo-cast':'two-Mend numeric components'}
for b in data['bindings']:
    if b['sourceId'] in ids:
        b['status']='REVIEWED / reference-VALIDATED: '+ids[b['sourceId']]+' only'
        b['reviewEvidence'].append('GPT_HEALING_EXTENSIONS_CLOSURE.md')
        b['operationalOverrides'].append('Exact helper in healing_source_extensions.py;21 reference checks. Crown recipients fixed at activation, with no denominator recomputation or replacement after lost eligibility.')
        b['openIssues']=['Other components, full source lifecycle and broader scheduler/copy interfaces remain outside this primitive closure.']
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Recorded candidate redirection and three bounded healing closures without modifying sources.')
