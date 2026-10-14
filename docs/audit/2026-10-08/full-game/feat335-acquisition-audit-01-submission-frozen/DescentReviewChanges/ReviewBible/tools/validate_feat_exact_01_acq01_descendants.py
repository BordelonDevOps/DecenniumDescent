"""Independently reconstruct allowed ACQ-01 descendants from preserved inputs.

No apply/builder import. Complete data/text comparison, including untouched
candidate artifacts, closes only this finite correction's preservation checks.
"""
from pathlib import Path
from copy import deepcopy
from hashlib import sha256
from datetime import datetime,timezone
import argparse,json

G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
I=R/'data/director/feat_candidates/exact_01';U=R/'data/public/feat_candidates/exact_01';D=R/'docs/feats/exact-candidate-01'
def read(p):return json.loads(p.read_text('utf-8-sig'))
def info(p):
    b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha256(b).hexdigest()}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--report',type=Path,default=A/'FEAT327_ACQ_01_INDEPENDENT_CHECK.json');args=parser.parse_args()
    assert not args.report.exists(),'Use a new report path to preserve evidence.'
    pres=read(A/'feat-exact-01-before-acq01/PRESERVATION_MANIFEST.json')
    fulfilled=read(A/'FEAT327_ACQ_01_DERIVED_FULFILLMENT.json')
    response=read(A/'FEAT327_ACQ_01_GPT_RESPONSE.json')
    paragraph=next(s[2:] for s in response['fullResponse'].splitlines() if s.startswith('> **Weapon prerequisite bridge.**'))
    sentence=next(s[2:] for s in response['fullResponse'].splitlines() if s.startswith('> For weapon prerequisites, apply FS-02'))
    anchor='Existing genuinely authorized legacy grants remain evidenced; no new builder option follows.'
    checks=[]
    def check(name,result):checks.append({'name':name,'pass':bool(result)})
    def original(p):return G/pres[p.relative_to(G).as_posix()]['preservedCopy']
    for rel,b in pres.items():check('Preserved exact bytes '+rel,info(G/b['preservedCopy'])['sha256']==b['sha256'] and info(G/b['preservedCopy'])['bytes']==b['bytes'])
    for p in [I/'shared_rules.json',U/'shared_rules.json']:
        old=read(original(p));expected=deepcopy(old);assert expected['rules'][1]['id']=='FS-02'
        expected['rules'][1]['wording']=expected['rules'][1]['wording'].replace(anchor,anchor+'\n\n'+paragraph)
        check('Only exact FS-02 insertion '+p.relative_to(G).as_posix(),read(p)==expected)
        check('All15 other shared rules unchanged '+str(p.parent),[x for x in read(p)['rules'] if x['id']!='FS-02']==[x for x in old['rules'] if x['id']!='FS-02'])
    p=D/'SHARED_RULES.md';expected=original(p).read_text('utf-8').replace(anchor,anchor+'\n\n'+paragraph)
    check('Complete reader differs by identical exact paragraph only',p.read_text('utf-8')==expected)
    expected_conv=read(original(I/'convention_dispositions.json'))
    identities=[(35,'combat','/sharedProposal/Authority and acquisition'),(42,'general_combat','/sharedProposal/Authority and acquisition'),
                (50,'general_combat','/proposedCombatConventionDependency/Authority and acquisition'),(84,'heritage_mutation','/proposedCombatDependency/Authority and acquisition')]
    expected_cohorts={c:read(original(I/f'cohorts/{c}.json')) for c in ['combat','general_combat','heritage_mutation']}
    for index,c,pointer in identities:
        entry=expected_conv['entries'][index];assert (entry['cohort'],entry['pointer'])==(c,pointer)
        entry['controllingDecisions'].append('FEAT327-ACQ-01');entry['replacement']+=' '+sentence
        components=pointer.strip('/').split('/');parent=expected_cohorts[c]
        for segment in components[:-1]:parent=parent[segment]
        parent[components[-1]]+=' '+sentence
    check('All91 conventions differ only at exact four reference entries',read(I/'convention_dispositions.json')==expected_conv)
    for c,expected in expected_cohorts.items():check('Whole cohort differs only at named reference '+c,read(I/f'cohorts/{c}.json')==expected)
    old=read(original(A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json'));current=read(A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json')
    for before,after in zip(old['records'],current['records']):
        expected=deepcopy(before)
        if 'pendingExactIssue' in expected:expected.pop('pendingExactIssue');expected['controllingAcquisitionAddendum']='FEAT327-ACQ-01'
        def walk(req):
            if 'bridgeIssue' in req:req['controllingAddendum']=req.pop('bridgeIssue')
            for child in req.get('requirements',[]):walk(child)
        walk(expected['requirements'])
        if expected['id']=='dragon_blood':
            expected['requirements']={'kind':'all','requirements':[deepcopy(expected['requirements']),{'kind':'actualEstablishedReceipt',
              'receipt':'one recorded actual draconic ancestry damage type for the qualifying lineage source','doesNotCreateSource':True}]}
            expected['normalizationCorrection']='Carry the existing final Dragon Blood procedure’s recorded damage-type requirement on both branches. No source rule changed.'
        check('Complete acquisition record exact allowed change '+after['id'],after==expected)
    check('Exactly335 acquisition records retained',len(current['records'])==len(old['records'])==335)
    check('17 typed weapon contracts carry addendum',sum('controllingAcquisitionAddendum' in x for x in current['records'])==17)
    for b in current['sourceBindings']:check('Current contract input bound '+b['path'],info(G/b['path'])==b)
    for rel,b in fulfilled['measuredCurrentDescendants'].items():check('Measured descendant '+rel,info(G/rel)==b)
    build=read(A/'FEAT_EXACT_CANDIDATE_01_BUILD.json')
    for rel,b in build['artifacts'].items():
        if rel not in fulfilled['measuredCurrentDescendants']:check('Untouched candidate artifact '+rel,{k:info(G/rel)[k] for k in ['bytes','sha256']}==b)
    for rel,b in build['originalSourceBindings'].items():check('Untouched original source '+rel,{k:info(G/rel)[k] for k in ['bytes','sha256']}==b)
    check('Nine finite expected source cases retained',len(fulfilled['expectedCases'])==9 and {x['id'] for x in fulfilled['expectedCases']}=={f'ACQ-T{i:02d}' for i in range(1,10)})
    check('130 source/reference checks passed',fulfilled['checks']==130 and fulfilled['failureCount']==0 and all(x['pass'] for x in fulfilled['results']))
    history=read(A/'FEAT_EXACT_01_ACQUISITION_HISTORY_AFTER_ACQ01_CHECK.json')
    for b in history['sourceBindings']:check('Current acquisition-history input '+b['path'],info(G/b['path'])==b)
    check('897 history/source checks passed',history['checks']==897 and history['failureCount']==0 and all(x['pass'] for x in history['results']))
    failures=[x for x in checks if not x['pass']]
    out={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'pass' if not failures else 'fail',
      'scope':'Independent complete comparison of exact ACQ-01 descendants and unchanged source/candidate bindings; not all prerequisite-actor validation.',
      'script':info(Path(__file__)),'sourceResponse':info(A/'FEAT327_ACQ_01_GPT_RESPONSE.json'),'fulfillment':info(A/'FEAT327_ACQ_01_DERIVED_FULFILLMENT.json'),
      'checks':len(checks),'failureCount':len(failures),'failures':failures,'results':checks,
      'onlyNamedCorrectionFulfilled':not failures,'all335ActorHistoriesValidated':False,'candidateReadyForSubmission':False,'exactApproved':False,'sourceInformationDeleted':0}
    args.report.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'report':info(args.report),'checks':len(checks),'failures':len(failures)}))
    if failures:raise SystemExit(1)

if __name__=='__main__':main()
