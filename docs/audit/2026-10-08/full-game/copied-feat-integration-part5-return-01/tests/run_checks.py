from pathlib import Path
import sys,runpy,json
sys.dont_write_bytecode = True
root=Path(sys.argv[1]).resolve(); name=sys.argv[2]; out=Path(sys.argv[3]) if len(sys.argv)>3 else None
T=root/'DescentReviewChanges/ReviewBible/tools';sys.path.insert(0,str(T))
import apply_di7_ap_as_01 as loc
loc.G=root;loc.R=root/'DescentReviewChanges/ReviewBible';loc.A=root/'docs/audit/2026-10-08/full-game';loc.V=loc.A/'di7-joint-review-01-verdict'
captured={}
def trace(frame,event,arg):
    if event=='return' and frame.f_code.co_name=='main' and frame.f_code.co_filename==str(T/name):
        for key in ['report','histories','results','ready_histories','coverage']:
            if key in frame.f_locals: captured[key]=frame.f_locals[key]
        captured['global_clean']=frame.f_globals.get('clean')
        captured['global_serial']=frame.f_globals.get('serial')
    return trace
sys.argv=[name];sys.settrace(trace)
try:runpy.run_path(str(T/name),run_name='__main__')
except SystemExit as e:
    if e.code not in (None,0):raise
finally:sys.settrace(None)
if out:
    obj=captured.get('report',{})
    clean=captured.get('global_clean');ser=captured.get('global_serial')
    if clean:obj=clean(obj)
    out.write_text(json.dumps(obj,indent=2,ensure_ascii=False,default=ser)+'\n')
    print('CAPTURED',out,len(obj),list(obj)[:12])
