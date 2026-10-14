"""Record bounded cross-package closures without promoting entire class cards."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
path=ROOT/'data/playtest/healing_remaining_bindings.json'
data=json.loads(path.read_text(encoding='utf-8'))
count=0
for package,guide,scope in [
    ('maximum_hp','MAXIMUM_HP_PLAYTEST.md','Maximum-HP/threshold role only'),
    ('redirection','DAMAGE_SHARING_PLAYTEST.md','Damage-sharing/prevention/retargeting role only'),
    ('healing_pulse','HEALING_PULSE_PLAYTEST.md','Recurring-healing scheduling or guard/exclusion role only'),
    ('device_lifecycle','DEVICE_LIFECYCLE_PLAYTEST.md','Device/Totem lifecycle, shared-command or guard/exclusion role only'),
    ('creature_lifecycle','CREATURE_LIFECYCLE_PLAYTEST.md','Selected creature lifecycle, command, dependency or guard role only; full form/tempHP effects excluded'),
    ('remaining_lifecycle','REMAINING_LIFECYCLE_PLAYTEST.md','Selected remaining lifecycle, object, command or guard role only; full tempHP/form/Time Loop effects excluded'),
    ('form_temphp','FORM_TEMP_HP_PLAYTEST.md','Selected form/tempHP grant, identity, lifecycle, payment, clock or guard role only; named deferred components and full card/runtime completion excluded')]:
    register=json.loads((ROOT/f'data/playtest/{package}_bindings.json').read_text(encoding='utf-8'))
    by_source={(b['sourcePath'],str(b['sourceId'])):b for b in register['bindings']}
    for row in data['bindings']:
        match=by_source.get((row['sourcePath'],str(row['sourceId'])))
        if not match:continue
        if package in ('creature_lifecycle','remaining_lifecycle','form_temphp') and not match['status'].startswith('REVIEWED'):continue
        assert match['sourceSha256']==row['sourceSha256']
        links=row.setdefault('reviewedInterfaces',[])
        item={'package':package,'scope':scope,'guide':'docs/mechanics/'+guide,'reviewEvidence':register['reviewClosure']}
        if item not in links:links.append(item);count+=1
        row['openIssues']=[v for v in row['openIssues'] if v!='Implement/verify relevant interface or record a bounded exclusion before broader closure.']
        issue='See reviewedInterfaces for bounded closures; other card components retain their own unfinished review requirements.'
        if issue not in row['openIssues']:row['openIssues'].append(issue)
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Linked',count,'bounded interfaces without changing whole-card statuses.')
