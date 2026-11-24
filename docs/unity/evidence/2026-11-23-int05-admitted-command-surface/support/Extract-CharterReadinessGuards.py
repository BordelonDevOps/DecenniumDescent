"""Share current assent/attempt eligibility; preserve non-admitted inspection outputs."""
import re,runpy,subprocess
from pathlib import Path
h=runpy.run_path(str(Path(__file__).with_name('Extract-NativePreflight.py')))
ROOT=h['ROOT']; BASE=h['BASE']; lab='engine/com.decennium.foundation/Laboratory/Model/'
groups={
 'SharedNextCharterAgreement.cs':['NextCharterAgreementAuthorityFailure','NextCharterAgreementPhysicalFailure','AssessNextCharterAgreementCommand'],
 'SharedCharterAttempt.cs':['CharterLocalScopeFailure','CharterFatigueFailure','CharterObjectiveAuthorityFailure','CharterObjectiveReadiness','AssessCharterAttempt']
}
names={name:name+'ConstraintV1' for methods in groups.values() for name in methods}
for file,methods in groups.items():
 path=lab+file; source=subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT).decode().replace('\r\n','\n')
 p=ROOT/path; raw=p.read_bytes(); eol='\r\n' if raw.count(b'\n')==raw.count(b'\r\n') else '\n'; current=p.read_text()
 for name in methods:
  match=re.search(r'        private string '+name+r'\((.*?)\)\s*\{',source,re.S); assert match,name
  a=match.start(); brace=source.index('{',a); b=brace+1; depth=1
  while depth:
   depth+=(source[b]=='{')-(source[b]=='}'); b+=1
  original=source[a:b]; assert current.count(original)==1,name
  args=[('out ' if x.strip().startswith('out ') else '')+x.split()[-1] for x in match[1].split(',') if x.strip()]
  wrapper=source[a:brace].rstrip()+'\n            => '+names[name]+'('+', '.join(args)+')?.NativeCode;\n\n'
  first=source[:a].count('\n')+1; lines=[]
  for i,line in enumerate(original.splitlines(keepends=True)):
   line=re.sub(r'(?<=return )"([A-Z][A-Za-z0-9]+)"',lambda m:'new NativeCommandConstraintV1("'+m[1]+'", "'+path+'", '+str(first+i)+')',line)
   # The unadmitted Inspect branch retains string detail and its legacy wrappers.
   if not 'string objective =' in line:
    line=re.sub(r'([?:]\s*)"([A-Z][A-Za-z0-9]+)"',lambda m:m[1]+'new NativeCommandConstraintV1("'+m[2]+'", "'+path+'", '+str(first+i)+')',line)
   lines.append(line)
  body=''.join(lines).replace('private string '+name,'private NativeCommandConstraintV1 '+name,1)
  # Preserve the entire inspection branch with old string wrappers. It is never a V1 seat route.
  protected=[]
  if name=='AssessCharterAttempt':
   sa=body.index('            if (command.Kind == CommandKind.InspectCharterAttempt)'); sb=body.index('            if (!attempt.ObjectiveOpen)',sa)
   protected.append(body[sa:sb]); body=body[:sa]+'__INSPECT_BRANCH__\n'+body[sb:]
  if name=='AssessNextCharterAgreementCommand':
   sa=body.index('                var current = ObserveNextCharterPlan'); sb=body.index('            if (command.Target != terms.OfferId)',sa)
   protected.append(body[sa:sb]); body=body[:sa]+'__INSPECT_BRANCH__\n'+body[sb:]
  for old,new in names.items():body=re.sub(r'\b'+old+r'\(',new+'(',body)
  body=re.sub(r'\bstring (failure|authorityFailure|physicalFailure)\s*=',r'var \1=',body)
  if name=='AssessNextCharterAgreementCommand':
   body=body.replace('state.RuleClock, state.Revision, physicalFailure);','state.RuleClock, state.Revision, physicalFailure?.NativeCode);')
  if protected:body=body.replace('__INSPECT_BRANCH__\n',protected[0])
  current=current.replace(original,wrapper+body,1)
 p.write_bytes(current.replace('\n',eol).encode()); print(path)
