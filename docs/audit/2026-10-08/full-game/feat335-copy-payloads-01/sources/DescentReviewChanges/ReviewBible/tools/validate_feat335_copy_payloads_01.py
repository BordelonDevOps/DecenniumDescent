"""Exercise source-qualified copied payloads after actual paid commitment."""
from copy import deepcopy
from dataclasses import asdict,is_dataclass
from datetime import datetime,timezone
from fractions import Fraction
from pathlib import Path
import ast,json,sys
from core_playtest_rules import LifeState
from control_playtest_rules import ClockMarker,SpeedRecord,turn_end_deadline
from form_temphp_playtest_rules import BufferGrant
from healing_playtest_rules import HealingReduction
from feat335_copy_payload_fixtures import CopyPayloadFixtures,R,G,A
from validate_feat_exact_01_composite_casting import info


def clean(value):
    if isinstance(value,Fraction):return {'fraction':[value.numerator,value.denominator]}
    if is_dataclass(value):return {'dataclass':type(value).__name__,**clean(asdict(value))}
    if isinstance(value,dict):
        if all(isinstance(k,str) for k in value):return {k:clean(v) for k,v in value.items()}
        return {'keyValueEntries':[{'key':clean(k),'value':clean(v)} for k,v in value.items()]}
    if isinstance(value,(list,tuple)):return [clean(v) for v in value]
    if isinstance(value,set):return [clean(v) for v in sorted(value,key=repr)]
    return value


def main():
    output=A/'FEAT335_COPY_PAYLOADS_01_CHECK.json';write=sys.argv[1:]==['--write-report']
    if sys.argv[1:] and not write:raise ValueError('Use no arguments or --write-report')
    if write:assert not output.exists(),'Preserve successful prior evidence'
    f=CopyPayloadFixtures();checks=[];histories=[]
    paths=f.paths+[Path(__file__),R/'tools/feat335_copy_payloads.py',R/'tools/feat335_copy_payload_fixtures.py',
        A/'FEAT335_COPY_RELEASE_01_CHECK.json',A/'FEAT335_COPY_RELEASE_01_PROGRESS.json',
        A/'feat335-copy-release-source-addendum-01/FEAT335_COPY_RELEASE_SOURCE_ADDENDUM_01.json',
        R/'data/public/feat_candidates/exact_01/shared_rules.json',R/'data/public/feat_candidates/exact_01/candidate.json',
        R/'docs/mechanics/CLASS_PLAYTEST_RULES.md',R/'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md',
        R/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md',R/'data/playtest/druid_form_profiles.json',R/'data/playtest/spell_form_profiles.json']
    pending=[p for p in paths if p.suffix=='.py'];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p)
        for node in ast.walk(ast.parse(p.read_text('utf8'))):
            names=[node.module] if isinstance(node,ast.ImportFrom) else [a.name for a in node.names] if isinstance(node,ast.Import) else []
            for name in names:
                if not name:continue
                dep=R/'tools'/(name.split('.')[0]+'.py')
                if dep.exists():
                    if dep not in paths:paths.append(dep)
                    pending.append(dep)
    bindings=[info(p) for p in paths]
    def check(label,ok):
        checks.append({'id':label,'passed':bool(ok)});assert ok,label
    def reject(label,m,fn):
        before=m.snapshot()
        try:fn()
        except ValueError:check(label,True)
        else:check(label,False)
        check(label+'/atomic',before==m.snapshot())
    def record(label,m):histories.append({'id':label,'state':clean(m.snapshot()),'acquisition':clean(m.captures.acquired.snapshot()),'sourceWitnesses':clean(m.captures.witnesses.snapshot())})
    def paid(profile,selection=None,source=None):
        m=f.make();f.capture(m,profile,source=source);f.start(m);f.declare(m,profile,selection=selection);return m
    def strike(m,faces=None,native=None,core=None):
        return m.resolve('cast',rolls={'nativeDice':[6] if native is None else native,
            'targets':{'target':{'faces':[10] if faces is None else faces,'core':f.core() if core is None else core}}})
    def burst(m,targets,faces,native=None,cores=None):
        return m.resolve('cast',rolls={'nativeDice':[6,6] if native is None else native,
            'targets':{t:{'faces':[d],'core':f.core() if cores is None else cores[t]} for t,d in zip(targets,faces)}})

    m=paid('strike');life=m.world.actors['target']['life'];result=strike(m,faces=[20],core=f.core(critical=True))
    check('Strike/critical-no-extra-damage-die',result['nativeBoundedAmount']==3 and life.hp==27 and result['targets']['target']['attack']['critical'])
    check('Strike/canonical-LifeState-retained',m.world.actors['target']['life'] is life)
    reject('Strike/replayed-resolution',m,lambda:strike(m));record('Strike-critical-bound',m)
    m=paid('strike');result=m.resolve('cast',rolls={'nativeDice':[],'targets':{'target':{'faces':[1],'core':None}}})
    check('Strike/miss-no-damage-RNG',result['nativeBoundedAmount'] is None and m.world.actors['target']['life'].hp==30)
    record('Strike-miss',m)
    m=paid('strike');reject('Strike/no-extra-critical-dice',m,lambda:strike(m,faces=[20],native=[6,6],core=f.core(critical=True)))
    strike(m,faces=[20],core=f.core(critical=True));record('invalid-RNG-retry-no-repayment',m)
    m=paid('strike');m.world.actors['target']['life']=LifeState(40,0)
    result=strike(m,faces=[20],core=f.core(critical=True))
    check('Strike/ordinary-critical-zeroHP-failures',m.world.actors['target']['life'].death_failures==2 and result['targets']['target']['deathFailuresAdded']==2)
    record('Strike-zeroHP-critical',m)
    m=paid('strike',source='source-mend');m.world.actors['target']['life']=LifeState(16,9)
    result=strike(m,native=[6,6],core=f.core(wound=10))
    check('Strike/canonical-Wound-save-at-zero',result['nativeBoundedAmount']==9 and m.world.actors['target']['life'].hp==0 and result['targets']['target']['woundSaves']==1 and not m.world.actors['target']['life'].wounds)
    record('Strike-Wound-and-zero',m)
    m=paid('strike',source='source-mend');m.world.actors['target']['life']=LifeState(16,9,wounds=(None,None,None))
    result=strike(m,native=[6,6],core=f.core(wound=5))
    check('Strike/fatal-existing-three-Wounds',m.world.actors['target']['life'].dead and len(m.world.actors['target']['life'].wounds)==3)
    record('Strike-fatal-Wound',m)

    targets=['target','target2','target3'];m=paid('burst',f.selection('burst',targets))
    m.world.actors['target2']['damageResistances'].add('fire');m.world.actors['target3']['damageImmunities'].add('fire')
    result=burst(m,targets,[1,20,1])
    check('Burst/shared-native-seven',result['nativeBoundedAmount']==7)
    check('Burst/per-target-save-and-defense',[m.world.actors[t]['life'].hp for t in targets]==[23,29,30])
    check('Burst/save-then-resistance',result['targets']['target2']['afterSave']==3 and result['targets']['target2']['afterDefenses']==1)
    check('Burst/no-retarget-fourth',m.world.actors['target4']['life'].hp==30)
    record('Burst-three-recipient-shared-roll',m)
    m=paid('burst',f.selection('burst',targets));m.world.observations[('owner','target3')]['areas']['area']['lineOfEffect']=False
    result=burst(m,targets[:2],[1,1]);check('Burst/blocked-original-recipient-not-replaced',set(result['targets'])==set(targets[:2]) and m.world.actors['target3']['life'].hp==30)
    record('Burst-late-cover',m)
    m=paid('burst');m.world.actors['target']['dexSaveModifier']=20
    result=burst(m,['target'],[1]);check('Burst/save-natural1-no-auto-failure',result['targets']['target']['save']['success'] and m.world.actors['target']['life'].hp==27)
    m=paid('burst');m.world.actors['target']['dexSaveModifier']=-10
    result=burst(m,['target'],[20]);check('Burst/save-natural20-no-auto-success',not result['targets']['target']['save']['success'] and m.world.actors['target']['life'].hp==23)
    record('Burst-binary-save',m)
    m=paid('strike',source='source-mend');m.world.actors['target']['flatDamageReduction']=3;m.world.actors['target']['damageResistances'].add('necrotic')
    result=strike(m,native=[6,6]);check('Damage/strongest-flat-before-resistance',result['targets']['target']['afterDefenses']==3 and m.world.actors['target']['life'].hp==27)
    record('Damage-defense-order',m)

    m=paid('mend');target=m.world.actors['target'];target['life']=LifeState(40,38,wounds=(None,None,None))
    ref=target['life'];result=m.resolve('cast',rolls={'nativeDice':[6,6]})
    check('Mend/half-native-and-Critical-cap',result['nativeBoundedAmount']==2 and ref.hp==39 and len(ref.wounds)==3 and result['targets']['target']['actualHpGained']==1)
    check('Mend/no-resource-conversion',result['resourceConversionAllowed'] is False and m.pool['rp']==42)
    record('Mend-Critical-cap',m)
    m=paid('mend');m.world.actors['target']['hpGainProhibited']=True
    result=m.resolve('cast',rolls={'nativeDice':[6,6]})
    check('Mend/HP-prohibition-no-refund',m.world.actors['target']['life'].hp==30 and result['targets']['target']['actualHpGained']==0 and m.pool['rp']==42)
    record('Mend-prohibited',m)
    m=paid('mend');m.world.actors['target']['healingSystemicFactors']=[Fraction(1,2)]
    result=m.resolve('cast',rolls={'nativeDice':[6,6]});check('Mend/actual-Corrupted-factor',m.world.actors['target']['life'].hp==31)
    m=paid('mend');m.world.actors['target']['healingReductions']=[HealingReduction('suppression','actual-reducer','flat',1)]
    result=m.resolve('cast',rolls={'nativeDice':[6,6]});check('Mend/existing-healing-reducer',m.world.actors['target']['life'].hp==31)
    record('Mend-reduction',m)
    m=paid('mend');m.world.actors['target']['life']=LifeState(40,0,death_failures=2)
    m.resolve('cast',rolls={'nativeDice':[6,6]})
    check('Mend/ordinary-living-zeroHP-recovery',m.world.actors['target']['life'].hp==2 and m.world.actors['target']['life'].death_failures==0)
    record('Mend-living-zero',m)

    m=paid('ward');life=m.world.actors['target']['life'];result=m.resolve('cast',rolls={'nativeDice':[6,6]})
    check('Ward/one-actual-grant',life.temp_hp==m.world.buffers.amount('target')==4 and len(m.world.buffers.active)==1)
    check('Ward/second-future-start',m.world.effects[result['effectId']]['deadline']==ClockMarker(18))
    m.lifecycle.ledger.end('owner','failed-concentration')
    check('Ward/cleanup-canonical-grant-and-LifeState',life.temp_hp==m.world.buffers.amount('target')==0 and not m.world.effects[result['effectId']]['active'])
    record('Ward-concentration-cleanup',m)
    for existing in [4,6]:
        m=paid('ward');grant=BufferGrant('older','other-real-source','target','target',existing,rest_epoch=0)
        m.world.buffers.offer(grant,m.world.now);m.world.projection()
        result=m.resolve('cast',rolls={'nativeDice':[6,6]})
        check('Ward/rejected-offer/'+str(existing),m.world.buffers.current('target').grant_id=='older' and m.world.buffers.amount('target')==existing and result['effectId'] is None and m.pool['rp']==42)
        record('Ward-rejected-'+str(existing),m)
    m=paid('ward');m.resolve('cast',rolls={'nativeDice':[6,6]});m.world.advance(Fraction(179,10),[m])
    check('Ward/before-deadline',m.world.buffers.amount('target')==4)
    m.world.advance(18,[m]);check('Ward/exact-deadline',m.world.buffers.amount('target')==0 and not m.lifecycle.ledger.current)
    record('Ward-deadline',m)
    # A distinct caster's genuine copy damage consumes the SAME buffer object.
    m=paid('ward');m.resolve('cast',rolls={'nativeDice':[6,6]});world=m.world;life=world.actors['target']['life']
    n=f.make('other',world,m.lifecycle.ledger);f.capture(n,'strike',source='source-mend');n.captures.start_regular('other-turn',1,1,actual_new_regular_start=True)
    f.declare(n,'strike');result=strike(n,native=[6,6])
    check('Ward/damage-shared-ledger-once',life.hp==25 and life.temp_hp==world.buffers.amount('target')==0 and result['targets']['target']['tempAbsorbed']==4)
    record('Ward-to-other-caster-damage',n)
    m=paid('ward');m.resolve('cast',rolls={'nativeDice':[6,6]})
    f.capture(m,'boon',event='next-capture',sid='eldritch_echo')
    m.captures.end_regular('turn1',actual_regular_end=True)
    m.captures.start_regular('turn2',2,2,actual_new_regular_start=True)
    m.world.advance(Fraction(121,10),[m]);m.world.actors['owner']['inProgressRegularEnd']=Fraction(49,4)
    f.declare(m,'boon',event='second-cast',cap='next-capture')
    check('new-concentration/old-actual-buffer-ends-at-commit',m.world.buffers.amount('target')==0 and m.world.actors['target']['life'].temp_hp==0)
    m.resolve('second-cast',countered=True)
    check('new-concentration/counter-no-old-buffer-return',m.world.buffers.amount('target')==0 and m.world.ac('target')==12 and m.pool['rp']==40 and not m.lifecycle.ledger.current)
    record('real-buffer-displaced-before-counter',m)

    m=paid('hindrance');result=m.resolve('cast',rolls={'faces':[1]})
    check('Hindrance/actual-speed-and-Reaction',m.world.speed('target')==20 and not m.world.reaction_allowed('target'))
    check('Hindrance/target-end-earlier-than-owner-cap',m.world.effects[result['effectId']]['deadline']==turn_end_deadline(Fraction(33,4)))
    m.world.speed_records.append(SpeedRecord('other-slow','other','target','other','half','half',expires=ClockMarker(30)))
    check('Hindrance/strongest-not-cumulative',m.world.speed('target')==15)
    m.lifecycle.ledger.end('owner','lost-concentration')
    check('Hindrance/cleanup-keeps-other-slow',m.world.speed('target')==15 and m.world.reaction_allowed('target'))
    record('Hindrance-arbitration-and-cleanup',m)
    m=paid('hindrance');m.resolve('cast',rolls={'faces':[1]})
    m.world.advance(ClockMarker(Fraction(33,4),10),[m]);check('Hindrance/through-end-effects',not m.world.reaction_allowed('target'))
    m.world.advance(turn_end_deadline(Fraction(33,4)),[m]);check('Hindrance/after-end-expiry',m.world.reaction_allowed('target') and m.world.speed('target')==30)
    record('Hindrance-ordered-end-expiry',m)
    for save,immune in [(20,False),(1,True)]:
        m=paid('hindrance');m.world.actors['target']['copyHindranceImmune']=immune;m.resolve('cast',rolls={'faces':[save]})
        check('Hindrance/save-or-immunity/'+str((save,immune)),m.world.speed('target')==30 and m.world.reaction_allowed('target') and not m.lifecycle.ledger.current)

    m=paid('boon');m.resolve('cast')
    check('Boon/AC-one-point',m.world.ac('target')==13)
    n=f.make('other',m.world,m.lifecycle.ledger);f.capture(n,'boon');n.captures.start_regular('other-turn',1,1,actual_new_regular_start=True);f.declare(n,'boon');n.resolve('cast')
    check('Boon/same-family-across-owners-no-stack',m.world.ac('target')==13)
    m.lifecycle.ledger.end('owner','lost-concentration');check('Boon/other-owner-persists',m.world.ac('target')==13)
    n.lifecycle.ledger.end('other','lost-concentration');check('Boon/all-ended-no-AC',m.world.ac('target')==12)
    record('Boon-multiowner-arbitration',n)
    m=paid('boon');m.resolve('cast');m.world.advance(Fraction(49,4),[m]);check('Boon/next-future-end-not-current',m.world.ac('target')==13)
    m.world.advance(turn_end_deadline(Fraction(49,4)),[m]);check('Boon/exact-next-end',m.world.ac('target')==12)
    record('Boon-end-boundary',m)
    m=paid('step');body=m.world.actors['owner'];position=body['position'];life=body['life'];hp=life.hp;rp=m.pool['rp'];m.resolve('cast')
    check('Step/same-body-personal-teleport',position==[10,0,0] and body['position'] is position and body['life'] is life and life.hp==hp and m.pool['rp']==rp and m.world.actors['target']['position']==[0,0,0])
    record('Step-no-body-or-passenger-copy',m)

    # Invalid declarations are rejected before any payment; post-commit world
    # changes consume the already-paid cast without substituting a new target.
    for profile in ['strike','burst','mend','ward','hindrance','boon']:
        m=f.make();f.capture(m,profile);f.start(m);m.world.observations[('owner','target')]['perceived']=False
        reject('preflight-unperceived/'+profile,m,lambda:f.declare(m,profile))
    for profile in ['mend','ward']:
        for field in ['living','willing']:
            m=f.make();f.capture(m,profile);f.start(m);m.world.actors['target'][field]=False
            reject('preflight/'+profile+'/'+field,m,lambda:f.declare(m,profile))
    m=f.make();f.capture(m,'burst');f.start(m)
    reject('Burst/four-targets-ineligible',m,lambda:f.declare(m,'burst',selection=f.selection('burst',['target','target2','target3','target4'])))
    m=f.make();f.capture(m,'boon');f.start(m)
    reject('Boon/no-unobserved-save-statistic',m,lambda:f.declare(m,'boon',selection={'targets':['target'],'statistic':'save'}))
    for field in ['visible','fitting','unoccupied','lineOfEffect','teleportAllowed']:
        m=f.make();f.capture(m,'step');f.start(m);s=f.selection('step');s[field]=False
        reject('Step/'+field,m,lambda:f.declare(m,'step',selection=s))
    m=f.make();f.capture(m,'step');f.start(m);s=f.selection('step');s['distanceFeet']=16
    reject('Step/half-observed-cap',m,lambda:f.declare(m,'step',selection=s))
    for profile in ['strike','burst','mend','ward','hindrance','boon','step']:
        m=paid(profile);rp=m.pool['rp'];result=m.resolve('cast',countered=True)
        check('counter/'+profile,not result['resolved'] and m.pool['rp']==rp and not m.world.effects and m.world.actors['target']['life'].hp==30)
    m=paid('ward');m.world.observations[('owner','target')]['lineOfEffect']=False
    result=m.resolve('cast');check('late-invalid-target-cost-retained',not result['resolved'] and m.pool['rp']==42 and m.world.buffers.amount('target')==0)
    record('late-invalid-target',m)
    m=paid('step');m.selections['cast']['current']['fitting']=False
    result=m.resolve('cast');check('late-obstruction-no-teleport-or-refund',not result['resolved'] and m.pool['rp']==42 and m.world.actors['owner']['position']==[0,0,0])
    m=paid('strike');m.selections['cast']['current']['targets']=['target2'];reject('no-retarget-after-cost',m,lambda:strike(m))
    m=paid('hindrance');m.lifecycle.ledger.end('owner','nested-loss');result=m.resolve('cast')
    check('lost-before-resolution-no-payload',not result['resolved'] and not m.world.effects and m.pool['rp']==42)
    record('lost-concentration-before-payload',m)
    for field in ['conscious','canAct','magicAllowed']:
        m=paid('burst');m.world.actors['owner'][field]=False;result=m.resolve('cast')
        check('caster-state-changed/'+field,not result['resolved'] and m.pool['rp']==42 and m.world.actors['target']['life'].hp==30)
    for field in ['conscious','canAct','magicAllowed','verbalAvailable','somaticAvailable']:
        m=f.make();f.capture(m,'burst');f.start(m);m.world.actors['owner'][field]=False
        reject('cannot-forge-action-frame/'+field,m,lambda:f.declare(m,'burst'))
    m=paid('strike');m.world.actors['target']['unsupportedInterceptors']=['actual-pending-redirection']
    reject('late-interceptor-not-silently-ignored',m,lambda:strike(m))
    m=paid('mend');m.world.actors['target']['healingReductions']=[HealingReduction('next','actual-source','flat',1,next_healing=True)]
    reject('late-next-heal-consumption-not-skipped',m,lambda:m.resolve('cast',rolls={'nativeDice':[6,6]}))
    check('source-bytes-unchanged',bindings==[info(p) for p in paths])
    report={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'pass','checks':len(checks),'failures':[],
        'sourceBindings':bindings,'results':checks,'histories':histories,'counts':{'histories':len(histories),'profiles':7},
        'scope':'Paid acquired copy permissions feed bounded native RNG, real canonical LifeState HP/Wounds/death, shared BufferLedger, healing prohibitions/reductions/Critical caps, source-owned speed/Reaction/AC effects, exact supplied markers and same-body personal teleport.',
        'limits':['Conditional source casts, captures, geometry/perception/LoE/body fit, action frames, legal target classifications and initiative markers are supplied by explicit fixtures, not a world engine.',
        'Finite defenses: actual typed immunity/resistance and strongest flat damage reduction; no general vulnerability/redirect/interceptor/whole-event death-replacement integration.',
        'Healing reuses actual reducers and systemic factors but next-healing consumption sources remain rejected pending their source-owned integration. No Wound cure, conversion, external amplification or resurrection is granted.',
        'Only the seven existing ordinary-spell component adapters are used. Current Boon source is Shield AC; next-attack/save Boons and nonteleport Step sources still require authentic eligible source adapters.',
        'Native attack/save roll modes and Core Wound/Injury inputs are supplied; no general roll-information/Fate/counterspell scheduler is executed.',
        'Full Ready transactions, Shaman/Mirrorsage providers/shared class allowances, price modifiers, suppression/dispels, body-end cleanup and save/load remain incomplete.',
        'Python integration tests do not constitute shipped-runtime, human-playtest, numerical-balance, cosmology-canon, feat335, whole-game or release approval.'],
        'newRuleAdoptions':0,'sourceInformationDeleted':0,'runtimeApproved':False,'fullFeatExactApproved':False,
        'humanBalanceApproved':False,'wholeGameComplete':False}
    if write:output.write_text(json.dumps(clean(report),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps({'checks':len(checks),'histories':len(histories),'sources':len(bindings),'report':info(output) if write else None}))


if __name__=='__main__':main()
