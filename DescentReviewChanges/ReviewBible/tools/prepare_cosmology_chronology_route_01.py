"""Freeze original conference sources plus the verified operating successor."""
from datetime import datetime,timezone
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib,json
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    root=A/'cosmology-chronology-research-route-01';archive=A/'DD_Cosmology_Chronology_Research_Route_01.zip'
    receipt=A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_PREPARATION.json'
    assert all(not p.exists() for p in [root,archive,receipt])
    old=A/'cosmology-souls-research-01';bindings=read(old/'SOURCE_BINDINGS.json');sources={}
    for row in bindings:
        raw=(old/'sources'/row['path']).read_bytes()
        assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
        sources[row['path']]=raw
    chronology=read(R/'data/director/cosmology/chronology_research_sites_draft_01.json')
    extra=[x['path'] for x in chronology['sourceBindings']]+[
      'DescentReviewChanges/ReviewBible/data/director/cosmology/souls_research_reviewed_01.json',
      'DescentReviewChanges/ReviewBible/docs/director-only/cosmology/SOULS_RESEARCH_REVIEWED_01.md',
      'docs/audit/2026-10-08/full-game/COSMOLOGY_SOULS_RESEARCH_01_APPLICATION_CHECK.json',
      'docs/audit/2026-10-08/full-game/COSMOLOGY_SOULS_RESEARCH_01_CONFIRMED_PATCH.json',
      'docs/audit/2026-10-08/full-game/ORIGINAL_COSMOLOGY_EPILOGUE_RULE_INVENTORY_01.json']
    for name in extra:
        if name not in sources:sources[name]=(G/name).read_bytes()
    now=datetime.now(timezone.utc).isoformat();root.mkdir()
    source_rows=[]
    for name,raw in sources.items():
        p=root/'sources'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
        source_rows.append({'path':name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    (root/'SOURCE_BINDINGS.json').write_bytes(encoded(source_rows))
    draft=(A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_REQUEST_DRAFT.txt').read_text(encoding='utf-8')
    request=draft.replace('NEXT CONFERENCE DRAFT — not submitted and no canon decision made by this file.\n\n','',1).replace('Once the souls/Research operating candidate is verified, continue','The souls/Research operating candidate is verified and locally adopted with the explicitly confirmed patch. Continue',1)
    (root/'REQUEST.txt').write_text(request,encoding='utf-8',newline='\n')
    context={'reviewId':'COSMOLOGY-CHRONOLOGY-RESEARCH-ROUTE-01','recordedAtUtc':now,'sourceCount':len(source_rows),'scope':'CE01–CE08 plus concrete new provisional route; existing EPI01–17 next-work ordering; no automatic cosmological identity or epoch adoption',
      'sourceAuthority':'Original cosmology/Matrix/World and explicit owner corrections first. The saved website is an authored source presentation, not proof of objective completeness.',
      'currentSoulsApplication':info(A/'COSMOLOGY_SOULS_RESEARCH_01_APPLICATION_CHECK.json'),
      'currentOperatingRules':'Read souls_research_reviewed_01.json/currentStateModel and SOULS_RESEARCH_REVIEWED_01.md. Frozen earlier souls drafts/returns are history. The application patch restores KT3 Dazed endpoint and corrects PT1 name.',
      'historicalWorkflowOverride':'Part3 is active. Planes and souls/Research are verified within scope. No continuation approval is pending. Historical workflow strings in source drafts do not override this status.',
      'frozenInputPolicy':'The79original souls-packet files remain byte-identical; supplementary current artifacts are additional frozen inputs. Source hashes refer to these supplied bytes, not all live navigation.',
      'stillOpen':['epoch/calendar bridge','Choir chronology/named Harmony relation','OldGod/Ul’nak/Binding/Interstice identities','actual library holdings and L2 placement','epilogue operating adoption','runtime/human balance/whole-game flow'],
      'newSourceInformationDeleted':0,'publishRequestedByThisPacket':False}
    (root/'CURRENT_REVIEW_CONTEXT.json').write_bytes(encoded(context))
    payload=[]
    for p in sorted(root.rglob('*')):
        if p.is_file():payload.append({'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    (root/'PACKAGE_MANIFEST.json').write_bytes(encoded({'reviewId':context['reviewId'],'sourceCount':len(source_rows),'payloads':payload}))
    with ZipFile(archive,'w',ZIP_DEFLATED) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(root).as_posix())
    receipt.write_bytes(encoded({'recordedAtUtc':now,'status':'prepared, not yet submitted','archive':info(archive),'frozenSources':len(source_rows),'prior79Unchanged':True,'currentSoulsApplication':context['currentSoulsApplication'],'request':info(root/'REQUEST.txt'),'sourceInformationDeleted':0}))
    print(json.dumps(read(receipt)))

if __name__=='__main__':main()
