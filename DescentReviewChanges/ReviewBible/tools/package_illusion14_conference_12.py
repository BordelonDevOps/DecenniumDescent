"""Package the completed Current12 repair using exact frozen predecessor sources."""
from datetime import datetime,timezone
import ast,hashlib,json,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded


def main():
    root=A/'illusion-perception-14-conference-12'; archive=A/'DD_Illusion_Perception_14_Conference_12.zip'
    req=A/'ILLUSION_PERCEPTION_14_CONFERENCE_12_REQUEST.txt';prep=A/'ILLUSION_PERCEPTION_14_CONFERENCE_12_PREPARATION.json'
    assert all(not p.exists() for p in [root,archive,req,prep])
    candidate=R/'data/director/spell_proposals/illusion_perception_14_current_12.json'
    check=A/'ILLUSION_PERCEPTION_14_GRAPPLE_CHECK_12.json'; ch=json.loads(check.read_bytes())
    assert info(candidate)==ch['candidate'] and all(ch['checks'].values())
    d=json.loads(candidate.read_bytes()); assert len(d['spells'])==14 and len(d['currentExamples'])==28 and len(d['conferenceDecisions10'])==16
    oldroot=A/'illusion-perception-14-conference-11'; prior=A/'DD_Illusion_Perception_14_Conference_11.zip'
    original=json.loads((oldroot/'MANIFEST.json').read_bytes())
    priorprep=json.loads((A/'ILLUSION_PERCEPTION_14_CONFERENCE_11_PREPARATION.json').read_bytes())
    assert info(prior)==priorprep['archive']
    sources={}; changed_live=[]
    with zipfile.ZipFile(prior) as z:
        assert z.testzip() is None
        for b in original['files']:
            raw=z.read('files/'+b['path']); assert len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256']
            sources[b['path']]={'binding':b,'raw':raw}
            if info(G/b['path'])!=b: changed_live.append({'originalFrozenBinding':b,'currentLiveBinding':info(G/b['path']),'treatment':'Preserve exact prior bytes at original logical archive path. The original archive, not the mutable live path, is the source for this historical binding.'})
    for p in [candidate,R/'data/director/spell_proposals/illusion_perception_14_current_11.json',A/'ILLUSION_PERCEPTION_14_GRAPPLE_DELTA_12.json',check,R/'tools/repair_illusion14_grapple_12.py',R/'tools/package_illusion14_conference_12.py',oldroot/'MANIFEST.json',oldroot/'README.md']:
        b=info(p);raw=p.read_bytes()
        if b['path'] in sources: assert sources[b['path']]['raw']==raw
        sources[b['path']]={'binding':b,'raw':raw}
    root.mkdir()
    # Reuse the authored request text only, without running the completed repair again.
    tree=ast.parse((R/'tools/repair_illusion14_grapple_12.py').read_text(encoding='utf8'))
    readme=next(node.value.value for node in ast.walk(tree) if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='readme' for t in node.targets))
    readme+='\nThe prior packet remains the exact frozen source for historical file bindings. Navigation changed during intervening development; MANIFEST.json records every such difference. No historical source is silently rebound to newer bytes.\n'
    (root/'README.md').write_text(readme,encoding='utf8',newline='\n')
    manifest={'id':'ILLUSION-PERCEPTION-14-CONFERENCE-12','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'candidate':info(candidate),'files':[x['binding'] for x in sources.values()],'frozenPriorArchive':info(prior),'historicalBindingsDifferingFromLive':changed_live,'counts':{'spells':14,'originalScenarios':28,'currentCases':28,'supplements':3,'questions':16},'authoredCounts':{'reviewed':480,'pending':368},'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}
    (root/'MANIFEST.json').write_bytes(encoded(manifest))
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in ['README.md','MANIFEST.json']:z.write(root/name,name)
        for name,s in sorted(sources.items()):z.writestr('files/'+name,s['raw'])
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for name,s in sources.items():assert z.read('files/'+name)==s['raw']
    b=info(archive)
    req.write_text(f'Please conduct the full illusion/perception14 semantic conference using {archive.name} ({b["bytes"]} bytes; SHA256 {b["sha256"]}). Read Current12 with all14 procedures,28 original/current cases,3 supplements and16 substantive questions plus full exact frozen sources. It supersedes UNSENT11, changing only the overlapping Shadow Step grapple fixture: real Medium5x5 bodies touch initially at distinct centers(0,0,0)/(0,5,0), floorz-3; teleport45ft leaves40ft whole-body gap and ends reach5 grapple. Full before/after preservation supplied. Settle every procedure/question, including the substantive source-specific new authorship in README; provide downloadable full exact corrections at Current12 pointers if needed. Conditional source gaps stay explicit; accepted AC6/DE4 and Fate scopes remain closed. No adoption/runtime/human gameplay/balance/cosmology/domain closure;480/368 unchanged.\n',encoding='utf8',newline='\n')
    prep.write_bytes(encoded({'archive':b,'candidate':info(candidate),'manifest':info(root/'MANIFEST.json'),'request':info(req),'fileCount':len(sources),'frozenPriorArchive':info(prior),'historicalBindingDifferences':len(changed_live),'allMemberHashesVerified':True,'status':'Prepared UNSENT; companion/life10 conference remains actually active.','newRuleAdoptions':0,'runtimeTestsExecuted':0}))
    print(json.dumps({'archive':b,'candidate':info(candidate),'sources':len(sources),'historicalBindingDifferences':len(changed_live),'preparation':info(prep)}))


if __name__=='__main__':main()
