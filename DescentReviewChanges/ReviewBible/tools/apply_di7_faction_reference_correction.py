"""Apply GPT's single-word targeting correction with preserved exact inverses."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded,node


def read(p): return json.loads(p.read_bytes())


def main():
    receipt=A/'DI7_FACTION_REFERENCE_RECEIVED.json'; delta=A/'DI7_FACTION_REFERENCE_DERIVED_OPERATIONS.json'
    preservation=A/'source-before-di7-faction-reference'
    assert all(not p.exists() for p in [receipt,delta,preservation])
    old='CORRECTION/explicit paid-reference boundary: public preflight validates the nominated visible creature, known faction and ordinary casting conditions; hidden membership, protected identification and the existence of readable activity are resolved only after legal payment.'
    new=old.replace('nominated visible creature','nominated perceived creature')
    dom=(A/'DI7_FACTION_REFERENCE_RECEIVED_DOM.txt').read_text(encoding='utf-8')
    assert 'DI7-FACTION-REFERENCE-01 — controlling wording correction' in dom and new in dom and 'Response complete' in dom and 'button "Stop"' not in dom
    now=datetime.now(timezone.utc).isoformat()
    receipt.write_bytes(encoded({'id':'DI7-FACTION-REFERENCE-01','recordedAtUtc':now,'status':'terminal-wording-correction-received',
        'question':info(A/'DI7_FACTION_REFERENCE_QUESTION.txt'),'sentProof':info(A/'DI7_FACTION_REFERENCE_SENT.png'),
        'responseDom':info(A/'DI7_FACTION_REFERENCE_RECEIVED_DOM.txt'),'visibleProof':info(A/'DI7_FACTION_REFERENCE_RECEIVED.png'),
        'classification':'CORRECTION visible to perceived in one sentence; KEEP existing perception and paid hidden-reference requirements. No new sense or sight requirement.',
        'exactOld':old,'exactReplacement':new,'reviewerDidNotRerunTests':True,'replyReceived':True,'pendingResponse':False,
        'newRuleAdoptions':0,'exactCardsApproved':False,'full49Fulfilled':False,'pushed':False,'cosmologyReviewed':False}))
    pubpath=R/'data/public/spell_candidates/divination_rank7_exact_01.json'
    intpath=R/'data/director/spell_candidates/divination_rank7_exact_01.json'
    exppath=R/'data/playtest/spell_candidates/divination_rank7_exact_01_expectations.json'
    mdpath=R/'docs/spells/candidates/DIVINATION_RANK7_EXACT_01.md'
    paths=[pubpath,intpath,exppath,mdpath]; before={p:p.read_bytes() for p in paths}
    pub=read(pubpath); internal=read(intpath); exp=read(exppath)
    assert internal['completePublicEnvelope']==pub and internal['finiteExpectations']==exp and internal['publicEnvelopeBinding']==info(pubpath)
    i=next(i for i,c in enumerate(pub['cards']) if c['id']=='faction-omniscience')
    original=pub['cards'][i]['operationalCandidate']['completeProcedure']; assert original.count(old)==1
    amended=original.replace(old,new,1)
    addenda=pub['sourceDirectionAddenda']+[{'id':'DI7-FACTION-REFERENCE-01','affectedSpellId':'faction-omniscience','authority':info(receipt),'scope':'One-word perceived-reference correction only.','exactApproval':False}]
    variants=[{'id':'DI7-FACTION-REF-A','expected':'Actually perceived but unseen local creature may qualify via an actual governing sense/permission, with existing120-foot range and line of effect. No new sense or barrier bypass.'},
        {'id':'DI7-FACTION-REF-B','expected':'Guessed unperceived creature fails before commitment/payment; no hidden membership oracle or paid-refund rule.'},
        {'id':'DI7-FACTION-REF-C-FALSE','expected':'Legal perceived reference with false actual membership pays normally then produces no faction feed or distinguishing diagnostic.'},
        {'id':'DI7-FACTION-REF-C-SCOPE','expected':'Legal perceived reference with protected membership is evaluated after payment under exact native protection scope, without bypass or blanket expansion; no refund or hidden-reason diagnostic.'}]
    supplements=exp['supplementalSourceExpectations']+[{'id':'DI7-FACTION-REFERENCE-01','authority':info(receipt),'evidenceKind':'Authored expected outcomes; execution evidence separate.','original49Unchanged':True,'variants':variants}]
    changes=[]
    def change(p,obj,ops):
        result=deepcopy(obj)
        for op in ops:
            parent,key=node(result,op['pointer']); assert parent[key]==op['old']; parent[key]=deepcopy(op['replacement'])
        inverse=deepcopy(result)
        for op in reversed(ops):
            parent,key=node(inverse,op['pointer']); assert parent[key]==op['replacement']; parent[key]=deepcopy(op['old'])
        assert encoded(inverse)==before[p]; changes.append((p,encoded(result),ops)); return result
    ops=[{'pointer':f'/cards/{i}/operationalCandidate/completeProcedure','old':original,'replacement':amended},
        {'pointer':'/sourceDirectionAddenda','old':pub['sourceDirectionAddenda'],'replacement':addenda}]
    pub=change(pubpath,pub,ops)
    expops=[{'pointer':'/supplementalSourceExpectations','old':exp['supplementalSourceExpectations'],'replacement':supplements}]
    exp=change(exppath,exp,expops)
    internal=change(intpath,internal,[*[{**op,'pointer':'/completePublicEnvelope'+op['pointer']} for op in ops],
        {'pointer':'/publicEnvelopeBinding','old':internal['publicEnvelopeBinding'],'replacement':info(pubpath,encoded(pub))},
        *[{**op,'pointer':'/finiteExpectations'+op['pointer']} for op in expops]])
    assert internal['completePublicEnvelope']==pub and internal['finiteExpectations']==exp
    md=mdpath.read_text(encoding='utf-8'); assert md.count(old)==1
    newmd=md.replace(old,new,1); assert newmd.replace(new,old,1).encode()==before[mdpath]
    changes.append((mdpath,newmd.encode(),[{'textReplace':True,'old':old,'replacement':new}]))
    preserved=[]
    for p in paths:
        dest=preservation/p.relative_to(G); dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(before[p]); assert dest.read_bytes()==before[p]
        preserved.append({**info(p),'preservedCopy':dest.relative_to(G).as_posix()})
    (preservation/'PRESERVATION_MANIFEST.json').write_bytes(encoded(preserved))
    done=[]
    for p,data,ops in changes:
        p.write_bytes(data); assert p.read_bytes()==data
        done.append({'before':next(x for x in preserved if x['path']==p.relative_to(G).as_posix()),'after':info(p),'operations':ops,'exactInverseBytesVerified':True})
    delta.write_bytes(encoded({'id':'DI7-FACTION-REFERENCE-01','recordedAtUtc':now,'authority':info(receipt),'changes':done,
        'allOtherCandidateContentUnchanged':True,'original49AndPriorSupplementsUnchanged':True,'newSupplementalExpectations':4,
        'allCostAccessApprovalSelectionFieldsUnchanged':True,'newRuleAdoptions':0,'sourceInformationDeleted':0,'spellPromotions':0}))
    print(json.dumps({'receipt':info(receipt),'delta':info(delta),'changedActiveFiles':len(done)}))


if __name__=='__main__': main()
