"""Read-only submission/guard/parity checks for the four-question Flora addendum.

Usage: python verify_flora_addendum.py /path/DD_FEAT335_Flora_Source_Check_01.zip
Run beside EXACT_FLORA_CORRECTIONS.json and SOURCE_BINDINGS.json.
Outputs deterministic JSON to stdout. Does not run the submitted Flora model,
modify an archive/repository, or execute a gameplay/companion/timing engine.
"""
import ast
import copy
import hashlib
import json
import sys
import zipfile
from pathlib import Path, PurePosixPath

def digest(b): return hashlib.sha256(b).hexdigest()

def main(archive):
    here=Path(__file__).resolve().parent
    binding=json.loads((here/'SOURCE_BINDINGS.json').read_text(encoding='utf-8'))
    patch=json.loads((here/'EXACT_FLORA_CORRECTIONS.json').read_text(encoding='utf-8'))
    results=[]
    def check(name,ok,detail=None):
        results.append({'id':name,'passed':bool(ok),'detail':detail})
        if not ok: raise AssertionError(name)
    blob=Path(archive).read_bytes()
    check('archive.size',len(blob)==binding['archiveBytes'])
    check('archive.sha256',digest(blob)==binding['archiveSha256'])
    with zipfile.ZipFile(archive) as z:
        names=z.namelist()
        check('archive.unique_paths',len(names)==len(set(names)))
        check('archive.safe_paths',all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts for n in names))
        check('archive.crc',z.testzip() is None)
        check('manifest.sha256',digest(z.read('PACKAGE_MANIFEST.json'))==binding['manifestSha256'])
        manifest=json.loads(z.read('PACKAGE_MANIFEST.json'))
        check('manifest.exact_payload_membership',set(manifest)==set(names)-{'PACKAGE_MANIFEST.json'})
        check('manifest.payload_count',len(manifest)==15)
        files={n:z.read(n) for n in names}
    for n,e in manifest.items():
        check('payload.bytes/'+n,len(files[n])==e['bytes'])
        check('payload.sha256/'+n,digest(files[n])==e['sha256'])
    base='DescentReviewChanges/ReviewBible/'
    candidate=base+'data/public/feat_candidates/exact_01/candidate.json'
    supplement=base+'data/public/feat_candidates/exact_01/supplements.json'
    contracts='docs/audit/2026-10-08/full-game/FEAT_EXACT_01_ACQUISITION_CONTRACTS.json'
    report_path='docs/audit/2026-10-08/full-game/FEAT335_FLORA_USE_CHECK.json'
    qual_path='docs/audit/2026-10-08/full-game/FEAT335_FLORA_USE_SCOPE_QUALIFICATION.json'
    docs={n:json.loads(files[n]) for n in [candidate,supplement,contracts,report_path,qual_path]}
    c,a=docs[candidate],docs[contracts]
    cm={x['id']:x for x in c['feats']};am={x['id']:x for x in a['records']}
    ids=['conjure_flora','trapcasting','verdant_bond']
    for fid in ids:
        check('submitted.full_procedure_mirrors/'+fid,cm[fid]['operationalRules']==cm[fid]['payloadOperational']==am[fid]['completeOperativeProcedure'])
        check('submitted.original_object_mirrors/'+fid,cm[fid]['sourceObject']==am[fid]['originalObject'])
        check('report.complete_contract_binding/'+fid,docs[report_path]['completeContracts'][fid]==am[fid])
    check('report.complete_flora_binding',docs[report_path]['completeFloraSupplement']==docs[supplement]['groups'][6]['value']['floraBody'])
    report=docs[report_path];qual=docs[qual_path]
    check('report.114_recorded_flags',len(report['results'])==report['checks']==qual['checks']==114 and all(x['passed'] for x in report['results']))
    check('report.23_recorded_histories',len(report['histories'])==qual['histories']==23)
    check('report.bound_qualification',qual['report']['sha256']==digest(files[report_path]) and qual['report']['bytes']==len(files[report_path]))
    check('report.four_open_source_questions',[x['id'] for x in qual['questions']]==['FLQ-01','FLQ-02','FLQ-03','FLQ-04'])
    check('report.explicit_unapproved_inference',qual['status']=='bounded-model-evidence-with-explicit-unapproved-inference' and 'does not approve' in qual['qualification'])
    # Local parsing and dependency inventory, not importing or executing those modules.
    localpy={PurePosixPath(p).stem:p for p in files if p.endswith('.py')}
    absent={}
    for mod,p in localpy.items():
        tree=ast.parse(files[p].decode('utf-8-sig'),filename=p)
        check('source.python_ast/'+mod,isinstance(tree,ast.Module))
        used=[n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and n.module and
              (n.module.startswith('feat') or n.module.startswith('validate_feat') or n.module=='core_playtest_rules')]
        absent[p]=sorted(set(m for m in used if m not in localpy))
    changed=copy.deepcopy(docs)
    def parent_at(root,pointer):
        parts=[x.replace('~1','/').replace('~0','~') for x in pointer.lstrip('/').split('/')]
        cur=root
        for token in parts[:-1]:cur=cur[int(token)] if isinstance(cur,list) else cur[token]
        return cur,parts[-1]
    check('amendment.ten_operations',len(patch['operations'])==10)
    for op in patch['operations']:
        check('amendment.source_binding/'+op['id'],digest(files[op['path']])==op['expectedSourceSha256'])
        par,key=parent_at(changed[op['path']],op['pointer'])
        check('amendment.exact_old_string/'+op['id'],par[key]==op['old'])
        parts=op['pointer'].split('/');g=op['identityGuard']
        check('amendment.record_identity/'+op['id'],changed[op['path']][parts[1]][int(parts[2])]['id']==g['id'])
        par[key]=op['replacement']
    nc,na=changed[candidate],changed[contracts]
    ncm={x['id']:x for x in nc['feats']};nam={x['id']:x for x in na['records']}
    for fid in ids:
        check('amended.full_procedure_mirrors/'+fid,ncm[fid]['operationalRules']==ncm[fid]['payloadOperational']==nam[fid]['completeOperativeProcedure'])
    check('amended.all_original_objects_unchanged',[x['sourceObject'] for x in nc['feats']]==[x['sourceObject'] for x in c['feats']] and [x['originalObject'] for x in na['records']]==[x['originalObject'] for x in a['records']])
    affected={'conjure_flora','trapcasting'}
    check('amended.other_333_candidates_unchanged',[x for x in nc['feats'] if x['id'] not in affected]==[x for x in c['feats'] if x['id'] not in affected])
    check('amended.other_333_contracts_unchanged',[x for x in na['records'] if x['id'] not in affected]==[x for x in a['records'] if x['id'] not in affected])
    for fid in sorted(affected):
        for before,after,exempt in [(cm[fid],ncm[fid],{'operationalRules','payloadOperational'}),(am[fid],nam[fid],{'completeOperativeProcedure'})]:
            check('amended.other_record_fields/'+fid+'/'+','.join(sorted(exempt)),{k:v for k,v in before.items() if k not in exempt}=={k:v for k,v in after.items() if k not in exempt})
    check('amended.top_level_flags_unchanged',{k:v for k,v in c.items() if k!='feats'}=={k:v for k,v in nc.items() if k!='feats'})
    ns=changed[supplement]
    before=copy.deepcopy(docs[supplement]);after=copy.deepcopy(ns)
    for field in ('dc','cadence','commandChoice','endpoints'):
        before['groups'][6]['value']['floraBody'].pop(field);after['groups'][6]['value']['floraBody'].pop(field)
    check('amended.other_supplement_fields_unchanged',before==after)
    check('amended.no_shared_rule_change',base+'data/public/feat_candidates/exact_01/shared_rules.json' not in {x['path'] for x in patch['operations']})
    for op in reversed(patch['operations']):
        par,key=parent_at(changed[op['path']],op['pointer']);par[key]=op['old']
    check('amended.exact_object_reversal',changed==docs)
    result={'reviewId':patch['reviewId'],'archiveSha256':digest(blob),'checks':len(results),'passed':sum(x['passed'] for x in results),'failed':sum(not x['passed'] for x in results),'results':results,
            'executedScope':'Read-only archive/manifest integrity; bound source/report equality; Python AST parsing; exact in-memory field amendments, symmetry and whole-object preservation/reversal. The recorded 114 result flags were inspected, not re-executed.',
            'original114SuiteReexecuted':False,'missingImportedLocalModulesInThisPacket':absent,
            'fullFloraStateMachineExecuted':False,'authored18AcceptanceGroupsExecuted':False,
            'runtimeApproved':False,'candidateApproved':False,'campaignFactsAuthenticated':False}
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('Usage: python verify_flora_addendum.py INPUT_ZIP')
    main(sys.argv[1])
