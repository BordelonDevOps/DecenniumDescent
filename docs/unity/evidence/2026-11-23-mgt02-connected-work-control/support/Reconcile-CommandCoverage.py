from pathlib import Path
import json,hashlib,sys
base=Path(sys.argv[1]);repo=Path(__file__).resolve().parents[5];read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
expected={'StartWaterFill','PauseWaterFill','ResumeWaterFill','CancelWaterFill','StartMining','PauseMining','ResumeMining','StartFormulaResearch','PauseFormulaWork','ResumeFormulaWork','CancelFormulaWork','StartManufacturing','PauseManufacturing','ResumeManufacturing','CancelManufacturing','ResolveManufacturingQuality'}
principal=base/'five-paths-02';assert read(principal/'comparison.json')['status']=='PASS'
branches=base/'console-branches-01';report=read(branches/'result.json');assert report['status']=='PASS' and len(report['branches'])==9
witnesses={k:[] for k in sorted(expected)}
paths=[principal/'ConsoleUninterrupted/inputs.jsonl']+[branches/x['name']/'inputs.jsonl' for x in report['branches']]
for path in paths:
    responses=path.parent/'responses.jsonl';answers=[json.loads(x) for x in responses.read_text(encoding='utf-8-sig').splitlines()]
    requests=[json.loads(x) for x in path.read_text(encoding='utf-8-sig').splitlines()];assert len(requests)==len(answers)
    for line,(request,response) in enumerate(zip(requests,answers),1):
        if request.get('op')!='submit' or request.get('kind') not in expected:continue
        assert response['Response']=='Committed'
        witnesses[request['kind']].append({'input':path.resolve().relative_to(repo).as_posix(),'response':responses.resolve().relative_to(repo).as_posix(),'line':line,'commandId':request['id'],'revision':response['Revision']})
assert all(witnesses.values()),[k for k,v in witnesses.items() if not v]
assert sum(x['commands'] for x in report['branches'])==50
assert all(x['typedConsoleCanonicalEqual'] and x['strictRestoreEqual'] for x in report['branches'])
out={'status':'PASS16_INCLUDED_COMMANDS_HAVE_GENUINE_HOST_AND_CONSOLE_WITNESSES','commands':witnesses,'consoleBranches':9,'branchCommands':50,'branchQueryDiscoveryWorkReadPairs':sum(x['pureReadPairs'] for x in report['branches']),'branchResultSha256':hashlib.sha256((branches/'result.json').read_bytes()).hexdigest(),'scope':'Principal and branches of genuine fresh work-control genesis. Each console branch matches its actual public-host final state, with strict restore and pure native query/discovery/work reads. MODEL_ONLY AwaitingCheck fixtures are deliberately excluded from these positive host witnesses.'}
(base/'command-coverage.json').write_bytes((json.dumps(out,indent=2)+'\n').encode());print('PASS16 command kinds;9 console branches,50 real commands; typed/console final bytes match')
