"""Paid copy acquisitions, conditional capture geometry and finite lifetimes."""
from copy import deepcopy
from datetime import datetime, timezone
from itertools import product
from pathlib import Path
import json
from feat335_copy_capture import CopyAcquisition, CopyCaptures
from feat335_copy_source_components import CopySourceComponents
from feat_exact_01_casting_credential_model import CastingSources
from validate_feat_exact_01_composite_casting import read, info, serial
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'


def main():
    output=A/'FEAT335_COPY_CAPTURE_CHECK.json';assert not output.exists()
    paths=[R/'data/playtest/character_foundation.json',R/'data/playtest/ancestry_background_candidate.json',
        R/'data/playtest/equipment_source_catalog.json',R/'data/public/feat_candidates/exact_01/supplements.json',
        R/'data/public/feat_candidates/exact_01/spell_dependencies.json',R/'data/public/class_playtests/wizard.json',
        A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',A/'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json',
        A/'FEAT335_COPY_SOURCE_COMPONENTS_CHECK.json',A/'FEAT335_COMPLETE_ACQUISITION_ASSEMBLY_AFTER_FLORA.json',
        R/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md',R/'data/public/feat_candidates/exact_01/shared_rules.json',
        Path(__file__),*[R/'tools'/n for n in ['feat335_copy_capture.py','feat335_copy_source_components.py',
        'feat_exact_01_composite_casting_model.py','feat_exact_01_casting_credential_model.py',
        'feat_exact_01_acquisition_models.py','feat_exact_01_training_prerequisite_model.py']]]
    bindings=[info(p) for p in paths]
    foundation,ancestry,equipment,sm,deps,wizard,contracts,prior,source_report,assembly=[read(p) for p in paths[:10]]
    classes={x['class']:x for x in foundation['classes']};skills={s:a for a,ss in foundation['skillAbilities'].items() for s in ss}
    equipment={x['id']:x for x in equipment['records']};backgrounds={x['id']:x for x in ancestry['backgrounds']}
    supplements={x['id']:x['value'] for x in sm['groups']};contracts={x['id']:x for x in contracts['records']}
    sources=CastingSources(G,deps['spells'],supplements,wizard);checks=[];histories=[]
    def check(label,ok):checks.append({'id':label,'passed':bool(ok)});assert ok,label
    def reject(label,m,fn):
        before=m.snapshot()
        try:fn()
        except ValueError:check(label,True)
        else:check(label,False)
        check(label+'/atomic',before==m.snapshot())
    def record(label,m):histories.append({'id':label,'acquisition':m.acquired.snapshot(),'state':m.snapshot(),'sourceEvents':m.witnesses.snapshot()})
    imperial=next(v for x in ancestry['ancestries'] if x['id']=='human' for v in x['variants'] if v['id']=='imperial-human')
    def history(first='Wizard',score=None):
        actor=deepcopy(prior['actorSourceProjection']);actor.update(firstClass=first,classLevels={first:1},selectedClassSkills=['Insight','Investigation'] if first=='Wizard' else ['Nature','Athletics'])
        if score is not None:
            bonus=imperial['combinedAbilityBonuses']['INT'];rolls=next(d for d in product(range(1,7),repeat=4) if sum(d)-min(d)+bonus==score)
            actor['abilityRolls']['INT']=list(rolls);actor['permanentScores']['INT']=score
        h=CopyAcquisition(actor,classes,equipment,skills,ancestry,backgrounds,contracts,supplements,sources)
        h.advance(4)
        if first=='Wizard':h.wizard(['arcane-ray','friends'],['find-familiar'],['find-familiar'])
        return h
    def buy(h,sid,level):
        h.advance(level);h.earn(level);return h.acquire_copy(sid,level)
    def make(feats=('eldritch_echo','mimicry','arcane_adaptation'),first='Wizard'):
        h=history(first)
        if first=='Warrior':h.earn(4);h.acquire_parent('forbidden_pact',4,{'sigil':'hex'})
        for sid,level in zip(feats,[4,8,12] if first=='Wizard' else [8,12,16]):buy(h,sid,level)
        witnesses=CopySourceComponents(sources)
        for row in source_report['histories']:
            if not row['id'].startswith('all-seven/'):continue
            for event,s in row['state'].items():witnesses.witness(event,s['spellId'],s['sourceRoute']['sourceClass'],s['sourceClassLevel'],s['premises'],s['outcome'])
        return CopyCaptures(h,witnesses)
    geometry={'actualCaptureWindow':True,'conscious':True,'actualFeatAvailable':True,
        'sourceCreatureDistance':30,'resolvedComponentDistance':30,'sourcePerceived':True,
        'effectPerceived':True,'lineOfEffect':True,'usedAgainstOwner':False,'sourceLawfulRange':True,'actualReactionLegal':True}
    def capture(m,event='capture',sid='mimicry',profile='strike',provider='Wizard/class-engine',geo=None,**kwargs):
        return m.capture(event,sid,'source-'+profile,profile,provider,deepcopy(geometry if geo is None else geo),**kwargs)

    check('unchanged-seven-profile-contract',source_report['completeCopyContract']==supplements['SUP-07']['copyProfileContract'])
    current_ids={'eldritch_echo','mimicry','arcane_adaptation'}
    for entry in assembly['entries']:
        if entry['id'] in current_ids:
            check('reviewed-initialization-present/'+entry['id'],'initial' in entry['initialState']['exactObligation'].lower())
            check('current-complete-procedure-unchanged/'+entry['id'],entry['currentCompleteContract']==contracts[entry['id']])
    for sid,minimum in [('mimicry',15),('arcane_adaptation',13)]:
        h=history(score=minimum-1);h.earn(4);reject(sid+'/permanent-ability-below',h,lambda:h.acquire_copy(sid,4))
        h=history(score=minimum);h.earn(4);h.acquire_copy(sid,4)
        check(sid+'/exact-boundary-paid',h.pay.has(sid) and h.pay.opportunities['Wizard:4']['spent'])
    for sid in current_ids:
        h=history('Warrior');h.earn(4);reject(sid+'/no-actual-casting',h,lambda sid=sid:h.acquire_copy(sid,4))
        h=history();reject(sid+'/no-earned-choice',h,lambda sid=sid:h.acquire_copy(sid,4))
        h.earn(4);h.acquire_copy(sid,4);h.advance(8);h.earn(8)
        reject(sid+'/nonrepeatable',h,lambda sid=sid:h.acquire_copy(sid,8))
    m=make();check('all-three-actual-distinct-paid-opportunities',len(m.acquired.pay.grants)==3 and {x['opportunity'] for x in m.acquired.pay.grants}=={'Wizard:4','Wizard:8','Wizard:12'})
    check('initial-empty-one-use-each',m.pending is None and not m.adapted and not m.resistances and m.uses==dict.fromkeys(current_ids,1))
    for profile in ['strike','burst','mend','ward','hindrance','boon','step']:
        for sid in ['eldritch_echo','mimicry']:
            m=make();before=m.acquired.casting.snapshot();r=capture(m,sid=sid,profile=profile)
            check(sid+'/'+profile+'/capture-source-and-own-route',r['component']['profile']==profile and r['provider']['ability']=='INT' and m.uses[sid]==0)
            check(sid+'/'+profile+'/only-Echo-spends-Reaction',m.reactions==(0 if sid=='eldritch_echo' else 1))
            check(sid+'/'+profile+'/capture-not-cast',m.acquired.casting.snapshot()==before and not r['captureIsCast'] and not r['grantsOriginalSpell'])
            reject(sid+'/'+profile+'/no-second-use',m,lambda:capture(m,'again',sid=sid,profile=profile,replace=True))
            record('capture/'+sid+'/'+profile,m)
    for sid in ['eldritch_echo','mimicry']:
        m=make()
        for field in ['actualCaptureWindow','conscious','actualFeatAvailable','sourcePerceived','effectPerceived']:
            g=deepcopy(geometry);g[field]=False
            reject(sid+'/isolated-'+field,m,lambda g=g:capture(m,sid=sid,geo=g))
        m.acquired.pay.suppress(sid)
        reject(sid+'/actual-owned-feat-suppressed',m,lambda:capture(m,sid=sid))
    for distance in [60,61]:
        m=make();g={**geometry,'sourceCreatureDistance':distance}
        if distance==60:capture(m,sid='eldritch_echo',geo=g);check('Echo-inclusive60',m.uses['eldritch_echo']==0)
        else:reject('Echo-beyond60',m,lambda:capture(m,sid='eldritch_echo',geo=g))
    for changes in [{'actualReactionLegal':False},{'lineOfEffect':False}]:
        m=make();reject('Echo-isolated/'+str(changes),m,lambda:capture(m,sid='eldritch_echo',geo={**geometry,**changes}))
    m=make();m.reactions=0;reject('Echo-spent-reaction',m,lambda:capture(m,sid='eldritch_echo'))
    capture(m,sid='mimicry',geo={**geometry,'actualReactionLegal':False});check('Mimicry-no-action-or-Reaction-capture',m.reactions==0)
    record('no-Reaction-Mimicry',m)
    for target,dist,loe,lawful,expected in [(False,30,True,True,True),(False,31,True,True,False),(False,30,False,True,False),
        (True,60,True,True,True),(True,60,False,True,True),(True,60,True,False,False)]:
        m=make();g={**geometry,'sourceCreatureDistance':dist,'resolvedComponentDistance':dist,'lineOfEffect':loe,'usedAgainstOwner':target,'sourceLawfulRange':lawful}
        label='Mimicry-clause/'+str((target,dist,loe,lawful))
        if expected:capture(m,geo=g);check(label,m.pending is not None)
        else:reject(label,m,lambda:capture(m,geo=g))
        record(label,m)
    m=make(first='Warrior');pact=next(k for k,g in m.acquired.casting.grants.items() if g['source']=='actual-paid-Forbidden-Pact')
    blast_ids={r['spellId'] for r in m.acquired.casting.qualifying() if r['spellId']==sources.blast()['spellId']}
    check('Pact-and-Echo-one-Blast-identity',len(blast_ids)==1)
    capture(m,sid='eldritch_echo',provider=pact);check('Pact-actual-rank0-CHA',m.pending['provider']['ability']=='CHA' and m.pending['provider']['maximumLearnableRank']==0)
    record('paid-Pact-and-Echo-rank0-only',m)
    m=make(first='Warrior');pact=next(k for k,g in m.acquired.casting.grants.items() if g['source']=='actual-paid-Forbidden-Pact')
    reject('Pact-does-not-supply-ranked-ceiling',m,lambda:capture(m,profile='burst',provider=pact))
    m=make();m.acquired.casting.grants['Wizard/class-engine']['removedAt']=m.acquired.casting.moment
    reject('removed-capture-provider',m,lambda:capture(m))
    echo=next(k for k,g in m.acquired.casting.grants.items() if g['source']=='actual-paid-Eldritch-Echo')
    capture(m,provider=echo);check('retained-Echo-rank0-route-independent',m.pending['provider']['ability']=='CHA')
    record('route-removal-no-invented-ranked-provider',m)

    for first,second in [('eldritch_echo','mimicry'),('mimicry','eldritch_echo')]:
        m=make();capture(m,'first',sid=first,profile='burst',adapt=True)
        reject('replacement-must-be-explicit/'+first,m,lambda:capture(m,'second',sid=second,profile='ward'))
        capture(m,'second',sid=second,profile='ward',replace=True)
        check('single-record-and-paid-old-loss/'+first,m.pending['captureEvent']=='second' and m.events['first']['recordStatus']=='replaced-without-refund' and m.uses[first]==m.uses[second]==0)
        check('adaptation-retains-exact-old-profile-no-extra-allowance/'+first,m.adapted['first']['component']['profile']=='burst' and m.adapted['first']['active'] and not m.adapted['first']['newReleaseAllowance'])
        check('observed-damage-only-resistance/'+first,m.resistances['first']['type']=='fire' and not m.resistances['first']['retroactive'] and 'second' not in m.resistances)
        record('shared-pending-slot/'+first,m)
    m=make();capture(m,sid='eldritch_echo',profile='burst',adapt=True)
    m.start_extra('extra',1,actual_extra_turn=True);check('extra-no-Echo-window-or-Reaction-refresh',m.regular_ordinal==0 and m.reactions==0 and m.pending['releaseRegularOrdinal']==1)
    m.end_extra('extra',actual_extra_end=True);check('extra-end-no-expiry',m.pending is not None and m.adapted['capture']['active'] and m.resistances['capture']['active'])
    m.start_regular('own1',1,1,actual_new_regular_start=True);check('first-future-regular-Echo-window',m.pending['releaseRegularOrdinal']==1 and m.reactions==1)
    m.end_regular('own1',actual_regular_end=True)
    check('Echo-missed-window-and-resistance-end',m.pending is None and not m.resistances['capture']['active'] and m.uses['eldritch_echo']==0)
    check('adapted-still-active-until-second-start',m.adapted['capture']['active'])
    m.start_regular('own2',2,2,actual_new_regular_start=True)
    check('second-future-start-ends-adapted-permission',not m.adapted['capture']['active'] and m.uses['arcane_adaptation']==0)
    record('exact-regular-boundaries-no-extra-refresh',m)
    m=make();m.start_regular('current',1,1,actual_new_regular_start=True);capture(m,sid='eldritch_echo')
    m.end_regular('current',actual_regular_end=True);check('current-end-not-next-future-end',m.pending is not None and m.pending['releaseRegularOrdinal']==2)
    m.start_regular('next',2,2,actual_new_regular_start=True);m.end_regular('next',actual_regular_end=True)
    check('capture-during-own-turn-expires-next-turn-end',m.pending is None);record('future-means-not-current',m)
    m=make();capture(m)
    check('nonbeneficial-rest-no-refill-or-expiry',not m.rest('debt',kind='SR',beneficial=False) and m.pending is not None and m.uses['mimicry']==0)
    check('actual-beneficial-SR-refills-permission-not-copy',m.rest('real-SR',kind='SR',beneficial=True) and m.pending is None and m.uses['mimicry']==1)
    capture(m,'new');check('replayed-rest-no-second-refill',not m.rest('real-SR',kind='SR',beneficial=True) and m.uses['mimicry']==0 and m.pending['captureEvent']=='new')
    check('actual-beneficial-LR-also-expires-Mimicry',m.rest('real-LR',kind='LR',beneficial=True) and m.pending is None and m.uses['mimicry']==1)
    record('actual-beneficial-rest-epochs',m)
    m=make(('arcane_adaptation',));reject('Adaptation-alone-no-capture-permission',m,lambda:capture(m));record('no-copy-created-by-adaptation-acquisition',m)
    m=make();m.acquired.pay.suppress('arcane_adaptation')
    reject('suppressed-adaptation-no-mark',m,lambda:capture(m,adapt=True))
    capture(m);check('suppressed-adaptation-no-passive-resistance',not m.resistances);record('actual-adaptation-suppression',m)
    m=make();capture(m,sid='eldritch_echo',adapt=True)
    reject('adaptation-use-not-refilled-by-another-capture',m,lambda:capture(m,'second',replace=True,adapt=True))
    m.start_regular('turn',1,1,actual_new_regular_start=True)
    reject('cannot-skip-unprocessed-end',m,lambda:m.start_regular('other',2,2,actual_new_regular_start=True))
    reject('extra-cannot-skip-unprocessed-end',m,lambda:m.start_extra('extra',1,actual_extra_turn=True))
    reject('current-turn-end-needs-real-event',m,lambda:m.end_regular('turn',actual_regular_end=False))
    record('guarded-timeline-identity',m)
    check('all-current-source-bindings-stable',bindings==[info(p) for p in paths])
    result={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'pass','checks':len(checks),'failures':[],
        'sourceBindings':bindings,'completeContracts':{k:contracts[k] for k in sorted(current_ids)},'results':checks,'histories':histories,
        'counts':{'conditionalHistories':len(histories),'copyFeats':3,'sourceProfiles':7},
        'scope':'Actual class-scheduled paid Echo/Mimicry/Adaptation acquisitions; exact source-component capture; own Wizard learning-rank or explicit feat-only Blast rank-zero provider; isolated perception/range/Reaction/use gates; one pending record, paid replacement, real rest epochs, future regular-turn expiry and bounded adapted permission/resistance records.',
        'limits':['Actual source spell completion, perception/geometry, willing/legal world targets and capture windows are explicit conditional fixtures inherited from the bound source adapter, not authenticated campaign events.',
            'Wizard ability/repertoire/level and paid feat histories are finite projections; full class-card selection, starting training, and ordinary spell payment/outcomes are not a complete character or combat engine.',
            'Only actual Wizard and explicit Forbidden Pact/Echo rank-zero routes are modeled. Other class/Initiate/monster/Mirrorsage sources require their own complete permission integrations.',
            'The timeline executes consecutive actual regular starts/ends and intervening completed extra turns. General initiative changes, out-of-combat elapsed deadlines, absence/death, interrupted/resumed slots and virtual markers are not executed.',
            'Rest tests isolate conditional genuine beneficial-completion identities; they do not execute the labor/time/safety/rest engine or invent a rest fitting between initiative ticks.',
            'Resistance and adapted permission are records only; actual damage mitigation, continued suppression/arbitration, paid copy release, RP/components/Dissonance/Refrain, interrupt/counter outcomes, shared numbered-round release cap and recipient payloads remain unfinished.',
            'A release attempt must recheck current provider and all ordinary use predicates; capture provenance never authorizes free release. No ordinary repertoire, donor engine or extra action/resource is granted.',
            'No full335 approval, runtime certification, human balance result, GitHub push or cosmology review follows.'],
        'newRules':0,'fullFeatExactApproved':False,'runtimeApproved':False,'humanBalanceApproved':False,'cosmologyReviewed':False}
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2,default=serial)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'checks':len(checks),'histories':len(histories),'report':info(output)}))


if __name__=='__main__':main()
