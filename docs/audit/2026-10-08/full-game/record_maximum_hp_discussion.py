"""Historical first maximumHP discussion capture; not a general build."""
from pathlib import Path
import re,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
text=(HERE/'GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md').read_text(encoding='utf-8')
pattern='^\\| '+chr(96)+'([^'+chr(96)+']+)'+chr(96)+' \\| ([^|]+) \\| (.+) \\|$'
roles={m[0]:(m[1].strip(),m[2].strip()) for m in re.findall(pattern,text,re.M)}
assert len(roles)==58,len(roles)
path=ROOT/'data/playtest/maximum_hp_bindings.json'
data=json.loads(path.read_text(encoding='utf-8'))
for b in data['bindings']:
    role,note=roles[b['bindingId']]
    b.update(status='DISCUSSED; precise boundaries / implementation pending',classification=role,
             operationalOverrides=[note],reviewEvidence=['GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md'],
             openIssues=['First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted.'])
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('All58 individual maximumHP/threshold discussion classifications preserved.')
