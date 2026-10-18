"""Original Suggestion virtual-start clocks within paid Fate/alignment histories.

Original elapsed-only component remains unchanged. Initiative schedules and
legal clock-mode transitions are explicit conditional upstream world events.
"""
from copy import deepcopy
from di7_alignment_component import AlignmentComponent,number
from di7_fate_transactions import FateTransactions
from control_playtest_rules import regular_control_endpoint


class AlignmentClockComponent(AlignmentComponent):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.mode='outside-initiative-elapsed'; self.schedule={}; self.clock_events=[]

    def snapshot(self):
        return {**super().snapshot(),'clockMode':self.mode,'currentRegularStartPhases':deepcopy(self.schedule),'clockEvents':deepcopy(self.clock_events)}

    def configure_clock(self,mode,schedule,event):
        if mode not in {'outside-initiative-elapsed','initiative-virtual-source-start'}:
            raise ValueError('Actual supported clock mode required')
        if not event.get('id') or not event.get('authorityEvent') or event.get('at')!=self.now or any(x['id']==event['id'] for x in self.clock_events):
            raise ValueError('Unique source-qualified current clock transition required')
        for actor,phase in schedule.items():
            if actor not in self.actors or not 0<=number(phase)<6:
                raise ValueError('Actual caster and original six-second schedule phase required')
        self.mode=mode; self.schedule=deepcopy(schedule)
        self.clock_events.append({**deepcopy(event),'mode':mode,'regularStartPhases':deepcopy(schedule),
            'existingDeadlinesRecomputed':False})

    def begin_conditional_committed_cast(self,receipt):
        if receipt['clockMode']!=self.mode:
            raise ValueError('Receipt must identify its actual current clock mode')
        if self.mode=='initiative-virtual-source-start' and receipt['caster'] not in self.schedule:
            raise ValueError('Actual regular-start phase required')
        # Reuse the original transaction validation only. Its elapsed-only
        # compatibility input is never retained as the actual clock authority.
        compatibility=deepcopy(receipt); compatibility['clockMode']='outside-initiative-elapsed'
        super().begin_conditional_committed_cast(compatibility)
        self.casts[receipt['castId']]['clockMode']=receipt['clockMode']

    def resolve(self,cast_id,**save):
        cast=self.casts[cast_id]
        if self.mode=='initiative-virtual-source-start' and cast['caster'] not in self.schedule:
            raise ValueError('Actual resolution-time schedule required')
        result=super().resolve(cast_id,**save)
        effect=self.effects.get(cast_id)
        if effect:
            if effect['spellId']=='alignment-suggestion' and self.mode=='initiative-virtual-source-start':
                phase=self.schedule[effect['caster']]
                endpoint=regular_control_endpoint(self.now,phase,count=10,boundary='start')
                effect['deadline']=float(endpoint.seconds)
                effect['durationClock']={'kind':'ten-original-future-source-starts','applicationClockMode':self.mode,
                    'source':effect['caster'],'originalRegularStartPhase':phase,'count':10,
                    'deadline':effect['deadline'],'expiryEventPhase':endpoint.phase,'keptThroughScheduleChanges':True}
            else:
                effect['durationClock']={'kind':'absolute-elapsed60','applicationClockMode':self.mode,
                    'deadline':effect['deadline'],'keptThroughScheduleChanges':True,
                    'scope':'Purge explicit60 seconds, or Suggestion applied outside initiative.'}
        return result

    def advance(self,when):
        number(when)
        if when<self.now: raise ValueError('Ordered time cannot rewind')
        deadlines=sorted({e['deadline'] for e in self.effects.values() if e['state']=='live' and self.now<=e['deadline']<=when})
        for deadline in deadlines: super().advance(deadline)
        super().advance(when)


class ClockedFateTransactions(FateTransactions):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.alignment=AlignmentClockComponent(self.world['alignmentActors'],self.alignment.sources)
        self.alignment.advance(self.now)

    def configure_clock(self,mode,schedule,event):
        self.alignment.configure_clock(mode,schedule,event)

    def declare(self,actor,sid,cast_id,request):
        if sid in {'alignment-suggestion','alignment-purge'} and self.alignment.mode=='initiative-virtual-source-start' and actor not in self.alignment.schedule:
            raise ValueError('Actual source-start schedule required before commitment')
        return super().declare(actor,sid,cast_id,request)

    def _child_check(self,actor,original_id,request,**kwargs):
        original=self.casts.get(original_id)
        if original and original['spellId']=='alignment-suggestion' and self.alignment.mode=='initiative-virtual-source-start' and actor not in self.alignment.schedule:
            raise ValueError('Actual copied-cast source-start schedule required before commitment')
        return super()._child_check(actor,original_id,request,**kwargs)

    def _register_alignment_commit(self,cast_id):
        cast=self.casts[cast_id]
        if cast['spellId'] in {'alignment-suggestion','alignment-purge'}:
            self.alignment.begin_conditional_committed_cast({'castId':cast_id,'spellId':cast['spellId'],
                'sourceBinding':self.alignment.sources[cast['spellId']],'caster':cast['actor'],'target':cast['request']['target'],
                'committedAt':self.now,'clockMode':self.alignment.mode,
                'paymentPremise':{'kind':'conditional-upstream-commit-not-executed-here','fixtureId':'actual-paid-parent-evaluator/'+cast_id,
                    'upstreamExecutedQuote':deepcopy(cast['quote']),'upstreamExecutedBudgetAndHistory':deepcopy(cast['afterCommit'])}})

    def begin_turn(self,actor,turn_id):
        # The caller supplies a real regular turn. Advancing first applies all
        # original virtual/absolute expirations before Reaction refresh/choices.
        if self.stack or turn_id in self.actors[actor]['turnHistory']:
            raise ValueError('New actual regular turn with no pending cast required')
        self.advance(self.now)
        return super().begin_turn(actor,turn_id)
