#!/usr/bin/env python3
"""Isolated fixture/receipt checks. No game/project imports or native scheduler.

Runs against complete delivered JSON data. The reward projection is intentionally
not a Counterspell, acquisition, source-prohibition, or persistence implementation.
It publishes positive awarded receipts and spent-round no-award receipts only.
Prohibited/cap-zero tests are read-only nonaward projections; they do not select
any previously unspecified consumption rule for an unused zero-award trigger.
"""
from __future__ import annotations
from pathlib import Path
from zipfile import ZipFile
from copy import deepcopy
import argparse, json, hashlib

FEATURE='wizard.supplement.arcane-feedback'
RETURN01='DD_Rank9_Resonance_Fields_3_Part5_Conference_Return_01.zip'

def encode(o): return (json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
def stable_key(scope,owner,source): return json.dumps([scope,owner,FEATURE,source],ensure_ascii=False,separators=(',',':'))
def canon(o): return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def digest(o): return hashlib.sha256(canon(o)).hexdigest()

def extract_state(full,owner):
    a=full['actors'][owner]
    return {'ownerId':owner, 'numberedRoundContext':deepcopy(full['numberedRoundContext']),
            'rp':a['rp'],'maxRP':a['maxRP'],'action':a['action'],'reaction':a['reaction'],
            'recharge':deepcopy(a['recharge']), 'limitedUses':deepcopy(a['limitedUses'])}

def event_from_receipt(r):
    return {'scopeId':r['scopeId'],'ownerId':r['ownerId'],'roundId':r['roundId'],
            'roundOrdinal':r['roundOrdinal'],'counterCastId':r['counterCastId'],
            'negatedCastId':r['negatedCastId'],'nativeCounterSourceRef':r['nativeCounterSourceRef'],
            'originalResolutionEventId':r['originalResolutionEventId'],'settledAt':r['settledAt'],
            'qualification':deepcopy(r['qualification']), 'nativeCounterTransactionComplete':True,
            'deliveryId':'first-delivery'}

def settle_positive_or_spent_round(state,event):
    """Reward-only pure projection; no payment, Reaction refresh, dice or source execution."""
    s=deepcopy(state);owner=s['ownerId'];ctx=s['numberedRoundContext']
    if event['ownerId']!=owner or event['scopeId']!=ctx['scopeId']:
        raise ValueError('Wrong authoritative owner or scope; no mutation')
    l=s['limitedUses'][FEATURE]
    if l['ownerId']!=owner or l['sourceRef']!='wizard#/cards/60':
        raise ValueError('Wrong feature ledger owner/source')
    # Validate a whole published ledger; never heal a partially committed recovery by repaying.
    for rid,link in l['roundUses'].items():
        rec=l['sourceSettlements'].get(link['settlementId'])
        if link['state']!='spent' or not rec or rec['status']!='awarded' or rec['roundId']!=rid or rec['creditedRP']!=1:
            raise ValueError('Incomplete or inconsistent atomic round/source receipt')
    for k,rec in l['sourceSettlements'].items():
        if k!=stable_key(rec['scopeId'],rec['ownerId'],rec['counterCastId']):
            raise ValueError('Unstable source identity')
        if rec['status']=='awarded' and l['roundUses'].get(rec['roundId'],{}).get('settlementId')!=k:
            raise ValueError('Award missing its atomic round claim')
    key=stable_key(event['scopeId'],owner,event['counterCastId'])
    if key in l['sourceSettlements']:
        old=l['sourceSettlements'][key]
        for name in ['scopeId','ownerId','roundId','roundOrdinal','counterCastId','negatedCastId','nativeCounterSourceRef']:
            if old[name]!=event[name]:raise ValueError('Conflicting immutable source outcome')
        return s,{'status':'duplicate-source-no-mutation','creditedRP':0,'originalSettlementId':key}
    if event['roundId']!=ctx['roundId'] or event['roundOrdinal']!=ctx['ordinal']:
        return s,{'status':'unsettled-old-round-needs-original-transaction','creditedRP':0}
    q=event['qualification']
    qualified=(event.get('nativeCounterTransactionComplete') is True and q['featureActuallyAcquired']
               and q['ownActualCounterspell'] and q['successfullyNegated']
               and not q['companionCounter'] and not q['reflectedCounter'] and not q['copiedCounter'])
    if not qualified:return s,{'status':'native-source-not-qualified','creditedRP':0}
    common={'id':key,'featureId':FEATURE,'sourceRef':'wizard#/cards/60','status':'awarded',
            **{k:deepcopy(event[k]) for k in ['scopeId','ownerId','roundId','roundOrdinal','counterCastId','negatedCastId','nativeCounterSourceRef','originalResolutionEventId','settledAt','qualification']},
            'requestedRP':1,'rpBeforeRecovery':s['rp'],'normalMaxRP':s['maxRP'],
            'creditedRP':0,'rpAfterRecovery':s['rp'],
            'frequencyDisposition':'spent; terminal source settlement and round pointer atomically committed with RP',
            'otherBudgetMutation':'none; native counter payment/Reaction/recharge/history already belongs to the counter transaction'}
    if event['roundId'] in l['roundUses']:
        common['status']='no-award-round-already-spent'
        common['frequencyDisposition']='existing round use retained; this distinct source receives no recovery'
        common['roundWinnerSettlementId']=l['roundUses'][event['roundId']]['settlementId']
        l['sourceSettlements'][key]=common
        return s,{'status':common['status'],'creditedRP':0}
    if not q['recoveryPermitted']:
        return s,{'status':'external-recovery-prohibition-no-award-projection','creditedRP':0,
                  'zeroAwardFrequencyPolicySelected':False}
    if not (0<=s['rp']<=s['maxRP']):raise ValueError('Invalid RP state')
    amount=min(1,s['maxRP']-s['rp'])
    if amount==0:
        return s,{'status':'normal-maximum-no-award-projection','creditedRP':0,
                  'zeroAwardFrequencyPolicySelected':False}
    common['creditedRP']=amount;common['rpAfterRecovery']=s['rp']+amount
    l['roundUses'][event['roundId']]={'state':'spent','settlementId':key}
    l['sourceSettlements'][key]=common;s['rp']+=amount
    return s,{'status':'awarded','creditedRP':amount,'settlementId':key}


def run(root):
    m=json.loads((root/'MODEL.json').read_bytes())
    with ZipFile(root/'input'/RETURN01) as z:old=json.loads(z.read('MODEL.json'))
    cases=[];assertions=[]
    def check(name,condition):
        assertions.append({'check':name,'pass':bool(condition)})
        if not condition:raise AssertionError(name)
    def record(name,before,event,after,result,premise,expected):
        cases.append({'id':name,'scope':'isolated reward/receipt diagnostic, not native casting or game runtime',
                      'premise':premise,'before':deepcopy(before),'sourceOutcome':deepcopy(event),
                      'after':deepcopy(after),'result':deepcopy(result),'expected':expected})
    pairs=[(4,2,0,'E','Counter1'),(5,0,1,'B','ClassCounter')]
    data={}
    for ci,bi,ti,owner,cid in pairs:
        newb=m['currentVectors'][ci]['independentBranches'][bi];oldb=old['currentVectors'][ci]['independentBranches'][bi]
        a=newb['timeline'][ti]['after'];before=newb['timeline'][ti]['before'];key=stable_key(a['numberedRoundContext']['scopeId'],owner,cid)
        l=a['actors'][owner]['limitedUses'][FEATURE];r=l['sourceSettlements'][key]
        missing=FEATURE not in oldb['timeline'][ti]['after']['actors'][owner]['limitedUses']
        check(newb['id']+' original explicit receipt absent',missing)
        paid=extract_state(a,owner);paid['rp']=r['rpBeforeRecovery'];paid['limitedUses'][FEATURE]=deepcopy(before['actors'][owner]['limitedUses'][FEATURE])
        event=event_from_receipt(r);paidBefore=deepcopy(paid)
        out,res=settle_positive_or_spent_round(paid,event);expected=extract_state(a,owner)
        check(newb['id']+' exact positive reward projection',out==expected)
        check(newb['id']+' pure input preserved',paid==paidBefore)
        for k in ['action','reaction','recharge']:
            check(newb['id']+' no reward '+k+' mutation',paid[k]==out[k])
        cost=a['castRecords'][cid]['quote']['total']
        check(newb['id']+' native payment distinct',before['actors'][owner]['rp']-cost==paid['rp'])
        check(newb['id']+' exact1 actual recovery',out['rp']-paid['rp']==1 and out['rp']<=out['maxRP'])
        check(newb['id']+' exact final full state retained',a==newb['finalState'])
        record(newb['id']+'-POSITIVE',paid,event,out,res,
               {'completeOriginalCase':f'AFFECTED_CASES.json#/cases/{len(data)}/completeBefore',
                'completeCorrectedCase':f'AFFECTED_CASES.json#/cases/{len(data)}/completeAfter',
                'nativePayment':{'beforeRP':before['actors'][owner]['rp'],'cost':cost,'afterPaymentRP':paid['rp']},
                'projectionBoundary':'Counter payment, Reaction spending, native success and other native effects are supplied complete case facts. Only the withheld1RP and its new receipt are recomputed.'},
               {'creditedRP':1,'afterRP':expected['rp'],'allOtherProjectionFieldsExact':True})
        data[owner]=(paid,event,out)
        for label,start,ev in [('DUPLICATE',out,event),('RENAMED-CALLBACK',out,dict(event,deliveryId='different-delivery')),
                               ('SAVE-RELOAD',json.loads(json.dumps(out)),dict(event,deliveryId='reload-delivery'))]:
            end,result=settle_positive_or_spent_round(start,ev)
            check(newb['id']+'/'+label+' no mutation',end==start)
            check(newb['id']+'/'+label+' no credit',result['creditedRP']==0)
            record(newb['id']+'/'+label,start,ev,end,result,'Replay of same immutable completed source; no new Reaction or source event.',{'exactNoMutation':True})
        newround=deepcopy(out);ctx=newround['numberedRoundContext'];ctx.update(roundId=ctx['scopeId']+':round:2',ordinal=2,startMarker=6,nextBoundaryMarker=12)
        nr,res2=settle_positive_or_spent_round(newround,event)
        check(newb['id']+' old source after round boundary no credit',nr==newround and res2['creditedRP']==0)
        check(newb['id']+' boundary grants no Reaction',nr['reaction'] is False)
        record(newb['id']+'/OLD-SOURCE-NEXT-ROUND',newround,event,nr,res2,'Only the supplied numbered-round marker changes; no own-turn START or Reaction refresh is run.',{'exactNoMutation':True})
    paid,event,first=data['E']
    # Genuine ordinary-Reaction refresh at E's first regular start2 is separate from numbered round1.
    refreshed=deepcopy(first);refreshed['reaction']=True;refreshed['action']=True;refreshed['recharge']['wizard.base.counterspell']=1
    after,res=settle_positive_or_spent_round(refreshed,event)
    check('own START does not refresh Feedback',after==refreshed and after['limitedUses'][FEATURE]['roundUses'])
    check('class recharge not bypassed by START',after['recharge']['wizard.base.counterspell']==1)
    record('OWN-START-REACTION-NOT-FEEDBACK',refreshed,event,after,res,
           'Actual E regular START2 supplies ordinary Reaction refresh and one recharge tick2→1; not an extra turn. Replayed Counter1 still does nothing.',{'reactionStillAvailable':True,'FeedbackRound1StillSpent':True,'classCounterNotYetReady':True})
    # A distinct genuine native counter is stipulated AFTER payment, not manufactured by the award helper.
    second=deepcopy(refreshed);second['rp']-=5;second['reaction']=False
    ev2=deepcopy(event);ev2.update(counterCastId='DiagnosticOrdinaryCounter2',negatedCastId='DiagnosticPendingSpell2',nativeCounterSourceRef='catalog#/spells/38/operational',originalResolutionEventId='diagnostic:second-native-counter',settledAt=3.2,deliveryId='new-delivery')
    secondout,res2=settle_positive_or_spent_round(second,ev2)
    check('distinct same-round actual counter pays5 and earns0',second['rp']==57 and secondout['rp']==57 and res2['creditedRP']==0)
    check('same-round new counter does not grant Reaction',secondout['reaction'] is False)
    check('same-round winner unchanged',secondout['limitedUses'][FEATURE]['roundUses']==first['limitedUses'][FEATURE]['roundUses'])
    check('same-round second source terminal',secondout['limitedUses'][FEATURE]['sourceSettlements'][stable_key(ev2['scopeId'],'E',ev2['counterCastId'])]['status']=='no-award-round-already-spent')
    record('SECOND-SOURCE-SAME-ROUND',second,ev2,secondout,res2,
           {'status':'CONDITIONAL_NATIVE_TRANSACTION_INPUT',
            'actualRequiredProvider':'Wizard ordinary Counterspell catalog#/spells/38; rank3/base5, actual prepared matrix, V/S/F, genuine perceived pending cast/range/LoE and actual successful native check. Not a class Counterspell while recharge1.',
            'preparationQualification':'W17-Conj already owns counterspell in its complete book but has not prepared it in the main fixture. This independent comparison requires actual prior preparation (16 matrices would fit the actual limit23); no instant acquisition/preparation is supplied.',
            'reactionQualification':'The real first regular START2, not the receipt or a numbered boundary, can refresh E\'s original Reaction. The full native second-counter opportunity and all cadence/hooks are external conditional inputs here.',
            'nativePayment':'62→57 after its actual undiscounted5RP fee; source-native histories and RNG are not implemented by this reward-only projection.'},
           {'afterRP':57,'secondFeedbackCredit':0})
    again,rr=settle_positive_or_spent_round(json.loads(json.dumps(secondout)),ev2)
    check('second source save/reload no award replay',again==secondout)
    record('SECOND-SOURCE-RELOAD',secondout,ev2,again,rr,'Reload of no-award terminal source receipt; its original round winner persists.',{'exactNoMutation':True})
    # The new numbered round does not itself ready the native Counterspell or Reaction.
    boundary=deepcopy(secondout);ctx=boundary['numberedRoundContext'];ctx.update(roundId=ctx['scopeId']+':round:2',ordinal=2,startMarker=6,nextBoundaryMarker=12)
    bo,br=settle_positive_or_spent_round(boundary,ev2)
    check('old no-award source cannot be cashed next round',bo==boundary and br['creditedRP']==0)
    record('OLD-DENIED-SOURCE-NEXT-ROUND',boundary,ev2,bo,br,'Old same-round-denied source stays terminal even though round2 has no credited use.',{'exactNoMutation':True})
    # At actual regular START8 class recharge1→0 and Reaction refresh can occur; a later native successful class counter is required.
    nextpaid=deepcopy(boundary);nextpaid['rp']-=3;nextpaid['reaction']=False;nextpaid['action']=True;nextpaid['recharge']['wizard.base.counterspell']=2
    ev3=deepcopy(event);ev3.update(roundId=ctx['roundId'],roundOrdinal=2,counterCastId='DiagnosticNativeCounter3',negatedCastId='DiagnosticPendingSpell3',originalResolutionEventId='diagnostic:new-round-success',settledAt=9.2)
    nout,nres=settle_positive_or_spent_round(nextpaid,ev3)
    check('new round distinct qualified counter credit1',nextpaid['rp']==54 and nout['rp']==55 and nres['creditedRP']==1)
    check('both historical round spends retained',len(nout['limitedUses'][FEATURE]['roundUses'])==2)
    check('new native event no free Reaction',nout['reaction'] is False and nout['recharge']==nextpaid['recharge'])
    record('NEW-ROUND-NEW-QUALIFIED-SOURCE',nextpaid,ev3,nout,nres,
           {'status':'CONDITIONAL_NATIVE_TRANSACTION_INPUT','clock':'Numbered boundary6 alone refreshes neither Reaction nor class recharge. Actual regular E START8 can tick recharge1→0 and refresh Reaction, after START2 already ticked2→1.',
            'nativeCounter':'A genuine later pending spell/successful class Counterspell at9.2 is required. No pending opponent or native cast execution is manufactured here. Actual fee3 is supplied after prior Matrix Efficiency expiry3;57→54; class use sets recharge2 and spends real Reaction. Other native history/RNG must be resolved by their existing provider.'},
           {'afterRP':55,'newCredit':1,'retainedRoundCount':2})
    for label,start,ev in [('EXTRA-TURN',first,event),('FIELD-EXIT-REENTRY',first,event),('CALLBACK-NEW-ID',first,dict(event,deliveryId='another-id'))]:
        out,res=settle_positive_or_spent_round(start,ev);check(label+' cannot reset receipt',out==start)
        record(label,start,ev,out,res,'No real round advance or new source-use; receipt persists. Field/recharge behavior is not rerun.',{'exactNoMutation':True})
    # Actual native qualification/exclusion predicates, negative projections only.
    for field,value,label in [('featureActuallyAcquired',False,'UNACQUIRED'),('ownActualCounterspell',False,'DISPEL-OR-ABSORPTION'),('successfullyNegated',False,'FAILED-NATIVE-COUNTER'),('companionCounter',True,'COMPANION'),('reflectedCounter',True,'REFLECTED'),('copiedCounter',True,'COPIED'),('recoveryPermitted',False,'RECOVERY-PROHIBITED')]:
        ev=deepcopy(event);ev['qualification'][field]=value;out,res=settle_positive_or_spent_round(paid,ev)
        check(label+' zero credit',res['creditedRP']==0 and out==paid)
        record(label,paid,ev,out,res,'Supplied actual source predicate; no source or prohibition is newly granted. This does not select an unused zero-award frequency-consumption convention.',{'creditedRP':0,'noOtherMutation':True})
    notcomplete=deepcopy(event);notcomplete['nativeCounterTransactionComplete']=False
    out,res=settle_positive_or_spent_round(paid,notcomplete);check('unresolved counter is not success',out==paid and res['creditedRP']==0)
    record('COUNTER-NOT-COMPLETED',paid,notcomplete,out,res,'A callback is not the actual native outcome.',{'creditedRP':0})
    atmax=deepcopy(paid);atmax['rp']=atmax['maxRP'];out,res=settle_positive_or_spent_round(atmax,event)
    check('normal maximum obeyed',out['rp']==64 and res['creditedRP']==0)
    record('POOL-ALREADY-MAXIMUM',atmax,event,out,res,'Read-only cap projection; zero-credit frequency consumption is not selected in this follow-through.',{'creditedRP':0,'noOverflow':True})
    missing=deepcopy(first);missing['limitedUses'][FEATURE]['sourceSettlements']={}
    errors=[('PARTIAL-ATOMIC-RECEIPT',missing,event),('WRONG-OWNER',paid,dict(event,ownerId='other')),('WRONG-SCOPE',paid,dict(event,scopeId='other'))]
    conflict=deepcopy(event);conflict['negatedCastId']='not-the-original-target';errors.append(('SOURCE-IDENTITY-CONFLICT',first,conflict))
    for label,start,ev in errors:
        snapshot=deepcopy(start)
        try:settle_positive_or_spent_round(start,ev)
        except ValueError as e:result={'status':'rejected-invalid-receipt-input','message':str(e),'creditedRP':0}
        else:raise AssertionError(label+' not rejected')
        check(label+' original input unchanged',start==snapshot)
        record(label,start,ev,start,result,'Invalid evidence cannot authorize another RP; recovery/storage implementation is not supplied.',{'noMutation':True,'rejected':True})
    # Source-affiliation stability and no coupling to Counterpulse.
    bp,be,ba=data['B'];check('Counterpulse key preserved separately',ba['limitedUses']['counterpulse-round1']=='spent')
    check('two feature namespaces distinct',FEATURE in ba['limitedUses'] and 'counterpulse-round1' in ba['limitedUses'])
    check('awards remain 1 under Supreme',ba['rp']-bp['rp']==1)
    return {'id':'RF9-FEEDBACK-ISOLATED-DIAGNOSTICS-02','scope':'New isolated finite data/receipt diagnostics only. No downloaded/project/game modules imported or executed.',
            'caseCount':len(cases),'assertionCount':len(assertions),'failures':sum(not a['pass'] for a in assertions),
            'cases':cases,'assertions':assertions,
            'limits':['Native counter checks, target spells, reaction-source eligibility, cadence, scheduler and cost quoting are supplied inputs, not implementations.',
                      'Positive main receipts are exact full-case projections. The two additional native-counter opportunities are expressly conditional, not new providers.',
                      'Negative recovery/cap projections prove nonaward, not a new unused-token consumption policy.',
                      'JSON roundtrip is an isolated persistence diagnostic, not runtime save/load/crash-recovery certification.']}

def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--report',type=Path);args=p.parse_args()
    result=run(args.root);b=encode(result)
    if args.report:
        if args.report.exists():raise SystemExit('Refusing to overwrite existing diagnostic evidence')
        args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_bytes(b)
    print(json.dumps({'caseCount':result['caseCount'],'assertionCount':result['assertionCount'],'failures':result['failures'],'reportSHA256':hashlib.sha256(b).hexdigest()}))
if __name__=='__main__':main()
