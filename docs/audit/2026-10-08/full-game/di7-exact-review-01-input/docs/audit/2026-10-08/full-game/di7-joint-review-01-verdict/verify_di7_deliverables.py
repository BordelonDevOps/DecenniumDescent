#!/usr/bin/env python3
"""Read-only source excerpt/reference descendant/coverage validation. No game runtime."""
import argparse,copy,hashlib,json,re,zipfile
from pathlib import Path

def main():
 a=argparse.ArgumentParser();a.add_argument('--archive',type=Path,required=True);a.add_argument('--output',type=Path,required=True);args=a.parse_args();h=Path(__file__).resolve().parent;rows=[]
 def check(name,ok):rows.append({'name':name,'pass':bool(ok)})
 def load(p):return json.loads((h/p).read_text(encoding='utf-8'))
 def digest(b):return hashlib.sha256(b).hexdigest()
 def ptr(x,p):
  for t in p.strip('/').split('/'):
   t=t.replace('~1','/').replace('~0','~');x=x[int(t)]if isinstance(x,list)else x[t]
  return x
 def setp(x,p,v):
  ts=p.strip('/').split('/');q=x
  for t in ts[:-1]:q=q[int(t)]if isinstance(q,list)else q[t]
  t=int(ts[-1])if isinstance(q,list)else ts[-1];q[t]=copy.deepcopy(v)
 with zipfile.ZipFile(args.archive)as z:
  check('Exact submission hash',digest(args.archive.read_bytes())=='9ca5cd879b951dc3d23c2cf2815814db6dea1e064ad1779cd34d2383b03eb576')
  for s in load('BOUND_DI7_SOURCES.json'):
   b=z.read(s['path']);check(s['id']+' raw source hash',digest(b)==s['sha256'])
   if 'exactText'in s:actual='\n'.join(b.decode('utf-8').splitlines()[s['startLine']-1:s['endLine']]);check(s['id']+' exact full line excerpt',actual==s['exactText'])
   else:check(s['id']+' exact full source object',ptr(json.loads(b),s['pointer'])==s['exactObject'])
  ops=load('EXACT_DI7_CORRECTIONS.json')['changes']
  for ref in load('REFERENCE_DESCENDANTS.json'):
   original=json.loads(z.read(ref['incomingPath']));actual=load(ref['newReferencePath']);expected=copy.deepcopy(original)
   for op in ops:
    check(ref['newReferencePath']+' old guard '+op['pointer'],ptr(expected,op['pointer'])==op['old']);setp(expected,op['pointer'],op['replacement'])
   check(ref['newReferencePath']+' whole object equality',actual==expected)
   b=(h/ref['newReferencePath']).read_bytes();check(ref['newReferencePath']+' bytes/hash',len(b)==ref['newBytes']and digest(b)==ref['newSha256'])
   for op in reversed(ops):setp(expected,op['pointer'],op['old'])
   check(ref['newReferencePath']+' inverse original object',expected==original)
  r=load('DI7_SOURCE_DECISION_REGISTER.json');text=(h/'DI7_COMPLETE_OPERATING_DIRECTIONS.md').read_text();ids=[]
  for row in r['records']:
   check(row['spellId']+' full paragraph in manuscript',row['procedure']in text)
   for ex in row['workedCases']:check(row['spellId']+' complete worked example',ex in text)
   ids.append(row['spellId'])
  check('Exactly seven unique spell IDs',len(ids)==len(set(ids))==7)
  for issue in r['jointIssues']:
   p,anchor=issue['operativeReference'].split('#');check(issue['id']+' operative anchor',f'id="{anchor}"' in(h/p).read_text())
  checks=load('FINITE_DI7_EXPECTATIONS.json');check('16 authored groups',checks['groupCount']==len(checks['groups'])==16);check('49 authored variants',checks['variantCount']==sum(len(g['variants'])for g in checks['groups'])==49)
  check('14 original examples',len(load('DI7_ORIGINAL_EXAMPLE_DISPOSITIONS.json'))==14)
 result={'checks':len(rows),'passed':sum(x['pass']for x in rows),'failed':sum(not x['pass']for x in rows),'scope':'Executed package/excerpt/full-object/coverage checks only; no additional gameplay or semantic acceptance inferred.','details':rows}
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in result.items()if k!='details'},indent=2))
 if result['failed']:
  for r in rows:
   if not r['pass']:print('FAIL',r['name'])
  raise SystemExit(1)
if __name__=='__main__':main()
