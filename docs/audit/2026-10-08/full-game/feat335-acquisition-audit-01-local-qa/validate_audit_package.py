#!/usr/bin/env python3
"""Validate reviewer deliverables and simulate exact edits in memory only."""
import argparse,copy,hashlib,json
from pathlib import Path
P='DescentReviewChanges/ReviewBible/'

def validate(submission,package):
    def load(root,p):return json.loads((root/p).read_text(encoding='utf-8-sig'))
    manifest=load(submission,'PACKAGE_MANIFEST.json');audit=load(package,'ACQUISITION_ROWS.json')
    cp='docs/audit/2026-10-08/full-game/FEAT_EXACT_01_ACQUISITION_CONTRACTS.json'
    pp=P+'data/public/feat_candidates/exact_01/candidate.json';ip=P+'data/director/feat_candidates/exact_01/candidate.json'
    con=load(submission,cp);pub=load(submission,pp);internal=load(submission,ip)
    results=[]
    def check(label,ok):
        results.append({'id':label,'passed':bool(ok)})
        if not ok:raise AssertionError(label)
    check('335-complete-order',[r['id'] for r in audit['rows']]==[r['id'] for r in con['records']] and len(audit['rows'])==335)
    work=load(package,'FINITE_REMAINING_WORK.json');wids={r['id'] for r in work['groups']}
    menus=load(package,'MENU_AND_SNAPSHOT_ATLAS.json');mids={r['id'] for r in menus['groups']}
    for r,c in zip(audit['rows'],con['records']):
        sid=r['id'];check('original/'+sid,r['a_acquisition']['completeOriginalObject']==c['originalObject'])
        check('complete-procedure/'+sid,r['a_acquisition']['completeControllingOperativeProcedure']==c['completeOperativeProcedure'])
        check('actual-selections-state/'+sid,bool(r['b_mandatorySelectionsAndSnapshots']['exactObligation']) and bool(r['c_initialState']['exactObligation']))
        check('evidence-and-scope/'+sid,'attachedReportReferences' in r['e_evidence'] and not r['promotionAuthorized'] and r['candidateSelectionEnabledUnchanged']==c['candidateSelectionEnabled'])
        check('obligation-groups/'+sid,set(r['e_evidence']['remainingObligationGroups'])<=wids and set(r['b_mandatorySelectionsAndSnapshots']['menuAtlasGroups'])<=mids)
        for name,b in r['sourceBindings'].items():check('bound/'+sid+'/'+name,b['path'] in manifest and b['sha256']==manifest[b['path']]['sha256'])
    ops=load(package,'GUARDED_CORRECTIONS.json')['operations'];js={};texts={};changes=[]
    def get(obj,p):
        for t in p.strip('/').split('/'):
            t=t.replace('~1','/').replace('~0','~');obj=obj[int(t)] if isinstance(obj,list) else obj[t]
        return obj
    def setv(obj,p,v):
        parts=p.strip('/').split('/');last=parts.pop()
        par=get(obj,'/'+('/'.join(parts))) if parts else obj
        if isinstance(par,list):par[int(last)]=v
        else:par[last.replace('~1','/').replace('~0','~')]=v
    for op in ops:
        path=op['path'];raw=(submission/path).read_bytes()
        check('guard-source/'+path+'/'+str(len(changes)),hashlib.sha256(raw).hexdigest()==op['submittedSha256'])
        if op['op']=='replace_json_string':
            if path not in js:js[path]=json.loads(raw.decode('utf-8-sig'))
            check('guard-old/'+path+op['pointer'],get(js[path],op['pointer'])==op['old'])
            setv(js[path],op['pointer'],op['replacement'])
        else:
            if path not in texts:texts[path]=raw.decode('utf-8')
            check('guard-text/'+path+'/'+str(len(changes)),texts[path].count(op['old'])==op['expectedOccurrences'])
            texts[path]=texts[path].replace(op['old'],op['replacement'])
        changes.append({'finding':op['finding'],'path':path,'pointer':op.get('pointer'),'section':op.get('section')})
    pp2=js[pp];ip2=js[ip];cm2=js[cp];oldI={r['id']:r for r in internal['records']};newI={r['id']:r for r in ip2['records']}
    for before,after in zip(pub['feats'],pp2['feats']):
        sid=before['id']
        if sid=='conjure_flora':
            b=copy.deepcopy(before);a=copy.deepcopy(after)
            for key in ['operationalRules','payloadOperational']:b.pop(key);a.pop(key)
            check('flora-source-flags-unchanged',a==b)
            check('flora-current-parity',after['operationalRules']==after['payloadOperational']==newI[sid]['operationalRules']==newI[sid]['payloadOperational']==cm2['records'][298]['completeOperativeProcedure'])
        else:check('unrelated-public/'+sid,before==after)
    for sid,before in oldI.items():
        after=newI[sid]
        if sid=='conjure_flora':
            b=copy.deepcopy(before);a=copy.deepcopy(after)
            for key in ['operationalRules','payloadOperational']:b.pop(key);a.pop(key)
            check('flora-originalQuestion-sourceDirection-flags-unchanged',a==b)
        else:check('unrelated-internal/'+sid,before==after)
    check('eight-reviewed-full-unchanged',ip2['unchangedReviewedFeats']==internal['unchangedReviewedFeats'])
    check('full-original-registry-unchanged',ip2['original335Registry']==internal['original335Registry'])
    for sid in ['astral_projection','planar_binding']:check('null-preserved/'+sid,newI[sid]['payloadOperational'] is None)
    for path,text in texts.items():
        if path.endswith('.py'):compile(text,path,'exec');check('derived-code-compiles/'+path,True)
    for path,spec in manifest.items():check('source-untouched/'+path,hashlib.sha256((submission/path).read_bytes()).hexdigest()==spec['sha256'])
    out={'status':'PASS','scope':'Reviewer deliverable completeness, source links, exact edit guards and in-memory preservation/parity only; no original input edited','checks':len(results),'passed':sum(r['passed'] for r in results),'failed':sum(not r['passed'] for r in results),'operations':changes,'results':results}
    (package/'DELIVERABLE_QA.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print({k:out[k] for k in ['status','checks','passed','failed']})
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--submission',type=Path,required=True);ap.add_argument('--package',type=Path,default=Path(__file__).resolve().parent);args=ap.parse_args();validate(args.submission,args.package)
