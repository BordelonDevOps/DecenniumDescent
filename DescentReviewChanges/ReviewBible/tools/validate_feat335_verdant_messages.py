"""Source-qualified acquisition and finite Verdant message/communication traces."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json
from feat335_verdant_messages import VerdantMessages
from feat_exact_01_flora_acquisition import FloraAcquisition
from feat_exact_01_initiate_acquisition_model import InitiateAcquisitions
from feat_exact_01_casting_credential_model import CastingSources
from validate_feat_exact_01_composite_casting import read, info, serial
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'


def main():
    output=A/'FEAT335_VERDANT_MESSAGE_CHECK.json';assert not output.exists()
    paths=[R/'data/playtest/character_foundation.json',R/'data/playtest/ancestry_background_candidate.json',
        R/'data/playtest/equipment_source_catalog.json',R/'data/public/feat_candidates/exact_01/supplements.json',
        R/'data/public/feat_candidates/exact_01/spell_dependencies.json',R/'data/public/class_playtests/wizard.json',
        A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',A/'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json',
        R/'data/director/magic_core_feat_operating_proposal_internal.json',
        R/'data/public/feat_candidates/exact_01/shared_rules.json',
        R/'docs/mechanics/CLASS_PLAYTEST_RULES.md',R/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md',
        Path(__file__),*[R/'tools'/n for n in ['feat335_verdant_messages.py','feat_exact_01_flora_acquisition.py',
            'feat_exact_01_casting_selections.py','feat_exact_01_remaining_owned_chains.py',
            'feat_exact_01_composite_casting_model.py','feat_exact_01_casting_credential_model.py',
            'feat_exact_01_initiate_acquisition_model.py','feat_exact_01_acquisition_models.py','feat_exact_01_training_prerequisite_model.py']]]
    bindings=[info(p) for p in paths]
    foundation,ancestry,equipment,sm,deps,wizard,contracts,prior,core=[read(p) for p in paths[:9]]
    classes={x['class']:x for x in foundation['classes']};skills={s:a for a,ss in foundation['skillAbilities'].items() for s in ss}
    equipment={x['id']:x for x in equipment['records']};backgrounds={x['id']:x for x in ancestry['backgrounds']}
    supplements={x['id']:x['value'] for x in sm['groups']};contracts={x['id']:x for x in contracts['records']}
    sources=CastingSources(G,deps['spells'],supplements,wizard);checks=[];histories=[]
    def check(label,ok):checks.append({'id':label,'passed':bool(ok)});assert ok,label
    def reject(label,m,call,reason=None):
        before=m.snapshot()
        try:call()
        except ValueError as e:check(label,reason is None or reason in str(e))
        else:check(label,False)
        check(label+'/no-uncommitted-mutation',before==m.snapshot())
    def record(label,m):histories.append({'id':label,'state':m.snapshot(),'evidenceMode':'conditional_source_qualified_not_campaign_fact'})
    def make():
        actor=deepcopy(prior['actorSourceProjection']);actor.update(firstClass='Warrior',classLevels={'Warrior':1},selectedClassSkills=['Nature','Athletics'])
        h=FloraAcquisition(actor,classes,equipment,skills,ancestry,backgrounds,contracts,supplements,sources);h.configure_choice_sources(core)
        paid=InitiateAcquisitions(actor,classes,equipment,skills,ancestry,backgrounds,contracts,supplements['SUP-04'],deps['spells'])
        paid.advance(4);paid.earn(4);_,cantrips,rank1=prior['authoredCurriculumChoices']['Wizard']
        paid.acquire('magicInitiate',4,{'curriculum':'Wizard','cantrips':cantrips,'rank1':rank1})
        h.advance(4);h.pay=paid.pay;h.casting.import_initiate(paid,4)
        h.advance(8);h.earn(8);h.acquire_named('verdant_bond',8)
        world={'owner':{'position':0,'actualReach':5,'canAct':True,'conscious':True,
            'actualRecordingCommunication':True,'actualOrdinaryCommunication':True},
            'knownAllyIds':['owner','ally'],'actors':['owner','ally','stranger','overhearer'],
            'stands':{'oak':{'position':5,'rooted':True,'alive':True,'reachable':True,'perceived':True,'lineOfEffect':True},
                'reed':{'position':50,'rooted':True,'alive':True,'reachable':False,'perceived':True,'lineOfEffect':True}}}
        return VerdantMessages(h,world)
    def ready(m,recipient='ally',text='Danger beyond the northern gate'):
        m.start('message','oak',text,recipient)
        return m.complete(60,actual_uninterrupted_active_work=True)
    def pass_by(m,event,now,actor='ally',qualifies=True,near=True,hearers=None):
        return m.passage(event,actor=actor,stand_id='oak',now=now,actual_future_passage=qualifies,
                         within_ten_feet=near,actual_hearers=['ally'] if hearers is None else hearers)

    check('source-owner-recipient-and-genuine-future-passage', 'owner may be the one chosen message recipient' in contracts['verdant_bond']['completeOperativeProcedure'])
    for recipient in ['owner','ally']:
        m=make();check(recipient+'/paid-source-no-Flora-or-message',m.acquired.pay.has('verdant_bond') and not m.acquired.pay.has('conjure_flora') and not m.records and m.allowance['current']==1)
        completed=ready(m,recipient)
        check(recipient+'/minute-and-original24h-endpoint',completed['recordedAt']==60 and completed['deadline']==86460 and m.allowance['current']==0)
        check(recipient+'/no-instant-creation-trigger',pass_by(m,'at-recording',60,recipient)==[])
        check(recipient+'/standing-nearby-not-future-passage',pass_by(m,'no-movement',61,recipient,qualifies=False)==[])
        check(recipient+'/outside-ten-feet-does-not-consume',pass_by(m,'too-far',62,recipient,near=False)==[] and m.records['message']['active'])
        other='ally' if recipient=='owner' else 'owner'
        check(recipient+'/other-ally-not-selected',pass_by(m,'wrong-recipient',63,other)==[])
        results=pass_by(m,'future-passage',64,recipient,hearers=[recipient,'stranger','overhearer'])
        check(recipient+'/ordinary-audible-once-not-private',len(results)==1 and results[0]['audibleMessage']=='Danger beyond the northern gate' and len(results[0]['actualHearers'])==3 and not results[0]['privateTelepathy'] and not results[0]['remoteConfirmation'])
        check(recipient+'/repeat-passage-does-not-replay',pass_by(m,'another-pass',65,recipient)==[])
        reject(recipient+'/same-event-cannot-replay',m,lambda:pass_by(m,'future-passage',66,recipient),'cannot be replayed')
        record('finite-delivery/'+recipient,m)
    m=make();m.start('maximum-message','oak',' '.join('word'+str(i) for i in range(25)),'ally')
    check('25-word-message-commits-before-active-minute',m.allowance['current']==0 and not m.records and m.pending is not None)
    reject('59-seconds-not-complete',m,lambda:m.complete(59,actual_uninterrupted_active_work=True),'active minute')
    m.complete(60,actual_uninterrupted_active_work=True)
    check('25-words-preserved',len(m.records['maximum-message']['message'].split())==25)
    record('maximum-length-and-active-time',m)
    m=make()
    for label,call in [('26-words',lambda:m.start('bad','oak',' '.join(['word']*26),'ally')),
                       ('no-message',lambda:m.start('bad','oak','','ally')),
                       ('unknown-recipient',lambda:m.start('bad','oak','Warning','unknown')),
                       ('nonally-recipient',lambda:m.start('bad','oak','Warning','stranger')),
                       ('no-actual-stand',lambda:m.start('bad','invented','Warning','ally')),
                       ('real-but-out-of-reach',lambda:m.start('bad','reed','Warning','ally'))]:
        reject('precommit/'+label,m,call)
    for field,value in [('rooted',False),('alive',False),('reachable',False)]:
        m.world['stands']['oak'][field]=value
        reject('precommit/stand-'+field,m,lambda:m.start('bad','oak','Warning','ally'))
        m.world['stands']['oak'][field]=True
    for field in ['canAct','actualRecordingCommunication']:
        m.world['owner'][field]=False;reject('precommit/owner-'+field,m,lambda:m.start('bad','oak','Warning','ally'));m.world['owner'][field]=True
    check('all-invalid-starts-retain-full-use',m.allowance['current']==1 and not m.events and not m.pending)
    record('actual-recording-gates',m)
    for cause in ['interrupted-work','range-loss','incapacity','destroyed-stand']:
        m=make();m.start('interrupted','oak','Warning','ally');m.advance(30)
        if cause=='destroyed-stand':m.destroy_stand('oak',30)
        else:
            if cause=='range-loss':m.world['owner']['position']=50
            if cause=='incapacity':m.world['owner']['canAct']=False
            reject(cause+'/cannot-complete-pretended-work',m,lambda:m.complete(60,actual_uninterrupted_active_work=cause!='interrupted-work'))
            m.interrupt(actual_interruption=True)
        check(cause+'/no-message-no-refund',not m.pending and not m.records and m.allowance['current']==0)
        record('interrupted-recording/'+cause,m)
    for now,delivered in [(86459,True),(86460,False),(90000,False)]:
        m=make();ready(m);result=pass_by(m,'deadline-passage',now)
        check('original-deadline/'+str(now),bool(result)==delivered and not m.records['message']['active'])
        if not delivered:check('expired-no-backlog/'+str(now),m.records['message']['endReason']=='original24-hour-expiry')
        record('elapsed-expiry/'+str(now),m)
    m=make();ready(m);m.destroy_stand('oak',120)
    check('destruction-ends-only-stored-message-no-refund',not m.records['message']['active'] and m.records['message']['endReason']=='stand-destroyed' and m.allowance['current']==0)
    reject('destroyed-stand-cannot-replay',m,lambda:pass_by(m,'later',130),'surviving rooted')
    record('message-generator-destroyed',m)
    m=make();ready(m)
    result=pass_by(m,'deaf-recipient-passage',100,hearers=[])
    check('first-trigger-not-banked-until-someone-hears',len(result)==1 and result[0]['actualHearers']==[] and not m.records['message']['active'])
    check('later-hearing-cannot-replay',pass_by(m,'hearing-restored',110)==[])
    record('audible-event-and-actual-hearing-separated',m)
    m=make();ready(m);original=deepcopy(m.records['message'])
    check('short-rest-no-message-use-recovery',not m.rest('short',kind='SR',beneficial=True) and m.allowance['current']==0)
    check('debt-only-LR-no-message-recovery',not m.rest('debt',kind='LR',beneficial=False) and m.allowance['current']==0)
    m.advance(86400)
    check('genuine-beneficial-LR-refills-only-use',m.rest('actual-LR',kind='LR',beneficial=True) and m.allowance['current']==1 and m.records['message']==original)
    check('same-rest-cannot-refill-twice',not m.rest('actual-LR',kind='LR',beneficial=True))
    m.start('next-message','oak','New actual message','owner');m.complete(86460,actual_uninterrupted_active_work=True)
    check('new-paid-record-own-deadline-old-not-restored',m.records['next-message']['deadline']==172860 and not m.records['message']['active'] and m.allowance['current']==0)
    record('real-beneficial-LR-new-record-no-old-duration-reset',m)
    for response in [None,'fear','hunger','dormancy']:
        m=make();before=m.snapshot();result=m.communicate('reed',actual_brief_simple_ideas=True,actual_coarse_reply=response)
        check('coarse-ordinary-reply/'+str(response),result['reply']==response and not any(result[k] for k in ['newIntelligence','historyExtracted','compelled','remoteKnowledge']) and m.snapshot()==before)
        record('plant-communication/'+str(response),m)
    m=make()
    for answer in ['An enemy named Aldren passed yesterday','secret map','hidden creature identity']:
        reject('no-extracted-history/'+answer,m,lambda answer=answer:m.communicate('reed',actual_brief_simple_ideas=True,actual_coarse_reply=answer),'coarse current response')
    for field in ['perceived','lineOfEffect']:
        m.world['stands']['reed'][field]=False
        reject('communication/'+field,m,lambda:m.communicate('reed',actual_brief_simple_ideas=True,actual_coarse_reply='fear'))
        m.world['stands']['reed'][field]=True
    m.world['stands']['reed']['position']=61
    reject('communication/outside60',m,lambda:m.communicate('reed',actual_brief_simple_ideas=True,actual_coarse_reply='fear'))
    m.world['stands']['reed']['position']=50;m.world['owner']['conscious']=False
    reject('communication/unconscious-owner',m,lambda:m.communicate('reed',actual_brief_simple_ideas=True,actual_coarse_reply='fear'))
    record('ordinary-sense-and-knowledge-boundaries',m)
    check('all-source-bindings-stable',bindings==[info(p) for p in paths])
    result={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'pass','checks':len(checks),'failures':[],
        'sourceBindings':bindings,'completeFeatContract':contracts['verdant_bond'],'results':checks,'histories':histories,
        'counts':{'conditionalHistories':len(histories),'maximumMessageWords':25,'recordingActiveSeconds':60,'storedDurationSeconds':86400},
        'scope':'Actual paid Verdant acquisition, real rooted-stand/reach/known-ally premises, finite recording and interruption, first genuinely future designated passage, ordinary audible event, destruction/absolute expiry and real beneficial-LR allowance; bounded plant communication has no invented knowledge.',
        'limits':['World stands/actors, consent/known-ally identity, ordinary speech, actual hearing, actual passage within10ft, uninterrupted work and beneficial-rest legality are conditional source-qualified fixtures, not an authenticated campaign or general perception/movement/acoustics engine.',
            'At-most25 ordinary words uses unambiguous whitespace-delimited test messages; no new general punctuation/tokenization rule is adopted.',
            'Communication and message storage do not execute Verdant wilderness-task advantage, plant-terrain movement or full Nature spell casting; Flora supporting-bonus predicates were checked separately in the current189-check source follow-through.',
            'Actual paid-start/cancellation traces preserve the shared no-refund timing convention. Arbitrary other magic suppression/dispels and global work/rest scheduling still require their own source scope.',
            'No new source rule, full feat gate, whole-game/runtime approval, human playtest, push or cosmology review follows.'],
        'newRules':0,'fullFeatExactApproved':False,'runtimeApproved':False,'humanBalanceApproved':False,'cosmologyReviewed':False}
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2,default=serial)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'checks':len(checks),'histories':len(histories),'report':info(output)}))

if __name__=='__main__':main()
