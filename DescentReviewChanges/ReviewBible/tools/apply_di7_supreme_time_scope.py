"""Apply exact GPT historical-scope insertion without replacing prior revisions."""
from copy import deepcopy
from datetime import datetime,timezone
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded,node


def read(p): return json.loads(p.read_bytes())


def main():
    receipt=A/'DI7_SUPREME_TIME_SCOPE_RECEIVED.json'; delta=A/'DI7_SUPREME_TIME_SCOPE_DERIVED_OPERATIONS.json'
    preservation=A/'source-before-di7-supreme-time-scope'
    assert all(not p.exists() for p in [receipt,delta,preservation])
    insertion=(A/'DI7_SUPREME_TIME_SCOPE_INSERTION.txt').read_text(encoding='utf-8')
    dom=(A/'DI7_SUPREME_TIME_SCOPE_RECEIVED_DOM.txt').read_text(encoding='utf-8')
    assert 'DI7-SUPREME-TIME-SCOPE-01 — controlling source addendum' in dom and 'Response complete' in dom and 'button "Stop"' not in dom
    assert insertion.startswith('NEW unresolved temporal applicability:') and len(insertion.split('\n\n'))==4
    for paragraph in insertion.split('\n\n'):
        if paragraph.startswith('NEW '): paragraph=paragraph.split(': ',1)[1]
        assert paragraph in dom
    now=datetime.now(timezone.utc).isoformat()
    receipt.write_bytes(encoded({'id':'DI7-SUPREME-TIME-SCOPE-01','recordedAtUtc':now,'status':'terminal-source-addendum-received',
        'question':info(A/'DI7_SUPREME_TIME_SCOPE_QUESTION.txt'),'sentProof':info(A/'DI7_SUPREME_TIME_SCOPE_SENT.png'),
        'responseDom':info(A/'DI7_SUPREME_TIME_SCOPE_RECEIVED_DOM.txt'),'visibleProof':info(A/'DI7_SUPREME_TIME_SCOPE_RECEIVED.png'),
        'exactInsertion':info(A/'DI7_SUPREME_TIME_SCOPE_INSERTION.txt'),
        'classification':'KEEP actual precision, native scopes, identity and independently readable facts. NEW unresolved temporal applicability and partial-history public projection.',
        'newRuleAdoptions':2,'scope':'Supreme Sight historical query only; no generic protection grant or native-scope expansion.',
        'reviewerDidNotRerunTests':True,'replyReceived':True,'pendingResponse':False,'exactCardsApproved':False,'full49Fulfilled':False,'pushed':False,'cosmologyReviewed':False}))
    pubpath=R/'data/public/spell_candidates/divination_rank7_exact_01.json'; intpath=R/'data/director/spell_candidates/divination_rank7_exact_01.json'
    exppath=R/'data/playtest/spell_candidates/divination_rank7_exact_01_expectations.json'; mdpath=R/'docs/spells/candidates/DIVINATION_RANK7_EXACT_01.md'
    paths=[pubpath,intpath,exppath,mdpath]; before={p:p.read_bytes() for p in paths}
    pub=read(pubpath); internal=read(intpath); exp=read(exppath)
    assert internal['completePublicEnvelope']==pub and internal['finiteExpectations']==exp and internal['publicEnvelopeBinding']==info(pubpath)
    i=next(i for i,c in enumerate(pub['cards']) if c['id']=='resonance-sight-supreme')
    old=pub['cards'][i]['operationalCandidate']['completeProcedure']
    anchor='Supply all independently useful readable information, not only public facts or a single trace.'
    assert old.count(anchor)==1; new=old.replace(anchor,anchor+'\n\n'+insertion,1)
    addenda=pub['sourceDirectionAddenda']+[{'id':'DI7-SUPREME-TIME-SCOPE-01','affectedSpellId':'resonance-sight-supreme','authority':info(receipt),
        'scope':'Unresolved applicability and partial-history positive assertions with uniform non-diagnostic notice.','exactApproval':False}]
    outcomes=[
        ('A-UNRESOLVED','Uncertain actual occurrence100–200 and genuine existence protection150–175 with unresolved relation: no attributable occurrence record or diagnostic; other readable history survives; no invented timestamp or subtracted range.'),
        ('A-OUTSIDE','Additional actual-world relation establishes occurrence outside protected span: eligible at genuinely established public precision, without automatically inventing an exact date.'),
        ('A-INSIDE','Additional actual-world relation establishes occurrence inside protected span: apply only the native covered facts, without broadening to unrelated history.'),
        ('A-FIELD','Existence independently readable but one field has unresolved applicability: supported permitted fields survive; omit unresolved field without announcing its status.'),
        ('B-CONTINUOUS','One actual continuous underlying effect100–200, trace protection150–175: retain one internal identity, publish readable genuine transitions/properties, no fabricated150/175 transition, certified continuous outer interval, redaction segment or protection-derived coverage gap.'),
        ('B-NONINTERFERENCE','Protected interior details differ but permitted exterior facts match: caster-facing positive assertions/presentation match with no internal count, sequencing or explanation leak.'),
        ('C-CURRENT-ONLY','Current-only defense leaves independently readable old history unchanged unless another actual applicable source governs it.'),
        ('REPEAT','Unchanged equivalent paid inquiry returns same overlapping readable facts; repetition neither resolves uncertainty nor creates diagnostic variants.')]
    supplements=exp['supplementalSourceExpectations']+[{'id':'DI7-SUPREME-TIME-SCOPE-01','authority':info(receipt),
        'evidenceKind':'Authored source expectations; execution evidence separate.','original49Unchanged':True,
        'variants':[{'id':'DI7-SUPREME-TIME-'+key,'expected':value} for key,value in outcomes]}]
    changes=[]
    def change(path,obj,ops):
        result=deepcopy(obj)
        for op in ops:
            parent,key=node(result,op['pointer']); assert parent[key]==op['old']; parent[key]=deepcopy(op['replacement'])
        inverse=deepcopy(result)
        for op in reversed(ops):
            parent,key=node(inverse,op['pointer']); assert parent[key]==op['replacement']; parent[key]=deepcopy(op['old'])
        assert encoded(inverse)==before[path]; changes.append((path,encoded(result),ops)); return result
    ops=[{'pointer':f'/cards/{i}/operationalCandidate/completeProcedure','old':old,'replacement':new},
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
    delta.write_bytes(encoded({'id':'DI7-SUPREME-TIME-SCOPE-01','recordedAtUtc':now,'authority':info(receipt),'changes':done,
        'allOtherCandidateContentUnchanged':True,'original49AndPriorSupplementsUnchanged':True,'newSupplementalExpectations':8,
        'allCostAccessApprovalSelectionFieldsUnchanged':True,'newRuleAdoptions':2,'sourceInformationDeleted':0,'spellPromotions':0}))
    print(json.dumps({'receipt':info(receipt),'delta':info(delta),'changedActiveFiles':len(done),'newExpectations':8}))


if __name__=='__main__': main()
