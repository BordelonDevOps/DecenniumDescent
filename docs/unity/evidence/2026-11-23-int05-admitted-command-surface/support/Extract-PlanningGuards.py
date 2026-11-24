"""Share native planning guards; verified V1 caller never enters historical fallback."""
import re,runpy,subprocess
from pathlib import Path
h=runpy.run_path(str(Path(__file__).with_name('Extract-NativePreflight.py')))
path='engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterPlan.cs'
source=subprocess.check_output(['git','show',h['BASE']+':'+path],cwd=h['ROOT']).decode().replace('\r\n','\n')
configs=[
 ('NextCharterPlanBasisFailure','        private long FindPlanningPassage(', 'state, previous, out passageRevision, verified'),
 ('NextCharterPlannerFailure','        private static bool NextCharterCommandPayloadValid(', 'state'),
 ('AssessNextCharterPlanCommand','        private void BookNextCharterPlan(', 'state, command, out job, out passageRevision, out observation, verified')
]
names={name:name+'ConstraintV1' for name,_,_ in configs}
for name,end,args in configs:
 a=source.index('        private string '+name+'('); brace=source.index('{',a)
 start=source[a:brace].rstrip(); b=source.index(end,a); fragment=source[a:b]; edits=[]
 for m in re.finditer(r'([?:]\s*)"([A-Z][A-Za-z0-9]+)"',fragment):
  line=source[:a+m.start()].count('\n')+1
  edits.append((m[0],m[1]+'new NativeCommandConstraintV1("'+m[2]+'", "'+path+'", '+str(line)+')'))
 if name=='AssessNextCharterPlanCommand':
  for old,new in names.items():
   if old==name:continue
   edits.append((old+'(',new+'('))
  edits += [('string invalid =','var invalid ='),('string failure =','var failure =')]
 # extract's one-replacement rule needs one edit per occurrence.
 expanded=[]
 for old,new in edits:expanded.extend([(old,new)]*fragment.count(old))
 h['extract'](path,start,end,names[name],start.replace('string '+name,'NativeCommandConstraintV1 '+names[name]),
     start+'\n            => '+names[name]+'('+args+')?.NativeCode;\n\n',expanded)
