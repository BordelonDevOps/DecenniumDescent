#!/usr/bin/env python3
"""Run isolated new specifications only; does not import the project or mutate its files."""
import json,sys,unittest,hashlib,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'specification'))
import test_reference
class Result(unittest.TextTestResult):
 def __init__(self,*a,**kw):super().__init__(*a,**kw);self.cases=[]
 def addSuccess(self,test):super().addSuccess(test);self.cases.append({'id':test.id(),'status':'pass'})
 def addFailure(self,test,err):super().addFailure(test,err);self.cases.append({'id':test.id(),'status':'failure'})
 def addError(self,test,err):super().addError(test,err);self.cases.append({'id':test.id(),'status':'error'})
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path,default=ROOT/'SPECIFICATION_REPORT.json');args=ap.parse_args()
 suite=unittest.defaultTestLoader.loadTestsFromModule(test_reference);r=unittest.TextTestRunner(verbosity=1,resultclass=Result).run(suite)
 report={'scope':'Isolated source-derived arithmetic and expressly NEW finite policy specifications. No project modules, runtime/scheduler, real actors, human gameplay or numerical-balance tests.','testsRun':r.testsRun,'failures':len(r.failures),'errors':len(r.errors),'cases':sorted(r.cases,key=lambda x:x['id']),'projectRuntimeTests':0,'sourceModulesImported':False}
 args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');return 0 if r.wasSuccessful() else 1
if __name__=='__main__':raise SystemExit(main())
