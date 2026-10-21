from pathlib import Path
import datetime,hashlib,json,re,zipfile
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game';O=A/'feat335-requirement-text-111'
assert not O.exists();O.mkdir()
def j(p):return json.loads(p.read_bytes())
def h(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def bind(p):return {'path':str(p),**h(p.read_bytes())}
def write(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
def ser(o):return (json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
checks=[]
def ck(n,v):checks.append({'name':n,'passed':bool(v)});assert v,n
authority=j(A/'FEAT335_ACCEPTANCE_EVIDENCE_MAP_107.json');b=authority['contract'];p=Path(b['path']);raw=p.read_bytes()
ck('Original acceptance contract exact',h(raw)=={'bytes':b['bytes'],'sha256':b['sha256']})
write(O/'ORIGINAL_GATE_CONTRACT.md',raw);text=raw.decode('utf-8-sig')
rows=[]
for code,rel in [('07','feat335-numeric-physical-109-v2/FXC07.json'),('08','feat335-numeric-physical-109-v2/FXC08.json'),('09','feat335-spell-state-110-v3/FXC09.json')]:
 p=A/rel;old=p.read_bytes();obj=json.loads(old);exact=next(g['completeOriginalRequirement'] for g in authority['gates'] if g['id']=='FXC-'+code)
 section=re.search(r'^## FXC-'+code+r'[^\n]*\n(.*?)(?=^## |\Z)',text,re.M|re.S)
 ck('Exact original section exists '+code,section is not None and section.group(1).strip()==exact)
 ck('Submitted field actually empty '+code,obj['completeOriginalRequirement']=='')
 before=b'"completeOriginalRequirement": ""';after=b'"completeOriginalRequirement": '+json.dumps(exact,ensure_ascii=False).encode()
 ck('One raw field occurrence '+code,old.count(before)==1)
 pos=old.index(before);new=old[:pos]+after+old[pos+len(before):]
 obj['completeOriginalRequirement']=exact
 ck('Only complete requirement value changed '+code,json.loads(new)==obj)
 ck('Exact full byte reversal '+code,new[:pos]+before+new[pos+len(after):]==old)
 write(O/'before'/p.name,old);write(O/'after'/p.name,new)
 rows.append({'id':'FT111-REQUIREMENT-'+code,'original':bind(p),'before':bind(O/'before'/p.name),'successor':bind(O/'after'/p.name),'jsonPointer':'/completeOriginalRequirement','beforeValue':'','afterValue':exact,'rawOperation':{'startByte':pos,'before':before.decode(),'after':after.decode()},'gameplayChanged':False,'status':'DERIVED_DOCUMENTARY_SUCCESSOR_ONLY'})
report={'id':'FEAT335-REQUIREMENT-TEXT-REPAIR-111','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'originalContract':bind(O/'ORIGINAL_GATE_CONTRACT.md'),'operations':rows,'passed':len(checks),'failed':0,'checks':checks,'reason':'Independent verification of empty source-requirement fields surfaced during GPT review. Full original contract and107 extraction agree. Exactly three documentary string replacements; all gameplay/evidence fields remain unchanged. Frozen submitted maps and archives preserved.','parent335Accepted':False,'canonicalApplied':False,'runtimeExecuted':False,'sourceInformationDeleted':False,'gptFinalVerdictClaimed':False}
write(O/'REPORT.json',ser(report))
z=O/'DD_Feat335_Requirement_Text_Successor_111.zip'
with zipfile.ZipFile(z,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as f:
 for p in sorted(O.rglob('*')):
  if p.is_file() and p!=z:f.write(p,p.relative_to(O).as_posix())
with zipfile.ZipFile(z) as f:assert f.testzip() is None
receipt={'id':report['id'],'archive':bind(z),'report':bind(O/'REPORT.json'),'successors':[r['successor'] for r in rows],'passed':len(checks),'failed':0,'canonicalApplied':False,'parent335Accepted':False,'actuallySentToGpt':False}
write(A/'FEAT335_REQUIREMENT_TEXT_RECEIPT_111.json',ser(receipt));write(A/Path(__file__).name,Path(__file__).read_bytes());print(json.dumps(receipt))
