"""Data-only independent checks of new fixtures and scoped replacement traces."""
from pathlib import Path
import hashlib, json, math

A=Path(r'C:\Github\DecenniumDescent\docs\audit\2026-10-08\full-game')
P=A/'bestiary-reconciliation-108'/'delivery'
checks=[]; case_reviews=[]; schedule=[]; deltas=[]
def load(n):return json.loads((P/n).read_bytes())
def h(b):return hashlib.sha256(b).hexdigest()
def check(n,v,detail=None):checks.append({'name':n,'passed':bool(v),'detail':detail})
def write(p,d):
    with p.open('xb') as f:f.write((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
def ptr(x,p):
    for k in p.split('/')[1:]:x=x[int(k)] if isinstance(x,list) else x[k.replace('~1','/').replace('~0','~')]
    return x
def delta(a,b,p=''):
    if type(a)!=type(b):return [{'path':p,'before':a,'after':b}]
    if isinstance(a,dict):
        r=[]
        for k in a.keys()|b.keys():
            q=p+'/'+k.replace('~','~0').replace('/','~1')
            if k not in a:r.append({'path':q,'beforeAbsent':True,'after':b[k]})
            elif k not in b:r.append({'path':q,'before':a[k],'afterAbsent':True})
            else:r.extend(delta(a[k],b[k],q))
        return r
    if isinstance(a,list) and len(a)==len(b):
        return [r for i,(aa,bb) in enumerate(zip(a,b)) for r in delta(aa,bb,p+'/'+str(i))]
    return [] if a==b else [{'path':p,'before':a,'after':b}]
def gap(a,b):return math.sqrt(sum(max(0,a['min'][i]-b['max'][i],b['min'][i]-a['max'][i])**2 for i in range(3)))
def validbox(body):
    f=body['foot'];d=body['dimensions'];b=body['box']
    return b['min']==[f[0]-d[0]/2,f[1]-d[1]/2,f[2]] and b['max']==[f[0]+d[0]/2,f[1]+d[1]/2,f[2]+d[2]]
def degree(d,total,dc):
    n=3 if total>=dc+10 else 2 if total>=dc else 0 if total<=dc-10 else 1
    return ['Critical Failure','Failure','Success','Critical Success'][max(0,min(3,n+(1 if d==20 else -1 if d==1 else 0)))]

new=load('DISTINGUISHING_CASES.json');native=load('BOUND_SOURCES.json')['nativeActors']
by_dossier={r['record']['id']:r['record']['statBlock'] for r in native.values()}
check('16 new complete cases; 28 transitions',len(new['completeCases'])==16 and sum(len(c['timeline']) for c in new['completeCases'])==28)
for ci,c in enumerate(new['completeCases']):
    name=c['id']; states=[c['initialState']]+[e['after'] for e in c['timeline']]
    check(name+' complete state chain',all(e['before']==states[i] for i,e in enumerate(c['timeline'])) and c['finalState']==states[-1])
    check(name+' event times match output clocks',all(e['time']==e['after']['time'] and e['time']>=e['before']['time'] for e in c['timeline']))
    check(name+' all native statistics preserved',all(a['nativeCore']==by_dossier[a['dossierId']]['printedCoreFields'] and a['abilities']==by_dossier[a['dossierId']]['abilities'] and a['defenses']==by_dossier[a['dossierId']]['printedDefenses'] for s in states for a in s['actors'].values()))
    check(name+' body bounds internally coherent',all(validbox(a['body']) for s in states for a in s['actors'].values()))
    check(name+' no overlapping occupied actor boxes',all(all(gap(a['body']['box'],b['body']['box'])>0 for j,a in enumerate(s['actors'].values()) for k,b in enumerate(s['actors'].values()) if j<k) for s in states))
    for ei,e in enumerate(c['timeline']):
        r=e['results'];before=e['before']['actors'];after=e['after']['actors'];prefix=name+'/'+e['id']
        for aid,a in after.items():
            old=before[aid]
            if a['regularStart']!=old['regularStart']:
                ok=old['nextRegularStart']==e['time']
                detail={'casePointer':f'/completeCases/{ci}','eventPointer':f'/completeCases/{ci}/timeline/{ei}','actor':aid,'declaredNextRegularStart':old['nextRegularStart'],'actualStartEvent':e['time'],'previousRegularStart':old['regularStart']}
                check(prefix+'/'+aid+' scheduled START agrees',ok,detail)
                if not ok:schedule.append(detail)
        if e['id'] in ['preflight','other-target']:
            check(prefix+' rejection preserves actor state and RNG',before==after and e['before']['rngHistory']==e['after']['rngHistory'])
        if 'attack' in r:
            v=r['attack'];hit=v['d20']!=1 and (v['d20']==20 or v['d20']+v['bonus']>=v['AC'])
            check(prefix+' attack arithmetic',v['hit']==hit)
            if not hit:check(prefix+' miss no damage/save RNG', 'damage' not in r and 'riderSave' not in r and 'admission' not in r and len(e['after']['rngHistory'])==len(e['before']['rngHistory'])+1)
        for label in ['save','admission','riderSave']:
            if label in r:
                v=r[label];mod=v.get('modifier',v.get('naturalModifier'));dc=v.get('dc',v.get('DC'))
                check(prefix+'/'+label+' binary total',v['d20']+mod==v['total'] and v['success']==(v['total']>=dc))
        if 'damage' in r:
            d=r['damage'];check(prefix+' damage dice and HP',sum(d['faces'])+d['flat']==d['native']==d['terminal'] and d['beforeHp']-d['afterHp']==d['terminal'] and d['tempAbsorbed']==0)
            target=[aid for aid in after if before[aid]['hp']!=after[aid]['hp']]
            check(prefix+' exactly one matching HP recipient',len(target)==1 and before[target[0]]['hp']==d['beforeHp'] and after[target[0]]['hp']==d['afterHp'])
            check(prefix+' no omitted Wound trigger in supplied damage',len(target)==1 and 2*d['terminal']<before[target[0]]['maximumHp'] and d['afterHp']>0 and d['WoundCheck'] is None)
        if r.get('kind')=='TASK':
            total=r['selected']+r['naturalModifier']+r['actualProficiency'];dg=degree(r['selected'],total,r['DC'])
            check(prefix+' task degree and modifier',total==r['total'] and dg==r['degree'] and r['success']==(dg in ['Success','Critical Success']))
            check(prefix+' actual help or ordinary single die',r['selected']==max(r['d20']) and (len(r['d20'])==2 if r['helpSource'] else len(r['d20'])==1))
        if 'geometry' in r:
            g=r['geometry'];dist=math.dist(g['emitter'],g['interiorWitness']);box=before['B']['body']['box'];point=g['interiorWitness']
            check(prefix+' actual interior same witness range',0<dist<=30 and math.isclose(dist,g['distanceFeet']) and all(box['min'][i]<point[i]<box['max'][i] for i in range(3)))
        if 'push' in r:
            pp=r['push'];check(prefix+' actual ten-foot displacement',pp['requested']==10 and math.isclose(math.dist(pp['from'],pp['to']),pp['actual']) and pp['actual']==10 and after['B']['body']['foot']==pp['to'] and after['B']['conditions']==before['B']['conditions'] and after['B']['movementSpent']==before['B']['movementSpent'])
    final=c['finalState']['actors']
    case_reviews.append({'id':name,'pointer':f'DISTINGUISHING_CASES.json#/completeCases/{ci}','qualification':c['qualification'],'premises':c['premises'],'fullStateFileSha256':h((P/'DISTINGUISHING_CASES.json').read_bytes()),'eventCount':len(c['timeline']),'finalProjection':{aid:{k:a[k] for k in ['hp','action','reaction','currentSpeedFeet','conditions','grappleApplications','coilingAppendage','helpEntitlements']} for aid,a in final.items()},'runtimeExecuted':False})

old=json.loads((A/'bestiary-deliveries-104'/'return02'/'CASEBOOK.json').read_bytes())
replacement=load('RETURN02_CASE_REPLACEMENTS.json')
current={'cases':{k:v for k,v in replacement['completeParentCases'].items()}}
def get_replacement(path):
    parts=path.split('/');x=replacement['completeParentCases'][parts[2]]
    for k in parts[3:]:x=x[int(k)] if isinstance(x,list) else x[k]
    return x
for d in replacement['traceDispositions']:
    before=ptr(old,d['path']);after=get_replacement(d['path'])
    check(d['id']+' trace identity exact',before['id']==after['id']==d['id'])
    states=[after['initialState']]+[e['after'] for e in after['timeline']]
    check(d['id']+' complete carried-forward chain',all(e['before']==states[i] for i,e in enumerate(after['timeline'])) and after['finalState']==states[-1])
    scoped_before={k:v for k,v in before.items() if k!='branches'};scoped_after={k:v for k,v in after.items() if k!='branches'}
    deltas.append({'path':d['path'],'id':d['id'],'declaredChanges':d['changes'],'actualFullFieldDeltas':delta(scoped_before,scoped_after)})
for ix,c in replacement['completeParentCases'].items():
    paths={d['path'] for d in replacement['traceDispositions']}
    for bi,b in enumerate(c['branches']):
        path=f'/cases/{ix}/branches/{bi}'
        if path not in paths:check(path+' unrelated branch byte-equivalent JSON',b==old['cases'][int(ix)]['branches'][bi])

mixed=replacement['completeParentCases']['36']['branches'][3]
end=mixed['finalState']['actors'];last=mixed['timeline'][-1];g=gap(end['creature']['parts'][0]['box'],end['recipient']['parts'][0]['box'])
check('Mixed Wave/Halberd independent gap/HP/action result',g==15 and g>10 and end['recipient']['hp']==348-12==336 and end['creature']['action']==0 and last['results']['attackD20']==[] and last['results']['damageFaces']==[])
wall=replacement['completeParentCases']['146']['branches'][1];r=wall['timeline'][0]['results']
check('Actual wall truncates movement independently',wall['initialState']['actors']['bear']['parts'][0]['box']['max'][0]==20 and wall['initialState']['environment']['obstacles'][0]['min'][0]==21 and r['requestedPush']==10 and r['actualPush']==1 and r['wallDamage']==0)
check('Gargantuan diagnostic explicitly conditional',new['separateConditionalSizeDiagnostic']['notCountedAsPositiveEncounter'] is True and new['separateConditionalSizeDiagnostic']['noActionRNGDamageOrConditionProduced'] is True)
report={'id':'BESTIARY-RECONCILIATION-CASE-REVIEW-108','status':'SCOPED_CHOICES_COHERENT_FIXTURE_SCHEDULE_METADATA_NEEDS_CORRECTION','passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'checks':checks,'scheduleDiscrepancies':schedule,'newCaseReviews':case_reviews,'replacementTraceDeltas':deltas,'mechanicalSelectionAssessment':{'PressureWave':'10ft/no new Prone, actual same emitter/interior witness; preserves native failure-only damage and source-qualified forced-movement constraints.','TailSweep':'DEX13 local NEW rider distinguished with native Bear DEX+2 versus STR+3; same paid attack/damage.','Constrict':'Task escape uses actual skills/Help distinct from initial binary STR save; single real coil and up-to-one-size-larger predicate retained; source stats unchanged.','status':'Suitable scoped authoring selections; fixture corrections and wider catalog review still pending.'},'limits':['Fresh source/state/arithmetic checks of the delivered data, not engine execution.','Changed original case traces assessed for reconciliation ripple only, not blanket approval of unrelated proposed traits, operators or catalog.','Four new fixture START events conflict with initial nextRegularStart metadata; report preserves the discrepancy and does not invent a schedule.','No canonical integration, broad acceptance, deletion, runtime, balance or cosmology change.']}
write(A/'BESTIARY_RECONCILIATION_CASE_REVIEW_108.json',report)
with (A/Path(__file__).name).open('xb') as f:f.write(Path(__file__).read_bytes())
print(json.dumps({'passed':report['passed'],'failed':report['failed'],'scheduleDiscrepancies':schedule,'failedChecks':[c for c in checks if not c['passed']]}))
