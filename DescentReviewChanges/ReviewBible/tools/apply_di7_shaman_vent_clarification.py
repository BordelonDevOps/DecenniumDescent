"""Add the exact shared Shaman interface note; retain all payload/class sources."""
from copy import deepcopy
from datetime import datetime,timezone
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded,node


def read(p): return json.loads(p.read_bytes())


def main():
    receipt=A/'DI7_SHAMAN_VENT_RECEIVED.json'; delta=A/'DI7_SHAMAN_VENT_DERIVED_OPERATIONS.json'
    preservation=A/'source-before-di7-shaman-vent'; note=R/'docs/spells/candidates/DI7_SHAMAN_CASTING_INTERFACE.md'
    assert all(not p.exists() for p in [receipt,delta,preservation,note])
    clarification=(A/'DI7_SHAMAN_VENT_CLARIFICATION.txt').read_text(encoding='utf-8')
    dom=(A/'DI7_SHAMAN_VENT_RECEIVED_DOM.txt').read_text(encoding='utf-8')
    assert 'DI7-SHAMAN-VENT-01 — KEEP the existing casting order' in dom and 'Response complete' in dom and 'button "Stop"' not in dom
    assert clarification.startswith('DI7-SHAMAN-VENT-01 — Shaman vent checkpoint.') and len(clarification.split('\n\n'))==5
    for i,p in enumerate(clarification.split('\n\n')):
        if i==0: p=p.split('checkpoint. ',1)[1]
        assert p in dom
    now=datetime.now(timezone.utc).isoformat()
    receipt.write_bytes(encoded({'id':'DI7-SHAMAN-VENT-01','recordedAtUtc':now,'status':'terminal-existing-source-clarification-received',
        'question':info(A/'DI7_SHAMAN_VENT_QUESTION.txt'),'sentProof':info(A/'DI7_SHAMAN_VENT_SENT.png'),
        'responseDom':info(A/'DI7_SHAMAN_VENT_RECEIVED_DOM.txt'),'visibleProof':info(A/'DI7_SHAMAN_VENT_RECEIVED.png'),
        'exactClarification':info(A/'DI7_SHAMAN_VENT_CLARIFICATION.txt'),
        'classification':'KEEP existing sequence: vent at step5 after step4 concentration displacement; no pre-commit aura snapshot. First qualifying cast occupies opportunity even at0; copied child excluded; Ready hold concentration matters.',
        'newRuleAdoptions':0,'reviewerDidNotRerunTests':True,'replyReceived':True,'pendingResponse':False,
        'exactCardsApproved':False,'full49Fulfilled':False,'pushed':False,'cosmologyReviewed':False}))
    pubpath=R/'data/public/spell_candidates/divination_rank7_exact_01.json'; intpath=R/'data/director/spell_candidates/divination_rank7_exact_01.json'
    exppath=R/'data/playtest/spell_candidates/divination_rank7_exact_01_expectations.json'; mdpath=R/'docs/spells/candidates/DIVINATION_RANK7_EXACT_01.md'
    paths=[pubpath,intpath,exppath,mdpath]; before={p:p.read_bytes() for p in paths}
    pub=read(pubpath); internal=read(intpath); exp=read(exppath)
    assert internal['completePublicEnvelope']==pub and internal['finiteExpectations']==exp and internal['publicEnvelopeBinding']==info(pubpath)
    addenda=pub['sourceDirectionAddenda']+[{'id':'DI7-SHAMAN-VENT-01','affectedInterface':'ordinary Shaman casting sequence and Fate route boundary',
        'authority':info(receipt),'scope':'Existing-source shared clarification; no payload or class-source rewrite.','exactApproval':False}]
    expected=[
        ('ORDINARY','Immediate nonconcentration ordinary DI7 inside own active aura with unused round opportunity: automatic generated-strain reduction1 minimum0; opportunity occupied.'),
        ('CONCENTRATION','Vision Quest/Purge ends shared totem concentration at step4; no active own aura at step5, no vent and no new occupancy of opportunity.'),
        ('OUTSIDE-INSIDE','Earlier ordinary cast outside own active aura does not spend opportunity; later otherwise legal qualifying cast inside same round spends it.'),
        ('ZERO','First qualifying rank0 cast with generated strain0 still occupies opportunity, removes no stored Dissonance and prevents later same-round vent.'),
        ('COUNTERED','Later counter does not refund the occupied opportunity, payment or chronological history, or restore displaced concentration.'),
        ('OVERLAP','Two own overlapping active totems yield one reduction and one shared opportunity, never one per totem.'),
        ('OTHER-OWNER','Only another Shaman aura contains caster: no vent and no consumption of this caster opportunity.'),
        ('FATE','Qualifying ordinary Fate outer receives reduction; fate-echo-copy child receives/occupies none. A concentration child ends incompatible totems without reversing outer benefit.'),
        ('READY','Readied Fate outer hold concentration displaces totem before preparation step5; no vent. Release grants no second outer checkpoint.')]
    supplements=exp['supplementalSourceExpectations']+[{'id':'DI7-SHAMAN-VENT-01','authority':info(receipt),
        'evidenceKind':'Source-derived authored expectations; execution evidence separate.','original49Unchanged':True,
        'variants':[{'id':'DI7-SHAMAN-VENT-'+k,'expected':v} for k,v in expected]}]
    changes=[]
    def change(p,obj,ops):
        result=deepcopy(obj)
        for op in ops:
            parent,key=node(result,op['pointer'])
            if op.get('add'): assert key not in parent
            else: assert parent[key]==op['old']
            parent[key]=deepcopy(op['replacement'])
        inverse=deepcopy(result)
        for op in reversed(ops):
            parent,key=node(inverse,op['pointer']); assert parent[key]==op['replacement']
            if op.get('add'): del parent[key]
            else: parent[key]=deepcopy(op['old'])
        assert encoded(inverse)==before[p]; changes.append((p,encoded(result),ops)); return result
    ops=[{'pointer':'/sharedOperatingRules/shamanCastingInterface','add':True,'replacement':clarification},
        {'pointer':'/sourceDirectionAddenda','old':pub['sourceDirectionAddenda'],'replacement':addenda}]
    pub=change(pubpath,pub,ops)
    expops=[{'pointer':'/supplementalSourceExpectations','old':exp['supplementalSourceExpectations'],'replacement':supplements}]
    exp=change(exppath,exp,expops)
    internal=change(intpath,internal,[*[{**op,'pointer':'/completePublicEnvelope'+op['pointer']} for op in ops],
        {'pointer':'/publicEnvelopeBinding','old':internal['publicEnvelopeBinding'],'replacement':info(pubpath,encoded(pub))},
        *[{**op,'pointer':'/finiteExpectations'+op['pointer']} for op in expops]])
    assert internal['completePublicEnvelope']==pub and internal['finiteExpectations']==exp
    md=mdpath.read_text(encoding='utf-8'); anchor='## Mass Revelation (mass-revelation)'; assert md.count(anchor)==1
    insertion='### shamanCastingInterface\n\n'+clarification+'\n\n'
    newmd=md.replace(anchor,insertion+anchor,1); assert newmd.replace(insertion+anchor,anchor,1).encode()==before[mdpath]
    changes.append((mdpath,newmd.encode(),[{'textReplace':True,'old':anchor,'replacement':insertion+anchor}]))
    preserved=[]
    for p in paths:
        dest=preservation/p.relative_to(G); dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(before[p]); assert dest.read_bytes()==before[p]
        preserved.append({**info(p),'preservedCopy':dest.relative_to(G).as_posix()})
    (preservation/'PRESERVATION_MANIFEST.json').write_bytes(encoded(preserved))
    done=[]
    for p,data,ops in changes:
        p.write_bytes(data); assert p.read_bytes()==data
        done.append({'before':next(x for x in preserved if x['path']==p.relative_to(G).as_posix()),'after':info(p),'operations':ops,'exactInverseBytesVerified':True})
    note.write_text('# DI7 Shaman casting interface\n\nKEEP / existing-source clarification. Source ruling: [DI7-SHAMAN-VENT-01](../../../../../docs/audit/2026-10-08/full-game/DI7_SHAMAN_VENT_RECEIVED.json).\n\n'+clarification+'\n\nThese source-derived expectations do not certify execution, exact seven-card acceptance or full runtime.\n',encoding='utf-8',newline='\n')
    delta.write_bytes(encoded({'id':'DI7-SHAMAN-VENT-01','recordedAtUtc':now,'authority':info(receipt),'changes':done,'newArtifacts':[info(note)],
        'allSevenPayloadsUnchanged':True,'classEngineAndCastingGuideOriginalsUnchanged':True,'original49AndPriorSupplementsUnchanged':True,
        'newSupplementalExpectations':9,'allCostAccessApprovalSelectionFieldsUnchanged':True,'newRuleAdoptions':0,'sourceInformationDeleted':0,'spellPromotions':0}))
    print(json.dumps({'receipt':info(receipt),'delta':info(delta),'changedActiveFiles':len(done),'newExpectations':9,'interfaceNote':info(note)}))


if __name__=='__main__': main()
