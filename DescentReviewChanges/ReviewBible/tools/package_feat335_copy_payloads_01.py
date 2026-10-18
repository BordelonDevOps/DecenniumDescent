"""Freeze complete paid-copy recipient implementation and bounded evidence."""
from datetime import datetime,timezone
from pathlib import Path
import json,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded


def main():
    root=A/'feat335-copy-payloads-01';progress=A/'FEAT335_COPY_PAYLOADS_01_PROGRESS.json'
    prep=A/'FEAT335_COPY_PAYLOADS_01_PREPARATION.json';request=A/'FEAT335_COPY_PAYLOADS_01_GPT_UPDATE.txt'
    zp=A/'DD_Feat335_Copy_Payloads_01.zip'
    assert not any(p.exists() for p in [root,progress,prep,request,zp])
    report_path=A/'FEAT335_COPY_PAYLOADS_01_CHECK.json';report=json.loads(report_path.read_bytes())
    assert report['status']=='pass' and report['checks']==115 and not report['failures']
    bindings={b['path']:b for b in report['sourceBindings']}
    def bind(p):b=info(p);bindings[b['path']]=b;return b
    for p in [report_path,A/'FEAT335_COPY_RELEASE_SOURCE_01_RECEIVED_DECISION.json',A/'FEAT335_COPY_RELEASE_01_PREPARATION.json',Path(__file__)]:bind(p)
    record={'id':'FEAT335-COPY-PAYLOADS-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
        'status':'AGREED_RULE_IMPLEMENTATION; ACTUAL_GPT_PROGRESS_UPDATE_UNSENT',
        'previousIntegration':info(A/'FEAT335_COPY_RELEASE_01_PROGRESS.json'),
        'sourceAuthority':info(A/'feat335-copy-release-source-addendum-01/FEAT335_COPY_RELEASE_SOURCE_ADDENDUM_01.json'),
        'validation':info(report_path),'implementation':info(R/'tools/feat335_copy_payloads.py'),
        'counts':{'checks':115,'conditionalHistories':27,'profiles':7},'scope':report['scope'],
        'completedAtThisBoundary':['Bounded native Strike damage with ordinary hit/critical/Wound/death consequences but no extra copied critical dice.',
        'One bounded Burst roll and independent original-target saves/defenses, no fourth or replacement recipient.',
        'Mend uses canonical ordinary HP recovery, actual reductions/prohibitions and Critical ceiling, with no Wound cure or conversion.',
        'Ward enters the single shared BufferLedger; rejected offers retain costs; concentration cleanup and exact supplied deadline remove the same grant.',
        'Hindrance participates in strongest-slow arbitration and blocks new Reactions until its source-qualified endpoint.',
        'Current Shield-derived Boon gives one family-wide AC point across owners, with real concentration cleanup.',
        'Current Mist Step-derived Step moves the existing body once after current supplied destination predicates; no passenger/body/resource copy.',
        'Late unsupported interceptors and next-healing consumption sources require their own integrations, rather than being silently ignored.'],
        'remainingWork':report['limits'],
        'queuedReadyQuestionUnchanged':{'source':info(A/'FEAT335_COPY_RELEASE_01_PROGRESS.json'),'id':'COPY-READY-ALLOWANCE-01','newDecisionSelected':False},
        'newRuleAdoptions':0,'sourceInformationDeleted':0,'runtimeApproved':False,'fullFeatExactApproved':False,
        'humanBalanceApproved':False,'wholeGameComplete':False}
    progress.write_bytes(encoded(record));bind(progress)
    request.write_text('Actual GPT progress update, to be delivered with the complete archive after the current Illusion/Companion review sequence: previously accepted SUP-07/CRS copy effects now connect to real canonical HP/Wounds/death, the single buffer ledger, healing limits, source-owned slow/Reaction/AC records and same-body personal teleport.115 checks across27 conditional paid histories pass. The attached complete sources/code/report preserve exact operands and intermediate/final states. Full scene geometry, runtime, Shaman/Mirrorsage providers, Ready transactions, price modifiers, general interceptors and other listed limits remain open. Current Boon is the actual Shield AC component; next-attack/save Boons and nonteleport Step still need authentic source adapters. COPY-READY-ALLOWANCE-01 remains an unanswered exact-source timing inquiry; no timing decision has been implemented. No source cards,335-feat approval or whole-game gate were promoted. Continue the full Illusion14 conference first; this is an implementation update, not a replacement conference or requested approval of unseen files.\n',encoding='utf8',newline='\n');bind(request)
    root.mkdir()
    for b in bindings.values():
        p=G/b['path'];assert info(p)==b
        dst=root/'sources'/b['path'];dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(p.read_bytes())
        assert dst.read_bytes()==p.read_bytes()
    (root/'MANIFEST.json').write_bytes(encoded({'progress':info(progress),'sources':list(bindings.values()),'sourceCount':len(bindings),'allBytesVerified':True,'newRuleAdoptions':0}))
    with zipfile.ZipFile(zp,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        z.write(progress,'PROGRESS.json')
        for p in root.rglob('*'):
            if p.is_file():z.write(p,p.relative_to(root).as_posix())
    with zipfile.ZipFile(zp) as z:
        assert z.testzip() is None
        for b in bindings.values():assert z.read('sources/'+b['path'])==(G/b['path']).read_bytes()
    prep.write_bytes(encoded({'archive':info(zp),'progress':info(progress),'request':info(request),'manifest':info(root/'MANIFEST.json'),'sourceCount':len(bindings),'allArchivedBytesVerified':True,'status':'Prepared UNSENT; no new rule or broader approval.'}))
    print(json.dumps({'archive':info(zp),'sources':len(bindings),'checks':115,'histories':27}))


if __name__=='__main__':main()
