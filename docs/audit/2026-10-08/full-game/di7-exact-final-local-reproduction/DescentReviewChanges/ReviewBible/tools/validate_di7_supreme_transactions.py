"""Historical Supreme queries, native temporal scope and non-diagnostic output."""
from copy import deepcopy
from datetime import datetime,timezone
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded
from di7_cast_transactions import DI7Sources
from di7_area_fixtures import make as area_fixture
from di7_supreme_transactions import SupremeTransactions,NOTICE


def main():
    output=A/'DI7_SUPREME_TRANSACTIONS_CHECK.json'; assert not output.exists()
    sources=DI7Sources(); checks=[]; histories=[]; coverage={}
    def check(label,ok): assert ok,label; checks.append(label)
    def record(label,m): histories.append({'id':label,'final':m.snapshot()})
    def reject(label,m,fn):
        before=m.snapshot()
        try: fn()
        except ValueError as e: check(label+'/rejected',bool(str(e)))
        else: raise AssertionError(label)
        check(label+'/atomic',m.snapshot()==before)
    def point(at): return {'kind':'point','at':at}
    def span(a,b,*,kind='continuous-interval',left=True,right=True): return {'kind':kind,'from':a,'to':b,'includeFrom':left,'includeTo':right}
    def occurrence(oid,*,time=None,portion='portion-0',identity=None,rank=7,magical=True):
        time=point(100) if time is None else time
        facts={}; ids=[]
        def add(key,field,value,t=None,part=None,domain='historical',channel='actual-historical-trace'):
            fid=oid+'/'+key; tm=deepcopy(time if t is None else t)
            facts[fid]={'id':fid,'occurrence':oid,'subjects':[oid],'authorityVersion':'actual-history-v1','authorityEvent':'Director-established/'+fid,
                'field':field,'value':deepcopy(value),'time':tm,'publicTimePrecision':deepcopy(tm),'domain':domain,
                'establishedAtQueryTime':3000,'evidenceChannel':channel,'historicalPortions':[portion if part is None else part]}
            ids.append(fid); return fid
        add('exists','existence',True)
        add('identity','identity',identity or 'Actual effect '+oid)
        add('category','category','spell' if rank is not None else 'nonspell-enchantment')
        if rank is not None: add('rank','rank',rank); add('school','school','Evocation')
        row={'id':oid,'authorityVersion':'actual-history-v1','authorityEvent':'Director-established-occurrence/'+oid,'actuallyMagical':magical,'facts':ids,
            'privateCasterIdentity':'SECRET-CASTER','privateBlueprint':'SECRET-BLUEPRINT','privatePool':999,'requiresPreexistingSoftwareLog':False}
        return row,facts,add
    def protection(subject,*,pid='native-history-protection',a=150,b=175,existence=True,fields=None,domains=None,left=True,right=False):
        return {'id':pid,'nativeScopePremise':{'kind':'conditional-actual-native-protection-scope','sourceVersion':'actual-native-v1',
            'sourceGrantEvent':'conditional-actual-upstream-protection','completeScopeText':'Conditional native source protects only its named subjects, fact domains/channels/fields and native historical endpoints against this query. It creates no general or selectable protection ability.'},
            'queryActiveFrom':3000,'queryActiveUntil':5000,'querySchools':['Divination'],'minimumQueryRank':7,'maximumQueryRank':7,
            'subjects':[subject],'factDomains':domains or ['historical','current'],'evidenceChannels':['actual-historical-trace'],
            'historicalTimeScope':span(a,b,kind='native-interval',left=left,right=right),'mode':'block','protectsExistence':existence,
            'fields':fields or [],'maskedFields':{}}
    def make(provider='Wizard',*,protections=None,uncertain=False,empty=False,count=0):
        base,request=area_fixture(sources,'resonance-sight-supreme',provider,points=[[0,0,0],[10,0,0],[20,20,20],[25,0,0],[200,0,0]])
        world=deepcopy(base.world); world['informationChannels']={}
        # Supreme reads historical places even when no object/effect is there now.
        for p in world['geometry']['portions'].values(): p['actuallyOccupiedNow']=False
        world['geometry']['pointRelations']['counter>point']=deepcopy(world['geometry']['pointRelations']['owner>point'])
        records={}; facts={}
        if uncertain:
            row,f,_=occurrence('uncertain',time=span(100,200,kind='occurrence-window'),identity='Bounded old enchantment',rank=None)
            records[row['id']]=row; facts.update(f)
        elif not empty:
            row,f,add=occurrence('continuous',time=span(100,200),identity='Continuous local enchantment',rank=9)
            add('persistence','persistence','Established continuous local persistence')
            add('beginning','transition',{'kind':'began'},point(100)); add('ending','transition',{'kind':'ended'},point(200))
            add('suppression','transition',{'kind':'suppressed'},point(160)); add('restored','transition',{'kind':'suppression-ended'},point(180))
            records[row['id']]=row; facts.update(f)
            row,f,add=occurrence('moved-object',time=span(50,90),portion='portion-2',identity='Moved object enchantment',rank=None)
            add('local-visit','persistence','Actual local visit',span(50,90))
            add('remote-only','state','SECRET-REMOTE-DESTINATION',point(200),part='portion-4')
            row['privateCurrentDestination']='SECRET-REMOTE-DESTINATION'; records[row['id']]=row; facts.update(f)
            row,f,add=occurrence('current-nonspell',time=point(3500),portion='portion-1',identity='Dormant current enchantment',rank=None)
            add('current-state','state','dormant',point(3600),domain='current'); records[row['id']]=row; facts.update(f)
            row,f,_=occurrence('ancient',time=point(-10**12),identity='Ancient magical nonspell',rank=None)
            records[row['id']]=row; facts.update(f)
            row,f,_=occurrence('never-magical',identity='SECRET-NONMAGIC',magical=False)
            records[row['id']]=row; facts.update(f)
        for i in range(count):
            row,f,_=occurrence('additional-'+str(i),time=point(-1000-i),rank=None); records[row['id']]=row; facts.update(f)
        data={'kind':'conditional-Director-established-spatial-history','occurrences':records,'facts':facts,'protections':protections or [],'softwareLog':None}
        m=SupremeTransactions(sources,base.actors,world,history=data)
        for aid in m.actors:
            m.learn(aid,'resonance-sight-supreme',m.actors[aid]['classLevel'],'actual-Supreme-learning/'+aid)
        m.learn('counter','counterspell',5,'actual-Counter-learning')
        if provider=='Wizard': m.learn('owner','fate-echo',13,'actual-Fate-learning')
        for aid,a in m.actors.items():
            if a['provider']=='Wizard': m.prepare_wizard(aid,list(a['learned']),aid+'/study',{'actor':aid,'completedAt':0,'sourceEvent':'conditional-actual-completed-rest'})
        m.begin_turn('owner','owner-turn1'); return m,request
    def cast(m,request,*,actor='owner',cid='supreme'):
        m.declare(actor,'resonance-sight-supreme',cid,request); return m.resolve_supreme(cid)
    def assertions(result): return [a for e in result['effects'] for a in e['assertions']]
    def field_values(result,name): return [a['value'] for a in assertions(result) if a['field']==name]
    for provider in ['Wizard','Cleric','Mirrorsage','Shaman']:
        m,request=make(provider); result=cast(m,request)
        check(provider+'/actual17RP-and-four-real-occurrences',m.actors['owner']['rp']==m.actors['owner']['maxRP']-17 and len(result['effects'])==4)
        check(provider+'/private-no-automatic-other-caster-result',len(m.readings)==1 and m.readings['supreme']['caster']=='owner')
        check(provider+'/one-continuing-interval-not-per-second-casts',len([a for a in assertions(result) if a['field']=='persistence' and a['value']=='Established continuous local persistence'])==1)
        check(provider+'/old-and-high-rank-no-arbitrary-ceiling',9 in field_values(result,'rank') and any(a.get('time')==point(-10**12) for a in assertions(result)))
        check(provider+'/missing-nonspell-rank-not-zero',field_values(result,'rank')==[9] and 0 not in field_values(result,'rank'))
        check(provider+'/real-local-moving-history-not-remote-tracking','SECRET-REMOTE' not in json.dumps(result) and 'Moved object enchantment' in field_values(result,'identity'))
        check(provider+'/no-caster-pool-blueprint-nonmagic',not any(s in json.dumps(result) for s in ['SECRET','999','nativeScopePremise','occurrence','factId']))
        check(provider+'/same-uniform-notice',result['notice']==NOTICE and not m.observations and m.history.data['softwareLog'] is None)
        record('actual-paid-historical-query/'+provider,m)
    m,request=make(count=125); result=cast(m,request)
    check('129-actual-occurrences-no-count-cap',len(result['effects'])==129); record('uncapped-established-history',m)
    m,request=make(); m.world['geometry']['portions']['portion-0']['clippingByOrigin']['0,0,0']['totalCover']=True
    result=cast(m,request); check('today-wall-clips-actual-historical-place',len(result['effects'])==2 and 'Ancient magical nonspell' not in field_values(result,'identity'))
    record('current-wall-clipping',m)
    m,request=make(); m.world['geometry']['pastLayoutNote']='This currently open site once had a solid wall.'
    result=cast(m,request); check('open-place-retains-its-actual-old-history',len(result['effects'])==4); record('changed-past-layout',m)
    # A: the date100..200 is uncertainty about one occurrence, never continuous
    # existence at every candidate date or a license to subtract blocked dates.
    native=protection('uncertain')
    m,request=make(uncertain=True,protections=[native]); result=cast(m,request)
    check('A-unresolved-potential-existence-no-record',result=={'effects':[],'notice':NOTICE})
    check('A-private-disposition-unresolved-not-broadened-protection',all(d['relation']=='unresolved' for d in m.history.dispositions) and m.history.data['protections'][0]==native)
    check('A-no-invented-actual-date',all(f['time']==span(100,200,kind='occurrence-window') for f in m.history.data['facts'].values()))
    record('A-unresolved',m); coverage['DI7-SUPREME-TIME-A-UNRESOLVED']='A-unresolved'
    for relation in ['outside','applies']:
        m,request=make(uncertain=True,protections=[native]); initial=cast(m,request)
        for fid in m.history.data['facts']:
            m.establish_temporal_relation(fid,native['id'],relation,event_id='new-relation/'+fid,authority_event='conditional-actual-world-evidence/'+fid)
        m.begin_turn('owner','owner-turn2'); later=cast(m,request,cid='after-evidence')
        check('A-'+relation+'/actual-additional-relation-not-repetition',not initial['effects'] and bool(later['effects'])==(relation=='outside'))
        check('A-'+relation+'/original-uncertain-precision-retained',all(f['time']==span(100,200,kind='occurrence-window') for f in m.history.data['facts'].values()) and m.actors['owner']['rp']==14)
        if relation=='outside': check('A-outside/no-new-exact-date',all(a['time']==span(100,200,kind='occurrence-window') for a in assertions(later)))
        record('A-'+relation,m)
    coverage['DI7-SUPREME-TIME-A-OUTSIDE']='A-outside'; coverage['DI7-SUPREME-TIME-A-INSIDE']='A-applies'
    m,request=make(uncertain=True,protections=[protection('uncertain',existence=False,fields=['identity'])]); result=cast(m,request)
    check('A-field/independent-existence-category-survive',len(result['effects'])==1 and field_values(result,'category')==['nonspell-enchantment'] and not field_values(result,'identity'))
    check('A-field/no-status-or-redaction-explanation',not any(s in json.dumps(result).lower() for s in ['unresolved','redacted','withheld','protection']))
    record('A-field-only',m); coverage['DI7-SUPREME-TIME-A-FIELD']='A-field-only'
    # An actual independent readable evidence channel can establish existence;
    # it never unmasks other facts protected through the trace channel.
    m,request=make(uncertain=True,protections=[native]); m.history.data['facts']['uncertain/exists']['evidenceChannel']='independent-source-established-history'
    result=cast(m,request); check('A-independent-readable-existence-only',len(result['effects'])==1 and not result['effects'][0]['assertions'])
    record('independent-readable-existence',m)
    m,request=make(protections=[protection('continuous')]); result=cast(m,request)
    continuous=result['effects'][0]; transitions=[a for a in continuous['assertions'] if a['field']=='transition']
    check('B-one-identity-genuine-positive-transitions',[a['time']['at'] for a in sorted(transitions,key=lambda a:a['time']['at'])]==[100,180,200])
    check('B-no-certified-continuity-or-filtering-boundaries',not any(a['field']=='persistence' for a in continuous['assertions']) and not any(a.get('time',{}).get('at') in {150,175} for a in continuous['assertions']))
    check('B-independent-properties-kept',9 in field_values(result,'rank') and 'Continuous local enchantment' in field_values(result,'identity'))
    check('B-private-real-continuity-and-hidden-transition-retained',m.history.data['facts']['continuous/persistence']['time']==span(100,200) and m.history.data['facts']['continuous/suppression']['time']==point(160))
    record('B-partial-history',m); coverage['DI7-SUPREME-TIME-B-CONTINUOUS']='B-partial-history'
    m2,request2=make(protections=[protection('continuous')]); hidden=deepcopy(m2.history.data['facts']['continuous/suppression'])
    hidden.update(id='continuous/additional-hidden-transition',time=point(170),publicTimePrecision=point(170),value={'kind':'SECRET-DIFFERENT-INTERIOR'})
    m2.history.data['facts'][hidden['id']]=hidden; m2.history.data['occurrences']['continuous']['facts'].insert(0,hidden['id'])
    m2.history.data['facts']['continuous/suppression']['value']={'kind':'SECRET-OTHER-INTERIOR'}
    changed=cast(m2,request2)
    check('B-protected-interior-noninterference',changed==result); record('B-different-protected-interior',m2)
    coverage['DI7-SUPREME-TIME-B-NONINTERFERENCE']=['B-partial-history','B-different-protected-interior']
    # A real transition coincident with a filtering boundary is still actual
    # history when the native endpoint explicitly excludes that timestamp.
    m,request=make(protections=[protection('continuous',left=False)])
    f=m.history.data['facts']['continuous/suppression']; f.update(time=point(150),publicTimePrecision=point(150))
    result=cast(m,request); check('native-open-endpoint-does-not-ban-real150-transition',any(a['field']=='transition' and a.get('time')==point(150) for a in assertions(result)))
    record('native-endpoint-real-transition',m)
    m,request=make(protections=[protection('continuous',a=100,b=160,pid='first',right=True),protection('continuous',a=150,b=200,pid='second',right=True)])
    result=cast(m,request); check('two-native-scopes-cover-full-history-no-positive-leak','Continuous local enchantment' not in field_values(result,'identity') and len(result['effects'])==3)
    record('union-of-actual-covered-intervals',m)
    m,request=make(); unprotected=cast(m,request)
    m2,request2=make(protections=[protection('continuous',a=0,b=4000,domains=['current'])]); current_only=cast(m2,request2)
    check('C-current-only-not-retroactive',current_only==unprotected)
    record('C-current-only',m2); coverage['DI7-SUPREME-TIME-C-CURRENT-ONLY']='C-current-only'
    for label,change in [('different-subject',lambda p:p.update(subjects=['unrelated'])),('different-school',lambda p:p.update(querySchools=['Illusion'])),
        ('different-rank',lambda p:p.update(maximumQueryRank=6)),('inactive-query-time',lambda p:p.update(queryActiveUntil=3500))]:
        p=protection('continuous',a=0,b=4000); change(p); m,request=make(protections=[p])
        check(label+'/native-scope-not-expanded',cast(m,request)==unprotected); record('scope/'+label,m)
    m,request=make(uncertain=True); m.history.data['facts']['uncertain/identity'].update(time={'kind':'relative-order'},publicTimePrecision={'kind':'relative-order','text':'Before the archive was built.'})
    result=cast(m,request); check('genuine-relative-order-no-invented-date',any(a.get('time')=={'kind':'relative-order','text':'Before the archive was built.'} for a in assertions(result)))
    record('actual-relative-precision',m)
    m,request=make(protections=[protection('continuous',a=0,b=4000,existence=False,fields=['identity'])])
    p=m.history.data['protections'][0]; p['mode']='mask'; p['nativeScopePremise']['explicitlyAuthorizesAlteredResult']=True; p['maskedFields']={'identity':'Native source-authorized altered identity'}
    result=cast(m,request); check('actual-authorized-mask-retains-altered-result','Native source-authorized altered identity' in field_values(result,'identity') and 'Continuous local enchantment' not in field_values(result,'identity'))
    record('native-explicit-field-mask',m)
    m,request=make(uncertain=True,protections=[native]); first=cast(m,request); m.begin_turn('owner','owner-turn2'); second=cast(m,request,cid='repeat')
    check('repeat-does-not-resolve-uncertainty',first==second and m.actors['owner']['rp']==14 and m.actors['owner']['refrain']==1)
    record('unchanged-paid-repeat',m); coverage['DI7-SUPREME-TIME-REPEAT']='unchanged-paid-repeat'
    m,request=make(); first=cast(m,request); m.begin_turn('counter','counter-query-turn'); other=cast(m,request,actor='counter',cid='other-caster')
    check('different-paid-caster-same-established-overlap',first==other and m.actors['counter']['rp']==31); record('two-casters-same-world',m)
    m,request=make(empty=True); absent=cast(m,request)
    m2,request2=make(uncertain=True,protections=[protection('uncertain',a=0,b=4000)]); protected=cast(m2,request2)
    m3,request3=make(uncertain=True,protections=[native]); unresolved=cast(m3,request3)
    check('absent-protected-unresolved-empty-presentation-identical',absent==protected==unresolved=={'effects':[],'notice':NOTICE})
    record('ordinary-empty-history',m); record('protected-empty-history',m2); record('unresolved-empty-history',m3)
    m,request=make(); m.declare('owner','resonance-sight-supreme','supreme',request)
    m.declare('counter','counterspell','counter-supreme',{'pendingCast':'supreme'}); m.resolve_counter('counter-supreme',20)
    reject('actual-counter-prevents-history-query',m,lambda:m.resolve_supreme('supreme'))
    check('actual-counter-keeps17-no-memory',m.actors['owner']['rp']==31 and not m.readings); record('actual-counterspell',m)
    m,request=make(); result=cast(m,request)
    reject('historical-occurrence-not-original-Fate-observation',m,lambda:m.begin_fate('owner','echo-old-history','continuous',{'target':'owner'}))
    check('no-restoration-acquisition-or-original-observation',not m.coins and not m.observations and set(m.actors['owner']['learned'])=={'resonance-sight-supreme','fate-echo'})
    known=deepcopy(assertions(result)[0]); m.world['informationChannels']['actual-transmission']={'authorityEvent':'conditional-actual-source-qualified-channel',
        'from':'owner','to':'counter','at':m.now,'received':True,'understood':True,'deliveredAssertions':[known]}
    received=m.communicate('supreme','counter','actual-transmission')
    check('only-actual-delivered-assertion-no-whole-private-copy',received['assertions']==[known] and 'effects' not in received and 'privateHistoricalWorld' not in received)
    reject('communication-not-replayed',m,lambda:m.communicate('supreme','counter','actual-transmission')); record('history-not-copy-access-and-limited-communication',m)
    m,request=make(); f=m.history.data['facts']['continuous/ending']; f.update(time=point(4000),publicTimePrecision=point(4000))
    result=cast(m,request); check('no-future-transition-disclosed',not any(a.get('time')==point(4000) for a in assertions(result))); record('future-is-not-history',m)
    expected={v['id'] for s in json.loads((R/'data/playtest/spell_candidates/divination_rank7_exact_01_expectations.json').read_bytes())['supplementalSourceExpectations'] if s['id']=='DI7-SUPREME-TIME-SCOPE-01' for v in s['variants']}
    check('all8-current-temporal-expectations-executed',set(coverage)==expected and len(expected)==8)
    bindings=sources.bindings+[info(p) for p in [R/'tools/di7_supreme_transactions.py',R/'tools/validate_di7_supreme_transactions.py',R/'tools/di7_area_geometry.py',
        R/'tools/di7_area_fixtures.py',R/'tools/di7_fate_transactions.py',R/'tools/di7_cast_transactions.py',A/'DI7_SUPREME_TIME_SCOPE_RECEIVED.json',
        R/'data/playtest/spell_candidates/divination_rank7_exact_01_expectations.json']]
    report={'status':'pass','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'checks':len(checks),'historyCount':len(histories),'sourceBindings':bindings,
        'sourceExpectationCoverage':coverage,'checkLabels':checks,'histories':histories,'failures':[],
        'scope':'Paid four-provider Supreme history using current scoped geometry; uncapped actual past/present local occurrences, real intervals/transitions, true precision, unresolved applicability and native partial-history protection without public gap diagnostics.',
        'conditionalPremises':['Actual Director-established history, magical nature, source-defined fields, local visits and native temporal relations are explicit upstream conditional facts; no real campaign or native grant is authenticated.',
            'Occupied geometry/clipping, caster attainment/rest and genuine channel delivery retain their existing conditional premises.',
            'Native block/authorized single-field mask scopes are executed against supplied query subject/domain/channel/school/rank and native exact endpoints; conflicting mask arbitration and authored acquisition of those defenses remain upstream.',
            'Input positive transitions/observations must actually be established; the evaluator does not manufacture missing observation timestamps or infer semantic facts from source prose.'],
        'remaining':['Actual ordinary Shaman totem vent and its casting-order source confirmation.',
            'Compile original49 and supplemental expectations and submit all complete7 public/internal cards for separate exact review.',
            'Broader arbitrary history authoring, native protection acquisition/arbitration, full runtime and human playtesting remain unproved.'],
        'supremeTime8Executed':True,'candidateApproved':False,'full49Fulfilled':False,'humanPlaytest':False,'spellPromotions':0,'newRuleAdoptions':0}
    output.write_bytes(encoded(report)); print(json.dumps({'report':info(output),'checks':len(checks),'histories':len(histories),'temporalExpectationsExecuted':len(coverage)}))


if __name__=='__main__': main()
