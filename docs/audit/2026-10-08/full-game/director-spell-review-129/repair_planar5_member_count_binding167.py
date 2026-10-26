from pathlib import Path
import hashlib,json,os
ROOT=Path.cwd().resolve()
AUDIT=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
PKG=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8planar5_reviewed_166'
INDEX=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
MODEL=PKG/'MODEL.json';APP=AUDIT/'PLANAR5_APPLICATION_167.json';OPS=AUDIT/'PLANAR5_INDEX_OPERATIONS_167.json';PENDING=AUDIT/'CURRENT113_PENDING_IDENTITY_AUDIT_167.json';QUEUE=AUDIT/'CURRENT_SPELL_QUEUE_167.json';HANDOFF=AUDIT/'CURRENT_HANDOFF_167.json'
IDS=['demiplane','maze','planar-seal','seal-of-banishment','gloom-bind']
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def jb(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def write(p,v):p.write_bytes(jb(v))
def bind(path,rel=None):
 b=path.read_bytes();return {'path':rel or path.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b)}
model=read(MODEL);app=read(APP);ops=read(OPS);pending=read(PENDING);queue=read(QUEUE);handoff=read(HANDOFF)
index_raw=INDEX.read_bytes();index=json.loads(index_raw.decode('utf-8-sig'));rows={r['id']:r for r in index['entries']}
assert len(model['returnArchiveOnlyMembers'])==6 and all(x.startswith('accepted-comparisons/') for x in model['returnArchiveOnlyMembers'])
assert app['acceptedIds']==IDS and ops['onlyIdentityIds']==IDS
assert app['candidateEnvelope']['sha256']==sha(MODEL.read_bytes())
assert all(rows[s]['completeEnvelopeBinding']==app['candidateEnvelope'] for s in IDS)
assert all(rows[s]['authoredApplicationReceipt']==bind(APP) for s in IDS)
assert ops['after']['sha256']==sha(index_raw) and ops['after']['bytes']==len(index_raw)
assert all(next(o for o in ops['operations'] if o['identity']==s)['after']==rows[s] for s in IDS)
# Correct the recorded count and clarify that all six remain preserved inside the fully audited return ZIP.
model['returnArchiveOnlyRationale']='Six accepted-comparison snapshots have long hash-prefixed filenames that exceed Windows path limits when unpacked under the candidate package. All six and every other return member remain byte-exact in DIRECTOR_RETURN_ARCHIVE.zip and were independently checked against the internal and delivery manifests.'
write(MODEL,model)
model_binding=bind(MODEL,f'{PKG.relative_to(ROOT).as_posix()}/MODEL.json')
app['candidateEnvelope']=model_binding
write(APP,app)
app_binding=bind(APP)
for sid in IDS:
 rows[sid]['completeEnvelopeBinding']=model_binding
 rows[sid]['authoredApplicationReceipt']=app_binding
index['additionalStandaloneEnvelopes'][-1]['binding']=model_binding
after_raw=jb(index);tmp=INDEX.with_suffix('.json.planar5-binding-repair.tmp');tmp.write_bytes(after_raw);os.replace(tmp,INDEX)
for op in ops['operations']:op['after']=rows[op['identity']]
ops['after']={'path':INDEX.relative_to(ROOT).as_posix(),'bytes':len(after_raw),'sha256':sha(after_raw)}
write(OPS,ops)
pending['indexBinding']=bind(INDEX);write(PENDING,pending)
queue['pendingIdentityAudit']['sha256']=sha(PENDING.read_bytes());write(QUEUE,queue)
handoff['currentIndexBinding']=bind(INDEX,'authority/authored_review_index.json')
handoff['currentQueueBinding']=bind(QUEUE)
handoff['pendingIdentityAudit']={'id':pending['id'],'path':PENDING.name,'pendingCount':113,'sha256':sha(PENDING.read_bytes())}
write(HANDOFF,handoff)
print(json.dumps({'status':'REBOUND','model':model_binding,'application':app_binding,'index':bind(INDEX),'pending':bind(PENDING),'queue':bind(QUEUE),'handoff':bind(HANDOFF)},indent=2))
