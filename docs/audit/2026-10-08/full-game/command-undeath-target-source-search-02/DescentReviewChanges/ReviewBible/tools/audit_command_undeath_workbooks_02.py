"""Read-only expansion of the exactCR2 Undead search; preserve sources and limits."""
from datetime import datetime,timezone
from fractions import Fraction
import hashlib,json,re,zipfile,xml.etree.ElementTree as ET
from apply_di7_ap_as_01 import G,R,A,info,encoded
from audit_bestiary_history import monsters

def read(p):return json.loads(p.read_bytes())
def exact_two(v):
 try:return Fraction(str(v).strip())==2
 except (ValueError,ZeroDivisionError):return False

def main():
 out=A/'COMMAND_UNDEATH_TARGET_SOURCE_SEARCH_02.json';root=A/'command-undeath-target-source-search-02';assert not out.exists() and not root.exists();historyp=A/'BESTIARY_HISTORY_PROVENANCE.json';history=read(historyp);groups=[x for x in history['inventory'] if x['kind']=='xlsx'];bindings=[];results=[];checks=[];packs=[]
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 def freeze(p):
  b=info(p);dst=root/p.relative_to(G);dst.parent.mkdir(parents=True,exist_ok=True);raw=p.read_bytes();dst.write_bytes(raw);ck('Preserved exact '+b['path'],dst.read_bytes()==raw);bindings.append({**b,'frozenCopy':dst.relative_to(G).as_posix()});return b
 root.mkdir()
 for p in [historyp,A/'BESTIARY_HISTORY_PROVENANCE.md',A/'BESTIARY_SOURCE_RUNTIME_AUDIT.json',A/'COMMAND_UNDEATH_TARGET_SOURCE_SEARCH_01.json',R/'tools/audit_bestiary_history.py',R/'tools/audit_crafting_history.py',R/'tools/audit_command_undeath_workbooks_02.py']:freeze(p)
 for n,group in enumerate(groups):
  sources=[freeze(G/p) for p in group['paths']];ck('Historical workbook group still byte-identical '+str(n),all(b['sha256']==group['sha256'] for b in sources));p=G/group['paths'][0]
  try:
   rows,sheets,extras,headers=monsters(p)
   undead=[row for row in rows if str(row['cellsByHeader'].get('Type','')).strip().casefold()=='undead'];cr2=[row for row in rows if exact_two(row['cellsByHeader'].get('Challenge'))];matches=[row for row in undead if exact_two(row['cellsByHeader'].get('Challenge'))]
   ck('Actual Type and Challenge columns '+str(n),'Type' in headers.values() and 'Challenge' in headers.values());monster=next(s for s in sheets if s['name']=='Monsters')
   results.append({'sources':sources,'status':'PARSED_READ_ONLY','sheet':'Monsters','namedRows':len(rows),'sheetSummary':sheets,'extraArchiveParts':extras,'monstersFormulaCount':monster['formulaCount'],'formulaLimit':'Read stored raw/cached values only, without recalculation. Any formula-bearing Monsters sheet is explicitly marked; no recalculation or live Excel claim.','columnBindings':{label:col for col,label in headers.items()},'allUndeadRowsComplete':undead,'allExactCR2RowsComplete':cr2,'exactCR2UndeadMatchesComplete':matches,'historicalScope':'Workbook provenance is historical or generated draft evidence, not an accepted native creature profile. Original Traits/NeedsReview/Combat Provenance and every row field remain intact.'})
  except (KeyError,StopIteration,ValueError,zipfile.BadZipFile,ET.ParseError) as ex:results.append({'sources':sources,'status':'UNPARSED_RETAINED','errorType':type(ex).__name__,'error':str(ex),'absenceClaimAllowed':False})
 base='docs/bestiary/Decennium_Descent_Monster_Manual_Canon_Rewrite_Source_Pack'
 for prefix in [G,R]:
  for volume in ['Monster_Manual_of_the_Known_Descent_Source','Directors_Sealed_Bestiary_Source']:
   folder=prefix/base/volume/'entries';files=sorted(folder.glob('*.md'));ck('Source-pack folder exists '+str(folder),folder.is_dir() and bool(files))
   for p in files:
    b=freeze(p);lines=p.read_text(encoding='utf8').splitlines();types=[{'line':i+1,'text':s,'size':m.group(1),'type':m.group(2).strip()} for i,s in enumerate(lines) if (m:=re.match(r'^\*\*(Tiny|Small|Medium|Large|Huge|Gargantuan) ([^,\n]+),[^\n]+\*\*',s))];ratings=[{'line':i+1,'text':s,'rating':m.group(1)} for i,s in enumerate(lines) if (m:=re.match(r'^\*\*Challenge\*\*\s+([^\s]+)',s))];isundead=any(t['type'].casefold()=='undead' for t in types);istwo=any(exact_two(x['rating']) for x in ratings)
    packs.append({'source':b,'volume':volume,'typeHeaders':types,'ratingHeaders':ratings,'exactCR2UndeadTextMatch':isundead and istwo,'structuralAmbiguity':len(types)!=1 or len(ratings)!=1,'authority':'Source text only. All clauses retained in frozen full file; neither type/rating parsing nor an existing label establishes an approved operative profile.'})
 for b in bindings:ck('All originals unchanged '+b['path'],info(G/b['path'])=={k:b[k] for k in ['path','bytes','sha256']})
 parsed=[r for r in results if r['status']=='PARSED_READ_ONLY'];workmatches=[{'sources':r['sources'],'row':m} for r in parsed for m in r['exactCR2UndeadMatchesComplete']];packmatches=[r for r in packs if r['exactCR2UndeadTextMatch']]
 report={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'BOUNDED_READ_ONLY_SOURCE_SEARCH_NO_PROFILE_ADOPTION','priorSearch':info(A/'COMMAND_UNDEATH_TARGET_SOURCE_SEARCH_01.json'),'workbookHistorySource':info(historyp),'scope':'All31 workbook paths grouped into24 unchanged byte-distinct contents from the existing history inventory, Monsters sheets including hidden/excluded named rows; plus both volume entry folders in main and ReviewBible source packs. Not a search of every un-inventoried workbook, arbitrary DOCX/PDF or other archive.','predicate':'Actual Type cell trimmed/casefold exactly Undead and Challenge stored numeric/rational value exactly2; markdown source type headers and Challenge headers parsed separately. Fractions such as1/2 are not2.','workbookGroupCount':len(groups),'workbookPathCount':sum(len(g['paths']) for g in groups),'parsedWorkbookGroups':len(parsed),'unparsedWorkbookGroups':len(results)-len(parsed),'uniqueWorkbookNamedRowsExamined':sum(r['namedRows'] for r in parsed),'workbookResults':results,'workbookExactCR2UndeadMatches':workmatches,'markdownEntryCount':len(packs),'markdownResults':packs,'markdownExactCR2UndeadMatches':packmatches,'checks':checks,'checkCount':len(checks),'failures':0,'frozenSources':bindings,'contentHoldDisposition':'Both current Command Undeath positive cases remain whole-case holds. Any discovered historical type/rating is evidence for a separate native profile/rating conference, never sufficient adoption. Do not re-rate source CR0 or grant CR2 to an unrated conjured profile.','newNPCProfiles':0,'newCRAssignments':0,'newRuleAdoptions':0,'workbooksRecalculated':0,'workbooksEdited':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}
 out.write_bytes(encoded(report));print(json.dumps({'report':info(out),'workbookGroups':len(groups),'workbookPaths':report['workbookPathCount'],'parsedGroups':len(parsed),'unparsed':len(results)-len(parsed),'namedRows':report['uniqueWorkbookNamedRowsExamined'],'workbookMatches':len(workmatches),'markdownEntries':len(packs),'markdownMatches':len(packmatches),'sources':len(bindings),'checks':len(checks)}))

if __name__=='__main__':main()
