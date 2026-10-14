"""Historical bounded closure transition, not a general rebuilding command."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
path=ROOT/'data/playtest/healing_pulse_bindings.json'
data=json.loads(path.read_text(encoding='utf-8'))
data['status']='REVIEWED / reference-VALIDATED; bounded100+6-source interface'
data['reviewClosure']='docs/audit/2026-10-08/full-game/GPT_HEALING_PULSE_FINAL_CLOSURE.md'
for row in data['bindings']:
    row['status']='REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only'
    row['reviewEvidence'].extend(['GPT_HEALING_PULSE_IMPLEMENTATION_FINDINGS.md','GPT_HEALING_PULSE_FINAL_CLOSURE.md'])
    row['operationalOverrides'].append('Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.')
    row['openIssues']=['Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.']
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
path=ROOT/'data/playtest/healing_pulse_profiles.json'
data=json.loads(path.read_text(encoding='utf-8'))
data['status']='REVIEWED / reference-VALIDATED; internal aliases for supplied sources'
data['reviewEvidence'].append('GPT_HEALING_PULSE_FINAL_CLOSURE.md')
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
path=ROOT/'data/playtest/game_development_coverage.json'
data=json.loads(path.read_text(encoding='utf-8'))
row=next(r for r in data['aspects'] if r['id']=='DD-24')
row['reviewEvidence'].append('docs/audit/2026-10-08/full-game/GPT_HEALING_PULSE_FINAL_CLOSURE.md')
row['validationEvidence'].append('DescentReviewChanges/ReviewBible/docs/mechanics/HEALING_PULSE_PROFILE_PROVENANCE.json')
row['completedScopes'].append('Recurring healing/pulse100-source roles plus6 supporting passages jointly reviewed:89 checks,301 reserve partitions and33 source-linked internal aliases. Full card behavior, companion commands, object lifecycle and other catalogs remain open.')
row['openIssues']=[v for v in row['openIssues'] if not v.startswith('100 pulse sources plus6')]
row['openIssues'].append('Next device/Totem lifecycle conference has74 exact passages plus3 shared paragraphs, including previously unsupplied MagneticWall interception. Wider healing, companion, temporaryHP and copy interfaces remain open.')
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for path in (HERE/'README.md',HERE/'REVIEW_STATUS.md'):
    with path.open('a',encoding='utf-8') as f:
        f.write('\n## Healing-pulse bounded closure\n\nThe [corrected exact disposition](CODEX_HEALING_PULSE_FINAL_DISPOSITION.md) received [GPT closure](GPT_HEALING_PULSE_FINAL_CLOSURE.md):100 class roles,6 supporting passages,89 targeted checks,301 reserve partitions and33 source-linked profile aliases. Each-fixed-target sources still require all currently eligible fixed recipients. This closes only the supplied scheduling/role interface. The next prepared device/Totem packet now has74 sources (73 lexical plus Magnetic Wall semantic supplement) and3 shared paragraphs; the earlier73 count excluded that added card. Original sources remain preserved.\n')
path=ROOT/'docs/mechanics/DEVELOPMENT_ROADMAP.md'
with path.open('a',encoding='utf-8') as f:
    f.write('\n- [Recurring healing, zones and upkeep](HEALING_PULSE_PLAYTEST.md):100 roles plus6 supporting passages;89 checks,301 reserve partitions and33 source-linked aliases. [GPT closure](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_PULSE_FINAL_CLOSURE.md) applies only to this bounded interface. Device/Totem lifecycle is next.\n')
path=ROOT.parents[1]/'START_HERE.md'
with path.open('a',encoding='utf-8') as f:
    f.write('\nThe selected [recurring healing and zone schedules](DescentReviewChanges/ReviewBible/docs/mechanics/HEALING_PULSE_PLAYTEST.md) are jointly reviewed:100 source roles plus6 supporting passages,89 checks and301 reserve partitions. All33 internal profiles link to supplied abilities; none adds a new spell or class card. Companion/device lifecycle and wider game development continue.\n')
print('Recorded bounded pulse closure; game remains active and incomplete.')
