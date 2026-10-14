"""Trace all47 reviewed Nature expectations to preserved finite evidence."""
from copy import deepcopy
from datetime import datetime,timezone
from pathlib import Path
import json
from feat335_nature_transactions import NatureTransactions,NativeNatureActor,NatureBorrowedTransactions,NATURE
from feat335_nature_acquisition import NatureAcquisitions
from feat_exact_01_casting_credential_model import CastingSources
from feat_exact_01_lineage_prerequisite_model import current_lineage
from validate_feat_exact_01_composite_casting import read,info,serial
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'


def main():
    output=A/'FEAT335_NATURE_FINITE_FULFILLMENT.json';assert not output.exists()
    names={'transactions':'FEAT335_NATURE_TRANSACTIONS_CHECK.json','spells':'FEAT335_NATURE_SPELL_INTEGRATION_CHECK.json',
        'source':'FEAT335_NATURE_SOURCE_PROPAGATION_CHECK.json','reproduced':'FEAT335_NATURE_SOURCE_CHECK_01_REPRODUCED.json'}
    reports={k:read(A/n) for k,n in names.items()}
    assert reports['transactions']['checks']==185 and reports['spells']['checks']==77 and reports['source']['checks']==137 and reports['reproduced']['checks']==124
    expectations_path=A/'feat335-nature-source-check-01-verdict/FINITE_NATURE_EXPECTATIONS.json';expectations=read(expectations_path)
    foundation=read(R/'data/playtest/character_foundation.json');classes={c['class']:c for c in foundation['classes']};skills={s:a for a,ss in foundation['skillAbilities'].items() for s in ss}
    ancestry=read(R/'data/playtest/ancestry_background_candidate.json');backgrounds={x['id']:x for x in ancestry['backgrounds']}
    equipment={x['id']:x for x in read(R/'data/playtest/equipment_source_catalog.json')['records']};supplements={x['id']:x['value'] for x in read(R/'data/public/feat_candidates/exact_01/supplements.json')['groups']}
    contracts={x['id']:x for x in read(A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json')['records']};class_sources={n:read(G/classes[n]['classCandidatePath']) for n in ['Ranger','Bard','Wizard']}
    sources=CastingSources(G,read(R/'data/public/feat_candidates/exact_01/spell_dependencies.json')['spells'],supplements,class_sources['Wizard'])
    allowance=next(x for x in read(A/'FEAT335_ALLOWANCE_DESCRIPTORS_AFTER_FLORA.json')['entries'] if x['id']=='versatile_mastery')['finiteAllowances'][0]
    fixture=next(x['final'] for x in reports['transactions']['histories'] if x['id']=='NWT-01/native-selected-Ranger1')
    bard_fixture=next(x['final'] for x in reports['transactions']['histories'] if x['id']=='NWT-01/paid-Human-Bard4')
    checks=[];histories=[]
    def check(label,condition):
        checks.append({'id':label,'pass':bool(condition)})
        if not condition:raise AssertionError(label)
    def reject(label,m,fn):
        before=m.snapshot()
        try:fn()
        except ValueError as e:check(label,True);checks[-1]['reason']=str(e)
        else:check(label,False)
        check(label+'/atomic-no-change',before==m.snapshot())
    def make(bard=False):
        src=bard_fixture if bard else fixture;actor=deepcopy(src['actor']['acquisition']['actor']);first='Bard' if bard else 'Ranger';actor['classLevels']={first:1}
        acquired=NatureAcquisitions(actor,classes,equipment,skills,ancestry,backgrounds,contracts,supplements,sources);acquired.advance(4)
        world=deepcopy(fixture['actor']['world']);world['owner']['personalRP']=class_sources[first]['rpByClassLevel'][3]
        if bard:
            lineage=current_lineage({**actor,'ancestryId':actor['ancestry'],'variantId':actor['variant']},ancestry)
            acquired.earn(4);acquired.pay.commit('versatile_mastery','Bard:4',prerequisites_met=lineage['lineage']=='Human')
            donors=deepcopy(bard_fixture['actor']['donors']);donors['donor']['RP']=class_sources['Ranger']['rpByClassLevel'][0]
            controller=NatureBorrowedTransactions(acquired,supplements['SUP-09'],class_sources,equipment,donors,world,allowance)
            controller.start_prepare('prepare','donor',NATURE);controller.complete_prepare(60,uninterrupted=True)
        else:controller=NativeNatureActor(acquired,world)
        m=NatureTransactions(controller,class_sources,fixture['authority'],native_selection=None if bard else fixture['nativeSelection'],spell_history={'dissonance':4,'previousSpell':'prior-spell-fixture','refrain':2,'classRecords':{}})
        m.begin_turn('turn1','round1',controller.now);return m
    def activate(m,bard=False):
        m.declare('use','site',route='borrowed' if bard else 'native',signal='audible',expected_version=m.version);m.resolve('use')
    def next_turn(m):m.end_turn('turn1',actual_end=True);m.begin_turn('turn2','round2',m.actor.now+6)

    # A source-paid replacing Expertise grant, not a hand-assigned training bonus.
    m=make();a=m.acquired;procedure=contracts['skill_expert']['completeOperativeProcedure']
    check('SkillExpert-source-order-and-no-ASI','acquisition order' in procedure and 'No additional ability increase' in procedure and contracts['skill_expert']['requirements']=={'kind':'noPrintedPrerequisite'})
    new='Survival';expert='Perception';before_scores=deepcopy(a.pay.scores)
    check('SkillExpert-actual-missing-new-and-trained-expertise',a.training_projection['skills'].get(new,0)==0 and a.training_projection['skills'][expert]==1)
    a.earn(4);paid=a.pay.commit('skill_expert','Ranger:4',choice={'newSkill':new,'expertiseSkill':expert},prerequisites_met=contracts['skill_expert']['requirements']['kind']=='noPrintedPrerequisite')
    a.training_projection['skills'][new]=1;a.training_projection['receipts'].append({'credential':new,'source':'skill_expert','stage':1,'paidGrant':deepcopy(paid),'procedure':procedure})
    a.training_projection['skills'][expert]=2;a.training_projection['receipts'].append({'credential':expert,'source':'skill_expert','stage':2,'contribution':'replacing2PB','paidGrant':deepcopy(paid),'procedure':procedure})
    check('SkillExpert-spent-own-opportunity-no-stat-increase',a.pay.opportunities['Ranger:4']['spent'] and a.pay.scores==before_scores and a.pay.has('skill_expert'))
    activate(m);next_turn(m);m.start_task('look','look');p=m.declare_check('look',expected_version=m.version);r=m.resolve_check('look',[2,12])
    check('Nature-uses-actual-replacing-Expertise',p['ownTrainingFactor']==2 and p['modifier']==5 and r['total']==17 and r['success']);histories.append({'id':'paid-Expertise','final':m.snapshot()})

    # Existing Bard engine state is an explicit source-bound fixture, not a Nature-generated grant.
    m=make(True);bard_rules=(R/'docs/mechanics/BARD_PLAYTEST_v0_1.md').read_text(encoding='utf-8')
    check('Bard-source-only-performance-trigger','Only started abilities tagged **performance**' in bard_rules and 'Ordinary spells neither gain nor spend Crescendo' in bard_rules)
    m.spell_history['classRecords']['bard-rhythm']={'Crescendo':5,'lastPerformance':'bard.base.dissonant-note','pendingEcho':None,'eligibleEchoSources':[],
        'sourceDocument':'docs/mechanics/BARD_PLAYTEST_v0_1.md','premise':'Conditional legal prior performed sequence established five stacks; this audit does not execute that earlier sequence.'}
    before=deepcopy(m.spell_history);donor=deepcopy(m.actor.donors);activate(m,True)
    check('Nature-does-not-start-spend-vent-or-create-Bard-hooks',m.spell_history==before and m.spell_history['dissonance']==4 and m.spell_history['classRecords']['bard-rhythm']['Crescendo']==5)
    check('source-capacity-donor1-unchanged-borrower7-to6',m.actor.donors==donor and donor['donor']['RP']==1 and m.owner['personalRP']==6);histories.append({'id':'Bard-existing-rhythm-and-legal-donor-pool','final':m.snapshot()})

    # Nature supplies no permission for an unlawful thought-reading task or missing sense.
    m=make();activate(m);next_turn(m);m.actor.world['tasks']['thoughts']={**deepcopy(m.actor.world['tasks']['look']),
        'actualLawfulCheck':False,'unsupportedRequest':'Read another creature thoughts using Nature alone; no actual thought-reading source exists.'}
    reject('no-lawful-thought-reading-check-from-Nature',m,lambda:m.start_task('thoughts','thoughts'));check('thought-request-keeps-unused-rider',m.rider is not None)
    m.actor.world['tasks']['look']['supportedEvidence']=[];m.actor.world['terrain']['track']['taskPerceived']=False
    m.actor.world['terrain']['track']['sensePremise']='An incorporeal hidden creature leaves no physical sign detectable by the owner actual senses; no additional perception source exists.'
    m.start_task('look','look');reject('no-new-incorporeal-sense-from-Nature',m,lambda:m.declare_check('look',expected_version=m.version));histories.append({'id':'no-new-thought-or-incorporeal-sense','final':m.snapshot()})

    # Every variant points to concrete preserved histories, not a count-only claim.
    T='transactions';S='spells';N='new';P='source';V='reproduced'
    mapping={
      'NWT-01':[[ (T,'NWT-01/native-selected-Ranger1') ],[(T,'NWT-01/paid-Human-Bard4')],[(T,'@NWT-01/null-not-rank')]],
      'NWT-02':[[ (T,'NWT-02/silenced'),(T,'NWT-02/freeHands'),(T,'NWT-02/hasFocus') ],[(T,'NWT-02/conscious'),(T,'NWT-02/canAct'),(T,'NWT-02/magicalTechniqueProhibited'),(T,'NWT-02/personalRP'),(T,'@NWT-02/no-required-Action')],[(T,'NWT-02/actual-terrain-perception'),(T,'NWT-02/requiresHands'),(T,'NWT-02/requiresTools')]],
      'NWT-03':[[ (T,'NWT-03/signal-not-component') ],[(T,'NWT-03/signal-not-component'),(T,'NWT-03/full-preparation')],[(T,'NWT-03/no-agreed-meaning'),(T,'NWT-03/impossible-visible'),(T,'NWT-03/invented-telepathy'),(T,'NWT-03/donor-willing'),(T,'NWT-03/donor-selectedCards'),(T,'NWT-03/donor-copiedOrBorrowed')]],
      'NWT-04':[[ (T,'NWT-04/own-payment-no-refill'),(N,'Bard-existing-rhythm-and-legal-donor-pool') ],[(T,'NWT-04/poolKind-borrowed-RP'),(T,'NWT-04/poolOwner-donor'),(T,'NWT-04/personalRP-0'),(T,'NWT-04/Warrior-no-invented-pool')],[(T,'NWT-04/own-payment-no-refill'),(T,'NWT-04/same-card-ledger')]],
      'NWT-05':[[ (S,'native-Ranger-actual-cast-Nature-repeated-cast'),(S,'borrowed-Wizard-actual-repeated-cantrip') ],[(T,'NWT-05/Ranger-existing-stabilization'),(S,'real-existing-Ranger-stabilization-next-cast')],[(T,'NWT-05/Bard-no-spell-hook'),(N,'Bard-existing-rhythm-and-legal-donor-pool'),(S,'ranked-vs-nonspell'),(S,'Wizard-prepared-family')]],
      'NWT-06':[[ (T,'NWT-06/legal-commit-idle'),(T,'NWT-06/illegal-idle') ],[(T,'NWT-06/later-task-and-extra-turn')],[(T,'NWT-06/later-task-and-extra-turn'),(T,'NWT-06/illegal-idle'),(T,'NWT-08/nonspell-ready-offturn')]],
      'NWT-07':[[ (T,'NWT-07/split-paid-pending') ],[(T,'NWT-07/split-paid-pending'),(T,'NWT-07/source-incapacity')],[(T,'NWT-07/actor-moved'),(T,'NWT-07/terrain-moved'),(T,'NWT-07/donor-leaves-after-commit')]],
      'NWT-08':[[ (T,'NWT-08/nonspell-ready-offturn') ],[(T,'NWT-08/nonspell-ready-offturn')],[(T,'NWT-08/Ready-borrowed-interrupted'),(T,'NWT-08/Ready-declined-expiry'),(T,'NWT-08/Ready-replacement')]],
      'NWT-09':[[ (T,'NWT-09/real-interrupt-only') ],[(T,'NWT-09/real-interrupt-only'),(T,'NWT-08/Ready-borrowed-interrupted')]],
      'NWT-10':[[ (T,'NWT-10/edge15-valid') ],[(T,'NWT-10/distance16'),(T,'NWT-10/new-terrain-not-fixed')],[(T,'NWT-10/lost-task-sense'),(T,'NWT-10/lost-task-line'),(T,'NWT-10/lost-access'),(T,'NWT-10/not-natural-anymore'),(T,'NWT-10/actual-terrain'),(T,'NWT-10/legitimate-site-unknown')]],
      'NWT-11':[[ (T,'NWT-11/strict-before-deadline'),(T,'NWT-07/source-incapacity') ],[(T,'NWT-11/strict-before-deadline'),(T,'NWT-11/deadline-121'),(T,'NWT-11/deadline-130')],[(T,'NWT-11/rest-label-and-donor-departure'),(T,'NWT-15/elapsed-initiative-boundary')]],
      'NWT-12':[[ (T,'NWT-12/task-cost-and-failure') ],[(T,'NWT-13/trained-v-untrained-look'),(T,'NWT-13/trained-v-untrained-survive'),(N,'paid-Expertise')],[(T,'NWT-12/task-cost-and-failure'),(T,'NWT-10/distance16'),(T,'NWT-12/interrupt-after-check-commit')]],
      'NWT-13':[[ (T,'NWT-13/trained-v-untrained-look'),(T,'NWT-13/trained-v-untrained-survive') ],[(T,'NWT-13/ordinary-cancellation'),(T,'NWT-13/no-stack-or-repeat')],[(S,'source-created-coin-replaces-one-Nature-check-die'),(S,'mandatory-replacement-even-worse'),(S,'ordinary-cancellation-with-reroll'),(S,'one-original-roll-guard'),(S,'postcommit-interruption'),(T,'NWT-13/no-stack-or-repeat')]],
      'NWT-14':[[ (T,'NWT-14/established-1'),(T,'NWT-12/task-cost-and-failure') ],[(T,'NWT-14/established-1'),(T,'NWT-14/unknown-0')],[(T,'NWT-14/no-through-cover'),(T,'NWT-14/established-1'),(N,'no-new-thought-or-incorporeal-sense')]],
      'NWT-15':[[ (T,'NWT-15/shared-native-borrowed-clock-and-rider'),(T,'NWT-15/elapsed-initiative-boundary') ],[(T,'NWT-15/shared-native-borrowed-clock-and-rider')],[(T,'NWT-15/preserved-old-failed'),(T,'NWT-15/preserved-old-interrupted')]],
      'NWT-16':[[ (P,'$complete-report'),(V,'$complete-report') ],[(T,'NWT-16/new-descendant-only')],[(T,'@NWT-16/362-and38-historical'),(T,'@NWT-16/all-input-bytes-unchanged'),(S,'@all-current-input-bytes-preserved')]]}
    matrix=[]
    for group in expectations['groups']:
        candidates=mapping[group['id']];check('matrix-count/'+group['id'],len(candidates)==len(group['variants']))
        for index,(expectation,refs) in enumerate(zip(group['variants'],candidates),1):
            resolved=[]
            for source,key in refs:
                report={'histories':histories,'results':checks} if source==N else reports[source]
                if key=='$complete-report':found=[{'completeReport':names[source],'checks':report['checks']}]
                elif key.startswith('@'):found=[{'checkId':x['id'],'pass':x['pass']} for x in report['results'] if x['id'].startswith(key[1:])]
                else:found=[{'historyId':x['id'],'historyIndex':i} for i,x in enumerate(report['histories']) if x['id']==key]
                check('evidence-exists/'+group['id']+'/'+str(index)+'/'+source+'/'+key,bool(found))
                resolved.append({'report':'this-receipt' if source==N else names[source],'evidence':found})
            matrix.append({'id':group['id']+'-V'+str(index).zfill(2),'expectation':expectation,'status':'fulfilled-in-finite-conditional-reference-scope','evidence':resolved})
    check('all47-exact-authored-expectations',len(matrix)==expectations['variantCount']==47 and len(mapping)==expectations['groupCount']==16)
    check('failed-check-no-hidden-evidence',next(h for h in reports[T]['histories'] if h['id']=='NWT-12/task-cost-and-failure')['final']['actor']['events']['look']['result']['revealedEvidence']==[])
    paths=[Path(__file__),R/'tools/feat335_nature_transactions.py',R/'tools/feat335_nature_acquisition.py',R/'tools/feat_exact_01_acquisition_models.py',
        R/'data/playtest/character_foundation.json',R/'data/playtest/ancestry_background_candidate.json',R/'data/playtest/equipment_source_catalog.json',
        R/'data/public/feat_candidates/exact_01/supplements.json',R/'data/public/feat_candidates/exact_01/spell_dependencies.json',R/'docs/mechanics/BARD_PLAYTEST_v0_1.md',
        A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',A/'FEAT335_ALLOWANCE_DESCRIPTORS_AFTER_FLORA.json',expectations_path,
        A/'feat335-nature-source-check-01-verdict/NATURE_FOLLOWTHROUGH_CONTRACT.json',*[A/n for n in names.values()],*[G/classes[n]['classCandidatePath'] for n in class_sources]]
    bindings=[info(p) for p in paths]
    for source in [T,S]:
        for binding in reports[source]['sourceBindings']:check('preserved-binding/'+source+'/'+binding['path'],info(G/binding['path'])==binding)
    result={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'reviewId':'FEAT335-NATURE-SOURCE-CHECK-01','status':'pass','checks':len(checks),'failures':[],
        'sourceBindings':bindings,'results':checks,'histories':histories,'expectationMatrix':matrix,
        'counts':{'groups':16,'variants':47,'additionalConditionalHistories':len(histories),'priorTransactionChecks':185,'priorTransactionHistories':75,'priorSpellIntegrationChecks':77,'priorSpellIntegrationHistories':28,'sourcePropagationChecks':137,'reproducedReviewerChecks':124},
        'disposition':'NWQ01–04 finite follow-through fulfilled under the actual reviewer contract: exact propagation plus all16/47 source-bound conditional-reference expectations. No generic repeat Nature conference required by that contract.',
        'scope':'Nature activation/own check/native-or-borrowed payment/Ready/clock and named spell-history/reroll interfaces only. Existing-class and world facts remain visibly conditional; the matrix does not transform source receipts into authenticated campaign events.',
        'limits':['No full335 feat approval, full character builder, complete spell/counter/damage/initiative runtime, human balance, whole-game flow confirmation, GitHub push or cosmology review.',
            'Full Fate Coin/Mark Omen behavior across all users, shared multi-die pools and simultaneous conflicts remains broader ordinary-spell work. Here the coin is genuinely created by the source-qualified own paid cast and applied to the original Nature check.',
            'Bard rhythm and Ranger stabilization begin with explicitly conditional source-legal prior histories; their earlier performances/weapon hits are not newly executed by this Nature audit.',
            'The paid Skill Expert case applies the actual ordered grants at earned Ranger4 and checks immediate Nature use; general later retraining/suppression/advancement is outside that additional history.',
            'Geometry, task permissions, no additional thought/incorporeal sense, lawful signals and interruptions remain conditional world facts. The tests do not certify a general perception or physical-world engine.',
            'The185/75 and77/28 reports retain their earlier incomplete-scope flags. This separate measured receipt supplies the later47-row disposition; no historical report is relabeled or overwritten.'],
        'natureAll47VariantsFulfilledInFiniteScope':True,'newRules':0,'fullFeatExactApproved':False,'runtimeApproved':False,'humanBalanceApproved':False,'cosmologyReviewed':False}
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2,default=serial)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'checks':len(checks),'additionalHistories':len(histories),'variants':len(matrix),'report':info(output)}))


if __name__=='__main__':main()
