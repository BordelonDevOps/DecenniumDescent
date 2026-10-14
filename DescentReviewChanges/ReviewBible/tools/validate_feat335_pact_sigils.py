"""Finite paid acquisition/use histories for all three mechanical pact sigils."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
from feat335_pact_sigils import PactSigils
from feat335_shared_acquisition_states import SharedAcquisitionStates, BLAST
from feat_exact_01_casting_credential_model import CastingSources
from validate_feat_exact_01_composite_casting import read, info, serial

R = Path(__file__).resolve().parents[1]; G = R.parents[1]; A = G / 'docs/audit/2026-10-08/full-game'


def main():
    output = A / 'FEAT335_PACT_SIGILS_CHECK.json'; assert not output.exists()
    paths = [R/'data/playtest/character_foundation.json', R/'data/playtest/ancestry_background_candidate.json',
        R/'data/playtest/equipment_source_catalog.json', R/'data/public/feat_candidates/exact_01/supplements.json',
        R/'data/public/feat_candidates/exact_01/spell_dependencies.json', R/'data/public/class_playtests/wizard.json',
        A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json', A/'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json',
        R/'data/public/feat_candidates/exact_01/candidate.json', R/'data/public/feat_candidates/exact_01/shared_rules.json',
        R/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md', G/'docs/reference/Player_Rulebook_v6_source_text.txt',
        Path(__file__), *[R/'tools'/n for n in ['feat335_pact_sigils.py','feat335_shared_acquisition_states.py',
        'feat_exact_01_casting_selections.py','feat_exact_01_remaining_owned_chains.py','feat_exact_01_composite_casting_model.py',
        'feat_exact_01_casting_credential_model.py','feat_exact_01_acquisition_models.py','feat_exact_01_initiate_acquisition_model.py',
        'feat_exact_01_training_prerequisite_model.py','feat335_copy_source_components.py','core_playtest_rules.py','spell_playtest_rules.py']]]
    bindings = [info(p) for p in paths]
    foundation, ancestry, equipment, sm, dependencies, wizard, contracts, prior, candidate, shared = [read(p) for p in paths[:10]]
    classes = {x['class']:x for x in foundation['classes']}; skills = {s:a for a,ss in foundation['skillAbilities'].items() for s in ss}
    equipment = {x['id']:x for x in equipment['records']}; backgrounds = {x['id']:x for x in ancestry['backgrounds']}
    supplements = {x['id']:x['value'] for x in sm['groups']}; contracts = {x['id']:x for x in contracts['records']}
    sources = CastingSources(G, dependencies['spells'], supplements, wizard)
    checks = []; histories = []
    def check(label, ok):
        checks.append({'id':label,'passed':bool(ok)}); assert ok,label
    def reject(label, m, fn):
        before = m.snapshot()
        try: fn()
        except ValueError: check(label, True)
        else: check(label, False)
        check(label+'/atomic', before == m.snapshot())
    def record(label, m): histories.append({'id':label,'state':m.snapshot(),'completeSigilSource':m.sigil_source})
    def acquired(choice):
        actor = deepcopy(prior['actorSourceProjection'])
        actor.update(firstClass='Warrior', classLevels={'Warrior':1}, selectedClassSkills=['Nature','Athletics'])
        h = SharedAcquisitionStates(actor, classes, equipment, skills, ancestry, backgrounds, contracts, supplements, sources)
        h.advance(4); h.earn(4); h.acquire_blast_source('forbidden_pact',4,choice)
        return h
    def world():
        owner = {'position':0,'footprintOffsets':[0],'canAct':True,'teleportAllowed':True}
        victim = {'position':5,'footprintOffsets':[0],'perceived':True,'hostile':True,'armorClass':15,'curseImmune':True}
        return {'actors':{'owner':owner,'foe':victim,'other':{**deepcopy(victim),'position':-5}},
            'light':{x:'dim' for x in range(-50,101)}, 'visibleCells':list(range(-50,101)),
            'fittingCells':list(range(-50,101)), 'walls':[],
            'weapon':{'profile':'martial-melee-weapons.longsword','heldBy':'owner','hands':1}}
    def make(sigil='hex', damage='fire'):
        choice = {'sigil':sigil, **({'damageType':damage} if sigil == 'energyResistance' else {})}
        return PactSigils(acquired(choice), world())
    current = next(x for x in candidate['feats'] if x['id'] == 'forbidden_pact')
    check('complete-current-procedure-matches-contract',current['operationalRules'] == contracts['forbidden_pact']['completeOperativeProcedure'])
    for sigil in ['shadowstep','hex','energyResistance']:
        m = make(sigil); check(sigil+'/one-actual-paid-opportunity',len(m.acquired.pay.grants)==1 and m.acquired.pay.opportunities['Warrior:4']['spent'])
        check(sigil+'/only-feat-rank0-no-class-engine',len(m.acquired.casting.qualifying())==1 and m.acquired.casting.qualifying()[0]['spellId']==BLAST and m.acquired.casting.qualifying()[0]['rank']==0)
        m.acquired.advance(8); m.acquired.earn(8)
        reject(sigil+'/no-reacquisition-change',m,lambda:m.acquired.acquire_blast_source('forbidden_pact',8,{'sigil':'hex'}))
        record('permanent-paid/'+sigil,m)
    for offset in [0,15,16]:
        m=make('shadowstep');m.world['actors']['foe']['position']=40;m.start('r1',regular=True,actual_turn_grant=True)
        if offset<=15:
            r=m.shadowstep('step',offset);check('shadowstep-distance/'+str(offset),r['to']==offset and m.state['sigilAllowance']['current']==0 and m.bonus_actions==0)
        else:reject('shadowstep-beyond15',m,lambda:m.shadowstep('step',offset))
        record('shadowstep-distance/'+str(offset),m)
    for failure in ['bright-origin-part','bright-destination-part','unseen-part','unfitting-part','occupied-part','wall','prohibited','incapacitated','suppressed','no-BA','no-turn']:
        m=make('shadowstep');m.owner()['footprintOffsets']=[0,5];m.world['actors']['foe']['position']=40;m.world['actors']['other']['position']=-20
        m.start('r1',regular=True,actual_turn_grant=True)
        if failure=='bright-origin-part':m.world['light'][5]='bright'
        elif failure=='bright-destination-part':m.world['light'][20]='bright'
        elif failure=='unseen-part':m.world['visibleCells'].remove(20)
        elif failure=='unfitting-part':m.world['fittingCells'].remove(20)
        elif failure=='occupied-part':m.world['actors']['foe']['position']=20
        elif failure=='wall':m.world['walls']=[10]
        elif failure=='prohibited':m.owner()['teleportAllowed']=False
        elif failure=='incapacitated':m.owner()['canAct']=False
        elif failure=='suppressed':m.acquired.pay.suppress('forbidden_pact')
        elif failure=='no-BA':m.bonus_actions=0
        else:m.end('r1')
        reject('shadowstep/'+failure,m,lambda:m.shadowstep('step',15));record('shadowstep/'+failure,m)
    m=make('shadowstep');m.owner()['footprintOffsets']=[0,5];m.world['actors']['foe']['position']=40;m.world['actors']['other']['position']=-20
    m.start('r1',regular=True,actual_turn_grant=True);m.shadowstep('step',15)
    check('shadowstep-full-footprint-moved',m.events['step']['destinationFootprint']==[15,20]);record('shadowstep/whole-footprint',m)
    for failure in ['range31','not-hostile','not-perceived','wall','self','no-target']:
        m=make();m.start('r1',regular=True,actual_turn_grant=True);target='foe'
        if failure=='range31':m.world['actors']['foe']['position']=31
        elif failure=='not-hostile':m.world['actors']['foe']['hostile']=False
        elif failure=='not-perceived':m.world['actors']['foe']['perceived']=False
        elif failure=='wall':m.world['walls']=[2]
        elif failure=='self':target='owner'
        else:target='absent'
        reject('hex/'+failure,m,lambda:m.hex('mark',target));record('hex/'+failure,m)
    m=make();m.start('r1',regular=True,actual_turn_grant=True);m.world['actors']['foe']['position']=30;m.hex('mark','foe')
    check('hex-inclusive30',m.mark['active']);record('hex/inclusive30',m)
    for mode in ['normal','critical','miss','other-target','suppressed','expired','extra-turn']:
        m=make();m.start('r1',regular=True,actual_turn_grant=True);m.hex('mark','foe')
        if mode=='suppressed':m.acquired.pay.suppress('forbidden_pact')
        if mode in {'expired','extra-turn'}:
            m.end('r1');m.start('r2' if mode=='expired' else 'extra1',regular=mode=='expired',actual_turn_grant=True)
        target='other' if mode=='other-target' else 'foe';natural=1 if mode=='miss' else 20 if mode=='critical' else 15
        contributes=mode in {'normal','critical','extra-turn'}
        r=m.weapon_attack('attack',target,natural,[] if mode=='miss' else [4,5] if mode=='critical' else [4], [3,4] if mode=='critical' else [3] if contributes else [])
        check('hex/'+mode+'/native',r['nativeNecrotic']==(7 if mode=='critical' else 3 if contributes else 0))
        check('hex/'+mode+'/mark',m.mark['active']==(mode in {'miss','other-target','suppressed'}))
        check('hex/'+mode+'/not-curse-or-spell',not r['newCastOrCurseOrDropReward'] and not m.events['mark']['curseClassification'])
        record('hex/attack/'+mode,m)
    m=make();m.start('r1',regular=True,actual_turn_grant=True);m.hex('mark','foe')
    reject('hex/bad-critical-dice',m,lambda:m.weapon_attack('bad','foe',20,[4,5],[4]))
    m.weapon_attack('good','foe',20,[4,5],[4,4]);reject('hex/no-second-ordinary-Action',m,lambda:m.weapon_attack('again','foe',15,[4],[]));record('hex/atomic-and-one-Action',m)
    for damage in ['acid','cold','fire','lightning','thunder']:
        for suppressed in [False,True]:
            m=make('energyResistance',damage);m.acquired.pay.suppress('forbidden_pact',suppressed)
            for amount in [0,1,11]:
                r=m.resist_packet('own-'+str(amount),damage,amount)
                check(damage+'/'+str(suppressed)+'/'+str(amount),r['afterResistanceStageOnly']==(amount if suppressed else amount//2))
            r=m.resist_packet('duplicate',damage,11,[damage,damage]);check(damage+'/duplicate'+str(suppressed),r['afterResistanceStageOnly']==5)
            r=m.resist_packet('other','force',11);check(damage+'/unowned-type'+str(suppressed),r['afterResistanceStageOnly']==11 and r['chargesCreated']==0)
            record('resistance/'+damage+'/'+str(suppressed),m)
    for sigil in ['shadowstep','hex']:
        m=make(sigil);m.start('r1',regular=True,actual_turn_grant=True)
        if sigil=='hex':m.hex('first','foe')
        else:m.shadowstep('first',15)
        m.end('r1');m.start('r2',regular=True,actual_turn_grant=True)
        m.acquired.pay.suppress('forbidden_pact');m.acquired.pay.suppress('forbidden_pact',False)
        operation=lambda:m.hex('second','foe') if sigil=='hex' else m.shadowstep('second',0)
        reject(sigil+'/suppression-no-refill',m,operation)
        check(sigil+'/nonbeneficial-no-refill',not m.rest('failed',kind='SR',beneficial=False) and m.state['sigilAllowance']['current']==0)
        check(sigil+'/actual-beneficial-SR',m.rest('rest1',kind='SR',beneficial=True));operation()
        check(sigil+'/duplicate-rest-no-refill',not m.rest('rest1',kind='SR',beneficial=True) and m.state['sigilAllowance']['current']==0)
        check(sigil+'/distinct-beneficial-LR',m.rest('rest2',kind='LR',beneficial=True) and m.state['sigilAllowance']['current']==1)
        record('lifecycle/'+sigil,m)
    for b in bindings:assert info(G/b['path'])==b
    report={'id':'FEAT335-PACT-SIGILS-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'pass',
        'sourceBindings':bindings,'completePactProcedure':contracts['forbidden_pact']['completeOperativeProcedure'],
        'completeSigils':supplements['SUP-07']['pactSigils'],'checks':len(checks),'historyCount':len(histories),
        'results':checks,'failures':[],'histories':histories,
        'conditionalPremises':['Actor initial four-d6 rolls, class advancement and paid source choices are explicit synthetic history inputs.',
            'Actual turn grants, perception, one-dimensional body footprints/light/obstructions, item custody and legitimate completed beneficial rests are conditional world inputs, not campaign authentication.',
            'Native Hex weapon damage is emitted before target defenses/life resolution. Energy Resistance applies one resistance stage only; immunity/vulnerability composition and life-state effects remain separate.',
            'Forbidden Pact HP substitution, Eldritch Blast casting, copy releases, generic movement/turn/rest systems and other feats are not executed by this report. No cosmology is reviewed.'],
        'fullForbiddenPactFulfilled':False,'fullFXC04Fulfilled':False,'fullFeatCandidateApproved':False,
        'sourceInformationDeleted':0,'sourceRulesChanged':0,'pushed':False,'cosmologyReviewed':False}
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2,default=serial)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'report':info(output),'checks':len(checks),'histories':len(histories),'fullFeatApproval':False}))


if __name__=='__main__':main()
