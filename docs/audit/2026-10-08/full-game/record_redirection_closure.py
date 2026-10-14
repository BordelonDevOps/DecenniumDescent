"""Historical bounded closure transition; not a general build."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
path=ROOT/'data/playtest/redirection_bindings.json'
data=json.loads(path.read_text(encoding='utf-8'))
data['status']='REVIEWED / reference-VALIDATED; bounded interface'
data['reviewClosure']='docs/audit/2026-10-08/full-game/GPT_REDIRECTION_FINAL_CLOSURE.md'
for b in data['bindings']:
    b['status']='REVIEWED / reference-VALIDATED: bounded damage-sharing role only'
    b['reviewEvidence'].append('GPT_REDIRECTION_FINAL_CLOSURE.md')
    b['operationalOverrides'].append('Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.')
    b['openIssues']=['Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.']
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
path=ROOT/'data/playtest/game_development_coverage.json'
data=json.loads(path.read_text(encoding='utf-8'))
row=next(r for r in data['aspects'] if r['id']=='DD-24')
row['reviewEvidence'].append('docs/audit/2026-10-08/full-game/GPT_REDIRECTION_FINAL_CLOSURE.md')
row['openIssues']=[x for x in row['openIssues'] if 'Obtain final bounded disposition' not in x]
row['completedScopes'].append('39-source redirection interface plus2Tinker engines jointly reviewed:94 checks and186 conservation states. Broader defense/companion/global trigger engine remains open.')
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
path=HERE/'REVIEW_STATUS.md'
text=path.read_text(encoding='utf-8').replace('The [final disposition](CODEX_REDIRECTION_FINAL_DISPOSITION.md) is submitted with94 checks/186 conservation states and preserved original source objects; bounded approval is pending.',
    'The [final disposition](CODEX_REDIRECTION_FINAL_DISPOSITION.md) and [GPT closure](GPT_REDIRECTION_FINAL_CLOSURE.md) close this bounded interface with94 checks/186 conservation states and preserved original source objects.')
path.write_text(text,encoding='utf-8')
print('Recorded bounded redirection closure; wider domains remain open.')
