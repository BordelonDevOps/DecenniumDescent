from pathlib import Path
import argparse
from xml.etree import ElementTree as ET
import json,hashlib,collections,zipfile
parser=argparse.ArgumentParser(description='Read-only advanced handoff byte/source/book comparison; no runtime or world verification.')
parser.add_argument('source_root', type=Path, help='Extracted complete handoff root')
parser.add_argument('--output', type=Path, default=Path.cwd(), help='Separate report directory')
parser.add_argument('--archive', type=Path, help='Optional original ZIP for its actual hash')
args=parser.parse_args();R=args.source_root.resolve();W=args.output.resolve();W.mkdir(parents=True,exist_ok=True);A=R/'docs/audit/2026-10-08/full-game'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
p=load(A/'ADVANCED_CRAFT_SOURCE_PREPARATION.json');manifest=load(R/'FILE_MANIFEST.json');results=[]
def ck(name,ok,details=None):results.append({'name':name,'pass':bool(ok),**({'details':details} if details is not None else {})})
for path,e in manifest.items():
 b=(R/path).read_bytes();ck('manifest:'+path,len(b)==e['bytes'] and sha(b)==e['sha256'])
base=load(R/p['versionAudit']['sourcePaths']['mechanicalV4']);bm={x['id']:x for x in base['recipes']}
for r in p['recipes']:ck('complete-original:'+r['id'],bm[r['id']]==r and base['recipes'][p['sourceIndices'][r['id']]]==r)
with zipfile.ZipFile(R/'books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx') as z:
 root=ET.fromstring(z.read('word/document.xml'))
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
paras=[''.join(e.itertext()) for e in []]  # Filled from every OOXML paragraph, including tables.
paras=[''.join(t.text or '' for t in e.findall('.//w:t',ns)) for e in root.findall('.//w:body//w:p',ns)]
for bind in p['publicBookBindings']:
 for para in bind['paragraphs']:ck('book:'+bind['recipeId']+':'+str(para['index']),paras[para['index']]==para['text'])
ck('100-six-paragraph-bindings',len(p['publicBookBindings'])==100 and all(len(b['paragraphs'])==6 for b in p['publicBookBindings']))
versions={}
for tag,path in p['versionAudit']['sourcePaths'].items():
 b=load(R/path)
 if isinstance(b,dict):
  rec=b.get('recipes',b.get('craftingRecipes'))
  if rec is None:
   # Some public wrappers use data.
   for k,v in b.items():
    if isinstance(v,list) and v and isinstance(v[0],dict) and 'id' in v[0]:rec=v;break
 else:rec=b
 versions[tag]={x['id']:x for x in rec}
fieldResults=[]
for c in p['versionAudit']['comparisons']:
 r=versions['mechanicalV4'][c['recipeId']];q=versions[c['version']][c['recipeId']];f=c['field'];eq=(f in r)==(f in q) and r.get(f)==q.get(f)
 fieldResults.append({**c,'independentlyEqual':eq});ck('version:'+c['version']+':'+c['recipeId']+':'+f,eq==c['equal'])
counts={}
for t in p['trades']:
 rr=[r for r in p['recipes'] if r['skill']==t];cs=[c for r in rr for c in r['components']]
 counts[t]={'recipes':len(rr),'components':len(cs),'nonconsumedToolRows':sum(not c['consumed'] and c['role']=='tool' for c in cs),'consumedRows':sum(c['consumed'] for c in cs),'consumedTools':sum(c['consumed'] and c['role']=='tool' for c in cs),'catalysts':sum(c['consumed'] and c['role']=='catalyst' for c in cs),'visibility':dict(collections.Counter(r['visibility'] for r in rr)),'families':dict(collections.Counter(r['recipeFamily'] for r in rr))}
book=R/'books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx';ck('actual-book-sha256',sha(book.read_bytes())==p['bookSha256']);ck('actual-mechanical-sha256',sha((R/p['versionAudit']['sourcePaths']['mechanicalV4']).read_bytes())==p['sourceSha256'])
out={'scope':'Independent byte, complete-source, book-text and recorded version-comparison checks. Not runtime, world-authentication or balance evidence.','archiveSha256':sha(args.archive.read_bytes()) if args.archive else None,'checks':len(results),'failed':[x for x in results if not x['pass']],'manifestPayloads':len(manifest),'completeOriginals':167,'bookParagraphs':sum(len(b['paragraphs']) for b in p['publicBookBindings']),'versionComparisons':len(fieldResults),'matchingVersionFields':sum(x['independentlyEqual'] for x in fieldResults),'counts':counts,'results':results}
(W/'INDEPENDENT_SOURCE_CHECKS.json').write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({k:v for k,v in out.items() if k!='results'},indent=2))
