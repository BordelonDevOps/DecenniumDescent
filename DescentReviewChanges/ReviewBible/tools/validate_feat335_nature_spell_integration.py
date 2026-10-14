"""Append paid-cast and source-created Fate Coin lineage evidence after Nature185."""
from copy import deepcopy
from datetime import datetime,timezone
from pathlib import Path
import json
from feat335_nature_spell_integration import NatureSpellIntegration
from feat335_nature_transactions import NativeNatureActor,NatureBorrowedTransactions,NATURE
from feat335_nature_acquisition import NatureAcquisitions
from feat_exact_01_casting_credential_model import CastingSources
from feat_exact_01_lineage_prerequisite_model import current_lineage
from validate_feat_exact_01_composite_casting import read,info,serial

G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'


def main():
    output=A/'FEAT335_NATURE_SPELL_INTEGRATION_CHECK.json';assert not output.exists()
    prior_path=A/'FEAT335_NATURE_TRANSACTIONS_CHECK.json';prior=read(prior_path)
    assert prior['checks']==185 and len(prior['histories'])==75 and not prior['failures']
    fixture=next(h['final'] for h in prior['histories'] if h['id']=='NWT-01/native-selected-Ranger1')
    borrowed_fixture=next(h['final'] for h in prior['histories'] if h['id']=='NWT-01/paid-Human-Bard4')
    foundation=read(R/'data/playtest/character_foundation.json');classes={x['class']:x for x in foundation['classes']}
    skills={s:a for a,ss in foundation['skillAbilities'].items() for s in ss};ancestry=read(R/'data/playtest/ancestry_background_candidate.json')
    backgrounds={x['id']:x for x in ancestry['backgrounds']};equipment={x['id']:x for x in read(R/'data/playtest/equipment_source_catalog.json')['records']}
    supplements={x['id']:x['value'] for x in read(R/'data/public/feat_candidates/exact_01/supplements.json')['groups']}
    contracts={x['id']:x for x in read(A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json')['records']}
    class_sources={n:read(G/classes[n]['classCandidatePath']) for n in ['Ranger','Wizard','Bard']}
    deps=read(R/'data/public/feat_candidates/exact_01/spell_dependencies.json')['spells'];sources=CastingSources(G,deps,supplements,class_sources['Wizard'])
    allowance=next(x for x in read(A/'FEAT335_ALLOWANCE_DESCRIPTORS_AFTER_FLORA.json')['entries'] if x['id']=='versatile_mastery')['finiteAllowances'][0]
    paths=[Path(__file__),R/'tools/feat335_nature_spell_integration.py',R/'tools/feat335_nature_transactions.py',R/'tools/feat335_nature_acquisition.py',
        R/'tools/feat335_borrowed_skill_transactions.py',R/'tools/feat335_borrowed_transactions.py',R/'tools/feat335_borrowed_stunts.py',R/'tools/feat335_allowance_bindings.py',
        R/'tools/feat_exact_01_composite_casting_model.py',R/'tools/feat_exact_01_acquisition_models.py',R/'tools/feat_exact_01_casting_credential_model.py',R/'tools/feat_exact_01_lineage_prerequisite_model.py',
        R/'tools/core_playtest_rules.py',R/'tools/spell_playtest_rules.py',R/'data/playtest/character_foundation.json',R/'data/playtest/ancestry_background_candidate.json',
        R/'data/playtest/equipment_source_catalog.json',R/'data/public/feat_candidates/exact_01/supplements.json',R/'data/public/feat_candidates/exact_01/spell_dependencies.json',
        A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',A/'FEAT335_ALLOWANCE_DESCRIPTORS_AFTER_FLORA.json',prior_path,
        A/'FEAT335_NATURE_SOURCE_CHECK_01_CONTROLLING_RECORD.json',A/'feat335-nature-source-check-01-verdict/FINITE_NATURE_EXPECTATIONS.json',
        R/'docs/mechanics/CLASS_PLAYTEST_RULES.md',R/'docs/mechanics/SPELL_INTEGRATION_RULES.md',R/'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md',
        *[G/classes[n]['classCandidatePath'] for n in class_sources],*[G/p for p in sorted({deps[s]['binding']['file'] for s in ['arcane-ray','fate-coin']})]]
    bindings=[info(p) for p in paths];checks=[];histories=[]
    def check(label,value):
        checks.append({'id':label,'pass':bool(value)})
        if not value:raise AssertionError(label)
    def reject(label,m,fn):
        before=m.snapshot()
        try:fn()
        except ValueError as e:check(label,True);checks[-1]['reason']=str(e)
        else:check(label,False)
        check(label+'/atomic-no-change',before==m.snapshot())
    def record(label,m):histories.append({'id':label,'final':m.snapshot()})
    def make(first='Ranger',level=4,learn=True):
        actor=deepcopy(fixture['actor']['acquisition']['actor']);actor.update(firstClass=first,classLevels={first:1})
        if first=='Wizard':actor['selectedClassSkills']=[]
        acquired=NatureAcquisitions(actor,classes,equipment,skills,ancestry,backgrounds,contracts,supplements,sources);acquired.advance(level)
        world=deepcopy(fixture['actor']['world']);world['owner'].update(personalRP=class_sources[first]['rpByClassLevel'][level-1],freeHands=2,hasFocus=True,ordinarySpellProhibited=False,
            hands={h:{'usable':True,'holding':None} for h in ['left','right']})
        world['ownRollObservation']={'facesAvailableUnderNormalRules':True,'actualGeneratorPerceived':True,'lineOfEffect':True,'distanceFeet':0}
        world['spellTargets']={'target':{'creature':True,'perceived':True,'lineOfEffect':True,'totalCover':False,'position':20,'ac':15,'hp':100,'forceImmunity':False,'forceResistance':False}}
        if first=='Wizard':
            lineage=current_lineage({**actor,'ancestryId':actor['ancestry'],'variantId':actor['variant']},ancestry)
            acquired.earn(4);acquired.pay.commit('versatile_mastery','Wizard:4',prerequisites_met=lineage['lineage']=='Human')
            controller=NatureBorrowedTransactions(acquired,supplements['SUP-09'],class_sources,equipment,borrowed_fixture['actor']['donors'],world,allowance)
            controller.start_prepare('prepare','donor',NATURE);controller.complete_prepare(60,uninterrupted=True)
            acquired.casting.wizard_snapshot(level,['arcane-ray'],['fate-coin'],['fate-coin'],level,intelligence=acquired.pay.scores['INT'])
        else:controller=NativeNatureActor(acquired,world)
        m=NatureSpellIntegration(controller,class_sources,fixture['authority'],native_selection=fixture['nativeSelection'] if first=='Ranger' else None,
            spell_history={'dissonance':0,'previousSpell':None,'refrain':0,'classRecords':{}},spell_sources=sources)
        if first=='Wizard':m.set_wizard_specialization('Divination')
        elif learn:m.learn_ranger_fate_coin('learn-coin')
        m.begin_turn('turn1','round1',controller.now);return m
    def next_turn(m,event):
        m.end_turn(m.actor.turn,actual_end=True);m.begin_turn(event,event+'-round',m.actor.now+6)
    def spell(m,event,sid='fate-coin',hand='left'):
        return m.declare_spell(event,sid,expected_version=m.version,hand=hand if sid=='fate-coin' else None,target='target' if sid=='arcane-ray' else None)
    def coin(m,event='coin',hand='left'):
        spell(m,event,hand=hand);return m.resolve_spell(event)['coin']['id']
    def nature(m,event='nature'):
        p=m.declare(event,'site',route='borrowed' if m.acquired.first=='Wizard' else 'native',signal='audible',expected_version=m.version)
        return p,m.resolve(event)
    def ready_check(m,*,faces=(2,5),disadvantage=False):
        cid=coin(m);next_turn(m,'nature-turn');nature(m);next_turn(m,'check-turn')
        if disadvantage:m.actor.world['tasks']['look']['disadvantageSources']=['Conditional actual task disadvantage']
        m.start_task('check','look');m.declare_check('check',expected_version=m.version)
        m.roll_check('check',list(faces));return cid

    # NWQ03/NWT05: the first and later ordinary spells really commit and resolve.
    m=make(level=5);cid=coin(m,'before');before=deepcopy(m.spell_history);check('Ranger-first-actual-spell',before=={'dissonance':1,'previousSpell':'fate-coin','refrain':0,'classRecords':{}})
    next_turn(m,'nature-turn');p,_=nature(m);check('Nature-retains-actual-paid-spell-history',m.spell_history==before and p['paidRP']==1 and m.owner['personalRP']==3)
    next_turn(m,'next-spell');p=spell(m,'after',hand='right')
    check('next-same-name-price-history-at-commit',p['quote']['cost']==2 and p['quote']['refrain']==1 and p['dissonanceAdded']==2 and m.spell_history['dissonance']==3 and m.owner['personalRP']==1)
    result=m.resolve_spell('after');check('actual-next-effect-replaces-only-prior-coin',result['resolved'] and m.coins[cid]['state']=='replaced' and m.rider is not None);record('native-Ranger-actual-cast-Nature-repeated-cast',m)
    m=make('Wizard');spell(m,'ray1','arcane-ray');m.resolve_spell('ray1',face=12,damage_faces=[4]);next_turn(m,'ray-turn2');spell(m,'ray2','arcane-ray');m.resolve_spell('ray2',face=12,damage_faces=[4])
    check('Wizard-history-from-two-real-casts',m.spell_history['dissonance']==1 and m.spell_history['refrain']==1)
    next_turn(m,'borrow-turn');before=deepcopy(m.spell_history);book=m.acquired.casting.snapshot();nature(m)
    check('borrowed-Nature-preserves-known-prepared-and-history',m.spell_history==before and m.acquired.casting.snapshot()==book)
    next_turn(m,'ray-turn3');p=spell(m,'ray3','arcane-ray');r=m.resolve_spell('ray3',face=12,damage_faces=[4])
    check('next-actual-Wizard-ray-refrain2',p['quote']['refrain']==2 and m.spell_history['dissonance']==3 and r['actualHpLoss']==4 and m.actor.world['spellTargets']['target']['hp']==88)
    check('Nature-no-Wizard-matrix-exemption-record',m.wizard_matrix_families==set());record('borrowed-Wizard-actual-repeated-cantrip',m)
    m=make(level=5);coin(m);next_turn(m,'nature-turn')
    engine=next(s for s in class_sources['Ranger']['engine'] if 'single-use/nonstacking' in s and '1 less Dissonance' in s)
    m.spell_history['refrain']=0;m.spell_history['classRecords']['ranger-stabilization']={'active':True,'consumed':False,'deadline':18,'sourceText':engine,'premise':'Conditional actual direct successful weapon hit occurred before Nature; hit execution is outside this scenario.'}
    before=deepcopy(m.spell_history);nature(m);check('existing-stabilization-not-consumed-by-Nature',before==m.spell_history)
    next_turn(m,'next-spell');p=spell(m,'stabilized',hand='right');m.resolve_spell('stabilized')
    check('next-ordinary-cast-consumes-real-stabilization-once',p['dissonanceAdded']==1 and m.spell_history['classRecords']['ranger-stabilization']['consumedBy']=='stabilized');record('real-existing-Ranger-stabilization-next-cast',m)
    m=make('Wizard');coin(m);check('Wizard-prepared-first-base-exemption',m.spell_history['dissonance']==0 and m.wizard_matrix_families=={'fate-coin'})
    next_turn(m,'nature-turn');nature(m);next_turn(m,'next-spell');p=spell(m,'repeated',hand='right');m.resolve_spell('repeated')
    check('Nature-does-not-refresh-Wizard-prepared-family',p['dissonanceAdded']==2 and not p['classHooks']);record('Wizard-prepared-family',m)
    for field,value in [('silenced',True),('freeHands',0),('hasFocus',False),('ordinarySpellProhibited',True),('personalRP',0)]:
        m=make();m.owner[field]=value;reject('real-spell-gate-'+field,m,lambda:spell(m,'bad'));record('component-or-cost-'+field,m)
    m=make(learn=False);reject('class-access-not-auto-known',m,lambda:spell(m,'bad'));record('unlearned-spell',m)
    m=make('Wizard');m.acquired.casting.prepared.clear();reject('book-not-current-preparation',m,lambda:spell(m,'bad'));record('unprepared-Wizard',m)
    m=make();m.spell_history['dissonance']=11;reject('ordinary-ranked-Fracture-still-blocks',m,lambda:spell(m,'bad'));nature(m);check('Nature-itself-not-ranked-Fracture',m.owner['personalRP']==3 and m.spell_history['dissonance']==11);record('ranked-vs-nonspell',m)
    m=make();p=spell(m,'paid');m.owner['canAct']=False;m.interrupt('paid','incapacitating-condition')
    check('interrupted-real-cast-retains-history-and-price',m.owner['personalRP']==2 and m.spell_history['dissonance']==1 and m.spell_history['previousSpell']=='fate-coin' and not m.coins)
    reject('no-replay-interrupted-cast',m,lambda:m.resolve_spell('paid'));record('paid-cast-interruption',m)

    # NWT13: the source is a coin created by this actor's own paid real cast.
    m=make();cid=ready_check(m);before=deepcopy(m.spell_history);actions=m.actor.actions;rp=m.owner['personalRP'];riderhistory=deepcopy(m.rider_history)
    check('original-faces-do-not-apply-consequences',m.actor.pending['currentFaces']==[2,5] and 'result' not in m.actor.events['check'] and m.rider is None)
    p=m.commit_coin_reroll('check','flip',cid,0,expected_version=m.version)
    check('coin-and-Reaction-commit-before-new-face',m.coins[cid]['state']=='expended' and m.reactions==0 and p['status']=='paid-awaiting-replacement' and m.roll_guards['check']['reservedBeforeReplacement'])
    reject('cannot-finish-before-replacement',m,lambda:m.finish_check('check'));reject('replacement-face21-invalid',m,lambda:m.resolve_coin_reroll('check','flip',21))
    m.resolve_coin_reroll('check','flip',12);result=m.finish_check('check')
    check('one-die-reselected-with-original-modifier',result['total']==15 and result['success'] and result['rollLineage']['originalFaces']==[2,5] and result['rollLineage']['finalFaces']==[12,5])
    check('no-second-Nature-cost-action-or-history',m.actor.actions==actions and m.owner['personalRP']==rp and m.spell_history==before and m.rider_history==riderhistory)
    reject('resolved-check-not-new-lineage',m,lambda:m.roll_check('check',[20,20]));reject('consequences-only-once',m,lambda:m.finish_check('check'));record('source-created-coin-replaces-one-Nature-check-die',m)
    m=make();cid=ready_check(m,faces=(12,15));m.commit_coin_reroll('check','worse',cid,1,expected_version=m.version);m.resolve_coin_reroll('check','worse',1);r=m.finish_check('check')
    check('mandatory-worse-replacement-reselects-kept-die',r['rollLineage']['finalFaces']==[12,1] and r['total']==15);record('mandatory-replacement-even-worse',m)
    m=make();cid=ready_check(m,faces=(2,),disadvantage=True);m.commit_coin_reroll('check','normal',cid,0,expected_version=m.version);m.resolve_coin_reroll('check','normal',12);r=m.finish_check('check')
    check('cancelled-advantage-one-die-lineage',r['total']==15 and r['rollLineage']['originalFaces']==[2] and r['rollLineage']['finalFaces']==[12]);record('ordinary-cancellation-with-reroll',m)
    for name,field,value in [('hidden-roll','facesAvailableUnderNormalRules',False),('no-generator-sense','actualGeneratorPerceived',False),('no-line','lineOfEffect',False),('outside30','distanceFeet',31)]:
        m=make();cid=ready_check(m);m.actor.world['ownRollObservation'][field]=value
        reject(name,m,lambda:m.commit_coin_reroll('check','bad',cid,0,expected_version=m.version));check(name+'-coin-unspent',m.coins[cid]['state']=='active' and m.reactions==1);record(name,m)
    for name,mutate in [('prohibited-Reaction',lambda m:m.owner.update(reactionLegal=False)),('no-Reaction',lambda m:setattr(m,'reactions',0)),
        ('unusable-held-hand',lambda m:m.owner['hands']['left'].update(usable=False)),('wrong-custody',lambda m:m.coins[next(iter(m.coins))].update(holder='other'))]:
        m=make();cid=ready_check(m);mutate(m);reject(name,m,lambda:m.commit_coin_reroll('check','bad',cid,0,expected_version=m.version));record(name,m)
    m=make();cid=coin(m);next_turn(m,'nature-turn');nature(m);next_turn(m,'check-turn');m.start_task('check','look');m.declare_check('check',expected_version=m.version)
    reject('cannot-reroll-before-complete-original-faces',m,lambda:m.commit_coin_reroll('check','early',cid,0,expected_version=m.version));m.roll_check('check',[2,5])
    reject('no-third-die-in-original',m,lambda:m.commit_coin_reroll('check','third',cid,2,expected_version=m.version));record('timing-and-one-original-die',m)
    m=make();cid=ready_check(m);m.commit_coin_reroll('check','first',cid,0,expected_version=m.version);m.resolve_coin_reroll('check','first',12)
    m.reactions=1 # Explicit independently granted extra-Reaction premise; not generated by coin or Nature.
    reject('extra-Reaction-cannot-repeat-original-lineage',m,lambda:m.commit_coin_reroll('check','second',cid,1,expected_version=m.version));m.finish_check('check');record('one-original-roll-guard',m)
    m=make();cid=ready_check(m);m.commit_coin_reroll('check','committed',cid,0,expected_version=m.version);m.owner['canAct']=False;m.interrupt('check','incapacitating-condition')
    check('interrupted-check-retains-coin-Reaction-and-Nature-spends',m.coins[cid]['state']=='expended' and m.reactions==0 and m.rider is None and m.roll_guards['check']['useEvent']=='committed' and m.replacement_receipts['committed']['status']=='interrupted-no-refund')
    reject('no-replacement-after-real-interrupt',m,lambda:m.resolve_coin_reroll('check','committed',12));record('postcommit-interruption',m)
    m=make();cid=coin(m);m.advance(3600);check('coin-actual-hour-expiry',m.coins[cid]['state']=='expired' and m.owner['freeHands']==2);record('source-hour-deadline',m)
    check('all-current-input-bytes-preserved',bindings==[info(p) for p in paths])
    report={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'pass','checks':len(checks),'failures':[],'sourceBindings':bindings,'results':checks,'histories':histories,
        'counts':{'conditionalHistories':len(histories),'reviewedSpellIds':2,'previousNatureChecks':185,'previousNatureHistories':75},
        'scope':'Actual paid native Ranger and acquired borrowed Wizard Nature interleaved with their own source-qualified committed/resolved ordinary spells; original Nature investigation check using one physically created and paid Fate Coin before consequences. Explicit conditional actors/worlds, not live campaign execution.',
        'priorOpenDetailsNowExercised':[{'group':'NWT-05','variant':1,'evidence':'Native Ranger Fate Coin and borrowed Wizard Arcane Ray histories are produced by actual earlier and later paid casts; Nature does not reset history. Protected Wizard prepared-family and source-existing Ranger stabilization interfaces are also exercised.'},
            {'group':'NWT-13','variant':3,'evidence':'Actual paid Fate Coin creates the physical token; original Nature check pays and consumes its rider before original faces, then one permitted Reaction reserves the root guard and replaces one die before one consequence application.'}],
        'limits':['All bodies, learning/conditional preparation, local perception, truthful timing, physical hands, task permission and interruption facts remain explicit conditional fixtures. These files do not authenticate a campaign.',
            'Repertoire projections are actual legal subsets, not complete Wizard books, full school-passive/class-card builds or a complete Ranger character. No full class balance or general spell runtime is certified.',
            'Ranger stabilization starts from an explicitly source-bound actual-hit premise; its generating weapon hit is not executed here. Native learned Fate Coin is the finite Ranger repertoire branch.',
            'Fate Coin is cast into the caster own hand and used for the caster own Nature check. Other holders/casters, handoff, multi-die damage/healing pools, simultaneous priority, Mark Omen attack resolution and full shared engine integration remain outside this finite adapter.',
            'Arcane Ray attacks execute ordinary hit/critical and finite force immunity/resistance against the conditional target; full damage/Wounds/concentration/downed or target-hook arbitration is outside these living-target cases.',
            'Only source incapacity interruption is executed. Nested Counterspell, general event scheduler authority, other providers/Expertise and full combat/rest/custody remain separately open.',
            'The two earlier named gaps are exercised; acceptance of all47 authored Nature variants still requires a traceable matrix against both reports. These checks alone do not assert all47 or335 fulfilled.'],
        'newRules':0,'natureAll47VariantsFulfilled':False,'fullFeatExactApproved':False,'runtimeApproved':False,'humanBalanceApproved':False,'cosmologyReviewed':False}
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2,default=serial)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'checks':len(checks),'histories':len(histories),'report':info(output)}))


if __name__=='__main__':main()
