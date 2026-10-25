"""Fresh reversible application of separately accepted four-ID Information return; no runtime code."""
from pathlib import Path
import json,hashlib,copy,datetime,shutil,sys
sys.stdout.reconfigure(encoding='utf-8')
D=Path(__file__).parent;G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';S=D/'information8_return01_received';E=R/'data/public/spell_candidates/information4_reviewed_129'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def sha(x):return hashlib.sha256(x).hexdigest()
def bind(p):return {'path':p.relative_to(G).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
def fresh(p,b):
 assert not p.exists(),str(p)
 p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def ptr(v,p):
 for k in p.strip('/').split('/'):
  k=k.replace('~1','/').replace('~0','~');v=v[int(k)] if isinstance(v,list) else v[k]
 return v
ap=D/'INFORMATION4_EXACT_ACCEPTANCE_129.json';a=read(ap);ids=['arcane-eye','faction-destiny','legend-lore','prophetic-frenzy'];excluded=['concordant-mindlink','faction-prophecy','find-the-path','resonance-prophecy']
assert a['approvedForCanonicalApplication'] and a['acceptedIdentities']==ids and a['semanticFindings']==[] and not a['canonicalApplied']
for b in a['acceptedFileBindings']+[a['referenceModel']]+a['evidenceReports']:assert bind(G/b['path'])==b
ip=R/'data/public/spell_playtests/authored_review_index.json';raw=ip.read_bytes();old=read(ip);idx=copy.deepcopy(old)
assert bind(ip)==a['canonicalBaseline'] and old['authoredCounts']=={'reviewed':628,'pending':220}
assert all(next(e for e in idx['entries'] if e['id']==sid)['authoredStatus']=='pending-authored-procedure' for sid in ids+excluded)
fresh(D/'authored_review_index.before_information4_129.json',raw)
assert not E.exists();shutil.copytree(S,E)
files=[p for p in S.rglob('*') if p.is_file()]
for p in files:assert p.read_bytes()==(E/p.relative_to(S)).read_bytes()
assert len(files)==114
fresh(E/'MODEL.json',(G/a['referenceModel']['path']).read_bytes())
model=read(E/'MODEL.json');procs=model['completeProcedures'];shared=model['sharedRules']
assert procs==read(E/'PROCEDURES.json')['spells'] and shared[:6]==read(E/'SHARED_RULES.json') and len(shared)==7
assert shared[6]['rule']==procs[2]['procedure'].split('\n\nINFO131-INSTITUTION: ',1)[1]
chapter=R/'docs/spells/candidates/INFORMATION4_REVIEWED_129.md'
text='# Information4 - applied authored review129\n\nArcane Eye, Faction Destiny, Legend Lore and Prophetic Frenzy are independently accepted by INFORMATION4_EXACT_ACCEPTANCE_129.json and selected by INFORMATION4_APPLICATION_129.json. The complete Information8 Return01 evidence is preserved byte for byte alongside a reference envelope assembling its unchanged complete procedure and shared-rule objects.\n\n'+a['scope']+'\n\nHistorical all-eight pending labels and628/220 counts describe delivery; the exact acceptance/application receipts select only these four identities. The institute clause imported by Faction Destiny is reproduced verbatim without accepting Faction Prophecy. No runtime selection is enabled.\n\n'
for s in procs:
 if s['id'] in ids:text+='## '+s['name']+'\n\n'+s['procedure']+'\n\n'
text+='## Exact shared requirements within the selected scope\n\n'
for rule in shared:text+='### '+rule['id']+'\n\n'+rule['rule']+'\n\n'
fresh(chapter,text.encode('utf-8'))
receipt={'id':'INFORMATION4-APPLICATION-129','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'APPLIED_FOUR_AUTHORED_IDENTITIES_WITH_RETAINED_HOLDS','ownerInstruction':'Apply each accepted ordinary-spell batch and continue until all232pending are applied; use Calibration review part6.','acceptedIds':ids,'excludedPendingIds':excluded,'authority':bind(ap),'acceptedReferenceModel':a['referenceModel'],'canonicalModel':bind(E/'MODEL.json'),'exactEvidenceRoot':E.relative_to(G).as_posix(),'evidenceManifest':bind(E/'MANIFEST.json'),'casebook':bind(E/'CASEBOOK.json'),'holds':bind(E/'HOLDS.json'),'chapter':bind(chapter),'runtimeSelectionEnabled':False,'runtimeImplemented':False,'historicalPendingLabelsPreserved':True,'localRuleOrCaseChanges':0,'localPackagingOnly':True,'scope':a['scope']}
rp=D/'INFORMATION4_APPLICATION_129.json';fresh(rp,enc(receipt));ops=[]
for n,e in enumerate(idx['entries']):
 if e['id'] not in ids:continue
 before=copy.deepcopy(e);i=next(i for i,s in enumerate(procs) if s['id']==e['id']);p='/completeProcedures/'+str(i)
 e.update({'authoredStatus':'reviewed-authored-operational-playtest','procedureFile':'../spell_candidates/information4_reviewed_129/MODEL.json','sourceCatalogWholeCardPointer':before['wholeCardPointer'],'wholeCardPointer':p,'wholeCardIdField':'id','procedurePointer':p,'procedureTextPointer':p+'/procedure','sharedRulesPointer':'/sharedRules','manuscript':'../../../docs/spells/candidates/'+chapter.name,'reviewId':receipt['id'],'runtimeSelectionEnabled':False,'completeEnvelopeBinding':bind(E/'MODEL.json'),'authoredAcceptanceReceipt':bind(ap),'authoredApplicationReceipt':bind(rp),'historicalCandidateLabelsPreserved':True,'casebookBinding':bind(E/'CASEBOOK.json'),'retainedHoldsBinding':bind(E/'HOLDS.json'),'completeEvidenceRoot':E.relative_to(G).as_posix(),'acceptedSharedRuleScope':a['scope']})
 ops.append({'pointer':'/entries/'+str(n),'before':before,'after':copy.deepcopy(e)})
idx['authoredCounts']={'reviewed':632,'pending':216};idx['representationCounts']['completeReviewedStandaloneProcedures']=356
idx['additionalStandaloneEnvelopes'].append({'file':'../spell_candidates/information4_reviewed_129/MODEL.json','binding':bind(E/'MODEL.json'),'reviewId':receipt['id'],'acceptedIds':ids,'excludedPendingIds':excluded,'authority':bind(ap),'receipt':bind(rp)})
for k in ['authoredCounts','representationCounts','additionalStandaloneEnvelopes']:ops.append({'pointer':'/'+k,'before':old[k],'after':copy.deepcopy(idx[k])})
assert sum(e['authoredStatus']=='reviewed-authored-operational-playtest' for e in idx['entries'])==632
unchanged=sum(b['id'] not in ids and b==c for b,c in zip(old['entries'],idx['entries']));assert unchanged==844
assert idx.get('scopedInterfaces')==old.get('scopedInterfaces')
reverse=copy.deepcopy(idx)
for o in reversed(ops):
 ks=o['pointer'].strip('/').split('/');v=reverse
 for k in ks[:-1]:v=v[int(k)] if isinstance(v,list) else v[k]
 k=int(ks[-1]) if isinstance(v,list) else ks[-1];assert v[k]==o['after'];v[k]=copy.deepcopy(o['before'])
assert reverse==old
for e in idx['entries']:
 if e['id'] in ids:
  v=read((ip.parent/e['procedureFile']).resolve());assert ptr(v,e['wholeCardPointer'])['id']==e['id'];assert ptr(v,e['procedureTextPointer'])==next(s for s in procs if s['id']==e['id'])['procedure'];assert len(ptr(v,e['sharedRulesPointer']))==7
out=enc(idx);fresh(D/'INFORMATION4_INDEX_OPERATIONS_129.json',enc({'id':'INFORMATION4-INDEX-OPERATIONS-129','before':{'bytes':len(raw),'sha256':sha(raw),'backup':'authored_review_index.before_information4_129.json'},'after':{'bytes':len(out),'sha256':sha(out)},'operations':ops,'reverseSemanticExact':True,'reverseByteExactBackup':True}))
assert ip.read_bytes()==raw;ip.write_bytes(out);assert read(ip)==idx
result={'id':'INFORMATION4-APPLICATION-VALIDATION-129','passed':True,'acceptedIdentitiesApplied':4,'unrelatedIndexEntriesUnchanged':unchanged,'excludedFourRemainUnchangedPending':True,'completeEvidenceFilesPreserved':len(files),'exactEvidencePreserved':True,'newReferenceEnvelopeIsExactAssembly':True,'forwardReverseIndexOperations':len(ops),'counts':idx['authoredCounts'],'representationCounts':idx['representationCounts'],'scopedInterfacesUnchanged':True,'index':bind(ip),'applicationReceipt':bind(rp),'acceptanceReceipt':bind(ap),'runtimeSelectionEnabled':False}
fresh(D/'INFORMATION4_APPLICATION_VALIDATION_129.json',enc(result));print(json.dumps(result,indent=2))
