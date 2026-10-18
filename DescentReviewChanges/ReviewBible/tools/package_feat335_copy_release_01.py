"""Freeze the agreed-rule implementation and explicitly bounded test evidence."""
import ast,json,zipfile
from datetime import datetime,timezone
from pathlib import Path
from apply_di7_ap_as_01 import G,R,A,info,encoded


def main():
    root=A/'feat335-copy-release-integration-01'
    progress=A/'FEAT335_COPY_RELEASE_01_PROGRESS.json'
    prep=A/'FEAT335_COPY_RELEASE_01_PREPARATION.json'
    zp=A/'DD_Feat335_Copy_Release_Integration_01.zip'
    request=A/'FEAT335_COPY_RELEASE_01_GPT_UPDATE.txt'
    assert not any(p.exists() for p in [root,progress,prep,zp,request])
    report_path=A/'FEAT335_COPY_RELEASE_01_CHECK.json';report=json.loads(report_path.read_bytes())
    assert report['status']=='pass' and report['checks']==136 and not report['failures']
    sources={b['path']:b for b in report['sourceBindings']}
    def bind(p):sources[p.relative_to(G).as_posix()]=info(p)
    for p in [report_path,A/'FEAT335_COPY_RELEASE_SOURCE_01_RECEIVED_DECISION.json',Path(__file__)]:bind(p)
    # Complete recursively reachable local Python imports, without executing
    # one-shot authoring scripts or silently rewriting their frozen evidence.
    pending=[G/b['path'] for b in sources.values() if b['path'].endswith('.py')];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p)
        for node in ast.walk(ast.parse(p.read_text('utf8'))):
            names=[node.module] if isinstance(node,ast.ImportFrom) else [x.name for x in node.names] if isinstance(node,ast.Import) else []
            for name in names:
                if not name:continue
                dep=R/'tools'/(name.split('.')[0]+'.py')
                if dep.exists():bind(dep);pending.append(dep)
    status={'id':'FEAT335-COPY-RELEASE-INTEGRATION-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
        'status':'IMPLEMENTED_BOUNDED_AGREED_RULES; GPT_UPDATE_PREPARED_UNSENT',
        'authority':info(A/'feat335-copy-release-source-addendum-01/FEAT335_COPY_RELEASE_SOURCE_ADDENDUM_01.json'),
        'actualDecisionReceipt':info(A/'FEAT335_COPY_RELEASE_SOURCE_01_RECEIVED_DECISION.json'),
        'implementation':info(R/'tools/feat335_copy_release.py'),'validation':info(report_path),
        'validationScope':report['scope'],'acceptanceCoverage':report['acceptanceCoverage'],
        'counts':{'checks':136,'conditionalPaidHistories':19,'copyProfiles':7,'acceptanceRowsTracked':13,'openActualClassProviderRows':2},
        'openWork':['Recipient damage/healing/buffer/control/movement payloads and real world clocks.',
        'Full Shaman and Mirrorsage qualification and class shared-release allowance integration.',
        'Full Ready payment/action/trigger/Reaction/expiry transaction; concentration boundary alone is implemented.',
        'Actual price modifiers, world suppression/dispels and executable game-engine integration.'],
        'queuedSourceIssue':{'id':'COPY-READY-ALLOWANCE-01','status':'Question for actual GPT; no new rule selected',
        'question':'FS-08 casts and pays Ready at preparation, while SUP-07 caps one feat-copy release per owner per numbered round and Mimicry consumes a failed/countered release. For a held feat-copy prepared in round N and released in N+1, identify an existing exact ruling or specify when the owner-round allowance (and an actually owned Mirrorsage shared allowance) is checked/reserved/spent, including countered preparation, failed/lost hold and a competing direct release. Do not infer a new timing from the lifecycle-only adapter.',
        'context':'Direct Action commitment reserves its round; Ready is deliberately not accepted by that adapter. Concentration-only tests begin from an already-paid preparation premise.'},
        'limits':report['limits'],'newRuleAdoptions':0,'sourceInformationDeleted':0,'fullFeatExactApproved':False,
        'runtimeApproved':False,'humanBalanceApproved':False,'wholeGameComplete':False}
    progress.write_bytes(encoded(status));bind(progress)
    request.write_text('Progress update for actual GPT after resuming the Illusion14 review: I implemented the previously accepted CRS-01..03 copy-release rules without new design decisions. The complete attached archive includes the original decision, exact source files, Python implementation and136 passing checks/19 conditional paid histories. Direct Action release connects real paid Echo/Mimicry/Adaptation acquisition and captured components to existing RP, shared chronological history, current provider checks, consumed permissions, owner-round allowance and canonical concentration. All7 profiles cross this boundary. Ready concentration is tested separately from already-paid preparation, not a complete Ready transaction. Shaman/Mirrorsage provider integration, recipient payloads, world timing and priced modifiers remain open. No source card, feat approval or game-wide gate was promoted. Please inspect the full files when this cohort is reached, particularly COPY-READY-ALLOWANCE-01 in the progress record: identify an existing exact timing ruling or confer on the missing Ready/shared-release allowance case before we implement it. Do not interrupt or replace the outstanding full Illusion14 conference merely to acknowledge this progress.\n',encoding='utf8',newline='\n');bind(request)
    root.mkdir();checks=[]
    for b in sources.values():
        p=G/b['path'];assert info(p)==b,b['path']
        dst=root/'sources'/b['path'];dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(p.read_bytes())
        assert dst.read_bytes()==p.read_bytes();checks.append({'source':b,'bytesVerified':True})
    (root/'MANIFEST.json').write_bytes(encoded({'progress':info(progress),'sources':list(sources.values()),'sourceCount':len(sources),'checks':checks,'newRuleAdoptions':0,'scope':report['scope']}))
    with zipfile.ZipFile(zp,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        z.write(progress,'PROGRESS.json')
        for p in root.rglob('*'):
            if p.is_file():z.write(p,p.relative_to(root).as_posix())
    with zipfile.ZipFile(zp) as z:
        assert z.testzip() is None
        for b in sources.values():assert z.read('sources/'+b['path'])==(G/b['path']).read_bytes()
    prep.write_bytes(encoded({'archive':info(zp),'progress':info(progress),'request':info(request),'manifest':info(root/'MANIFEST.json'),'sourceCount':len(sources),'allArchivedBytesVerified':True,'status':'Prepared UNSENT for actual GPT; no new decision or approval inferred.'}))
    print(json.dumps({'archive':info(zp),'sources':len(sources),'newRuleAdoptions':0}))


if __name__=='__main__':main()
