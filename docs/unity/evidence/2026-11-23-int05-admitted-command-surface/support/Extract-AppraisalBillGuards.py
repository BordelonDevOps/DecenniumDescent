"""Exact shared current-record appraisal and bill guards; no booking or settlement."""
import re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
BASE='67f3d201b202ab2f815ab69940682f04e78c511c'
groups={
 'SharedHavenAppraisal.cs': ['AppraisalTermsFailure','AppraisalSubject','AppraisalWorkerFailure','AppraisalBasisFailure','AssessHavenAppraisal'],
 'SharedExpeditionBill.cs': ['ExpeditionBillAuthorityFailure','ExpeditionBillInputs','ExpeditionBillWorkerFailure','AssessExpeditionBill'],
}
names={name:name+'ConstraintV1' for methods in groups.values() for name in methods}
for file,methods in groups.items():
    path='engine/com.decennium.foundation/Laboratory/Model/'+file
    source=subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT).decode().replace('\r\n','\n')
    p=ROOT/path; raw=p.read_bytes(); eol='\r\n' if raw.count(b'\r\n')==raw.count(b'\n') else '\n'
    current=p.read_text(encoding='utf8')
    for name in methods:
        match=re.search(r'        private string '+name+r'\((.*?)\)\s*\{',source,re.S)
        assert match,name
        a=match.start(); brace=source.index('{',a); depth=1; b=brace+1
        while depth:
            depth+=(source[b]=='{')-(source[b]=='}'); b+=1
        original=source[a:b]; assert current.count(original)==1,name
        signature=source[a:brace].rstrip(); arguments=[]
        for param in match[1].split(','):
            param=param.strip()
            if param: arguments.append(('out ' if param.startswith('out ') else '')+param.split()[-1])
        wrapper=signature+'\n            => '+names[name]+'('+', '.join(arguments)+')?.NativeCode;\n\n'
        first=source[:a].count('\n')+1
        lines=[]
        for i,line in enumerate(original.splitlines(keepends=True)):
            def typed(m):
                return 'new NativeCommandConstraintV1("'+m[1]+'", "'+path+'", '+str(first+i)+')'
            line=re.sub(r'(?<=return )"([A-Z][A-Za-z0-9]+)"',typed,line)
            line=re.sub(r'([?:]\s*)"([A-Z][A-Za-z0-9]+)"',
                lambda m:m[1]+'new NativeCommandConstraintV1("'+m[2]+'", "'+path+'", '+str(first+i)+')',line)
            lines.append(line)
        typedbody=''.join(lines).replace('private string '+name,'private NativeCommandConstraintV1 '+name,1)
        for old,new in names.items():
            typedbody=re.sub(r'\b'+old+r'\(',new+'(',typedbody)
        typedbody=re.sub(r'\bstring (failure|terms|subject|invalid|eligibility|authorityFailure)\s*=',r'var \1=',typedbody)
        current=current.replace(original,wrapper+typedbody,1)
    p.write_bytes(current.replace('\n',eol).encode())
    print(path)
