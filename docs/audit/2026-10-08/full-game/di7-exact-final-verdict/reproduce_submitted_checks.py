"""Rerun submitted bounded evaluators without editing any submitted bytes.
Only import roots, report destinations, and report-path metadata are redirected.
No game predicate/assertion is changed. Standard library; fresh output required.
"""
from pathlib import Path
import argparse, contextlib, hashlib, importlib, io, json, subprocess, sys, traceback

SUITES = [
'validate_di7_acquisition_matrix','validate_di7_alignment_component',
'validate_di7_cast_transactions','validate_di7_shield_late_transactions',
'validate_di7_fate_transactions','validate_di7_alignment_transactions',
'validate_di7_vision_transactions_v2','validate_di7_faction_transactions_v2',
'validate_di7_area_geometry','validate_di7_mass_transactions',
'validate_di7_alignment_clock','validate_di7_shaman_transactions',
'validate_di7_supreme_transactions','validate_di7_boundary_and_copy_source',
'validate_di7_fate_mode_admission']
REPORT_NAMES = dict(zip(SUITES,[
'DI7_ALL_SEVEN_ACQUISITION_CHECK.json','DI7_ALIGNMENT_COMPONENT_CHECK.json',
'DI7_CAST_TRANSACTIONS_CHECK.json','DI7_SHIELD_LATE_TRANSACTIONS_CHECK.json',
'DI7_FATE_TRANSACTIONS_CHECK.json','DI7_ALIGNMENT_TRANSACTIONS_CHECK.json',
'DI7_VISION_TRANSACTIONS_V2_CHECK.json','DI7_FACTION_TRANSACTIONS_V2_CHECK.json',
'DI7_AREA_GEOMETRY_CHECK.json','DI7_MASS_TRANSACTIONS_CHECK.json',
'DI7_ALIGNMENT_CLOCK_CHECK.json','DI7_SHAMAN_TRANSACTIONS_CHECK.json',
'DI7_SUPREME_TRANSACTIONS_CHECK.json','DI7_BOUNDARY_AND_COPY_SOURCE_CHECK.json',
'DI7_FATE_MODE_ADMISSION_CHECK.json']))

def worker(root,out,suite):
    sys.dont_write_bytecode=True
    repo=root/'DescentReviewChanges/ReviewBible'
    audit=root/'docs/audit/2026-10-08/full-game'
    sys.path.insert(0,str(repo/'tools'))
    import apply_di7_ap_as_01 as roots
    class AuditRoot:
        def __truediv__(self,key):
            return out/key if str(key)==REPORT_NAMES[suite] else audit/key
    roots.G=root; roots.R=repo; roots.A=AuditRoot(); roots.V=audit/'di7-joint-review-01-verdict'
    def info(p,b=None):
        p=Path(p); b=p.read_bytes() if b is None else b
        try: name=p.relative_to(root).as_posix()
        except ValueError: name='reviewer_fresh_results/'+p.name
        return {'path':name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
    roots.info=info
    importlib.import_module(suite).main()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--submission',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--suite',choices=SUITES)
    args=ap.parse_args();root=args.submission.resolve();out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    if args.suite:worker(root,out,args.suite);return
    results=[]
    for suite in SUITES:
        proc=subprocess.run([sys.executable,'-B',__file__,'--submission',str(root),'--out',str(out),'--suite',suite],capture_output=True,text=True,timeout=40)
        row={'suite':suite,'exitCode':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr,'executionScope':'Fresh bounded evaluator execution on submitted current files; conditional premises remain premises.'}
        if proc.returncode==0:
            p=out/REPORT_NAMES[suite];report=json.loads(p.read_bytes());baseline=json.loads((root/'docs/audit/2026-10-08/full-game'/REPORT_NAMES[suite]).read_bytes())
            row.update(checks=report['checks'],histories=report['historyCount'],submittedChecks=baseline['checks'],sameCheckCount=report['checks']==baseline['checks'],report=REPORT_NAMES[suite],reportSha256=hashlib.sha256(p.read_bytes()).hexdigest())
        results.append(row);print(suite,proc.returncode,row.get('checks'),flush=True)
        (out.parent/'REPRODUCTION_RESULTS.json').write_text(json.dumps({'suites':results,'totalChecksOfSuccessfulRuns':sum(x.get('checks',0) for x in results),'failedSuites':[x['suite'] for x in results if x['exitCode']],'method':'Unchanged submitted logic imported with root/report routing only. Historical reports are untouched, not recertified as current. Not full payload/runtime/campaign verification.'},indent=2)+'\n')
if __name__=='__main__': main()
