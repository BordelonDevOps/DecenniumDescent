"""Inspect exact depth-excluded archives read-only; execute or extract no archive content."""
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
import importlib.util,io,json,stat,zipfile
H=Path(__file__).parent
spec=importlib.util.spec_from_file_location('backup57',H/'deliver_progress_2026_10_20_memory_denial57.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
policy=b.h.p.policy
cache={};members=[];occurrences=[];expanded=0;issues=[]

def inspect(name,raw,depth=0):
 global expanded
 assert depth<=16,'separate archive depth bound exceeded'
 why=policy.reason(name)
 if why and not why.startswith('generated'):issues.append({'path':name,'reason':why})
 suffix=Path(name).suffix.lower()
 if suffix in policy.TEXT:
  if b.h.raw_capture(raw):issues.append({'path':name,'reason':'unrelated raw browser capture'})
  if any(rx.search(raw) for rx in policy.SECRET):issues.append({'path':name,'reason':'credential pattern'})
 if suffix!='.zip':return
 digest=b.digest(raw);occurrences.append({'path':name,'depth':depth,'bytes':len(raw),'sha256':digest})
 if digest in cache:return
 cache[digest]={'firstPath':name,'bytes':len(raw),'firstDepth':depth,'complete':False,'members':0}
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  names=set()
  for item in z.infolist():
   parts=PurePosixPath(item.filename)
   assert not parts.is_absolute() and '..' not in parts.parts and '\\' not in item.filename and ':' not in item.filename,item.filename
   assert item.filename not in names,item.filename
   names.add(item.filename)
   assert not stat.S_ISLNK(item.external_attr>>16),item.filename
   if item.is_dir():continue
   assert not item.flag_bits&1,'encrypted archive member'
   expanded+=item.file_size
   assert expanded<=8*1024**3 and len(members)<100000,'bounded unique archive inspection exceeded'
   content=z.read(item);assert len(content)==item.file_size
   members.append({'archiveSha256':digest,'path':item.filename,'bytes':len(content),'sha256':b.digest(content)})
   cache[digest]['members']+=1
   inspect(item.filename,content,depth+1)
 cache[digest]['complete']=True

def main():
 path=b.W/'plan.json';plan=json.loads(path.read_bytes());report=b.W/'nested-archive-additional-review.json'
 assert not report.exists() and b.git('status','--porcelain=v1','-z')==b''
 candidates=[x for x in plan['excluded'] if 'nested archive depth' in x['reason']]
 reviewed=[]
 for row in candidates:
  raw=b.lp(b.G/row['path']).read_bytes()
  assert b.digest(raw)==row['sha256'] and len(raw)==row['bytes']
  inspect(row['path'],raw);reviewed.append(row)
 assert all(x['complete'] for x in cache.values())
 assert not issues,issues
 receipt={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),
  'scope':'Complete bounded read-only inspection of exact depth-excluded ZIP content. Identical nested archives are inspected once by SHA256 while each containing name is checked separately. No content executed or extracted.',
  'originalScannerExclusions':reviewed,'uniqueArchives':cache,'archiveOccurrences':occurrences,
  'uniqueArchiveCount':len(cache),'archiveOccurrenceCount':len(occurrences),
  'maxObservedDepth':max((x['depth'] for x in occurrences),default=0),'uniqueMemberCount':len(members),
  'uniqueExpandedBytes':expanded,'memberBindings':members,'issues':issues,'sourceChanged':False}
 b.write_new(report,b.jsraw(receipt));receiptsha=b.digest(report.read_bytes())
 baseline=b.h.oldtree(b.BASE);names={x['path'] for x in reviewed}
 for old in reviewed:
  row={k:v for k,v in old.items() if k!='reason'}
  row['changedFromBaseline']=baseline.get(row['path'],{}).get('oid')!=row['gitBlob']
  plan['included'].append(row)
 plan['included'].sort(key=lambda x:x['path']);plan['excluded']=[x for x in plan['excluded'] if x['path'] not in names]
 plan['additionalArchiveInspection']={'receipt':str(report),'receiptSha256':receiptsha,'includedArchivePaths':sorted(names),'uniqueArchivesInspected':len(cache),'uniqueMemberCount':len(members),'issues':0}
 plan['separatelyReviewedArchives']=[{'originalScannerDisposition':x,'additionalInspectionReceipt':str(report),'receiptSha256':receiptsha,'currentDisposition':'Included unchanged after complete recursive inspection;zero policy or credential issues.'} for x in reviewed]
 path.write_bytes(b.jsraw(plan))
 changed=[x['path'] for x in plan['included'] if x['changedFromBaseline']]
 (b.W/'changed-source-paths.json').write_bytes(b.jsraw(changed))
 print(json.dumps({'newlyIncludedArchives':len(reviewed),'uniqueArchivesInspected':len(cache),'archiveOccurrences':len(occurrences),'uniqueMemberCount':len(members),'uniqueExpandedBytes':expanded,'maxObservedDepth':receipt['maxObservedDepth'],'issues':0,'includedFiles':len(plan['included']),'changedFiles':len(changed)}))

if __name__=='__main__':main()
