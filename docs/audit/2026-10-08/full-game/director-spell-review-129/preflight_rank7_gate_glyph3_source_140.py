import hashlib,json,pathlib,zipfile
from datetime import datetime,timezone
R=pathlib.Path('C:/Github/DecenniumDescent');A=R/'docs/audit/2026-10-08/full-game/director-spell-review-129'
ARCH=R/'docs/audit/2026-10-08/full-game/DD_Rank7_Gate_Glyph_3_Source_Conference_01.zip'
CAND=R/'DescentReviewChanges/ReviewBible/data/director/spell_review/rank7_gate_glyph_3_source_conference_01.json'
QUEUE=A/'CURRENT_SPELL_QUEUE_140.json';INDEX=R/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def bind(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}
q=json.loads(QUEUE.read_text(encoding='utf-8'));g=q['currentPendingGroups'][0]
assert g['group']=='rank7-gate-glyph3' and bind(ARCH)==g['archive'] and bind(CAND)==g['candidate']
raw=ARCH.read_bytes()
with zipfile.ZipFile(ARCH) as z:
 assert z.testzip() is None
 names=z.namelist();m=json.loads(z.read('MANIFEST.json'));candidate=json.loads(z.read('CANDIDATE.json'));preflight=json.loads(z.read('PREFLIGHT.json'))
 records=m['files'];bad=[];checked=[]
 for rec in records:
  member=rec['path'] if rec['path'] in names else 'sources/'+rec['path']
  if member not in names:bad.append({'path':rec['path'],'reason':'missing'});continue
  b=z.read(member);checked.append(member)
  if len(b)!=rec['bytes'] or sha(b)!=rec['sha256']:bad.append({'path':rec['path'],'reason':'hash-or-length'})
 assert len(names)==93 and len(records)==89 and len(checked)==89 and not bad
 hidden=[n for n in names if pathlib.PurePosixPath(n).name.startswith('.') or '.tmp' in pathlib.PurePosixPath(n).name.casefold()]
 assert not hidden
 assert z.read('CANDIDATE.json')==CAND.read_bytes()
 assert candidate['id']=='RANK7-GATE-GLYPH-3-SOURCE-CONFERENCE-01'
 report={'id':'RANK7-GATE-GLYPH3-SOURCE-PREFLIGHT-140','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'authority':q['currentAuthority'],'pendingGroup':g['group'],'pendingIds':g['pendingIds'],'sourceArchive':bind(ARCH),'candidate':bind(CAND),'zipMembers':len(names),'manifestBindings':len(records),'memberBindingsPassed':len(checked),'crcPassed':True,'hiddenTemporaryMembers':hidden,'sourceProgramsExecuted':False,'liveSourceProgramsExecuted':False,'questions':[x['id'] for x in candidate['questions']],'spellRecords':[x['spellId'] for x in candidate['records']],'futureCaseRequirements':len(candidate['futureCaseRequirements']),'currentAcceptedInterfaceComparisons':len(candidate['currentAcceptedInterfaceComparisons']),'completeAcceptedCounterparts':len(candidate['completeAcceptedCounterparts']),'pendingComparisonSources':len(candidate['pendingComparisonSources']),'historicalIndexSnapshotSuperseded':True,'failures':bad}
(A/'RANK7_GATE_GLYPH3_SOURCE_PREFLIGHT_140.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
