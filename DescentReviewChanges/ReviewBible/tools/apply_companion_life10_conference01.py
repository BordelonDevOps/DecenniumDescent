"""Replay actual GPT additions into a new preserved layer; no adoption or current cases."""
from copy import deepcopy
from datetime import datetime,timezone
import hashlib,json,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_ac5_current_interfaces_01 import at

def main():
    out=R/'data/director/spell_review/companion_life_10_conference_applied_02.json';check=A/'COMPANION_LIFE_10_CONFERENCE_APPLIED_02_CHECK.json';receipt=A/'COMPANION_LIFE_10_CONFERENCE_APPLIED_02.json'
    assert all(not p.exists() for p in [out,check,receipt]);root=A/'companion-life10-conference-01-review';pp=root/'PROPOSED_CORRECTIONS.json';proposal=json.loads(pp.read_bytes());source=G/proposal['targetCandidate']['path'];originalraw=source.read_bytes();original=json.loads(originalraw);assert info(source)==proposal['targetCandidate'];current=deepcopy(original);checks=[]
    def ck(label,v):checks.append({'check':label,'passed':bool(v)});assert v,label
    archive=A/'DD_Companion_Life_10_Conference_01.zip';rb=json.loads((A/'COMPANION_LIFE_10_CONFERENCE_01_RECEIPT.json').read_bytes());ck('Actual returned archive unchanged',info(A/rb['returnedArchive']['path'].split('/')[-1])==rb['returnedArchive'])
    with zipfile.ZipFile(archive) as z:
        manifest=json.loads(z.read('MANIFEST.json'));frozen={}
        for b in manifest['sources']:
            raw=z.read(b['archivePath']);ck('Frozen source bytes '+b['path'],len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256']);frozen[b['path']]=raw
        ck('Frozen target is actual original',frozen[proposal['targetCandidate']['path']]==originalraw)
        for b in original['sourceBindings']:ck('Nested binding '+b['path'],len(frozen[b['path']])==b['bytes'] and hashlib.sha256(frozen[b['path']]).hexdigest()==b['sha256'])
    expected=[f'/records/{i}/conferenceAuthorshipProposal01' for i in range(10)]+['/conferenceSharedRuleProposals01'];ck('Exact11 operation paths',[o['pointer'] for o in proposal['operations']]==expected)
    for n,o in enumerate(proposal['operations']):
        ck('Only reversible addition '+o['id'],o['op']=='add' and o['expectedBefore']=={'present':False} and o['targetFile']==proposal['targetCandidate']['path']);parts=o['pointer'].split('/');key=parts[-1];parent=at(current,'/'.join(parts[:-1])) if len(parts)>2 else current;ck('Real existing absent field '+o['id'],isinstance(parent,dict) and key not in parent);parent[key]=deepcopy(o['completeValue']);ck('Exact proposal value '+o['id'],o['completeValue']==(proposal['procedureProposals'][n] if n<10 else proposal['sharedRuleProposals']))
    for n,(old,rec) in enumerate(zip(original['records'],current['records'])):
        p=rec['conferenceAuthorshipProposal01'];ck('Same spell '+str(n),p['spellId']==old['spellId']);ck('Exact preserved procedure '+str(n),p['historicalCompleteProcedureUnchanged']==old['completeEarlierRecordUnchanged']['procedure']);ck('Exact preserved access '+str(n),p['completeSourceAndAccessUnchanged']==old['completeCurrentCatalogSourceAndAccess']);rest=deepcopy(rec);del rest['conferenceAuthorshipProposal01'];ck('Other record bytes meaning unchanged '+str(n),rest==old)
    ck('All20 originals exact',current['all20HistoricalScenarioTexts']==original['all20HistoricalScenarioTexts']);ck('Four full shared contexts exact',current['completeOriginalSharedProposalsUnchanged']==original['completeOriginalSharedProposalsUnchanged']);ck('No new current vectors',current['newCurrentVectorsSubmitted']==0);ck('Counts unchanged',current['countsUnchanged']=={'reviewed':480,'pending':368})
    reverse=deepcopy(current)
    for o in reversed(proposal['operations']):
        parts=o['pointer'].split('/');key=parts[-1];parent=at(reverse,'/'.join(parts[:-1])) if len(parts)>2 else reverse;ck('Reverse exact addition '+o['id'],parent[key]==o['completeValue']);del parent[key]
    ck('Reverse complete object equals original',reverse==original);ck('Original file bytes retained',source.read_bytes()==originalraw)
    canon=lambda d:hashlib.sha256(json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf8')).hexdigest()
    ck('Reverse canonical SHA',canon(reverse)==canon(original));out.write_bytes(encoded(current));check.write_bytes(encoded({'candidate':info(out),'original':info(source),'proposal':info(pp),'checks':checks,'checkCount':len(checks),'failures':0,'operations':11,'frozenSourcesVerified':47,'nestedSourcesVerified':len(original['sourceBindings']),'originalCases':20,'newCurrentVectors':0,'reverseCanonicalSha256':canon(reverse),'scope':'Structural replay and complete history preservation; actual proposed rule texts locally read. This is not runtime or final exact acceptance.'}));receipt.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'original':info(source),'appliedProposalLayer':info(out),'actualReviewReceipt':info(A/'COMPANION_LIFE_10_CONFERENCE_01_RECEIPT.json'),'replayCheck':info(check),'operationsAppliedToNewLayer':11,'originalReplaced':False,'status':'SOURCE_CONFERENCE_PROPOSAL_LAYER_APPLIED_NOT_ADOPTED','interpretation':'Original root/record statuses remain exact historical text. conferenceAuthorshipProposal01 and conferenceSharedRuleProposals01 hold the actual returned proposed text. Complete current encounter authorship and final exact acceptance remain required.','newCurrentVectors':0,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}));print(json.dumps({'appliedLayer':info(out),'receipt':info(receipt),'checks':len(checks),'operations':11,'reverseExact':True}))

if __name__=='__main__':main()
