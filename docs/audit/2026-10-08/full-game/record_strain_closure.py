from pathlib import Path
import json
GAME=Path(__file__).resolve().parents[4]
ROOT=GAME/'DescentReviewChanges/ReviewBible'
AUDIT=Path(__file__).resolve().parent
EVIDENCE='docs/audit/2026-10-08/full-game/GPT_STRAIN_FINAL_REVIEW.md'
p=ROOT/'data/playtest/strain_bindings.json'
data=json.loads(p.read_text(encoding='utf-8'))
data['status']='REVIEWED / reference-VALIDATED in supplied bounded scope'
if EVIDENCE not in data['reviewEvidence']:
    data['reviewEvidence'].append(EVIDENCE)
data['openIssues']=['Broader rest rewards, travel, class resource semantics, future sources, resurrection at expedition6 and human balance remain separate open gates.']
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=ROOT/'data/playtest/game_development_coverage.json'
data=json.loads(p.read_text(encoding='utf-8'))
for row in data['aspects']:
    if row['number'] in (16,40,41):
        scope='Supplied serum/expedition Strain namespace, penalties, gain/cap transitions, Dash clocks, maxHP composition and generic recovery bookkeeping reviewed with GPT;71 transition checks,30 source checks and4949 maxHP scenarios pass. Broad domain remains open.'
        if scope not in row.setdefault('completedScopes',[]):
            row['completedScopes'].append(scope)
        additions={'reviewEvidence':[EVIDENCE],
                   'draftEvidence':['DescentReviewChanges/ReviewBible/docs/mechanics/STRAIN_PLAYTEST.md','DescentReviewChanges/ReviewBible/data/playtest/strain_bindings.json'],
                   'validationEvidence':['DescentReviewChanges/ReviewBible/docs/mechanics/STRAIN_PLAYTEST_VALIDATION.json']}
        for field,values in additions.items():
            for value in values:
                if value not in row[field]:
                    row[field].append(value)
    if row['number']==16:
        row['openIssues'][0]='Complete root/slow/mark and curse/disease metadata and exhaustive semantic coverage across active class/spell effects. Bounded generic conditions, periodic families and Strain namespacing are reviewed; DD16 remains open.'
    if row['number']==24:
        issue='Resolve actual resurrection with expedition6 still present and death-replacement features under HP prohibition; Strain reduction itself never revives.'
        if issue not in row['openIssues']:
            row['openIssues'].append(issue)
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=ROOT/'data/playtest/custom_condition_bindings.json'
data=json.loads(p.read_text(encoding='utf-8'))
data['openIssues']=[s for s in data['openIssues'] if not s.startswith('Reconcile Warrior serum Strain')]
scope={'id':'strain-namespace-2026-10-08','name':'Strain namespaces (separate reference)',
       'status':'REVIEWED / reference-VALIDATED',
       'scope':'See STRAIN_PLAYTEST.md for the separate serum0–3 and expedition0–6 systems. These are not additional periodic-family records or generic Exhaustion.',
       'reviewEvidence':EVIDENCE}
data['completedScopes']=[s for s in data.get('completedScopes',[]) if s['id']!=scope['id']]+[scope]
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=AUDIT/'REVIEW_STATUS.md'
text=p.read_text(encoding='utf-8')
text+='\n## Strain bounded closure\n\nThe [Strain reference](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/STRAIN_PLAYTEST.md) now separates Warrior serum0–3 from expedition0–6, corrects the level2 attack/save placement, preserves rest reward caps and closes replay/overflow/Dash-clock gaps. The [exact GPT review](GPT_STRAIN_FINAL_REVIEW.md) closes this supplied scope. Validation passes71 transition checks,30 exact source checks and4,949 maximumHP scenarios. DD16, Expedition/rest, all-source class integration, resurrection at expedition6 and human balance remain open.\n\nNext: source-qualified roots/slows/marks, curse/disease metadata and remaining physical control; see [next control notes](NEXT_CONTROL_REVIEW_NOTES.md).\n'
p.write_text(text,encoding='utf-8')
print('Recorded bounded Strain closure; full-game and broader domain gates remain open.')
