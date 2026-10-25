import json, math, sys
from pathlib import Path

# Independent read-only inspection of serialized return data. No return code imports.
root = Path(sys.argv[1]).resolve()
issues, counts = [], {'cases': 0, 'events': 0, 'states': 0, 'paidCasts': 0, 'damageRecords': 0}
def issue(where, message, values=None):
    issues.append({'pointer': where, 'finding': message, 'values': values})
def check(ok, where, message, values=None):
    if not ok: issue(where, message, values)
def close(a,b): return abs(a-b) < 1e-7

def inspect_case(c, loc):
    counts['cases'] += 1
    events=c['timeline']; times=[e['time'] for e in events]
    check(times==sorted(times),loc,'Case events are not chronological',times)
    defs=c.get('actorDefinitions',{})
    for aid, a in defs.items():
        level=a.get('classLevel',a.get('level'))
        for k in ['automaticCards','completeAutomaticCardsAtApplicableGates']:
            for i, raw in enumerate(a.get(k,[])):
                card=raw.get('completeCard',raw)
                if isinstance(level,(int,float)) and card.get('minimumClassLevel',0)>level:
                    issue(f'{loc}/actorDefinitions/{aid}/{k}/{i}','Actor contains an automatic card above its actual class level',{'level':level,'card':card.get('id'),'minimum':card.get('minimumClassLevel')})
        for i, acquisition in enumerate(a.get('selectedAcquisition',[])):
            if isinstance(level,(int,float)) and acquisition.get('classLevel',0)>level:
                issue(f'{loc}/actorDefinitions/{aid}/selectedAcquisition/{i}','Actor contains acquisition history above its class level')
    for i,e in enumerate(events):
        counts['events']+=1; p=f'{loc}/timeline/{i}'
        before,after=e['before'],e['after']
        def inspect_observation(value, where):
            if isinstance(value, dict):
                if isinstance(value.get('id'), str) and value['id'] in after.get('sources', {}):
                    actual = after['sources'][value['id']]
                    if len(set(value) & set(actual)) > 3:
                        check(value == actual, where, 'Embedded source observation differs from this event after-state', value['id'])
                for key, child in value.items(): inspect_observation(child, where+'/'+key)
            elif isinstance(value, list):
                for idx, child in enumerate(value): inspect_observation(child, where+'/'+str(idx))
        inspect_observation(e.get('observations', {}), p+'/observations')
        for which,st in [('before',before),('after',after)]:
            counts['states']+=1
            for aid,a in st.get('actors',{}).items():
                ap=f'{p}/{which}/actors/{aid}'
                for current,maximum in [('HP','maxHP'),('RP','maxRP')]:
                    if current in a and maximum in a:
                        check(0<=a[current]<=a[maximum],ap,f'{current} outside current capacity',{current:a[current],maximum:a[maximum]})
                if a.get('life')=='dead': check(a.get('HP')==0,ap,'Dead actor has positive HP')
                check(a.get('Dissonance',0)>=0,ap,'Negative Dissonance')
        added={k:v for k,v in after.get('castLedger',{}).items() if k not in before.get('castLedger',{})}
        charges={}
        for cid,r in added.items():
            counts['paidCasts']+=1
            owner=r['owner'];charges[owner]=charges.get(owner,0)+r['actualPaid']
            plan=r.get('plan', {})
            point=plan.get('sourcePoint')
            if point and 'declaredSourcePoint' in plan:
                check(point == plan['declaredSourcePoint'],p+'/after/castLedger/'+cid+'/plan',
                      'Two different source points declared for one cast',plan)
            if point and 'center' in plan and r.get('spell')=='antimagic-field-lesser':
                check(math.dist(point, plan['center']) <= 10+1e-7,p+'/after/castLedger/'+cid+'/plan',
                      'Actual Antimagic casting point exceeds native 10ft range',math.dist(point, plan['center']))
            check(r['actualPaid']>=0,p+'/after/castLedger/'+cid,'Negative cast payment')
            check(close(r['commitTime'],e['time']),p+'/after/castLedger/'+cid,'New cast commitment timestamp differs from this event')
        for aid,total in charges.items():
            delta=before['actors'][aid]['RP']-after['actors'][aid]['RP']
            check(close(delta,total),p,'New cast payments do not match payer RP delta',{'actor':aid,'castPayments':total,'RPdelta':delta})
        newdamage={k:v for k,v in after.get('damageLedger',{}).items() if k not in before.get('damageLedger',{})}
        for rid,r in newdamage.items():
            counts['damageRecords']+=1;dp=p+'/after/damageLedger/'+rid
            check(sum(v['resolved'] for v in r['components'])==r['resolved'],dp,'Resolved components do not sum to damage total')
            check(r['resolved']-r['tempAbsorbed']==r['postTempDamage'],dp,'Temporary absorption arithmetic mismatch')
            check(r['actualHPDamage']+r['overkill']==r['postTempDamage'],dp,'HP damage/overkill arithmetic mismatch')
            check(r['preHP']-r['actualHPDamage']==r['postHP'],dp,'HP subtraction mismatch')
            for component in r['components']:
                want=component['native']//2 if component['resistance'] else component['native']
                check(component['resolved']==want,dp,'Declared resistance rounding mismatch',component)
    if events:check(c['expectedFinalState']==events[-1]['after'],loc,'Final state differs from last event after-state')
    for i,b in enumerate(c.get('independentBranches',[])):inspect_case(b,f'{loc}/independentBranches/{i}')

def locate(v,p):
    if isinstance(v,dict):
        if all(k in v for k in ['timeline','initialState','expectedFinalState']) and isinstance(v['timeline'],list):
            inspect_case(v,p);return
        for k,a in v.items():locate(a,p+'/'+str(k))
    elif isinstance(v,list):
        for i,a in enumerate(v):locate(a,p+'/'+str(i))

casefile=root/'CASEBOOK.json'
locate(json.loads(casefile.read_text(encoding='utf-8-sig')),'CASEBOOK.json')
print(json.dumps({'scope':'Independent serialized-data checks; findings require semantic reconciliation, not runtime validation','counts':counts,'findings':issues},ensure_ascii=False,indent=2))
