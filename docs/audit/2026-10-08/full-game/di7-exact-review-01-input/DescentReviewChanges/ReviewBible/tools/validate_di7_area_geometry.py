"""Execute the19 GPT geometry expectations and paid-cast edge histories."""
from copy import deepcopy
from datetime import datetime,timezone
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded
from di7_cast_transactions import DI7Sources
from di7_area_geometry import AreaGeometryTransactions,grid_distance,mass_contains


def main():
    output=A/'DI7_AREA_GEOMETRY_CHECK.json'; assert not output.exists()
    sources=DI7Sources(); checks=[]; histories=[]; coverage={}
    def check(label,ok): assert ok,label; checks.append(label)
    def record(label,m): histories.append({'id':label,'final':m.snapshot()})
    def reject(label,m,fn):
        before=m.snapshot()
        try: fn()
        except ValueError as e: check(label+'/rejected',bool(str(e)))
        else: raise AssertionError(label)
        check(label+'/atomic',m.snapshot()==before)
    def volume(cell,center): return {'cellId':cell,'min':[x-2.5 for x in center],'max':[x+2.5 for x in center]}
    def make(sid='mass-revelation',provider='Wizard',*,center=None,origin=None,direction=None,points=None):
        center=[0,0,0] if center is None else center; origin=[0,0,0] if origin is None else origin
        direction=[1,0,0] if direction is None else direction; points=[[10,0,0]] if points is None else points
        level=13 if provider in {'Wizard','Cleric'} else 20; actors={}
        for aid,cls,lv,pos in [('owner',provider,level,0),('counter','Wizard',13,10)]:
            actors[aid]={'provider':cls,'classLevel':lv,'totalLevel':lv,'abilityScore':18,
                'attainmentPremise':'Conditional attained ordinary caster/body/rest slice; no full character progression claimed.',
                'heroPath':'Soothsayer' if cls=='Shaman' else 'ordinary-provider-retained','specialization':'Evocation',
                'providerRetained':True,'bookPresent':True,'studyUninterrupted':True,'positionFeet':pos,'position3d':[pos,0,0],
                'knownFactions':[],'body':{'conscious':True,'canAct':True,'ordinarySpellProhibited':False,'silenced':False,'canSpeak':True,'reactionLegal':True,
                    'hands':{'left':{'usable':True,'holding':None},'right':{'usable':True,'holding':'focus/'+aid}},
                    'focus':{'id':'focus/'+aid,'owner':aid,'qualifiedClasses':[cls],'accessible':True}}}
        entities={aid:{'kind':'creature','positionFeet':a['positionFeet'],'willing':True,'alliedTo':{},'relatedQuestions':[]} for aid,a in actors.items()}
        entities['point']={'kind':'point','positionFeet':center[0],'position3d':deepcopy(center)}
        cells={'origin':{'center':[0,0,0]},'counter-cell':{'center':[10,0,0]}}; portions={}
        origin_key=','.join(str(x) for x in (origin if sid=='mass-revelation' else center))
        for i,p in enumerate(points):
            cell='test-cell-'+str(i); cells[cell]={'center':p}
            portions['portion-'+str(i)]={'cellId':cell,'actuallyOccupiedNow':True,'authorityEvent':'conditional-actual-portion/'+str(i),
                'actualLocalFootprint':{'part':'local-portion-'+str(i),'center':p},'clippingByOrigin':{origin_key:{
                    'authorityEvent':'conditional-current-open-source-line/'+str(i),'lineOfEffect':True,'totalCover':False,'blockedCorner':False}}}
        geometry={'kind':'conditional-actual-occupied-volumes-and-source-clipping','cells':cells,'portions':portions,
            'bodies':{a:{'authorityEvent':'conditional-actual-body/'+a,'sourceVersion':'world-v1','actualOccupiedVolumes':[volume('origin' if a=='owner' else 'counter-cell',v['position3d'])]} for a,v in actors.items()},
            'pointRelations':{'owner>point':{'authorityEvent':'conditional-perception-and-open-line','point':deepcopy(center),'perceived':True,'lineOfEffect':True,'blockedCorner':False}}}
        world={'entities':entities,'relations':{a+'>'+t:{'sourceFact':'conditional-straight-line-counter-range','perceived':True,'visible':True,'lineOfEffect':True} for a in actors for t in actors},
            'geometry':geometry,'alignmentActors':{a:{'underlying':{'order':'Lawful','ethics':'Good'},'immunities':[],'permanentIdentity':{'id':a},'acquisitionSnapshots':[],'usedAllowances':{}} for a in actors},
            'encounter':{'id':'conditional-real-encounter','isRealEncounter':True},'identificationFacts':{},'triggerEvents':{}}
        m=AreaGeometryTransactions(sources,actors,world)
        m.learn('owner',sid,level,'actual-owner-learning'); m.learn('counter','counterspell',5,'actual-counter-learning')
        for aid,a in m.actors.items():
            if a['provider']=='Wizard': m.prepare_wizard(aid,list(a['learned']),aid+'/study',{'actor':aid,'completedAt':0,'sourceEvent':'conditional-completed-rest'})
        m.begin_turn('owner','turn-1')
        request={'origin':origin,'originCell':'origin','direction':direction} if sid=='mass-revelation' else {'target':'point'}
        return m,request
    def paid(m,request,sid='mass-revelation'):
        before=m.actors['owner']['rp']; m.declare('owner',sid,'area',request)
        check('paid/'+sid+'/'+str(len(histories)),m.actors['owner']['rp']==before-17 and m.actors['owner']['actions']==0)
        return m.resolve_area_geometry('area')
    def move(m,position,eid):
        cell='move/'+eid; m.world['geometry']['cells'][cell]={'center':deepcopy(position)}
        m.move_actor('owner',position,[volume(cell,position)],event_id=eid,authority_event='conditional-actual-legally-permitted-displacement/'+eid)
    for provider in ['Wizard','Cleric','Mirrorsage','Shaman']:
        for sid in ['mass-revelation','resonance-sight-supreme']:
            m,request=make(sid,provider); gate=paid(m,request,sid)
            check(provider+'/'+sid+'/geometry-only-no-premature-information',len(gate['readableSpatialPortions'])==1 and not gate['informationPayloadExecuted'] and not gate['publicInformationDelivered'])
            check(provider+'/'+sid+'/fixed-commit-record',gate['committedGeometry']==m.casts['area']['committedGeometry'])
            record(provider+'/'+sid,m)
    expected=[([20,20,0],True),([20,20,20],True),([0,0,20],True),([20,0,5],True),([25,0,0],False)]
    for n,(point,inside) in enumerate(expected,1):
        sid='resonance-sight-supreme'; m,request=make(sid,points=[point]); gate=paid(m,request,sid)
        cid='DI7-GEO-S'+str(n); check(cid,bool(gate['readableSpatialPortions'])==inside); record(cid,m); coverage[cid]=cid
    for n,(point,legal) in enumerate([([120,120,120],True),([125,0,0],False)],1):
        sid='resonance-sight-supreme'; m,request=make(sid,center=point,points=[point]); cid='DI7-GEO-R'+str(n)
        if legal: check(cid,bool(paid(m,request,sid)))
        else: reject(cid,m,lambda:m.declare('owner',sid,'area',request))
        record(cid,m); coverage[cid]=cid
    expected=[([60,30,0],True),([60,0,30],True),([60,25,25],False),([60,35,0],False),([65,0,0],False)]
    for n,(point,inside) in enumerate(expected,1):
        m,request=make(points=[point]); gate=paid(m,request); cid='DI7-GEO-M'+str(n)
        check(cid,bool(gate['readableSpatialPortions'])==inside); record(cid,m); coverage[cid]=cid
    m,request=make(direction=[12,5,0],points=[[65,0,0]])
    check('DI7-GEO-M6',bool(paid(m,request)['readableSpatialPortions']) and grid_distance([0,0,0],[65,0,0])==65)
    record('DI7-GEO-M6',m); coverage['DI7-GEO-M6']='DI7-GEO-M6'
    for position,passes,cid in [([0,5,0],True,'DI7-GEO-I1'),([-5,0,0],False,'DI7-GEO-I2')]:
        sid='resonance-sight-supreme'; m,request=make(sid,center=[120,0,0],points=[[120,0,0]])
        m.declare('owner',sid,'area',request); committed=deepcopy(m.casts['area']['committedGeometry']); move(m,position,cid)
        gate=m.resolve_area_geometry('area'); check(cid,bool(gate)==passes and m.casts['area']['committedGeometry']==committed and m.actors['owner']['rp']==31)
        record(cid,m); coverage[cid]=cid
    for failure in ['perceived','lineOfEffect','blockedCorner']:
        sid='resonance-sight-supreme'; m,request=make(sid)
        m.declare('owner',sid,'area',request)
        m.world['geometry']['pointRelations']['owner>point'][failure]=(failure=='blockedCorner')
        check('DI7-GEO-I3/'+failure,m.resolve_area_geometry('area') is None and m.actors['owner']['rp']==31 and m.casts['area']['refund']==0)
        record('DI7-GEO-I3/'+failure,m)
    coverage['DI7-GEO-I3']=['DI7-GEO-I3/perceived','DI7-GEO-I3/lineOfEffect','DI7-GEO-I3/blockedCorner']
    m,request=make(); m.declare('owner','mass-revelation','area',request); move(m,[5,0,0],'moved-away')
    check('DI7-GEO-I4',m.resolve_area_geometry('area') is None and m.actors['owner']['rp']==31 and m.casts['area']['refund']==0)
    record('DI7-GEO-I4',m); coverage['DI7-GEO-I4']='DI7-GEO-I4'
    m,request=make(); m.declare('owner','mass-revelation','area',request); committed=deepcopy(m.casts['area']['committedGeometry'])
    move(m,[5,0,0],'leave'); move(m,[0,0,0],'return'); m.actors['owner']['facingNow']=[-1,0,0]
    gate=m.resolve_area_geometry('area')
    check('DI7-GEO-I5',bool(gate['readableSpatialPortions']) and gate['committedGeometry']==committed)
    record('DI7-GEO-I5',m); coverage['DI7-GEO-I5']='DI7-GEO-I5'
    for label,origin,direction in [('nonlocal-origin',[5,0,0],[1,0,0]),('zero-direction',[0,0,0],[0,0,0]),('rear-boundary',[-2.5,0,0],[1,0,0])]:
        m,request=make(origin=origin,direction=direction)
        reject('DI7-GEO-I6/'+label,m,lambda:m.declare('owner','mass-revelation','area',request)); record('DI7-GEO-I6/'+label,m)
    coverage['DI7-GEO-I6']=['DI7-GEO-I6/nonlocal-origin','DI7-GEO-I6/zero-direction','DI7-GEO-I6/rear-boundary','DI7-GEO-R2']
    m,request=make(origin=[2.5,0,0],points=[[5,0,0]])
    gate=paid(m,request); check('forward-boundary-nominates-one-origin-cell',bool(gate['readableSpatialPortions']) and gate['committedGeometry']['originCell']=='origin')
    record('forward-boundary',m)
    m,request=make(origin=[-2.5,0,0],direction=[-1,0,0],points=[[-5,0,0]])
    check('negative-facing-forward-boundary',bool(paid(m,request)['readableSpatialPortions'])); record('negative-facing-forward-boundary',m)
    # An interior origin positioned behind its nominated cell center still
    # excludes that same nominated cell, rather than relying on a==0 alone.
    m,request=make(origin=[-1,0,0],points=[[0,0,0]])
    m.world['geometry']['portions']['portion-0']['cellId']='origin'
    check('nominated-origin-cell-excluded',not paid(m,request)['readableSpatialPortions']); record('origin-cell-exclusion',m)
    for sid in ['mass-revelation','resonance-sight-supreme']:
        m,request=make(sid,points=[[10,0,0],[15,0,0],[20,0,0],[0,10,0]])
        portions=m.world['geometry']['portions']
        portions['portion-1']['clippingByOrigin']['0,0,0']['totalCover']=True
        portions['portion-2']['clippingByOrigin']['0,0,0']['blockedCorner']=True
        portions['portion-3']['actuallyOccupiedNow']=False
        gate=paid(m,request,sid)
        names=[p['portionId'] for p in gate['readableSpatialPortions']]
        check(sid+'/clipping-and-no-assumed-occupancy',names==(['portion-0'] if sid=='mass-revelation' else ['portion-0','portion-3']))
        check(sid+'/local-portion-not-whole-footprint',gate['readableSpatialPortions'][0]['localFootprint']=={'part':'local-portion-0','center':[10,0,0]})
        record(sid+'/clipping-and-empty-history-location',m)
    m,request=make('resonance-sight-supreme',center=[120,0,0],points=[[120,0,0]])
    m.declare('owner','resonance-sight-supreme','area',request); move(m,[-5,0,0],'supreme-leave'); move(m,[0,0,0],'supreme-return')
    check('supreme-restored-endpoint-not-continuous-range',bool(m.resolve_area_geometry('area'))); record('supreme-return',m)
    for sid in ['mass-revelation','resonance-sight-supreme']:
        m,request=make(sid); m.declare('owner',sid,'area',request)
        m.declare('counter','counterspell','counter-area',{'pendingCast':'area'}); m.resolve_counter('counter-area',20)
        reject(sid+'/countered-no-geometry-resolution',m,lambda:m.resolve_area_geometry('area'))
        check(sid+'/counter-keeps-payment',m.actors['owner']['rp']==31 and 'geometryGate' not in m.casts['area']); record(sid+'/actual-counter',m)
        m,request=make(sid); m.declare('owner',sid,'area',request); m.actors['owner']['body']['canAct']=False
        check(sid+'/actual-interruption-prevents-geometry',m.resolve_area_geometry('area') is None and m.casts['area']['status']=='interrupted-no-refund' and m.actors['owner']['rp']==31)
        record(sid+'/incapacitated-before-resolution',m)
    expected_ids={v['id'] for s in json.loads((R/'data/playtest/spell_candidates/divination_rank7_exact_01_expectations.json').read_bytes())['supplementalSourceExpectations'] if s['id']=='DI7-GEOMETRY-3D-01' for v in s['variants']}
    check('all19-source-expectation-ids-covered',set(coverage)==expected_ids and len(expected_ids)==19)
    bindings=sources.bindings+[info(p) for p in [R/'tools/di7_area_geometry.py',R/'tools/validate_di7_area_geometry.py',R/'tools/di7_fate_transactions.py',R/'tools/di7_cast_transactions.py',
        A/'DI7_GEOMETRY_3D_RECEIVED.json',R/'data/playtest/spell_candidates/divination_rank7_exact_01_expectations.json',R/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md']]
    report={'status':'pass','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'checks':len(checks),'historyCount':len(histories),
        'sourceBindings':bindings,'checkLabels':checks,'histories':histories,'sourceExpectationCoverage':coverage,'failures':[],
        'scope':'Exact scoped source geometry and fixed committed origin/center resolution checkpoints integrated with actual conditional paid acquisition/preparation/casting and Counterspell.',
        'conditionalPremises':['Actual attained provider/body/rest slices; full character history remains upstream.',
            'Actual occupied filled box volumes, cell registration and source-qualified line-of-effect/total-cover/corner clipping are conditional world inputs, not generic movement or ray-tracing computation.',
            'Displacement and incapacity are explicit legally originating upstream events; the area spells grant no such actions.',
            'Counterspell uses the existing straight-line local fixture; scoped DI7 three-axis geometry is not generalized to every source.'],
        'remaining':['Mass and Supreme information payloads and observer knowledge are deliberately not delivered by this geometry gate.',
            'General arbitrary body/terrain geometry, perception acquisition and native information-protection grants remain outside this finite adapter.',
            'Suggestion initiative clock, ordinary Shaman totem vent, full original49 compilation and separate exact-seven review remain.'],
        'geometry19Executed':True,'informationPayloadExecuted':False,'candidateApproved':False,'full49Fulfilled':False,'humanPlaytest':False,'spellPromotions':0,'newRuleAdoptions':0}
    output.write_bytes(encoded(report)); print(json.dumps({'report':info(output),'checks':len(checks),'histories':len(histories),'geometryExpectationsExecuted':len(coverage)}))


if __name__=='__main__': main()
