import hashlib,json,pathlib,zipfile
from datetime import datetime,timezone
R=pathlib.Path('C:/Github/DecenniumDescent');A=R/'docs/audit/2026-10-08/full-game/director-spell-review-129'
Q=A/'CURRENT_SPELL_QUEUE_140.json';IDX=R/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def bind(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}
q=json.loads(Q.read_text(encoding='utf-8'));g=q['currentPendingGroups'][1]
assert g['group']=='rank8-resource6' and g['pendingCount']==6
assert q['currentAuthority']['pending']==162
archive=R/g['archive']['path'];candidate=R/g['candidate']['path']
assert bind(archive)==g['archive'] and bind(candidate)==g['candidate']
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 names=z.namelist();m=json.loads(z.read('MANIFEST.json'));records=m['files'];bad=[];checked=[]
 for rec in records:
  member=rec['path'] if rec['path'] in names else 'sources/'+rec['path']
  if member not in names:bad.append({'path':rec['path'],'reason':'missing'});continue
  b=z.read(member);checked.append(member)
  if len(b)!=rec['bytes'] or sha(b)!=rec['sha256']:bad.append({'path':rec['path'],'reason':'hash-or-length'})
 hidden=[n for n in names if pathlib.PurePosixPath(n).name.startswith('.') or '.tmp' in pathlib.PurePosixPath(n).name.casefold()]
 assert not bad and not hidden
 assert z.read('CANDIDATE.json')==candidate.read_bytes()
 report={'id':'RANK8-RESOURCE6-SOURCE-PREFLIGHT-140','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'currentAuthority':q['currentAuthority'],'group':g['group'],'pendingIds':g['pendingIds'],'sourceArchive':bind(archive),'candidate':bind(candidate),'zipMembers':len(names),'manifestBindings':len(records),'memberBindingsPassed':len(checked),'crcPassed':True,'hiddenTemporaryMembers':hidden,'sourceProgramsExecuted':False,'questions':len(json.loads(candidate.read_text(encoding='utf-8')).get('questions',[])),'failures':bad}
(A/'RANK8_RESOURCE6_SOURCE_PREFLIGHT_140.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
