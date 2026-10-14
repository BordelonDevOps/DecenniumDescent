"""Historical closure transition. Do not use as a general build."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
path=ROOT/'data/playtest/maximum_hp_bindings.json'
data=json.loads(path.read_text(encoding='utf-8'))
data['status']='REVIEWED / reference-VALIDATED; bounded interface'
data['reviewClosure']='docs/audit/2026-10-08/full-game/GPT_MAXIMUM_HP_FINAL_CLOSURE.md'
for b in data['bindings']:
    b['status']='REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only'
    for evidence in ('GPT_MAXIMUM_HP_BOUNDARIES.md','GPT_MAXIMUM_HP_FINAL_CLOSURE.md'):
        if evidence not in b['reviewEvidence']: b['reviewEvidence'].append(evidence)
    b['operationalOverrides'].append('Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.')
    b['openIssues']=['Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.']
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
path=ROOT/'data/playtest/game_development_coverage.json'
data=json.loads(path.read_text(encoding='utf-8'))
row=next(r for r in data['aspects'] if r['id']=='DD-24')
row['reviewEvidence'].append('docs/audit/2026-10-08/full-game/GPT_MAXIMUM_HP_FINAL_CLOSURE.md')
row['completedScopes'].append('58-source maximum-HP/threshold interface jointly reviewed:60 targeted checks and909 systemic states. Guide records global Monk arbitration, compatible bonuses, capacity clamps, exact thresholds and historical event predicates; wider advancement/companion/feat lifecycle remains open.')
for value in ('DescentReviewChanges/ReviewBible/docs/mechanics/MAXIMUM_HP_PLAYTEST.md','DescentReviewChanges/ReviewBible/docs/mechanics/MAXIMUM_HP_PLAYTEST_VALIDATION.json'):
    if value not in row['sourceEvidence']:row['sourceEvidence'].append(value)
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for path in (HERE/'README.md',HERE/'REVIEW_STATUS.md'):
    with path.open('a',encoding='utf-8') as f:
        f.write('\n## Maximum-HP bounded closure\n\nThe [exact implementation](CODEX_MAXIMUM_HP_IMPLEMENTATION_REVIEW.md) received [GPT closure](GPT_MAXIMUM_HP_FINAL_CLOSURE.md) for58 source records,60 checks and909 systemic states. The [boundary reply](GPT_MAXIMUM_HP_BOUNDARIES.md) supplies the missing first-review tail and corrects global Monk trauma and independent Deathless clocks. This closes the supplied maximum-HP/threshold roles; character advancement, companion/control lifecycle, unsupplied modifiers and whole-game development remain open. The next conference covers recurring healing pulses, zones and upkeep.\n')
path=HERE/'README.md'
value=path.read_text(encoding='utf-8').replace('Discussion and implementation are pending.','This historical submission has since reached the bounded closure recorded below.')
path.write_text(value,encoding='utf-8')
path=ROOT/'docs/mechanics/DEVELOPMENT_ROADMAP.md'
value=path.read_text(encoding='utf-8').replace('Zone scheduling, maximum-HP composition, companion/device lifecycle and complete copy semantics remain open.','Zone scheduling, companion/device lifecycle and complete copy semantics remain open; the selected maximum-HP interface is closed below.').replace('The next conference supplies51 class and7 feat passages for maximum-HP composition.','')
value+='\n- [Maximum-HP and exact thresholds](MAXIMUM_HP_PLAYTEST.md):58 supplied records,60 targeted checks and909 systemic states; [GPT closure](../../../../docs/audit/2026-10-08/full-game/GPT_MAXIMUM_HP_FINAL_CLOSURE.md). Other advancement, companion and modifier sources remain open.\n'
path.write_text(value,encoding='utf-8')
path=ROOT.parents[1]/'START_HERE.md'
with path.open('a',encoding='utf-8') as f:
    f.write('\nThe selected [maximum-HP and threshold interface](DescentReviewChanges/ReviewBible/docs/mechanics/MAXIMUM_HP_PLAYTEST.md) is now jointly reviewed:58 source records,60 checks and909 systemic states. This is one bounded part of the continuing full-game review.\n')
print('Recorded maximum-HP bounded closure.')
