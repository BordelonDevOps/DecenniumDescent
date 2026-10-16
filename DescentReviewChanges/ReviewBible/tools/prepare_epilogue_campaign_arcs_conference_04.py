"""Bundle the current contract and atmosphere successors without claiming submission."""
from datetime import datetime,timezone
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib,json,shutil
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_epilogue_campaign_arcs_conference_03 import REQUEST as OLD_REQUEST
def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    now=datetime.now(timezone.utc).isoformat();local=A/'cosmology-epilogue-campaign-arcs-local-draft-01'
    previous=A/'cosmology-epilogue-campaign-arcs-03';packet=A/'cosmology-epilogue-campaign-arcs-04';archive=A/'DD_Cosmology_Epilogue_Campaign_Arcs_04.zip';receipt=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_04_PREPARATION.json'
    assert all(not p.exists() for p in [packet,archive,receipt])
    contract=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_CONTRACT_STATES_05.json';air=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ATMOSPHERE_INTERFACES_06.json'
    assert read(air)['model']==info(local/'ARCS_MODEL.json') and read(air)['casebook']==info(local/'CASEBOOK.json')
    assert read(local/'CASEBOOK.json')['count']==51 and read(contract)['failureCount']==read(air)['failureCount']==0
    shutil.copytree(previous,packet)
    bindings=read(packet/'SOURCE_BINDINGS.json');original=G/'docs/reference/Player_Rulebook_v6_source_text.txt';row=info(original)
    assert row['sha256']=='a346670f4244efe3641cfb06814819d83ffb8512153858205f0621bd8ab8a04b'
    assert row['path'] not in {x['path'] for x in bindings};bindings.append(row);dest=packet/'sources'/row['path'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(original.read_bytes())
    for source in bindings:
        raw=(packet/'sources'/source['path']).read_bytes();assert len(raw)==source['bytes'] and sha(raw)==source['sha256'] and (G/source['path']).read_bytes()==raw
    assert len(bindings)==43;(packet/'SOURCE_BINDINGS.json').write_bytes(encoded(bindings))
    for name in ['ARCS_MODEL.json','CASEBOOK.json']:(packet/name).write_bytes((local/name).read_bytes())
    for p,name in [(contract,'CONTRACT_STATES_05.json'),(air,'ATMOSPHERE_INTERFACES_06.json')]:(packet/name).write_bytes(p.read_bytes())
    prefix='''CURRENT REVISION04: Read CONTRACT_STATES_05.json and ATMOSPHERE_INTERFACES_06.json as well as the current complete model,51-case casebook and preserved earlier audit/voyage files. The source set is43files: all prior42 unchanged plus the exact original Player_Rulebook_v6_source_text.txt, whose hash matches the source-reference header. The older reviews remain dated history; current model and cases are the exact bytes identified in CURRENT_REVIEW_CONTEXT.

The new local contract procedure proposes record numbering and fixed400day due timestamps; one fixed first-rejection grace per record; genuine pending-review and unavailable-channel protection; a refund requiring at least one accepted statement and all originally due statements accepted; no demand for an undued new-year statement at exit; finite original-deposit custody; true-death termination distinct from Downed/Undead type. Independently challenge all these choices, simultaneous ordering, notice, missing paper and early/late exits. Preserve all51IDs and original source meaning; detailed terms are NEW, not approved law or canon.

The local atmosphere successor proposes nonmagical cold-inhalation plus thin-air fatigue, one CON15save, and14exact source-bound dispositions. Some are direct source applications; natural climate-acclimation advantage, component-selection and passive-completion ordering are explicitlyNEW interpretations for your review. No ancestry/class file changed. Preserve actual costs, minimum levels, selection, windows, one-minute continuity and three-round expiry. Do not assume that the source-reference’s Chapter5 mention supplied a numerical climate rule: the targeted original-extract reading did not establish one. Check the actual source before accepting or correcting the local completions.

Finite crew/scrap payment custody and a substantive patent-knowledge/free-will arc remain underdeveloped. Complete those rather than treating numerical administrative closure as sufficient adventure design. The ordinary voyage itself remains the previous complete32100second sample; contract/atmosphere edits did not change that route schedule. EPI08–14 exact archive remains unretrieved and unreviewed locally, so cross-module adoption is still open. Nothing in this packet is submitted or jointly adopted until actual conference occurs.

'''
    request=OLD_REQUEST.replace('revision03','revision04').replace('28case IDs','51case IDs').replace('42frozen','43frozen').replace('all28IDs','all51IDs').replace('all28current','all51current').replace('all42 supplied','all43 supplied').replace('Finish the unresolved annual contract operating state:','Review and complete the proposed annual contract operating state:')
    (packet/'REQUEST.txt').write_text(prefix+request,encoding='utf-8',newline='\n')
    validation={'recordedAtUtc':now,'model':info(local/'ARCS_MODEL.json'),'casebook':info(local/'CASEBOOK.json'),'frozenSourcesVerifiedAgainstCurrentAndPacket':43,'contractEvidence':'CONTRACT_STATES_05.json','contractChecks':52,'atmosphereEvidence':'ATMOSPHERE_INTERFACES_06.json','atmosphereChecks':68,'failureCount':0,'scope':'Exact current source/package bytes, retained case IDs and explicitly bounded inherited source/arithmetic checks. Counts overlap and are not a total of independent gameplay tests. No semantic/runtime/human certification.','newRulesAdopted':False,'runtimeTestsExecuted':0,'humanPlaytested':False}
    (packet/'LOCAL_VALIDATION.json').write_bytes(encoded(validation))
    context=read(packet/'CURRENT_REVIEW_CONTEXT.json');context.update(recordedAtUtc=now,packetRevision='04',sourceCount=43,authoredCases=51,currentLocalModel=info(local/'ARCS_MODEL.json'),currentLocalCases=info(local/'CASEBOOK.json'),currentValidation=validation,contractStates=info(contract),atmosphereInterfaces=info(air),openJointReviewIssues='All current local choices need actual GPT semantic review. Contract05/atmosphere06 now propose resolutions for ARC03-07/08/09; finite wage/scrap custody, substantive patent/free-will design and EPI08–14 integration remain undeveloped/open.',status='prepared-not-submitted; all later arc procedures remain unadopted')
    (packet/'CURRENT_REVIEW_CONTEXT.json').write_bytes(encoded(context))
    entries=[{'path':p.relative_to(packet).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(packet.rglob('*')) if p.is_file() and p!=packet/'PACKAGE_MANIFEST.json']
    (packet/'PACKAGE_MANIFEST.json').write_bytes(encoded({'files':entries}))
    with ZipFile(archive,'w',ZIP_DEFLATED) as z:
        for p in sorted(packet.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(packet).as_posix())
    with ZipFile(archive) as z:
        assert set(z.namelist())=={e['path'] for e in entries}|{'PACKAGE_MANIFEST.json'}
        for e in entries:
            raw=z.read(e['path']);assert len(raw)==e['bytes'] and sha(raw)==e['sha256']
    receipt.write_bytes(encoded({'recordedAtUtc':now,'status':'prepared-not-submitted','archive':info(archive),'supersedesForSubmission':info(A/'DD_Cosmology_Epilogue_Campaign_Arcs_03.zip'),'sourceCount':43,'authoredCases':51,'contractStates':info(contract),'atmosphereInterfaces':info(air),'currentModel':info(local/'ARCS_MODEL.json'),'currentCases':info(local/'CASEBOOK.json'),'sourceInformationDeleted':0,'newRulesAdopted':False,'campaignEpochChosen':False,'runtimeTestsExecuted':0,'humanPlaytested':False,'jointReviewComplete':False,'dependency':'Restore actual GPT exchange; retrieve/review EPI08–14 before cross-module adoption.'}))
    print(json.dumps({'preparation':info(receipt),'archive':info(archive),'sources':43,'cases':51,'submitted':False}))
if __name__=='__main__':main()
