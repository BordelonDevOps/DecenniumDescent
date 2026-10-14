"""Paid four-category snapshots, factual/protection limits and observer histories."""
from copy import deepcopy
from datetime import datetime,timezone
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded
from di7_cast_transactions import DI7Sources
from di7_area_fixtures import make as area_fixture
from di7_mass_transactions import MassTransactions


def main():
    output=A/'DI7_MASS_TRANSACTIONS_CHECK.json'; assert not output.exists()
    sources=DI7Sources(); checks=[]; histories=[]
    def check(label,value): assert value,label; checks.append(label)
    def record(label,m): histories.append({'id':label,'final':m.snapshot()})
    def reject(label,m,fn):
        before=m.snapshot()
        try: fn()
        except ValueError as e: check(label+'/rejected',bool(str(e)))
        else: raise AssertionError(label)
        check(label+'/atomic',before==m.snapshot())
    def fact(fid,value,*,subject=None,category='information',at=3500):
        return {'id':fid,'subject':subject or fid.split('/')[0],'category':category,'actualTime':at,'establishedAt':at,
            'authorityVersion':'conditional-world-v1','authorityEvent':'Director-established/'+fid,'publicFields':{'value':value}}
    def protection(subject,category,*,existence=True):
        return {'id':subject+'/'+category,'nativeScopePremise':{'kind':'conditional-actual-native-protection-scope','sourceVersion':'conditional-native-v1',
                'sourceGrantEvent':'actual-upstream-conditional-protection','completeScopeText':'Conditional actual native source blocks only the named subject and category/value for rank7 Divination during the supplied time scope; no new selectable protection is authored.'},
            'mode':'block','activeFrom':3500,'activeUntil':4000,'subjects':[subject],'querySchools':['Divination'],
            'minimumQueryRank':7,'maximumQueryRank':7,'categories':[category],'factTimeFrom':0,'factTimeUntil':4000,
            'protectsExistence':existence,'fields':['value'],'maskedFields':{}}
    def make(provider='Wizard',*,count=1,protections=None):
        base,request=area_fixture(sources,provider=provider,points=[[10,0,0],[15,0,0],[20,0,0],[60,30,0],[65,0,0]])
        world=deepcopy(base.world); actors=deepcopy(base.actors)
        facts={}; records={}; assertions=[]
        world['currentParty']={'owner':['ally']}; world['informationChannels']={}
        world['creatures']={a:{'conditions':[],'currentPortions':[],'locationRevision':'initial/'+a} for a in ['owner','counter','ally']}
        world['observerStates']={}
        def record_row(rid,kind,portion,fields):
            facts[rid+'/exists']=fact(rid+'/exists',True,category='existence')
            facts[rid+'/location']=fact(rid+'/location',True,category='location')
            for name,value in fields.items(): facts[rid+'/'+name]=fact(rid+'/'+name,value,category=name)
            records[rid]={'category':kind,'subject':rid,'existsNow':True,'portionIds':[portion],
                'authorityEvent':'actual-record/'+rid,'sourceVersion':'world-v1','existenceFact':rid+'/exists','locationFact':rid+'/location',
                'fieldFacts':{name:rid+'/'+name for name in fields}}
            return records[rid]
        trap=record_row('plate','trap','portion-0',{'armedState':'armed','immediateTriggerCategory':'weight-on-plate'}); trap['actualPhysicalTrap']=True
        trap['privateDisarmCode']='SECRET-DISARM-CODE'
        spell=record_row('actual-spell','magic','portion-1',{'spellOrNonspell':'spell','school':'Abjuration','rank':3,'state':'suppressed'}); spell['actuallyMagical']=True
        enchantment=record_row('dormant-enchantment','magic','portion-1',{'spellOrNonspell':'nonspell','state':'dormant'}); enchantment['actuallyMagical']=True
        enchantment['privateCharges']=999; enchantment['privateFullPower']='SECRET-POWER'
        decoy=record_row('nonmagic-decoration','magic','portion-0',{'spellOrNonspell':'nonspell','rank':0,'state':'active'}); decoy['actuallyMagical']=False
        for i in range(count):
            enemy='hostile-'+str(i); row=record_row(enemy,'enemy','portion-2',{})
            facts[enemy+'/intent']=fact(enemy+'/intent',{'state':'intending','meaningfulHostileAct':True,'targetIds':['ally']},category='intent')
            row['intentFact']=enemy+'/intent'; row['privateName']='SECRET-IDENTITY'; row['privatePlan']='SECRET-PLAN'
            world['creatures'][enemy]={'conditions':['invisible'],'currentPortions':['portion-2'],'locationRevision':'initial/'+enemy}
            for observer in ['owner','ally','counter']: world['observerStates'][observer+'>'+enemy]={'hidden':True,'visible':False,'darkness':False}
        # Same real local creature can sincerely err or deliberately deceive.
        world['creatures']['speaker']={'conditions':[],'currentPortions':['portion-0'],'locationRevision':'initial/speaker'}
        for aid,at,believed_false,semantic in [('lie-at-six',3594,True,'actual-assertion'),('sincere-error',3598,False,'actual-assertion'),
            ('irony',3599,True,'irony-not-an-assertion'),('too-old',3593.999,True,'actual-assertion'),('decoded-sign',3600,True,'actual-assertion')]:
            facts[aid+'/exists']=fact(aid+'/exists',True,subject='speaker',category='existence',at=at)
            facts[aid+'/belief']=fact(aid+'/belief',believed_false,subject='speaker',category='assertion-belief',at=at)
            assertions.append({'id':aid,'authorityEvent':'actual-assertion/'+aid,'speaker':'speaker','at':at,'semanticKind':semantic,
                'existenceFact':aid+'/exists','beliefFact':aid+'/belief','actualObjectiveTruth':'SECRET-CORRECT-ANSWER',
                'actualReception':{'owner':{'authorityEvent':'actual-understood-speech-or-decoded-sign/'+aid,'perceived':True,'understood':True,'understoodAssertion':aid+' content understood by caster'}}})
        data={'kind':'explicit-conditional-Director-established-world','facts':facts,'protections':protections or [],'questions':{},'canonicalQuestions':{},'steps':{}}
        m=MassTransactions(sources,actors,world,dossier=data,records=records,assertions=assertions)
        level=m.actors['owner']['classLevel']; m.learn('owner','mass-revelation',level,'owner-actual-learning')
        m.learn('counter','counterspell',5,'counter-actual-learning')
        for aid,a in m.actors.items():
            if a['provider']=='Wizard': m.prepare_wizard(aid,list(a['learned']),aid+'/study',{'actor':aid,'completedAt':0,'sourceEvent':'conditional-completed-rest'})
        m.begin_turn('owner','owner-turn1'); return m,request
    def cast(m,request):
        m.declare('owner','mass-revelation','mass',request); return m.resolve_mass('mass')
    for provider in ['Wizard','Cleric','Mirrorsage','Shaman']:
        m,request=make(provider); result=cast(m,request)
        check(provider+'/actual17RP-all-four-categories',m.actors['owner']['rp']==m.actors['owner']['maxRP']-17 and all(result[c] for c in ['traps','enemies','magic','lies']))
        check(provider+'/readable-party-hostility-not-self-only',result['readableEnemyCount']==1)
        check(provider+'/overlapping-magic-separate-null-not-zero',len(result['magic'])==2 and result['magic'][1]['rank']=='Indeterminate' and result['magic'][1]['school']=='Indeterminate')
        check(provider+'/suppressed-and-dormant-real-effects', [r['state'] for r in result['magic']]==['suppressed','dormant'])
        check(provider+'/inclusive6-and-current-decoded-sign-only',[r['assertedAt'] for r in result['lies']]==[3594,3600])
        public=json.dumps(result)
        check(provider+'/no-private-code-power-identity-truth',not any(x in public for x in ['SECRET','999','privateName','privatePlan']))
        check(provider+'/no-disarm-dispel-or-new-sense',m.records['plate']['actualPhysicalTrap'] and m.information.data['facts']['plate/armedState']['publicFields']['value']=='armed' and not m.world['observerStates']['owner>hostile-0']['visible'])
        record('paid-four-categories/'+provider,m)
    m,request=make(count=125); result=cast(m,request)
    check('no-arbitrary-enemy-count-cap',len(result['enemies'])==125 and result['readableEnemyCount']==125); record('125-actual-enemies',m)
    for predicate in ['peaceful','disagreement','foreign-target','enemy-flag-only']:
        m,request=make(); intent=m.information.data['facts']['hostile-0/intent']['publicFields']['value']
        m.records['hostile-0'].update(enemyFlag=True,alignment='Evil',species='disliked',reputation=-100)
        if predicate=='peaceful': intent['state']='no-hostile-intent'
        elif predicate=='disagreement': intent['meaningfulHostileAct']=False
        elif predicate=='foreign-target': intent['targetIds']=['unrelated-nonparty']
        else: del m.information.data['facts']['hostile-0/intent']
        result=cast(m,request); check(predicate+'/no-invented-enemy',result['readableEnemyCount']==0 and not m.knows_current_location('owner','hostile-0'))
        record('actual-hostility/'+predicate,m)
    for category in ['existence','intent','location']:
        m,request=make(protections=[protection('hostile-0',category)])
        result=cast(m,request)
        if category in {'existence','intent'}: check(category+'/no-enemy-or-count',not result['enemies'] and result['readableEnemyCount']==0)
        else: check('location/independent-readable-count',result['readableEnemyCount']==1 and result['enemies'][0]['localFootprint']=='Indeterminate')
        check(category+'/no-observer-location-grant',not m.knows_current_location('owner','hostile-0') and m.world['observerStates']['owner>hostile-0']['hidden'])
        check(category+'/other-categories-useful',len(result['traps'])==1 and len(result['magic'])==2)
        refs=[r['reference'] for cat in ['traps','enemies','magic','lies'] for r in result[cat]]
        check(category+'/no-hidden-sequence-gap',sorted(refs)==sorted('reading-'+str(i+1) for i in range(len(refs))))
        record('native-scope/'+category,m)
    m,request=make(protections=[protection('plate','immediateTriggerCategory')]); result=cast(m,request)
    check('protected-trigger-keeps-site-state',result['traps'][0]['armedState']=='armed' and result['traps'][0]['localFootprint']!='Indeterminate' and result['traps'][0]['immediateTriggerCategory']=='Indeterminate')
    record('trap-field-protection',m)
    m,request=make(protections=[protection('speaker','assertion-belief')]); result=cast(m,request)
    check('belief-protection-no-lie-inference',not result['lies']); record('belief-protection',m)
    for label in ['unheard','not-understood','speaker-left','recorded-sound','future-assertion']:
        m,request=make()
        for assertion in m.assertions:
            if label=='unheard': assertion['actualReception']['owner']['perceived']=False
            elif label=='not-understood': assertion['actualReception']['owner']['understood']=False
            elif label=='speaker-left': m.world['creatures']['speaker']['currentPortions']=['portion-4']
            elif label=='recorded-sound': assertion['semanticKind']='recorded-sound-without-current-speaker-assertion'
            else: assertion['at']=3601
        result=cast(m,request); check(label+'/no-invented-assertion-reading',not result['lies']); record('lie-admission/'+label,m)
    for label in ['wall','corner','empty-bounding-box']:
        m,request=make(); portion=m.world['geometry']['portions']['portion-2']
        if label=='wall': portion['clippingByOrigin']['0,0,0']['totalCover']=True
        elif label=='corner': portion['clippingByOrigin']['0,0,0']['blockedCorner']=True
        else: portion['actuallyOccupiedNow']=False
        result=cast(m,request); check(label+'/no-geometry-bypass',not result['enemies'] and not m.knows_current_location('owner','hostile-0'))
        record('geometry/'+label,m)
    m,request=make(); m.records['hostile-0']['portionIds']=['portion-3','portion-4']; m.world['creatures']['hostile-0']['currentPortions']=['portion-3','portion-4']
    result=cast(m,request)
    check('partial-footprint-only-no-radial-cap',result['enemies'][0]['localFootprint']==[{'part':'local-portion-3','center':[60,30,0]}]); record('partial-footprint-at-cone-boundary',m)
    m,request=make(); before=m.attack_modifiers('owner','hostile-0')
    result=cast(m,request)
    check('actual-location-ends-Hidden-for-caster',not m.world['observerStates']['owner>hostile-0']['hidden'] and m.world['observerStates']['ally>hostile-0']['hidden'])
    check('Invisible-target-own-attack-modifier-removed',before['rollMode']=='disadvantage' and m.attack_modifiers('owner','hostile-0')['rollMode']=='normal')
    check('Invisible-attacker-own-attack-modifier-removed',m.attack_modifiers('hostile-0','owner')['rollMode']=='normal' and m.attack_modifiers('hostile-0','ally')['rollMode']=='advantage')
    check('independent-darkness-remains',m.attack_modifiers('owner','hostile-0',other_disadvantage=True)['rollMode']=='disadvantage')
    m.world['creatures']['owner']['conditions'].append('blinded')
    check('independent-blindness-remains',m.attack_modifiers('owner','hostile-0')['rollMode']=='disadvantage')
    check('location-never-creates-sight',not m.world['observerStates']['owner>hostile-0']['visible'])
    record('condition-helper-observer-specific-results',m)
    # Actual received records, not an automatic party copy or private dossier.
    enemy_row=deepcopy(result['enemies'][0]); m.world['informationChannels']['actual-warning']={'authorityEvent':'conditional-source-qualified-delivered-warning',
        'from':'owner','to':'ally','at':m.now,'received':True,'understood':True,'deliveredRecords':[enemy_row]}
    communicated=m.communicate('mass','ally','actual-warning')
    check('actual-warning-only-delivered-record',communicated['deliveredRecords']==[enemy_row] and 'traps' not in communicated and 'privateLocationBindings' not in communicated)
    check('informed-ally-gets-current-location-effect',m.knows_current_location('ally','hostile-0') and not m.world['observerStates']['ally>hostile-0']['hidden'] and not m.world['observerStates']['ally>hostile-0']['visible'])
    reject('channel-event-not-replayed',m,lambda:m.communicate('mass','ally','actual-warning')); record('actual-limited-communication',m)
    m,request=make(); result=cast(m,request); m.advance(3601)
    m.world['creatures']['hostile-0'].update(locationRevision='actual-move-v2',currentPortions=['portion-3'])
    check('snapshot-no-tracking-after-actual-move',not m.knows_current_location('owner','hostile-0') and m.revelations['mass']['public']==result)
    m.world['informationChannels']['late-warning']={'authorityEvent':'conditional-source-qualified-delivery-of-old-location','from':'owner','to':'ally',
        'at':m.now,'received':True,'understood':True,'deliveredRecords':[deepcopy(result['enemies'][0])]}
    m.communicate('mass','ally','late-warning')
    check('old-location-warning-no-current-Hidden-removal',not m.knows_current_location('ally','hostile-0') and m.world['observerStates']['ally>hostile-0']['hidden'])
    record('snapshot-and-stale-communication',m)
    m,request=make(); m.declare('owner','mass-revelation','mass',request)
    m.declare('counter','counterspell','counter-mass',{'pendingCast':'mass'}); m.resolve_counter('counter-mass',20)
    reject('actual-counter-no-information',m,lambda:m.resolve_mass('mass'))
    check('countered-cost-kept-private-state-empty',m.actors['owner']['rp']==31 and not m.revelations and not m.knowledge); record('actual-counterspell',m)
    m,request=make(); m.declare('owner','mass-revelation','mass',request)
    m.information.data['facts']['hostile-0/intent']['publicFields']['value']['state']='ceased-before-resolution'
    result=m.resolve_mass('mass'); check('actual-resolution-time-snapshot',not result['enemies']); record('actual-change-during-counter-window',m)
    m,request=make(); first=cast(m,request); m.begin_turn('owner','owner-turn2')
    m.declare('owner','mass-revelation','mass-again',request); second=m.resolve_mass('mass-again')
    check('equivalent-actual-paid-repeated-inquiry-consistent',first==second and m.actors['owner']['rp']==14 and m.casts['mass-again']['quote']['cost']==17 and m.actors['owner']['refrain']==1 and m.actors['owner']['dissonance']==3)
    record('repeated-paid-query-with-Refrain',m)
    bindings=sources.bindings+[info(p) for p in [R/'tools/di7_mass_transactions.py',R/'tools/validate_di7_mass_transactions.py',R/'tools/di7_area_fixtures.py',
        R/'tools/di7_area_geometry.py',R/'tools/di7_vision_transactions.py',R/'tools/di7_fate_transactions.py',R/'tools/di7_cast_transactions.py',R/'tools/condition_playtest_rules.py',
        R/'data/playtest/spell_candidates/divination_rank7_exact_01_expectations.json']]
    report={'status':'pass','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'checks':len(checks),'historyCount':len(histories),'sourceBindings':bindings,
        'checkLabels':checks,'histories':histories,'failures':[],
        'scope':'Actual conditional paid Mass Revelation geometry and all four snapshot categories, protection scope, source-defined facts, observer-specific Hidden/Invisible consequences and actual literal communication.',
        'conditionalPremises':['Actual attained caster/body/rest inputs; general character progression remains upstream.',
            'Director-established real traps, magical effects, hostile intent against current party, semantic assertions and actual perceived/understood content; this is not a natural-language belief oracle.',
            'Actual source-qualified native protection grants/scopes and geometry/clipping remain conditional interfaces; no new native protection ability or generic ray tracing is authored.',
            'Observer condition sources and movement revisions, and the actual legal communication event/delivery, are upstream premises. The current attack helper computes modifiers, not a complete paid attack/damage history.'],
        'remaining':['Supreme Sight historical information payload, Suggestion initiative clock and ordinary Shaman totem vent.',
            'Named native protection acquisition and conflicting-mask arbitration; full ordinary communication and attacks are not implemented here.',
            'Compile original49 and supplemental source expectations and obtain separate exact-seven-card acceptance.'],
        'candidateApproved':False,'full49Fulfilled':False,'humanPlaytest':False,'spellPromotions':0,'newRuleAdoptions':0}
    output.write_bytes(encoded(report)); print(json.dumps({'report':info(output),'checks':len(checks),'histories':len(histories)}))


if __name__=='__main__': main()
