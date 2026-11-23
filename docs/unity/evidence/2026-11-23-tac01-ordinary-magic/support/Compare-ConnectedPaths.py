from pathlib import Path
import json,hashlib,re,sys
b=Path(sys.argv[1]);modes=['ConsoleUninterrupted','ConsoleRestored','TypedUninterrupted','TypedRestored','ReceiptReplay'];counts=[];bad=[]
ref=b/modes[0]; files=sorted(p.name for p in ref.iterdir() if re.match(r'^r[0-9]+\.ddsave(?:$|\.)',p.name));comparisons=0
assert len(files)==468, len(files)
for mode in modes:
 r=json.loads((b/mode/'result.json').read_text(encoding='utf-8-sig'));assert r['status']=='PASS';counts.append({'mode':mode,'commands':r['commands'],'checkpoints':r['checkpoints'],'resultSha256':hashlib.sha256((b/mode/'result.json').read_bytes()).hexdigest()})
 if mode==modes[0]:continue
 for name in files:
  comparisons+=1
  if (ref/name).read_bytes()!=(b/mode/name).read_bytes():bad.append(mode+'/'+name)
x={'status':'PASS' if not bad else 'FAIL','filesPerPath':len(files),'crossPathComparisons':comparisons,'mismatches':bad,'paths':counts,'scope':'Actual five440-command paths,18 checkpoints, four seats and six ordered projections; full raw canonical save bytes include RNG and receipts. Only exact named checkpoint artifacts are compared; run metadata correctly differs.'}
(b/'comparison.json').write_text(json.dumps(x,indent=2)+'\n');print(json.dumps(x,indent=2));assert not bad
