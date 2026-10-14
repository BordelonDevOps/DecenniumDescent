"""Apply/verify TEX-01–04 only in an explicit working copy, against a frozen tree.
Never run --apply against the preserved submission. This does not set approval labels.
"""
from pathlib import Path
from hashlib import sha256
from urllib.parse import unquote
import argparse,copy,json,re,shutil

def h(b):return sha256(b).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def get(o,pointer):
 for k in pointer.strip('/').split('/'):o=o[int(k)] if isinstance(o,list) else o[k]
 return o
def setval(o,pointer,value):
 ks=pointer.strip('/').split('/');par=o
 for k in ks[:-1]:par=par[int(k)] if isinstance(par,list) else par[k]
 par[int(ks[-1]) if isinstance(par,list) else ks[-1]]=value

def main():
 ap=argparse.ArgumentParser();ap.add_argument('baseline',type=Path);ap.add_argument('working',type=Path);ap.add_argument('--additional-baseline',required=True,type=Path);ap.add_argument('--out',required=True,type=Path);ap.add_argument('--apply',action='store_true');a=ap.parse_args();assert a.baseline.resolve()!=a.working.resolve(),'Do not amend frozen submission';c=load(Path(__file__).with_name('TEX_EXACT_CORRECTIONS.json'));groups={}
 for op in c['operations']:groups.setdefault(op['path'],[]).append(op)
 rows=[]
 def ck(name,x,y=True):rows.append({'name':name,'passed':x==y,'actual':x,'expected':y})
 changed={}
 for rel,ops in groups.items():
  base=a.baseline/rel
  if not base.exists():base=a.additional_baseline/rel
  b=base.read_bytes();ck(rel+' submitted hash',h(b),ops[0]['beforeFileSha256']);
  if h(b)!=ops[0]['beforeFileSha256']:raise ValueError('Frozen base hash mismatch: '+rel)
  isjson=rel.endswith('.json');obj=load(base) if isjson else b.decode('utf-8-sig').replace('\r\n','\n');expected=copy.deepcopy(obj)
  for op in ops:
   t=get(expected,op['jsonPointer']) if isjson else expected;ck(op['id']+' one exact before occurrence',t.count(op['before']),1);
   if t.count(op['before'])!=1:raise ValueError('Expected one exact old string: '+op['id'])
   t=t.replace(op['before'],op['replacement'],1)
   if isjson:setval(expected,op['jsonPointer'],t)
   else:expected=t
  dest=a.working/rel
  if a.apply:
   dest.parent.mkdir(parents=True,exist_ok=True);txt=json.dumps(expected,ensure_ascii=False,indent=2)+'\n' if isjson else expected
   if b'\r\n' in b:txt=txt.replace('\n','\r\n')
   dest.write_bytes((b'\xef\xbb\xbf' if b.startswith(b'\xef\xbb\xbf') else b'')+txt.encode())
  actual=load(dest) if isjson else dest.read_text(encoding='utf-8-sig');ck(rel+' exact amended object/text only',actual==expected)
  if isjson:
   ck(rel+' original recipe cards unchanged',actual['cards']==obj['cards']);ck(rel+' original body models unchanged',actual['bodyModels']==obj['bodyModels'])
   if 'tinkerInterfaceRegister' in obj:
    ck('48 interface original sourceCard objects unchanged',[x['sourceCard'] for x in actual['tinkerInterfaceRegister']['cards']]==[x['sourceCard'] for x in obj['tinkerInterfaceRegister']['cards']])
  changed[rel]={'beforeSha256':h(b),'correctedBeforeLabelsSha256':h(dest.read_bytes())}
 # No protected source/candidate byte outside these exact permitted working targets changes.
 mf=load(a.baseline/'FILE_MANIFEST.json')
 for rel,v in mf.items():
  if rel not in groups:ck('Unchanged payload '+rel,h((a.working/rel).read_bytes()),v['sha256'])
 for rel,v in mf.items():ck('Frozen original still unchanged '+rel,h((a.baseline/rel).read_bytes()),v['sha256'])
 root='DescentReviewChanges/ReviewBible/';pub=load(a.working/root/'data/crafting/advanced_craft_recipe_candidate_public.json');ck('Full public operatingGuideText equals full public guide',pub['operatingGuideText'],(a.working/root/'docs/mechanics/ADVANCED_CRAFT_CANDIDATE_GUIDE.md').read_text())
 # Avoid logging the complete full guide twice.
 rows[-1]['actual']={'characters':len(pub['operatingGuideText']),'utf8Sha256':h(pub['operatingGuideText'].encode())};rows[-1]['expected']={'characters':len((a.working/root/'docs/mechanics/ADVANCED_CRAFT_CANDIDATE_GUIDE.md').read_text()),'utf8Sha256':h((a.working/root/'docs/mechanics/ADVANCED_CRAFT_CANDIDATE_GUIDE.md').read_text().encode())}
 checklist=load(a.baseline/'docs/audit/2026-10-08/full-game/TEACHING_NAVIGATION_REVIEW_CHECKLIST.json');links=[]
 def anchors(t):
  return {''.join(c for c in re.sub(r'\[([^]]+)\]\([^)]+\)',r'\1',x).lower() if c.isalnum() or c in '_- ').replace(' ','-') for x in re.findall(r'^#{1,6}\s+(.+)$',t,re.M)}
 for rel in checklist['candidateFiles']:
  if not rel.endswith('.md'):continue
  p=a.working/rel
  for raw in re.findall(r'\]\(([^)]+)\)',p.read_text()):
   if re.match(r'\w+://|mailto:',raw):continue
   file,_,anchor=unquote(raw.strip('<>')).partition('#');dest=(p.parent/file).resolve() if file else p
   ok=dest.is_file() and (not anchor or anchor in anchors(dest.read_text(encoding='utf-8-sig')));ck('Amended link '+p.name+' -> '+raw,ok);links.append({'from':rel,'link':raw,'passed':ok})
 out={'scope':'Reviewer working copy only; all nine exact string/field replacements, unchanged originals and public full-guide parity. Approval labels/admin fulfillment are not applied here. No runtime/human claim.','checks':len(rows),'failed':[x for x in rows if not x['passed']],'changedCurrentFiles':changed,'links':links,'results':rows}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'checks':len(rows),'failures':len(out['failed']),'failed':out['failed'][:8],'directLinks':len(links),'changedFiles':len(changed)}))
 if out['failed']: raise SystemExit(1)
if __name__=='__main__':main()
