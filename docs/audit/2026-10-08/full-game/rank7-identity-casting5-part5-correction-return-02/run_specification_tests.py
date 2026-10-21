#!/usr/bin/env python3
"""Run only inspected isolated specifications; no project import or canonical writes."""
import json,sys,unittest,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/"specification"))
import test_reference,test_corrections
class Result(unittest.TextTestResult):
 def __init__(self,*args,**kwargs):
  super().__init__(*args,**kwargs);self.cases=[]
 def addSuccess(self,t):
  super().addSuccess(t);self.cases.append({"id":t.id(),"status":"pass"})
 def addFailure(self,t,e):
  super().addFailure(t,e);self.cases.append({"id":t.id(),"status":"failure"})
 def addError(self,t,e):
  super().addError(t,e);self.cases.append({"id":t.id(),"status":"error"})
def main():
 p=argparse.ArgumentParser();p.add_argument("--report",type=Path,required=True);a=p.parse_args()
 if a.report.exists():raise SystemExit("Refusing to overwrite an existing report")
 modules=[test_reference,test_corrections]
 counts={v.__name__:unittest.defaultTestLoader.loadTestsFromModule(v).countTestCases() for v in modules}
 suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromModule(v) for v in modules])
 r=unittest.TextTestRunner(verbosity=1,resultclass=Result).run(suite)
 out={"scope":"Inspected prior isolated92-test reference suite plus new finite fixture/acquisition/ledger/history tests. No project or production-engine modules.",
      "testsRun":r.testsRun,"moduleCounts":counts,"failures":len(r.failures),"errors":len(r.errors),
      "cases":sorted(r.cases,key=lambda x:x["id"]),"projectRuntimeTests":0,"sourceModulesImported":False,
      "localDiagnosticScriptExecuted":False}
 a.report.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({k:v for k,v in out.items() if k not in ("cases","scope")}))
 return 0 if r.wasSuccessful() else 1
if __name__=="__main__":raise SystemExit(main())
