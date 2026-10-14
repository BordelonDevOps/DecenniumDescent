"""Read-only audit of the submitted low-rank spell archive; Python stdlib only.
Writes only to the reviewer evidence directory, never to submitted files.
"""
from pathlib import Path
import hashlib,json,zipfile,xml.etree.ElementTree as ET,re,os
from collections import Counter
ROOT=Path(os.environ.get('DD_SOURCE_ROOT','/mnt/data/low_rank_source_v3')); R=ROOT/'DescentReviewChanges/ReviewBible'; A=ROOT/'docs/audit/2026-10-08/full-game'; O=Path(os.environ.get('DD_REVIEW_OUTPUT',str(Path(__file__).resolve().parent)))/'evidence'; O.mkdir(parents=True,exist_ok=True)
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def digest(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
checks=[]
def ck(group,name,ok,detail=None):checks.append(dict(group=group,name=name,pass_=bool(ok),**({'detail':detail} if not ok and detail is not None else {})))
manifest=load(ROOT/'FILE_MANIFEST.json')
archive=Path(os.environ.get('DD_SUBMITTED_ARCHIVE','/mnt/data/DD_Low_Rank_Spells_137_Source_Prepared_v3.zip'))
ck('archive','archive bytes and SHA256',archive.stat().st_size==29192630 and sha(archive)=='5acb3e4c6d9b3652b5731ffc111539a558874285c87dd0952a3398431b896640')
for p,h in manifest.items():ck('payload',p,(ROOT/p).stat().st_size==h['bytes'] and sha(ROOT/p)==h['sha256'])
for file in ['LOW_RANK_SPELL_FILE_HANDOFF_PREPARATION.json','LOW_RANK_SPELL_FILE_HANDOFF_V2_PREPARATION.json']:
 for p,h in load(A/file)['currentFileHashes'].items():ck('frozen-history',file+':'+p,sha(ROOT/p if (ROOT/p).exists() else A/p)==h)
cat=load(R/'data/public/spell_playtests/catalog.json'); by={s['id']:s for s in cat['spells']}; core=load(R/'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json'); src=load(R/'data/playtest/spell_sources/catalog.json')
js=json.JSONDecoder().raw_decode((R/'src/data/spells.js').read_text().split('export const SPELLS = ',1)[1])[0]
ck('catalog','full source JSON equals JS literal',src==js)
for s in by.values():
 ck('original',s['id'],s['source']['original']==src[s['id']])
 for e in s['source']['coreEntries']+s['source']['possibleHistoricalAliases']:ck('core',s['id']+':'+str(e['index']),e['original']==core['spells'][e['index']])
sel=[]; allbindings=[]; cls=load(R/'data/public/class_playtests/manifest.json');clspath={c['class']:(R/'docs/mechanics'/c['data']).resolve() for c in cls['classes']}
for co in load(A/'LOW_RANK_SPELL_FILE_HANDOFF_PREPARATION.json')['cohorts']:
 stem=co['prefix'];p=A/(stem+'_SOURCE_PREPARATION.json');d=load(p)
 ck('access',stem+' rank costs',d['currentRankCosts']==cat['costByRank']);ck('access',stem+' class progression',d['currentClassProgression']==cat['classProgression'])
 for s in d['selectedSpells']:
  x=s['fullSourceAndCurrentAccessRecord'];sel.append(s['spellId'])
  ck('selection',s['questionId']+' complete record',x==by[s['spellId']]);ck('selection',s['questionId']+' digest',digest(x)==s['recordSha256']);ck('selection',s['questionId']+' pending',x['operational'] is None)
 for c in d['completeCounterparts']:ck('counterpart',stem+':'+c['id'],c==by[c['id']])
 for c in d['classComparisonRecords']:
  data=load(ROOT/c['path'] if 'path' in c else clspath[c['mention']['class']])
  ok=c['card'] in data['cards'] if 'card' in c else c['engine']==data['engine'] if 'engine' in c else c['paragraph']==data['engine'][c['engineIndex']]
  ck('class-interface',stem+':'+str(c.get('card',{}).get('id',c.get('mention'))),ok)
 for e in d['currentGoverningExcerpts']:ck('governing',stem+':'+e['file']+':'+e['heading'],sha(ROOT/e['file'])==e['sha256'] and e['exactText'] in (ROOT/e['file']).read_text(encoding='utf-8'))
 allbindings+=d['currentBookBindings']
ck('coverage','137 unique full selected identities',len(sel)==len(set(sel))==137)
low={s['id'] for s in by.values() if s['operational'] is None and min(v['rank'] for v in s['classAccess'].values())<=3}
ck('coverage','all remaining low rank identities exactly once',set(sel)==low)
ck('coverage','276 operational/572 pending unchanged',sum(s['operational'] is not None for s in by.values())==276 and len(by)==848)
ck('coverage','141 preserved book bindings',len(allbindings)==141)
book=R/'books/player/Decennium_Descent_Player_Rulebook_v6.docx';ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with zipfile.ZipFile(book) as z:xml=ET.fromstring(z.read('word/document.xml'))
paras=[''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in xml.findall('.//w:body/w:p',ns)]
booklines=(R/'rulebook_output.txt').read_bytes().decode('utf-16').splitlines()
for b in load(A/'LOW_RANK_SPELL_FILE_HANDOFF_PREPARATION.json')['bookBindingsWithActualDocx']:
 text=b['currentBookRow']['exactText']; idx=b['actualDocxZeroBasedParagraphIndices']; ck('book',b['spellId']+':'+str(b['currentBookRow']['line']),all(paras[i]==text for i in idx) and booklines[b['currentBookRow']['line']-1]==text and b['catalogPlacement'] in by[b['spellId']]['source']['original']['placements'])
# The fulfillment carry check does not rerun pre-label assertions on final labels.
f=load(A/'LANGUAGE_EXACT_FULFILLMENT.json')
for p,h in f['finalHashes'].items():ck('LAX-carry',p,sha(ROOT/p if (ROOT/p).exists() else A/p)==h)
ck('LAX-carry','scoped labels and nonpromoted other systems',f['exactLanguageApproval'] and not any(f[k] for k in ['classSpellFeatPromotion','runtimeImplemented','humanBalanceApproved','wholeGameFlowApproved','cosmologyReviewed','pushPerformed']))
for p,h in f['reportHashes'].items():ck('LAX-carry-report',p,sha(ROOT/p if (ROOT/p).exists() else A/p)==h)
props=[]
for fn in ['LOW_RANK_LANGUAGE_SPELL_AUTHORING_PROPOSALS.json','ILLUSION_UTILITY_CANTRIP_AUTHORING_PROPOSALS.json']:
 for p in load(A/fn)['proposals']:
  s=p.get('unchangedCompleteSourceAndAccess',p.get('completeOriginalSourceAndAccess'));ck('proposal',p['spellId']+' full source',s==by[p['spellId']]);props.append(p['spellId'])
ck('proposal','eight distinct proposals',len(props)==len(set(props))==8)
report={'archiveSha256':sha(archive),'payloadCount':len(manifest),'selectedIdentities':len(sel),'questionCount':136,'receiptOnly':['blink'],'bookBindings':len(allbindings),'checkCount':len(checks),'groupCounts':dict(Counter(x['group'] for x in checks)),'failedChecks':[x for x in checks if not x['pass_']],'checks':checks,'scope':'Read-only byte/JSON/source-membership/book-text checks, not human balance, world authentication or spell runtime.'}
(O/'READ_ONLY_SOURCE_AUDIT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print({k:v for k,v in report.items() if k!='checks'})
