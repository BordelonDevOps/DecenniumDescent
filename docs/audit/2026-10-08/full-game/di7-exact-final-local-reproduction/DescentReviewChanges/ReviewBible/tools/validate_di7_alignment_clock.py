"""Paid Suggestion/Purge and Fate-copy durations retain original source clocks."""
from copy import deepcopy
from datetime import datetime,timezone
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded
from di7_cast_transactions import DI7Sources
from di7_area_fixtures import make as area_fixture
from di7_alignment_clock import ClockedFateTransactions


def main():
    output=A/'DI7_ALIGNMENT_CLOCK_CHECK.json'; assert not output.exists()
    sources=DI7Sources(); checks=[]; histories=[]
    def check(label,value): assert value,label; checks.append(label)
    def record(label,m): histories.append({'id':label,'final':m.snapshot()})
    def reject(label,m,fn):
        before=m.snapshot()
        try: fn()
        except ValueError as e: check(label+'/rejected',bool(str(e)))
        else: raise AssertionError(label)
        check(label+'/atomic',m.snapshot()==before)
    def make(*,provider='Wizard',initiative=True,phase=0):
        base,_=area_fixture(sources,provider=provider); world=deepcopy(base.world)
        world['entities']['target']={'kind':'creature','positionFeet':25,'willing':True,'alliedTo':{},'relatedQuestions':[]}
        world['alignmentActors']['target']={'underlying':{'order':'Chaotic','ethics':'Evil'},'immunities':[],'permanentIdentity':{'id':'target'},'acquisitionSnapshots':[],'usedAllowances':{}}
        for actor in base.actors:
            world['relations'][actor+'>target']={'sourceFact':'conditional-open-local-target','perceived':True,'visible':True,'lineOfEffect':True}
        m=ClockedFateTransactions(sources,base.actors,world)
        m.learn('owner','alignment-purge',m.actors['owner']['classLevel'],'actual-Purge-learning')
        if provider in {'Wizard','Mirrorsage'}: m.learn('owner','alignment-suggestion',1,'actual-Suggestion-learning')
        if provider=='Wizard': m.learn('owner','fate-echo',13,'actual-Fate-learning')
        m.learn('counter','counterspell',5,'actual-Counter-learning'); m.learn('counter','alignment-suggestion',1,'counter-original-Suggestion')
        for aid,a in m.actors.items():
            if a['provider']=='Wizard': m.prepare_wizard(aid,list(a['learned']),aid+'/study',{'actor':aid,'completedAt':0,'sourceEvent':'conditional-completed-rest'})
        if initiative: m.configure_clock('initiative-virtual-source-start',{'owner':phase,'counter':2},{'id':'initial-clock','at':3600,'authorityEvent':'conditional-actual-initiative-order'})
        m.begin_turn('owner','owner-turn1'); return m
    def cast(m,sid='alignment-suggestion',cid='suggestion',face=1):
        m.declare('owner',sid,cid,{'target':'target'}); m.resolve_alignment(cid,face=face,modifier=0)
        return m.alignment.effects.get(cid)
    def transition(m,mode,schedule,eid): m.configure_clock(mode,schedule,{'id':eid,'at':m.now,'authorityEvent':'conditional-actual-clock-transition/'+eid})
    for provider in ['Wizard','Mirrorsage']:
        for now,phase,expected in [(3600,0,3660),(3601,0,3660),(3601,3,3657),(3603,3,3663)]:
            m=make(provider=provider,phase=phase); m.advance(now); e=cast(m)
            check(provider+'/'+str(now)+'/'+str(phase)+'/tenth-strictly-future-start',e['deadline']==expected and e['durationClock']['count']==10 and m.actors['owner']['rp']==m.actors['owner']['maxRP']-2)
            m.advance(expected-.001); check('live-before-'+str(len(histories)),m.alignment.effective('target')=={'order':'Neutral','ethics':'Neutral'})
            m.advance(expected); check('ended-at-original-start-'+str(len(histories)),m.alignment.effective('target')=={'order':'Chaotic','ethics':'Evil'} and m.actors['owner']['concentration'] is None and e['endedAt']==expected)
            record(provider+'/'+str(now)+'/'+str(phase),m)
    m=make(); m.advance(3601); e=cast(m); original=deepcopy(e['durationClock'])
    m.advance(3610); transition(m,'initiative-virtual-source-start',{'owner':4,'counter':1},'reroll-reorder')
    m.advance(3620); transition(m,'outside-initiative-elapsed',{},'leave-initiative')
    m.advance(3630); transition(m,'initiative-virtual-source-start',{'owner':5,'counter':2},'return-initiative')
    check('mode-changes-preserve-original-virtual-clock',e['durationClock']==original and e['deadline']==3660)
    m.advance(3700); check('long-jump-records-actual-expiry-not-late-observation',e['endedAt']==3660 and m.alignment.now==3700)
    record('reorder-leave-return-original-phase',m)
    m=make(initiative=False); m.advance(3601); e=cast(m)
    check('outside-absolute60',e['deadline']==3661 and e['durationClock']['kind']=='absolute-elapsed60')
    m.advance(3610); transition(m,'initiative-virtual-source-start',{'owner':0,'counter':2},'enter-initiative')
    m.advance(3660); check('entry-does-not-shorten-absolute-clock',e['state']=='live')
    m.advance(3661); check('original-absolute-deadline-preserved',e['state']=='ended' and e['endedAt']==3661)
    record('outside-to-inside',m)
    for provider in ['Wizard','Cleric','Mirrorsage','Shaman']:
        m=make(provider=provider); m.advance(3601); e=cast(m,'alignment-purge','purge')
        check(provider+'/Purge-not-converted-to-Suggestion-clock',e['deadline']==3661 and e['durationClock']['kind']=='absolute-elapsed60' and m.actors['owner']['rp']==m.actors['owner']['maxRP']-17)
        m.advance(3660); check(provider+'/Purge-still-live-at-Suggestion-boundary',e['state']=='live')
        m.advance(3661); check(provider+'/Purge-expires-at60',e['state']=='ended')
        record(provider+'/Purge-explicit-elapsed',m)
    m=make(); m.advance(3601); e=cast(m); m.alignment.suppress('suggestion',True)
    m.advance(3659); check('suppression-does-not-shift-clock',e['deadline']==3660 and m.alignment.effective('target')=={'order':'Chaotic','ethics':'Evil'})
    m.alignment.suppress('suggestion',False); check('return-before-expiry-restores-same-values',m.alignment.effective('target')=={'order':'Neutral','ethics':'Neutral'})
    m.advance(3660); reject('no-suppression-return-after-expiry',m,lambda:m.alignment.suppress('suggestion',False)); record('suppression-keeps-clock',m)
    m=make(); m.advance(3601); e=cast(m)
    # Separate legal extra-turn grants are not authored here. Even if a caller
    # invokes an additional turn budget, deadlines use elapsed virtual markers.
    m.begin_turn('owner','conditional-otherwise-legal-extra-budget'); check('extra-budget-no-clock-tick-or-reset',e['deadline']==3660 and e['state']=='live')
    m.advance(3660); m.actors['owner']['reactions']=0; m.begin_turn('owner','actual-expiry-start')
    check('expiry-before-turn-refresh-and-voluntary-decisions',e['state']=='ended' and m.actors['owner']['concentration'] is None and m.actors['owner']['reactions']==1)
    record('turn-budget-does-not-tick-duration',m)
    m=make(); m.advance(3601); old=cast(m)
    m.advance(3606); m.begin_turn('owner','owner-turn2'); new=cast(m,cid='replacement')
    check('actual-recast-gets-new-clock-old-never-revives',old['state']=='ended' and new['deadline']==3666 and m.actors['owner']['rp']==44)
    m.advance(3660); check('old-deadline-not-new-deadline',new['state']=='live')
    m.advance(3666); check('new-clock-ends-once',new['state']=='ended'); record('paid-recast-clock',m)
    m=make(); m.advance(3601); e=cast(m)
    m.advance(3606); m.begin_turn('owner','owner-turn2'); cast(m,cid='saved-recast',face=20)
    check('successful-save-no-new-timer-or-restored-old-concentration',e['state']=='ended' and 'saved-recast' not in m.alignment.effects and m.actors['owner']['concentration'] is None)
    record('failed-application-no-timer',m)
    m=make(); m.advance(3601); m.declare('owner','alignment-suggestion','countered',{'target':'target'})
    m.declare('counter','counterspell','interrupt',{'pendingCast':'countered'}); m.resolve_counter('interrupt',20)
    check('actual-counter-no-clock-application',not m.alignment.effects and m.actors['owner']['concentration'] is None and m.actors['owner']['rp']==46)
    record('actual-countered-clock',m)
    m=make(); m.advance(3601); e=cast(m); m.alignment.caster_loses_concentration('owner','death'); m.advance(3601)
    check('source-death-ends-concentration-despite-virtual-clock',e['state']=='ended' and e['endedAt']==3601 and m.actors['owner']['concentration'] is None)
    record('actual-concentration-ending',m)
    m=make(); transition(m,'initiative-virtual-source-start',{'counter':2},'missing-caster-schedule')
    reject('unsupported-missing-schedule-prepayment',m,lambda:m.declare('owner','alignment-suggestion','missing',{'target':'target'})); record('missing-schedule-fails-closed',m)
    # A real original Suggestion and an actually paid/observed Fate child use
    # different casters' original phases; the copy does not inherit its timer.
    m=make(); m.begin_turn('counter','counter-original-turn')
    m.declare('counter','alignment-suggestion','original',{'target':'target'})
    m.world['identificationFacts']['actual-original']={'observer':'owner','castId':'original','kind':'conditional-actual-direct-identification'}
    m.observe_cast('owner','original','actual-original'); m.resolve_alignment('original',face=1,modifier=0)
    original=m.alignment.effects['original']; m.advance(3601); m.begin_turn('owner','owner-Fate-turn')
    m.begin_fate('owner','echo','original',{'target':'target'}); child=m.finish_fate_outer('echo'); m.resolve_alignment(child['id'],face=1,modifier=0)
    copied=m.alignment.effects[child['id']]
    check('Fate-original-paid-and-own-phase',original['deadline']==3656 and original['durationClock']['originalRegularStartPhase']==2 and m.actors['counter']['rp']==46)
    check('Fate-child-paid-with-new-caster-clock',copied['deadline']==3660 and copied['durationClock']['originalRegularStartPhase']==0 and m.actors['owner']['rp']==29)
    check('Fate-copy-replaces-old-family-without-inheriting-timer',original['state']=='ended' and copied['state']=='live' and m.casts[child['id']]['copyLineage']['original']=='original')
    record('actual-Fate-copied-Suggestion-clock',m)
    bindings=sources.bindings+[info(p) for p in [R/'tools/di7_alignment_clock.py',R/'tools/validate_di7_alignment_clock.py',R/'tools/di7_alignment_component.py',
        R/'tools/di7_fate_transactions.py',R/'tools/di7_cast_transactions.py',R/'tools/control_playtest_rules.py',R/'tools/combat_playtest_rules.py',
        R/'tools/di7_area_fixtures.py',R/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md']]
    report={'status':'pass','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'checks':len(checks),'historyCount':len(histories),'sourceBindings':bindings,
        'checkLabels':checks,'histories':histories,'failures':[],
        'scope':'Original Alignment Suggestion tenth-future-source-start duration and Purge explicit elapsed60 integrated with actual conditional paid casting, counters and one actual paid Fate child.',
        'conditionalPremises':['Original regular-start phases and legal schedule/mode changes are conditional source-qualified upstream initiative facts.',
            'Extra turn legality, full initiative scheduling, acquired source death/conditions, class progression and rest are not implemented here.',
            'Full source-bound Fate/cast and prior alignment components remain separately qualified; this extension settles their retained timing seam only.'],
        'remaining':['Supreme historical payload and actual ordinary Shaman totem vent.','Compile original49 and source supplements and obtain separate exact-seven-card review.'],
        'candidateApproved':False,'full49Fulfilled':False,'humanPlaytest':False,'spellPromotions':0,'newRuleAdoptions':0}
    output.write_bytes(encoded(report)); print(json.dumps({'report':info(output),'checks':len(checks),'histories':len(histories)}))


if __name__=='__main__': main()
