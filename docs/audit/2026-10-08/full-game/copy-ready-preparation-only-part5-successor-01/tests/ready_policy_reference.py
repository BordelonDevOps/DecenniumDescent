"""Isolated policy reference, NOT a game adapter or production Ready implementation.

The caller supplies source-qualified actions, triggers, targets, deadlines and
world predicates. Numbers and IDs are harness operands, not granted game content.
Only the preparation/hold/release accounting and their no-replay invariants are
modeled. Historical mode exists only to expose the superseded policy outcomes.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from copy import deepcopy
from typing import Any

PROFILES = ('Strike','Burst','Mend','Ward','Hindrance','Boon','Step')
SUSTAINED = frozenset(('Ward','Hindrance','Boon'))

@dataclass
class ReadyPolicyReference:
    policy: str = 'preparation-only'
    owns_mirrorsage: bool = False
    rp: int = 30
    # Abstract supplied authorization receipts, not a new capture-slot mechanic.
    authorizations: int = 3
    reaction_available: bool = True
    feat_rounds: dict[str,str] = field(default_factory=dict)
    class_rounds: dict[str,str] = field(default_factory=dict)
    hold: dict[str,Any] | None = None
    concentration: dict[str,Any] | None = None
    preparations: list[str] = field(default_factory=list)
    committed_releases: dict[str,str] = field(default_factory=dict)
    casts: list[dict[str,Any]] = field(default_factory=list)
    counts: dict[str,int] = field(default_factory=lambda:dict(actions=0,reactions=0,payments=0,permissions=0,components=0,history=0,counter_windows=0,payloads=0))
    last_target: str | None = None

    def snapshot(self) -> dict[str,Any]:
        return deepcopy(self.__dict__)

    @classmethod
    def restore_fixture(cls, state: dict[str,Any]) -> 'ReadyPolicyReference':
        # Tests data continuity only; not a durable game save/load subsystem.
        obj=cls();obj.__dict__=deepcopy(state);return obj

    def _valid_new_cast(self, event: str, round_id: str, quote: int,
                        legal_action: bool, legal_sources: bool) -> bool:
        return (legal_action and legal_sources and type(quote) is int and quote>=0
                and self.rp>=quote and self.authorizations>0
                and event not in self.preparations
                and round_id not in self.feat_rounds
                and (not self.owns_mirrorsage or round_id not in self.class_rounds))

    def _pay(self, event: str, round_id: str, quote: int, family: str) -> None:
        self.feat_rounds[round_id]=event
        if self.owns_mirrorsage:self.class_rounds[round_id]=event
        self.rp-=quote; self.authorizations-=1;self.preparations.append(event)
        for k in ('actions','payments','permissions','components','history','counter_windows'):self.counts[k]+=1
        self.casts.append(dict(event=event,family=family,round=round_id,quote=quote))

    def prepare(self,event:str,round_id:str,now:int,*,ready_expiry:int=6,
                capture_expiry:int=20,quote:int=7,legal_action:bool=True,
                legal_sources:bool=True,profile:str='Strike',q:int=4,
                mode:str='fixed-source-component',family:str='feat-copy::source-A',
                countered:bool=False) -> str:
        if (profile not in PROFILES or now>=min(ready_expiry,capture_expiry)
            or not self._valid_new_cast(event,round_id,quote,legal_action,legal_sources)):
            return 'preparation-rejected'
        self._pay(event,round_id,quote,family)
        self.hold=dict(id=event,owner='fixture-owner',profile=profile,q=q,mode=mode,
                       prep_round=round_id,ready_expiry=ready_expiry,capture_expiry=capture_expiry,
                       paid_quote=quote,required_class_receipt=self.owns_mirrorsage,
                       feat_ledger='fixture-canonical-feat-ledger',class_ledger='fixture-canonical-class-ledger' if self.owns_mirrorsage else None)
        self.concentration=dict(id=event,state='held')
        if countered:self.end('countered');return 'preparation-countered'
        return 'prepared'

    def release(self,event:str,round_id:str,now:int,*,trigger_completed:bool=True,
                trigger_perceived:bool=True,declined:bool=False,legal_target:bool=True,
                legal_source:bool=True,target:str='current-release-target',
                expected_profile:str|None=None,expected_mode:str|None=None,
                late_prevented:bool=False) -> str:
        if event in self.committed_releases:return 'duplicate-release'
        h=self.hold
        if not h:return 'no-hold'
        if now>=min(h['ready_expiry'],h['capture_expiry']):self.end('expired');return 'expired'
        if self.concentration!=dict(id=h['id'],state='held'):
            self.hold=None;return 'concentration-lost'
        if (not trigger_completed or not trigger_perceived or declined or not legal_target
            or not legal_source or not self.reaction_available
            or (expected_profile is not None and expected_profile!=h['profile'])
            or (expected_mode is not None and expected_mode!=h['mode'])):
            return 'release-not-committed'
        # Verify durable PREPARATION receipts, never current-round availability.
        if (self.feat_rounds.get(h['prep_round'])!=h['id'] or
            (h['required_class_receipt'] and self.class_rounds.get(h['prep_round'])!=h['id'])):
            return 'invalid-preparation-receipt'
        if self.policy=='historical-both-rounds' and round_id!=h['prep_round']:
            if (round_id in self.feat_rounds or
                (h['required_class_receipt'] and round_id in self.class_rounds)):
                return 'release-not-committed'
            self.feat_rounds[round_id]=h['id']
            if h['required_class_receipt']:self.class_rounds[round_id]=h['id']
        elif self.policy not in ('preparation-only','historical-both-rounds'):
            raise ValueError('Unrecognized isolated reference policy')
        # The consume precedes modeled payload, so repeated/reentrant calls cannot replay.
        self.hold=None;self.committed_releases[event]=h['id']
        self.reaction_available=False;self.counts['reactions']+=1
        self.last_target=target
        if not late_prevented:self.counts['payloads']+=1
        self.concentration=(dict(id=h['id'],state='sustained')
                            if h['profile'] in SUSTAINED and not late_prevented else None)
        return 'release-committed-prevented' if late_prevented else 'release-committed'

    def direct(self,event:str,round_id:str,now:int,*,legal_action:bool=True,
               legal_sources:bool=True,quote:int=7,profile:str='Strike',
               family:str='feat-copy::source-B') -> str:
        if not self._valid_new_cast(event,round_id,quote,legal_action,legal_sources):return 'direct-rejected'
        self._pay(event,round_id,quote,family)
        if profile in SUSTAINED:
            self.end('concentration-replaced')
            self.concentration=dict(id=event,state='sustained')
        self.counts['payloads']+=1
        return 'direct-committed'

    def supplied_class_use(self,event:str,round_id:str,*,legal_opportunity:bool=True,
                           breaks_concentration:bool=False) -> str:
        # Class cost/native effects are not modeled. This is a source-qualified
        # external shared-allowance event, not an implemented class Echo.
        if not self.owns_mirrorsage or not legal_opportunity or round_id in self.class_rounds:return 'class-use-rejected'
        self.class_rounds[round_id]=event
        if breaks_concentration:self.end('native-concentration-replaced')
        return 'external-class-use-recorded'

    def end(self,reason:str) -> str:
        if self.hold and self.concentration and self.concentration.get('id')==self.hold['id']:
            self.concentration=None
        self.hold=None
        return reason
