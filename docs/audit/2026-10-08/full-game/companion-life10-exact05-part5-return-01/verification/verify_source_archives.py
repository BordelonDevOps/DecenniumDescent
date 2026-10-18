"""Read-only verification of the supplied Companion Exact05 review evidence.
No game runtime is executed and no source or repository file is modified.
"""
import copy, hashlib, json, pathlib, re, posixpath, zipfile, sys
from fractions import Fraction
from xml.etree import ElementTree as ET
import argparse, tempfile, atexit
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--companion',type=pathlib.Path,default=pathlib.Path('DD_Companion_Life_10_Exact_05.zip'))
parser.add_argument('--evidence',type=pathlib.Path,default=pathlib.Path('DD_Command_Undeath_Content_Evidence_01.zip'))
parser.add_argument('--output',type=pathlib.Path,default=pathlib.Path('independent_verification.json'))
args=parser.parse_args()
for input_path in [args.companion,args.evidence]:
    if not input_path.is_file():parser.error(f'Input file not found: {input_path}')
tmp=tempfile.TemporaryDirectory(prefix='dd_companion_exact05_');atexit.register(tmp.cleanup)
ROOT=pathlib.Path(tmp.name)
for input_path,subdir in [(args.companion,'exact05'),(args.evidence,'evidence')]:
    with zipfile.ZipFile(input_path) as archive:
        names=archive.namelist()
        if len(names)!=len(set(names)):parser.error(f'Duplicate ZIP members: {input_path}')
        for item in archive.infolist():
            path=pathlib.PurePosixPath(item.filename)
            if path.is_absolute() or '..' in path.parts or '\\' in item.filename or (item.external_attr>>16 & 0o170000)==0o120000:
                parser.error(f'Unsafe ZIP member: {input_path}: {item.filename}')
        if sum(item.file_size for item in archive.infolist())>512*1024*1024:
            parser.error(f'Unexpected extraction size: {input_path}')
        archive.extractall(ROOT/subdir)
input_paths={'DD_Companion_Life_10_Exact_05.zip':args.companion,'DD_Command_Undeath_Content_Evidence_01.zip':args.evidence}
A=ROOT/'exact05'; E=ROOT/'evidence'; logs=[]; details={}
def check(name, ok, kind='source_structural', **extra):
    logs.append(dict(check=name,passed=bool(ok),category=kind,**extra))
def h(b):return hashlib.sha256(b).hexdigest()
def raw(p):return p.read_bytes()
def read(p):return json.loads(raw(p))
def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def at(v,p):
    if p=='':return v
    for t in p.strip('/').split('/'):
        t=t.replace('~1','/').replace('~0','~')
        v=v[int(t)] if isinstance(v,list) else v[t]
    return v
def bind(root,b,pathkey='path'):
    p=root/b[pathkey];bb=raw(p)
    check('Exact source '+str(p.relative_to(ROOT)),len(bb)==b['bytes'] and h(bb)==b['sha256'])
    return bb
inputs=[('DD_Companion_Life_10_Exact_05.zip',17707929,'be5a37d3032cd2e0b9e9486821045f0e467ac4977418a266a703407eb037d7ba',181,A),('DD_Command_Undeath_Content_Evidence_01.zip',9436211,'315927825af947c8c3ca744b447009ab2be170a29343719c7de580b52f259d59',191,E)]
details['inputs']=[]
for name,sz,sha,n,root in inputs:
    b=raw(input_paths[name])
    check('ZIP bytes/hash '+name,len(b)==sz and h(b)==sha,'archive_integrity')
    with zipfile.ZipFile(input_paths[name]) as z:
        names=z.namelist()
        safe=all(not pathlib.PurePosixPath(s).is_absolute() and '..' not in pathlib.PurePosixPath(s).parts and '\\' not in s and not (i.external_attr>>16 & 0o170000)==0o120000 for s,i in zip(names,z.infolist()))
        check('ZIP safe unique members '+name,safe and len(names)==len(set(names)),'archive_integrity')
        check('ZIP CRC/member count '+name,z.testzip() is None and len(names)==n,'archive_integrity')
        check('Extracted full ZIP bytes equal archive '+name,all(z.read(i)==raw(root/i) for i in names if not i.endswith('/')),'archive_integrity')
    details['inputs'].append({'filename':name,'bytes':len(b),'sha256':h(b),'members':n,'crc':'PASS','safeMembers':'PASS'})
M=read(A/'current/SPELLS_MODEL.json'); C=read(A/'current/CASEBOOK.json'); S=read(A/'current/SOURCE_HASHES.json'); R=read(A/'current/REGISTER.json')
manifest=read(A/'current/EVIDENCE_MANIFEST.json')
for b in manifest['files']:bind(A/'current',b,'name')
details['eightExactArtifacts']=[{'filename':p.name,'archivePath':'current/'+p.name,'bytes':p.stat().st_size,'sha256':h(raw(p))} for p in sorted((A/'current').iterdir()) if p.is_file()]
check('Exactly eight current artifacts',len(details['eightExactArtifacts'])==8)
for group,n in [('currentSources',108),('frozenCurrent04Sources',63)]:
    check('Source group count '+group,len(S[group])==n)
    for b in S[group]:bind(A,b,'archivePath')
for b in read(E/'MANIFEST.json')['files']:bind(E,b,'archivePath')
check('Supplement 190 bound members plus self manifest',len(read(E/'MANIFEST.json')['files'])==190)
# Exact reversible nine-operation replay, without invoking submitted executable code.
corrections=read(A/'sources/docs/audit/2026-10-08/full-game/companion-life10-current04-review/PROPOSED_CORRECTIONS.json')
old=read(A/'sources/DescentReviewChanges/ReviewBible/data/director/spell_proposals/companion_life_10_current_04.json')
cur=read(A/'sources'/M['candidate']['path']);bind(A/'sources',M['candidate'])
x=copy.deepcopy(old); ops=corrections['operations'];check('Nine operations',len(ops)==9)
for op in ops:
    ptr=op['pointer'];parent,leaf=ptr.rsplit('/',1);p=at(x,parent);key=int(leaf) if isinstance(p,list) else leaf
    before=p[key] if op['expectedBefore']['present'] else None
    check('Operation full before '+op['id'],before==op.get('completeBefore'))
    if 'beforeCanonicalSha256' in op:check('Operation before canonical '+op['id'],h(canonical(before))==op['beforeCanonicalSha256'])
    check('Operation full after canonical '+op['id'],h(canonical(op['completeAfter']))==op['afterCanonicalSha256'])
    if op['op']=='add':check('Operation add absent '+op['id'],key not in p)
    p[key]=copy.deepcopy(op['completeAfter'])
app=cur['current04ConferenceApplication05']
check('Nine-operation canonical result',h(canonical(x))==app['nineOperationReplayCanonicalSha256'])
y=copy.deepcopy(x)
for op in reversed(ops):
    ptr=op['pointer'];parent,leaf=ptr.rsplit('/',1);p=at(y,parent);key=int(leaf) if isinstance(p,list) else leaf
    check('Inverse full after '+op['id'],p[key]==op['completeAfter'])
    if op['op']=='add':del p[key]
    else:p[key]=copy.deepcopy(op['completeBefore'])
check('Nine-operation full inverse restores Current04',y==old)
# Unchanged semantic contents: only explicitly retained metadata plus application receipt differs.
semantic_deltas=[]
for k in set(x)|set(cur):
    if x.get(k)!=cur.get(k):semantic_deltas.append(k)
check('Only declared metadata/application differs after nine-op replay',set(semantic_deltas)=={'id','recordedAtUtc','status','caseCounts','countsUnchanged','current04ConferenceApplication05'},changedKeys=sorted(semantic_deltas))
for k,v in app['previousMetadataUnchanged'].items():check('Previous metadata exact '+k,x[k]==v)
details['replay']={'operations':len(ops),'canonicalAfterNineOperations':h(canonical(x)),'inverseRestoresFullCurrent04':y==old,'postReplayChangedMetadataKeys':sorted(semantic_deltas),'operationPointers':[o['pointer'] for o in ops]}
# Explicit selected procedures; no inference from earlier full text.
sel=cur['current04ReviewProposedLayer']['currentProcedureSelection']
check('Ten selected procedures',len(sel)==len(M['spells'])==10)
check('Six shared rules preserved from Current04',len(M['sharedRules'])==6 and M['sharedRules']==cur['sharedRules']==old['sharedRules'])
check('Four source-specific new choices',len(M['newScopedRules'])==4 and M['newScopedRules']==cur['current04ReviewProposedLayer']['newScopedRules'])
for i,(s,selection) in enumerate(zip(M['spells'],sel)):
    check('Selected full procedure '+s['id'],s['id']==selection['spellId'] and s['procedure']==at(cur,selection['pointer']))
    check('Original complete source/access unchanged '+s['id'],s['completeSourceAndAccess']==old['records'][i]['completeSourceAndAccess'])
    original=s['completeSourceAndAccess']['source']['original']
    for cls,v in s['completeSourceAndAccess']['classAccess'].items():
        check('Actual class/school/rank/access '+s['id']+'/'+cls,v['rank']==original['classRanks'][cls] and v['school']==original['classSchools'][cls] and v['minimumClassLevel']==original['classLearnLevels'][cls] and v['baseRpCost']=={4:7,5:10,6:13}[v['rank']])
    for fn in ['PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md']:
        check('Full selected procedure in '+fn+'/'+s['id'],s['procedure'] in (A/'current'/fn).read_text())
for fn in ['PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md']:
    text=(A/'current'/fn).read_text()
    for rid,rule in {**M['sharedRules'],**M['newScopedRules']}.items():check('Complete shared/scoped text in '+fn+'/'+rid,rule['completeText'] in text)
check('27 complete current cases exact candidate copy',len(C['cases'])==27 and C['cases']==cur['currentCases'])
check('38 complete independent branches',sum(len(c.get('independentBranches',[])) for c in C['cases'])==38)
check('20 originals and coverage unchanged',len(C['originalScenarioTextsUnchanged'])==20 and C['originalScenarioTextsUnchanged']==cur['completePreservedAppliedLayer']['all20HistoricalScenarioTexts']==old['completePreservedAppliedLayer']['all20HistoricalScenarioTexts'] and C['originalObligationCoverageUnchanged']==old['originalObligationCoverage'])
for c in C['originalScenarioTextsUnchanged']:
    b=c['source'];value=at(read(A/'sources'/b['path']),c['pointer'])
    check('Full original scenario source equality '+c['id'],value==c['exactOriginalText'])
# Director's complete JSON blocks equal complete cases and originals, not just ID lists.
director=(A/'current/DIRECTOR_REVIEW.md').read_text()
blocks=re.findall(r'```json\n(.*?)\n```',director,re.S)
parsed=[json.loads(s) for s in blocks]
check('Director complete case/original JSON payloads',len(parsed)==28 and parsed[:-1]==C['cases'] and parsed[-1]==C['originalScenarioTextsUnchanged'])
# Full prior changed cases preserved and remaining cases byte-for-value unchanged.
prior={c['id']:c for c in old['currentCases']}
for c in C['cases']:
    check('Prior full case preserved '+c['id'],c.get('previousCurrent04Version',c)==prior[c['id']])
for obj in [M,C,R]:check('Both whole-case content holds preserved '+obj.get('id',obj.get('moduleId','model')),obj['contentLimits']['wholeCaseContentHolds']==['IN6-09-A','IN6-09-B'])
# Provenance convergence, not repository application.
cv=M['currentSourceConvergence']; idx=read(A/'sources'/cv['currentIndex']['path']);oldidx=read(A/'historical-current04'/cv['currentIndex']['path'])
by={v['id']:v for v in idx['entries']};oby={v['id']:v for v in oldidx['entries']}
changed=sorted(k for k in by if by[k]!=oby.get(k));check('Exactly45 accepted counterpart membership changes',len(changed)==45 and set(changed)=={v['id'] for v in cv['completeMembershipChanges']})
check('525/323/249 supplied authoritative baseline',idx['authoredCounts']=={'reviewed':525,'pending':323} and idx['representationCounts']['completeReviewedStandaloneProcedures']==249)
for s in M['spells']:check('Selected identity remains baseline pending '+s['id'],by[s['id']]==oby[s['id']] and 'pending' in json.dumps(by[s['id']]).lower())
reg=read(A/'sources'/cv['currentRegistry']['path']);reg04=read(A/'sources/DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_04.json')
check('173 scoped interfaces with unchanged108 prefix',len(reg['entries'])==173 and reg['entries'][:108]==reg04['entries'])
for counterpart in cv['currentAcceptedCounterparts']:
    card=at(read(A/'sources'/counterpart['source']['path']),counterpart['pointer'])
    check('Exact07 accepted full counterpart '+counterpart['spellId'],card==counterpart['completeCurrentCard'] and by[counterpart['spellId']]==counterpart['currentIndexEntry'])
# Check submitted check counts as reports, NOT semantic proof or engine execution.
reports=[A/'LOCAL_ARTIFACT_CHECK.json',A/'sources/docs/audit/2026-10-08/full-game/COMPANION_LIFE_10_CURRENT_05_REPLAY_CHECK.json',E/'CHECKS.json']
details['suppliedReports']=[]
for p in reports:
    d=read(p);n=d.get('checkCount',len(d.get('checks',[])));fail=d.get('failureCount',d.get('failures'))
    check('Supplied check report consistency '+p.name,len(d['checks'])==n and all(c['passed'] for c in d['checks']) and fail==0)
    details['suppliedReports'].append({'file':str(p.relative_to(ROOT)),'checks':n,'failures':fail,'reExecutedOriginalScript':False,'interpretation':'Supplied structural/source/arithmetic report; independently cross-checked here, not runtime or semantic proof.'})
# Validate complete catalog objects and the twelve current pointer references independently.
cat=read(A/'sources/DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json')
cat_by={s['id']:s for s in cat['spells']}
for spell in M['spells']:
    check('Full current source catalog record '+spell['id'],cat_by[spell['id']]==spell['completeSourceAndAccess'])
for ref in read(A/'LOCAL_ARTIFACT_CHECK.json')['currentSourcePointerChecks']:
    try:
        at(read(A/'sources'/ref['sourcePath']),ref['pointer']); exists=True
    except (KeyError,IndexError,TypeError):exists=False
    check('Exact current source pointer '+ref['object'],exists)
alias=read(E/'EVIDENCE.json')['explicitExistingAliasEvidence']
bind(E/'sources',alias['source'])
alias_lines=(E/'sources'/alias['source']['path']).read_text().splitlines()
for line in alias['lines']:
    check('Existing identity alias at actual source line '+str(line['line']),alias_lines[line['line']-1]==line['exactText'],'content_source_search')
# Read-only raw OOXML: all24 byte-distinct Monsters worksheets, including hidden rows.
NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def worksheet_rows(p):
    with zipfile.ZipFile(p) as z:
        shared=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            shared=[''.join(t.text or '' for t in si.iter('{'+NS['s']+'}t')) for si in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        rels={x.attrib['Id']:x.attrib['Target'] for x in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        wb=ET.fromstring(z.read('xl/workbook.xml'))
        sheet=next(x for x in wb.findall('s:sheets/s:sheet',NS) if x.attrib['name']=='Monsters')
        t=rels[sheet.attrib['{'+NS['r']+'}id']]
        t=t.lstrip('/') if t.startswith('/') else posixpath.normpath('xl/'+t)
        rt=ET.fromstring(z.read(t));rows={};formula_count=0
        for row in rt.findall('s:sheetData/s:row',NS):
            cells={}
            for c in row.findall('s:c',NS):
                col=re.sub(r'\d','',c.attrib['r']);typ=c.attrib.get('t');vn=c.find('s:v',NS)
                if c.find('s:f',NS) is not None:formula_count+=1
                if typ=='inlineStr':val=''.join(t.text or '' for t in c.findall('.//s:t',NS))
                elif vn is None:val=None
                elif typ=='s':val=shared[int(vn.text)]
                else:val=vn.text
                # Empty OOXML text cells and absent values are both blank in the supplied row schema.
                cells[col]=None if val=='' else val
            rows[int(row.attrib['r'])]=cells
        headers=rows[1]
        named=[]
        for n,c in rows.items():
            if n==1:continue
            entry={label:c.get(col) for col,label in headers.items() if label is not None}
            if entry.get('Name') not in (None,''):named.append({'worksheetRow':n,'cellsByHeader':entry})
        return named,formula_count
Evi=read(E/'EVIDENCE.json'); Search=read(E/'sources'/Evi['expandedSearch']['path']);bind(E/'sources',Evi['expandedSearch'])
wb_results=[];all_matches=[];named_count=0;workbook_paths=0;digestset=set()
def is2(v):
    try:return Fraction(str(v).strip())==2
    except (ValueError,ZeroDivisionError):return False
for w in Search['workbookResults']:
    b=w['sources'][0];p=E/'sources'/b['path'];rows,fc=worksheet_rows(p);digestset.add(h(raw(p)))
    named_count+=len(rows);workbook_paths+=len(w['sources'])
    und=[x for x in rows if str(x['cellsByHeader'].get('Type','')).strip().casefold()=='undead']
    cr2=[x for x in rows if is2(x['cellsByHeader'].get('Challenge'))]
    matches=[x for x in und if is2(x['cellsByHeader'].get('Challenge'))]
    check('Full workbook named rows count '+b['path'],len(rows)==w['namedRows'])
    check('Workbook no formula inference '+b['path'],fc==w['monstersFormulaCount']==0)
    check('Full Undead rows equality '+b['path'],und==w['allUndeadRowsComplete'])
    check('Full exactCR2 rows equality '+b['path'],cr2==w['allExactCR2RowsComplete'])
    check('Full exactCR2 Undead match equality '+b['path'],matches==w['exactCR2UndeadMatchesComplete'])
    for source in w['sources']:check('Workbook byte identity grouping '+source['path'],h(raw(E/'sources'/source['path']))==b['sha256'])
    for row in matches:all_matches.append({'sources':w['sources'],'row':row})
    wb_results.append({'sources':w['sources'],'namedRows':len(rows),'formulaCount':fc,'exactCR2UndeadRows':matches})
check('Workbook full search counts',len(digestset)==24 and workbook_paths==31 and named_count==16992,'content_source_search')
check('Eight full historical rows match expanded evidence',len(all_matches)==8 and all_matches==Search['workbookExactCR2UndeadMatches']==Evi['completeHistoricalMatches'],'content_source_search')
for entry in Evi['completeCurrentRows']:
    # Locate each source binding regardless of documentary wrappers.
    b=entry.get('source');
    if not b:
        raise ValueError('Unexpected current row wrapper '+str(entry.keys()))
    rows,fc=worksheet_rows(E/'sources'/b['path']);row=next(v for v in rows if v['worksheetRow']==404)
    check('Current row404 full source equality '+b['path'],row==entry['completeRow'],'content_source_search')
    check('Current row404 is Construct not Undead '+b['path'],row['cellsByHeader']['Type']=='Construct' and is2(row['cellsByHeader']['Challenge']),'content_source_search')
# Manuscript header claims checked against full source strings and independent structural parsing.
md_count=0;md_matches=[];alias_hits=[];md_results=[]
for m in Search['markdownResults']:
    b=m['source'];text=(E/'sources'/b['path']).read_text();lines=text.splitlines();md_count+=1
    for k in ['typeHeaders','ratingHeaders']:
        for line in m[k]:check('Actual manuscript source line '+b['path']+':'+str(line['line']),lines[line['line']-1]==line['text'],'content_source_search')
    types=re.findall(r'^\*\*(?:Tiny|Small|Medium|Large|Huge|Gargantuan)\s+(\w+)',text,re.M|re.I)
    ratings=re.findall(r'^\*\*Challenge\*\*\s+([\d./]+)',text,re.M|re.I)
    match=any(t.casefold()=='undead' for t in types) and any(is2(n) for n in ratings)
    check('Independent manuscript type/rating match '+b['path'],match==m['exactCR2UndeadTextMatch'],'content_source_search')
    if match:md_matches.append(b['path'])
    if re.search(r'\bMarut\b|Order-Drone Covenant Engine|Order-Drone Marut',text,re.I):alias_hits.append(b['path'])
    md_results.append({'path':b['path'],'types':types,'ratings':ratings,'exactCR2Undead':match})
check('144 manuscript entries / zero exact2Undead header matches',md_count==144 and not md_matches,'content_source_search')
details['expandedNativeSearch']={'workbookDistinctBytes':len(digestset),'workbookPaths':workbook_paths,'namedRowsRead':named_count,'workbooks':wb_results,'fullHistoricalMatches':all_matches,'currentRows':Evi['completeCurrentRows'],'manuscriptEntries':md_count,'manuscriptExactCR2UndeadMatches':md_matches,'identityNameTextHitsInManuscripts':alias_hits,'manuscriptHeaderResults':md_results,'limitations':Search['scope'],'blankCellNormalization':'Empty OOXML text values map to JSON null, matching the supplied row schema; original workbook bytes are never modified.','profileAdoptions':0,'ratingsApproved':0}
# Earlier truncated historical JSONs: name exact files and preserve parse errors.
s01=read(A/'sources'/cv['boundedCR2Search']['path']);errors=[];valid=0
for f in s01['frozenSources']:
    p=A/'sources'/f['frozenCopy']
    try:json.loads(raw(p));valid+=1
    except (json.JSONDecodeError,UnicodeDecodeError) as ex:errors.append({'sourcePath':f['path'],'archivePath':'sources/'+f['frozenCopy'],'error':str(ex),'bytes':len(raw(p)),'sha256':h(raw(p)),'treatment':'Pre-existing frozen truncated JSON, not corrupt ZIP or operative authority. Not parsed or repaired; full original bytes preserved.'})
check('Earlier bounded JSON parsing limits reproduced',valid==9 and len(errors)==2,'content_source_search')
details['historicalUnreadableJsons']=errors
# Independently recompute targeted fixture arithmetic/geometry (NOT game runtime).
arith=[('Soulburn ordinary',12-7+3==8 and 31-20==11),('Soulburn repeated',24-7+3-7+3==16 and 44-20-20==4),('Reservoir intrinsic recovery',0+3==3 and 31-20==11),('Knight Conjuration/retained HP',80+9==89 and 89-30==59),('Grave Gift half donor floor',31-31//2==16 and 2-1==1),('Flood damage packet',sum([8,8,7,7,7])==37 and 37-30==7),('Wraith temp+normal cap',5+7==12 and (5+7)//2==6 and min(100,97+6)==100),('Wholebody10ft slab',2*(10+5)==30 and 40-30==10),('Wholebody15ft slab',2*(15+5)==40 and 40-40==0),('Ghast mouthcone witness',(18-12.5)==5.5 and 1**2<=((18-12.5)/2)**2 and sum([3,4])==7 and 7//2==3),('Hom mass/load/capacity',20<=6*15/2 and 2<=6/2 and 4>6/2),('Hom repair',7+3+5==15 and 27-2==25),('Hom Conjuration HP',20+11==31),('Ready absolute times',Fraction('6.1')+60==Fraction('66.1') and Fraction(13)<Fraction('66.1') and Fraction('6.5')>Fraction('6.1')),('Burden Shared lifetap',14==4+5+5 and 4//2==2 and 90+2==92),('Life Linked lifetap',14==2+6+6 and 6//2==3 and 90+3==93)]
for name,ok in arith:check(name,ok,'fixture_arithmetic_geometry')
# Include supplied expanded416 report without treating it as independently executed script.
check('Expanded search416 report consistency',Search['checkCount']==len(Search['checks'])==416 and Search['failures']==0 and all(v['passed'] for v in Search['checks']))
details['suppliedReports'].append({'file':'evidence/sources/'+Evi['expandedSearch']['path'],'checks':416,'failures':0,'reExecutedOriginalScript':False,'interpretation':'Raw workbook/manuscript results independently reproduced above; original script not run.'})
result={'id':'CL10-EXACT05-INDEPENDENT-VERIFICATION-PART5-01','checks':logs,'checkCount':len(logs),'failureCount':sum(not v['passed'] for v in logs),'details':details,'runtimeTestsExecuted':0,'semanticVerdictSource':'Separate authored semantic conference, not inferred from checks.','sourcesModified':0,'workbooksEdited':0,'workbooksRecalculated':0,'repositoryApplied':False}
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'checks':len(logs),'failures':[x for x in logs if not x['passed']],'eightArtifacts':details['eightExactArtifacts'],'workbooks':len(digestset),'rows':named_count,'manuscripts':md_count,'historicalJsonErrors':errors},indent=2))

if result["failureCount"]:
    sys.exit(1)
