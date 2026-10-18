"""Package the complete unaccepted control15 procedures and repaired case records."""
from datetime import datetime,timezone
import json,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded


def main():
    oldroot=A/'control-15-conference-11';root=A/'control-15-conference-12'
    archive=A/'DD_Control_15_Conference_12.zip';prep=A/'CONTROL_15_CONFERENCE_12_PREPARATION.json';req=A/'CONTROL_15_CONFERENCE_12_REQUEST.txt'
    assert all(not p.exists() for p in [root,archive,prep,req])
    source=R/'data/director/spell_proposals/control_15_current_12.json';d=json.loads(source.read_bytes())
    old=json.loads((oldroot/'MANIFEST.json').read_bytes());paths={};checks=[]
    for b in old['files']:
        p=G/b['path'];assert info(p)==b,b['path'];paths[p]=b;checks.append({'source':b,'exactBytesVerified':True})
    for p in [source,A/'CONTROL_15_GEOMETRY_DELTA_12.json',A/'CONTROL_15_GEOMETRY_CHECK_12.json',R/'tools/repair_control15_geometry_12.py',R/'tools/package_control15_conference_12.py',oldroot/'MANIFEST.json']:
        paths[p]=info(p)
    assert len(d['spells'])==15 and len(d['currentExamples'])==30 and len(d['conferenceQuestions10'])==13
    root.mkdir()
    manifest={'id':'CONTROL15-CONFERENCE12','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'candidate':info(source),'files':list(paths.values()),'counts':{'spells':15,'originalScenarios':30,'currentCases':30,'questions':13},'conditionalBranchesAreNotFullyProvedGames':True,'authoredCounts':d['countsUnchanged'],'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}
    (root/'MANIFEST.json').write_bytes(encoded(manifest))
    readme='''# Control15 substantive conference12

Read the complete current candidate identified by MANIFEST.json, including all15 original proposals/current full procedures,30 original scenario texts,30 current cases and13 genuine conference questions. Complete accepted and pending counterparts and all prior source/history files remain supplied. No rule selection is implied by this package.

Current12 preserves Current11 and changes29 current case records with complete reversible before/after evidence in CONTROL_15_GEOMETRY_DELTA_12.json. Real Medium bodies occupy5x5ft with explicitly measured height6; the chosen coordinate origin leaves centers atz1 and actual floorz-2. Nonphysical apparent4x4x4 images are separately classified. Vaskor's source-only CR8 case is unchanged; no bestiary profile or companion CR/check proficiency is invented.

Review the whole-body consequences: helper/grappler separation; twelve guards at5ft spacing; first Group Illusion contact at5.5ft; Mind Fog entry after2.5ft; Mental Prison expands the actual body by5ft per side; the original10ft safe Eyebite retreat retains a corrected full-body support edge. The five actual Lesser Antimagic examples now place their chosen point9ft from the caster, within its actual10ft range. A caster may intersect its own exempt field. When its later legal Minor Illusion commitment changes concentration, the old field ends before the new payload; this inherits the full accepted source and grants no new Action. Paid Ready, phase clocks, suppression history and original scenario obligations remain.

Resolve all13 design questions explicitly, retaining settled accepted interfaces and conditional missing-profile/Quicken branches. Return a downloadable review with actual per-spell and per-question dispositions and full exact source-linked replacements where needed. No catalog membership, runtime, human gameplay, balance, cosmology,75-domain closure or release approval is requested.480 reviewed/368 pending remain unchanged.
'''
    (root/'README.md').write_text(readme,encoding='utf8',newline='\n')
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        z.write(root/'README.md','README.md');z.write(root/'MANIFEST.json','MANIFEST.json')
        for p,b in sorted(paths.items(),key=lambda x:x[1]['path']):z.write(p,'sources/'+b['path'])
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for p,b in paths.items():assert z.read('sources/'+b['path'])==p.read_bytes()
    b=info(archive)
    req.write_text(f'Please conduct the control15 substantive conference using {archive.name} ({b["bytes"]} bytes; SHA256 {b["sha256"]}). This replaces UNSENT11 with full Current12 and preserved before/after body/range repairs; all15 procedures,30 original/current scenarios and13 genuine questions remain. Read the full candidate and sources, not only the repair summary. Actual Medium5x5 bodies require real clearance, guards5ft apart, illusion contact5.5ft, Mind Fog boundary52.5, actual Mental Prison body expansion and whole-body safe ledge. Five actual Lesser Antimagic casts now place the field9ft away, within10ft; own-family exemption and genuine concentration transition remain as accepted. Vaskor/CR2/companion-contest and Quicken gaps stay explicit. Resolve all13 questions and return complete source-linked correction/disposition files; no runtime, adoption, balance, cosmology or domain closure.\n',encoding='utf8',newline='\n')
    prep.write_bytes(encoded({'archive':b,'candidate':info(source),'manifest':info(root/'MANIFEST.json'),'request':info(req),'sourceCount':len(paths),'verifiedPriorSources':len(checks),'allArchiveFilesVerified':True,'status':'Prepared UNSENT; actual companion/life10 conference remains active.','newRuleAdoptions':0,'runtimeTestsExecuted':0}))
    print(json.dumps({'archive':b,'candidate':info(source),'sources':len(paths),'preparation':info(prep)}))


if __name__=='__main__':main()
