"""Verify, or stage a NEW isolated reference tree; never alter project files.
No project module executes. --output must name a nonexistent directory outside
this package and outside --source-root. Default invocation is read-only.
"""
from pathlib import Path
import argparse,json,shutil,sys
sys.dont_write_bytecode = True
from verify_bundle import verify,read,B,digest,safe

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output');parser.add_argument('--source-root');parser.add_argument('--variant',choices=['baseline','proposed'],default='proposed');args=parser.parse_args()
 report,union=verify()
 source=Path(args.source_root).resolve() if args.source_root else None
 if source:
  for path,data in union.items():
   p=source/path
   if not p.is_file() or p.read_bytes()!=data:
    raise SystemExit('Source baseline drift at '+path+'; read/reconcile the complete actual successor. No writes performed.')
 staged=dict(union)
 if args.variant=='proposed':
  for meta in read('CODE_BINDINGS.json')['files']:staged[meta['path']]=(B/'proposed'/meta['path']).read_bytes()
 if not args.output:
  print(json.dumps({'verified':True,'variant':args.variant,'sourceFiles':len(staged),'written':0,'note':'Supply --output only to create a separate new reference tree.'}));return
 target=Path(args.output).resolve()
 if target.exists() or target.is_relative_to(B) or B.is_relative_to(target) or source and (target.is_relative_to(source) or source.is_relative_to(target)):
  raise SystemExit('Output must be a new separate directory, not the package, a source tree, or their ancestor/child.')
 if not target.parent.is_dir():raise SystemExit('The output parent directory must already exist.')
 if not all(safe(path) for path in staged):raise SystemExit('Unsafe staged path; no writes performed.')
 target.mkdir()
 try:
  for path,data in staged.items():
   p=target/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
  if not all((target/path).read_bytes()==data for path,data in staged.items()):raise ValueError('Staged byte verification failed')
 except Exception:
  shutil.rmtree(target);raise
 print(json.dumps({'verified':True,'variant':args.variant,'sourceFiles':len(staged),'written':len(staged),'output':str(target),'gameRuntimeExecuted':False,'ruleJsonProposalApplied':False}))
if __name__=='__main__':main()
