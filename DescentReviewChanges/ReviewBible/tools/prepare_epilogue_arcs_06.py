"""Carry the preserved67-case proposal forward with accepted EPI08-14 dependencies."""
from pathlib import PurePosixPath
from datetime import datetime,timezone
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib,json
from apply_di7_ap_as_01 import G,R,A,info,encoded

def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_bytes())

def main():
    original=A/'DD_Cosmology_Epilogue_Campaign_Arcs_05.zip'
    root=A/'cosmology-epilogue-campaign-arcs-06';archive=A/'DD_Cosmology_Epilogue_Campaign_Arcs_06.zip'
    receipt=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_06_PREPARATION.json'
    assert all(not p.exists() for p in [root,archive,receipt])
    assert info(original)['sha256']=='4e91303bb0dcf0a86abb17aaea3c00a9462b7b1336f9e76beb3b60c5896d7434'
    with ZipFile(original) as z:
        names=z.namelist();assert len(names)==len(set(names))==58
        assert all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts for n in names)
        files={n:z.read(n) for n in names}
    before=dict(files);sources=json.loads(files['SOURCE_BINDINGS.json']);assert len(sources)==44
    checks=[]
    def ck(name,ok):checks.append({'name':name,'passed':bool(ok)});assert ok,name
    for x in sources:
        b=files['sources/'+x['path']];ck('frozen-and-current-'+x['path'],len(b)==x['bytes'] and sha(b)==x['sha256'] and (G/x['path']).read_bytes()==b)
    app=A/'COSMOLOGY_EPILOGUE_RELIC_NULL_01_APPLICATION_CHECK.json';application=read(app)
    ck('complete-module-applied',application['newProvisionalModuleAdopted'] and application['failureCount']==0)
    additions=[R/'data/director/cosmology/epilogue_relic_null_reviewed_01.json',R/'data/director/cosmology/epilogue_relic_null_cases_01.json',R/'docs/mechanics/COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md',R/'docs/director-only/cosmology/EPILOGUE_RELIC_NULL_REVIEWED_01.md',R/'docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md',R/'docs/mechanics/DAMAGE_SHARING_PLAYTEST.md',R/'docs/mechanics/GAMEPLAY_LOOP_CANON.md']
    for p in additions:
        binding=info(p);assert all(v['path']!=binding['path'] for v in sources);sources.append(binding);files['sources/'+binding['path']]=p.read_bytes()
    for n in ['SOURCE_BINDINGS.json','CURRENT_REVIEW_CONTEXT.json','REQUEST.txt','LOCAL_VALIDATION.json','PACKAGE_MANIFEST.json']:
        files['history/revision05/'+n]=before[n]
    now=datetime.now(timezone.utc).isoformat()
    fields=[
      ('ARCX-01','Null fragments, local silence and exposure are distinct',
       'ARCS_MODEL /arcs/0/hook and /arcs/0/map/sites/0/visible propose fragments driving a10-ft acoustic suppression zone. Accepted EPI08–14 gives Null exposure only to an explicitly authored field identity/boundary/clock; a realm name, glow or fragment label alone is not exposure.',
       'Decide explicitly whether each arc site has an actual Residual Null field. If none, print that; if NEW exposure is intended, provide field identity, geometry, clock, first failure and actual purge access without rewriting accepted Null. Preserve the original weaponized-silence premise and distinguish audible V/communication blockage from blanket antimagic.',
       'Use actual elapsed site time across exit/reentry and compare sound-only zone against an explicitly authored exposure field, including real verbal and nonverbal interfaces.'),
      ('ARCX-02','Hush spindle creature lifecycle under qualifying Null damage',
       'ARCS_MODEL /profiles/1 calls the spindle an objectlike Construct destroyed at0; its targets/actions identify a creature. Accepted Null ordinaryNonlivingConstruct replaces damage-caused destruction with Null Disabled0; it does not turn a creature into an object. Site recovery currently names power-off or destruction.',
       'Bind the new actor explicitly to its actual creature lifecycle. Distinguish ordinary destruction, Null Disabled, independent powered-off state, legal detachment and delivered salvage. A creature cannot bypass Null using the adjective objectlike; body mass and serial remain conserved.',
       'Compare ordinary and Veiled roots reducing the same printed spindle to0; operate independent controls, then determine legal fragment removal and finite scrap payment without invented death/loot or duplicate stock.'),
      ('ARCX-03','Damage-root ownership and mechanism hazards',
       'Accepted Null flags roots at creation only when the actual dealer is a character with unsuppressed Veil. Transfers preserve the flag; independent companion attacks and new reflection roots use their actual dealer. Arc machinery has its own force, bolt, cage and loft hazards.',
       'Name actual dealers/roots where necessary. Do not label all Null-themed damage nonlethal. Preserve existing Root/transfer rules and independent non-damage support, source-expiry and cost events.',
       'Trace one Veiled-character attack, one independent construct bolt and one triggered site hazard, with explicit dealer/flag, recipient life branch and any sharing; no controller or fragment-name inference.'),
      ('ARCX-04','Xi cancellation is spell-specific',
       'Accepted Xi requires a single ongoing spell-effect target branch, actual caster and selected target consent, Action/range and an item-bound charge. Arc controls, silence machines, patent obligations and CF-pattern machinery are not automatically ongoing spells.',
       'Keep the relic legal where all spell predicates hold; explain why ordinary machinery or an agreement has no cancellable spell branch. Never broaden it into a universal machine/contract switch or grant charge reset on travel.',
       'Show one ineligible machine/contract attempt with correct Action/charge consequence and one eligible actual source-bound spell branch if the supplied source set contains one; otherwise explain the conditional legal interface without inventing a spell.'),
      ('ARCX-05','Mirror save benefit and finite reformation',
       'Accepted Mirror affects the next WIS save within24 elapsed hours, after actual cancellation/rerolls; final failure shatters it, and CH12 supplies only one lifetime repair using the three actual tabs. Arc saves, long voyages and annual clocks cannot duplicate these resources.',
       'Retain actual save type, pending-benefit consumption, expiry and final-result shattering. An ability check, CON hazard save or calendar deadline is not a WIS save. No arc site silently creates repair stock or a second Sentinel.',
       'Trace an eligible WIS save and an ineligible check/CON save, then an unused24-hour expiry or final failed WIS save, preserving the same item and repair opportunity.'),
      ('ARCX-06','Glove, mask confession and antidote keep narrow scope',
       'Accepted Glove requires real language/visibility and current sincere stance; it is not a loyalty/motive detector. The mask-confession Action purges only Null Veil under its vow/communication predicate. Antidote uses actual finite ingredients and cures only Null Veil.',
       'Do not treat these as proof of contract compliance, automatic translation, compelled confession, mechanical deactivation, general poison/disease cures or permission to mint plant/flame-water stock. Preserve informed choice in the envoy scene.',
       'Run a concrete envoy or salvage interaction with a real language/stance boundary, one actual purge and exact inventory/custody consequences; no knowledge, machine or contract reset follows.'),
    ]
    cross={'recordedAtUtc':now,'status':'Source-linked cross-module questions for actual GPT; no arc rule adopted','currentDependency':info(app),'issues':[{'id':i,'title':t,'evidence':e,'requestedDisposition':r,'requiredWorkedCase':c} for i,t,e,r,c in fields],'newRulesAdopted':False,'sourceInformationDeleted':0}
    files['CROSS_MODULE_REVIEW_06.json']=encoded(cross)
    files['EPI08_14_APPLICATION_RECEIPT.json']=app.read_bytes()
    files['EPI08_14_FULL_MODULE_CONFIRMATION_DOM.txt']=(G/application['confirmation']['path']).read_bytes()
    context=json.loads(before['CURRENT_REVIEW_CONTEXT.json']);context.update(recordedAtUtc=now,packetRevision='06',sourceCount=51,
      relicNullReview='Complete corrected EPI08–14 explicitly accepted in actual Review Continuation Part4 and locally applied as NEW provisional authored playtest reference. Read the four added current module/chapter/case sources, application receipt and actual full-module acceptance. Historical unavailable-return statements in revision05/model seams are superseded only as availability/status; all arc integration still needs this review.',
      currentDependency=info(app),crossModuleQuestions='ARCX-01..06 in CROSS_MODULE_REVIEW_06.json',
      historicalContext='Original revision05 request/context/source list/manifest/validation preserved in history/revision05. Original model and67-case bytes remain unchanged.')
    files['CURRENT_REVIEW_CONTEXT.json']=encoded(context);files['SOURCE_BINDINGS.json']=encoded(sources)
    request=before['REQUEST.txt'].decode();request=request.replace('current revision 05','current revision 06').replace('all 44 supplied source files','all 51 supplied source files').replace('all 44 exact input source identities','all 51 exact input source identities')
    old=next(p for p in request.split('\n\n') if p.startswith('Dependency:'))
    new='Dependency now satisfied: the complete corrected EPI-08–14 module was jointly accepted in actual Review Continuation Part 4 and locally applied. Its exact accepted patch archive SHA-256 is 748593ca501cd43c6557a4101525ed1362d89d3283c7c41bad4070df540aefcb. The added current module, casebook and Player/Director chapters provide that reference; the application receipt and actual acceptance are included. The original 44 source bindings remain unchanged; seven additional current sources bring this packet to 51. Old unavailable-return statements in the unchanged draft/history are obsolete availability status, not an excuse to omit integration. Read CROSS_MODULE_REVIEW_06.json and independently disposition ARCX-01 through ARCX-06, adding at least one explicit authored case with each of those stable IDs. Keep all 67 original arc case IDs and correct expectations explicitly. Earlier accepted modules keep their bounded authority; do not silently rewrite EPI-01–14.'
    request=request.replace(old,new,1)
    request=request.replace('all fifteen review issues, exact source locations','all fifteen review issues plus the six cross-module questions, exact source locations')
    request=request.replace('plus necessary new cases.','plus the six ARCX-01–06 integration cases and any other necessary new cases. At least 73 authored cases, not runtime tests.')
    files['REQUEST.txt']=request.encode()
    ck('original44bindingsunchanged',sources[:44]==json.loads(before['SOURCE_BINDINGS.json']))
    for n in ['ARCS_MODEL.json','CASEBOOK.json','SEMANTIC_REVIEW_03.json','VOYAGE_REFINEMENT_04.json','VOYAGE_GEOMETRY_04A.json','CONTRACT_STATES_05.json','ATMOSPHERE_INTERFACES_06.json','ECONOMY_PATENTS_07.json','SCENE_BOUNDARIES_07A.json']:ck('unchanged-proposal-'+n,files[n]==before[n])
    casebook=json.loads(files['CASEBOOK.json']);ids=[x['id'] for x in casebook['cases']];ck('67-unique-original-cases',len(ids)==len(set(ids))==67)
    ck('no-existing-cross-case-id-collision',not set(ids)&{x[0] for x in fields})
    files['LOCAL_VALIDATION.json']=encoded({'recordedAtUtc':now,'checks':checks,'checkCount':len(checks),'failureCount':0,'scope':'Exact frozen/current source bytes, unchanged proposals and case identity only. No semantic/runtime/human approval.','sourceCount':51,'authoredCases':67,'newCaseSpecifications':6,'newRulesAdopted':False})
    files['PACKAGE_MANIFEST.json']=encoded({'packetRevision':'06','files':[{'path':n,'bytes':len(b),'sha256':sha(b)} for n,b in sorted(files.items()) if n!='PACKAGE_MANIFEST.json']})
    root.mkdir()
    for n,b in files.items():p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
    with ZipFile(archive,'w',ZIP_DEFLATED) as z:
        for n,b in sorted(files.items()):z.writestr(n,b)
    receipt.write_bytes(encoded({'recordedAtUtc':now,'status':'prepared-not-submitted','archive':info(archive),'supersedesForSubmission':info(original),'sourceCount':51,'originalSourceCount':44,'additionalSources':[info(p) for p in additions],'authoredCases':67,'additionalCaseSpecifications':6,'unchangedModel':info(root/'ARCS_MODEL.json'),'unchangedCases':info(root/'CASEBOOK.json'),'localValidation':info(root/'LOCAL_VALIDATION.json'),'dependencyApplied':info(app),'newRulesAdopted':False,'sourceInformationDeleted':0,'campaignEpochChosen':False,'jointReviewComplete':False}))
    print(json.dumps({'preparation':info(receipt),'archive':info(archive),'sourceCount':51,'checks':len(checks),'failures':0,'existingCases':67,'newCaseSpecifications':6}))

if __name__=='__main__':main()
