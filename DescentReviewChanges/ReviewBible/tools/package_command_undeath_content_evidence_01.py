"""Preserve the expanded search and exact historical/current classification distinction."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded
from audit_bestiary_history import monsters

def read(p):return json.loads(p.read_bytes())
def main():
 root=A/'command-undeath-content-evidence-01';out=A/'COMMAND_UNDEATH_CONTENT_EVIDENCE_01.json';zp=A/'DD_Command_Undeath_Content_Evidence_01.zip';prep=A/'COMMAND_UNDEATH_CONTENT_EVIDENCE_01_PREPARATION.json';assert not any(p.exists() for p in [root,out,zp,prep]);searchp=A/'COMMAND_UNDEATH_TARGET_SOURCE_SEARCH_03.json';search=read(searchp);current=[];buffers={};checks=[]
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 for b in search['frozenSources']:
  raw=Path(chr(92)*2+'?'+chr(92)+str(G/b['frozenCopy'])).read_bytes();ck('Exact expanded search source '+b['path'],len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256']);buffers['sources/'+b['path']]=raw
 for p in [G/'Bestiary.xlsx',R/'Bestiary.xlsx']:
  rows,_,_,headers=monsters(p);row=next(x for x in rows if x['worksheetRow']==404);ck('Current row404 is CR2 Construct '+str(p),row['cellsByHeader']['Type']=='Construct' and row['cellsByHeader']['Challenge']=='2');current.append({'source':info(p),'sheet':'Monsters','row':404,'completeRow':row,'columnBindings':{label:col for col,label in headers.items()}})
 aliasp=R/'scripts/scrub_bestiary_ip.py';lines=aliasp.read_text(encoding='utf8').splitlines();aliases=[{'line':i+1,'exactText':s} for i,s in enumerate(lines) if '"Marut": "Order-Drone Covenant Engine"' in s or '"Order-Drone Marut": "Order-Drone Covenant Engine"' in s];ck('Two explicit retained aliases',len(aliases)==2)
 for p in [searchp,aliasp,R/'tools/package_command_undeath_content_evidence_01.py',G/'docs/bestiary/Decennium_Descent_Monster_Manual_Canon_Rewrite_Source_Pack/README.md',R/'docs/bestiary/Decennium_Descent_Monster_Manual_Canon_Rewrite_Source_Pack/README.md']:
  buffers['sources/'+p.relative_to(G).as_posix()]=p.read_bytes()
 ck('24 complete parsed groups31 source paths',search['workbookGroupCount']==search['parsedWorkbookGroups']==24 and search['workbookPathCount']==31 and search['unparsedWorkbookGroups']==0)
 ck('8 historical matches and zero144-source text matches',len(search['workbookExactCR2UndeadMatches'])==8 and search['markdownEntryCount']==144 and not search['markdownExactCR2UndeadMatches'])
 ck('No Monsters formulas requiring recalculation',all(r['monstersFormulaCount']==0 for r in search['workbookResults']))
 findings={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PREPARED_UNSENT_EVIDENCE_SUPPLEMENT_NOT_PROFILE_ADOPTION','expandedSearch':info(searchp),'completeHistoricalMatches':search['workbookExactCR2UndeadMatches'],'completeCurrentRows':current,'explicitExistingAliasEvidence':{'source':info(aliasp),'lines':aliases},'interpretation':'Eight historical byte-distinct workbook variants contain exactCR2/Undead at row404, under Marut or its explicit existing Covenant Engine alias. Current main and ReviewBible row404 are CR2 Construct. Historical records either omit combat stats or carry generator/NeedsReview warnings and inconsistent Tiny/Medium,HP45/50/68. This does not supply an authoritative native CR2 Undead target; reverting Type would be a new substantive change, not restoring a proven current rule. No creature dossier for this name exists in the144 searched source-pack entries; no broader absence claim is made.','originalSearchScopePreserved':'The earlier11-JSON no-match finding was correctly bounded. This expanded evidence adds historical workbook matches and does not falsify that narrower result. The unchanged exact Companion05 packet retains its dated bounded statement and two whole-case holds.','proposedConferenceQuestions':['Concur that the historical row404 type/rating does not clear either Command Undeath hold, given the current Construct type and generator provenance.','Choose the next separate native NPC content/profile review using actual source material and a justified exactCR2 role; do not re-rate Ferry WraithCR0 or assign2 to the existing unrated conjured Undead profiles.','Any new profile must explicitly supply complete body/anatomy/abilities/actions/defenses/life/gear/agency/command/suppression and provenance; numerical rating remains a separate playtest gate. No undocumented soul/native-plane/cosmology is required to resolve the mechanical content gap.'],'countsUnchanged':{'reviewed':525,'pending':323},'newNPCProfiles':0,'newCRAssignments':0,'newRuleAdoptions':0,'workbooksEdited':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}
 root.mkdir();out.write_bytes(encoded(findings));buffers['EVIDENCE.json']=out.read_bytes();buffers['CHECKS.json']=encoded({'checks':checks,'checkCount':len(checks),'failures':0,'scope':'Read-only source/hash/classification comparison; no creature semantic approval.'})
 buffers['README.md']=b'Expanded Command Undeath content evidence. Read EVIDENCE.json and full search03 report. Eight historical workbook matches are not eligible current profiles: both current workbooks identify row404 as Construct. Preserve historical type/name/statistics/review warnings and all original source bytes. Both positive spell cases remain held. Discuss a separate native NPC profile/rating review; do not alter the sealed Companion exact05 package or its dated bounded findings.\n'
 buffers['MANIFEST.json']=encoded({'files':[{'archivePath':n,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()} for n,raw in sorted(buffers.items())],'selfHashConvention':'Manifest bound by outer preparation; all other members bound here.','sourceInformationDeleted':0})
 with zipfile.ZipFile(zp,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for n,raw in sorted(buffers.items()):z.writestr(n,raw)
 with zipfile.ZipFile(zp) as z:
  assert z.testzip() is None
  for n,raw in buffers.items():assert z.read(n)==raw
 for n in ['README.md','MANIFEST.json','CHECKS.json']:(root/n).write_bytes(buffers[n])
 prep.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'Prepared UNSENT; send with next actual companion exact05 handoff','archive':info(zp),'evidence':info(out),'manifest':info(root/'MANIFEST.json'),'check':info(root/'CHECKS.json'),'sourceCount':len([n for n in buffers if n.startswith('sources/')]),'allArchiveMembersVerified':True,'newRuleAdoptions':0,'sourceInformationDeleted':0}));print(json.dumps({'archive':info(zp),'evidence':info(out),'preparation':info(prep),'checks':len(checks),'members':len(buffers)}))

if __name__=='__main__':main()
