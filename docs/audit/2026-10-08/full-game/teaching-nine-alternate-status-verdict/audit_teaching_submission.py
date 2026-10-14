"""Read-only checks for the frozen teaching submission. No gameplay/runtime certification.
Usage: python audit_teaching_submission.py --archive /path/DD_Teaching_Navigation_9_Exact_Review_v1.zip --out /path/evidence
Python standard library for source checks; installed PyMuPDF/pypdf for form inspection.
"""
from pathlib import Path, PurePosixPath
import argparse, zipfile, json, hashlib, re, io, unicodedata, collections

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--archive',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();p=Path(a.archive);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
 z=zipfile.ZipFile(p);m=json.loads(z.read('FILE_MANIFEST.json'));rows=[]
 def h(b):return hashlib.sha256(b).hexdigest()
 def check(cat,key,actual,expected=True):rows.append(dict(category=cat,id=key,actual=actual,expected=expected,passed=actual==expected))
 def txt(n):return z.read(n).decode('utf-8-sig').replace('\r\n','\n')
 B='DescentReviewChanges/ReviewBible/';D='docs/audit/2026-10-08/full-game/'
 check('archive','zipBytes',p.stat().st_size,65100794);check('archive','zipSha256',h(p.read_bytes()),'df0390f6a17a00428e102d3de2b8195d4334f1ead80493b70ffb6dfa21b03085')
 check('archive','exactManifestMembership',set(z.namelist())==set(m)|{'FILE_MANIFEST.json'});check('archive','noDuplicateZipNames',len(z.namelist())==len(set(z.namelist())))
 for n,v in m.items():check('payload',n,[len(z.read(n)),h(z.read(n))],[v['bytes'],v['sha256']])
 staging=json.loads(z.read(D+'TEACHING_NAVIGATION_REVIEW_STAGING.json'))
 for n,v in staging['sourceFiles'].items():
  nn=D+'teaching-before-exact-dispatch/TEACHING_NAVIGATION_REVIEW_README.md' if n==D+'TEACHING_NAVIGATION_REVIEW_README.md' else n
  check('preserved147',n,[len(z.read(nn)),h(z.read(nn))],[v['bytes'],v['sha256']])
 cases=json.loads(z.read(D+'TEACHING_NAVIGATION_REVIEW_CHECKLIST.json'))
 check('checklist','exact29IDs',[x['id'] for x in cases['questions']],[f'TE-{i:02}' for i in range(1,30)])
 check('checklist','nineArtifacts',len(cases['candidateFiles']),9)
 for n in cases['candidateFiles']:check('artifact','complete:'+n,n in m and len(z.read(n))>0)
 nav=json.loads(z.read(D+'CHARACTER_CREATION_NAVIGATION_CANDIDATE_RECEIPT.json'))
 t=txt(nav['candidate']);t=t.replace(nav['candidateBanner'],'',1)
 for i,c in enumerate(nav['changes']):
  check('navigation','uniqueReplacement'+str(i),t.count(c['proposedReplacement']),1);t=t.replace(c['proposedReplacement'],c['old'],1)
 check('navigation','fiveNotes',len(nav['changes']),5)
 check('navigation','reversedContentOriginalLFBytes',t.encode('utf-8'),z.read(nav['original']))
 # Serialize equality only for this byte comparison, not the entire two texts.
 rows[-1]['actual']=h(t.encode());rows[-1]['expected']=h(z.read(nav['original']))
 snapshots=[];engine_n=0;card_n=0
 for n in sorted(m):
  if n.startswith(B+'data/public/class_playtests/') and n.endswith('.json'):
   o=json.loads(z.read(n));slug=PurePosixPath(n).stem;g=B+'docs/mechanics/classes/'+slug+'.md';gt=txt(g)
   check('classMembership',slug,len({x['id'] for x in o['cards']}),len(o['cards']));card_n+=len(o['cards'])
   for i,e in enumerate(o['engine']):check('classEngineGuideParity',slug+':engine:'+str(i),e in gt);engine_n+=1
   snapshots.append(dict(className=slug,source=n,sourceSha256=h(z.read(n)),guide=g,guideSha256=h(z.read(g)),cards=len(o['cards']),engineParagraphs=len(o['engine'])))
 bard=json.loads(z.read(B+'data/public/Decennium_Descent_Bard_Playtest_v0_1.json'));card_n+=len(bard['cards']);snapshots.append(dict(className='bard',source=B+'data/public/Decennium_Descent_Bard_Playtest_v0_1.json',cards=len(bard['cards']),engineSource=B+'docs/mechanics/BARD_PLAYTEST_v0_1.md'))
 check('classMembership','seventeenClasses',len(snapshots),17);check('classMembership','complete1223ComparisonCards',card_n,1223)
 # Direct links are tested in the assembled repository tree; nested immutable source catalog is a lookup fallback.
 nested=zipfile.ZipFile(io.BytesIO(z.read(D+'DD_Low_Rank_136_Exact_Review_v1.zip')))
 def read(n):return z.read(n) if n in z.namelist() else nested.read(n) if n in nested.namelist() else None
 def normpath(n):
  parts=[]
  for q in n.split('/'):
   if q in ('','.'):continue
   if q=='..':
    if parts:parts.pop()
   else:parts.append(q)
  return '/'.join(parts)
 def anchor(s):
  s=re.sub(r'\[([^\]]+)\]\([^)]*\)',r'\1',s).strip().lower();s=re.sub(r'[^\w\- ]','',s);return s.replace(' ','-')
 links=[]
 for n in cases['candidateFiles']:
  if not n.endswith('.md'):continue
  for label,target in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',txt(n)):
   if re.match(r'[a-z]+:',target):continue
   path,_,frag=target.partition('#');dest=normpath(str(PurePosixPath(n).parent)+'/'+path) if path else n;data=read(dest);ok=data is not None
   if ok and frag:
    heads=re.findall(r'^#{1,6}\s+(.+?)\s*$',data.decode('utf-8-sig').replace('\r\n','\n'),re.M);ok=frag in [anchor(x) for x in heads]
   links.append(dict(source=n,label=label,target=dest,anchor=frag,available=ok,nestedFallback=dest not in z.namelist() and data is not None));check('directLinks',n+'->'+target,ok)
 # Supplied eight record contracts are retained, not converted to a gameplay save schema.
 lang=json.loads(z.read(B+'data/playtest/language_communication_candidate_public.json'))
 (out/'LANGUAGE_RECORD_CONTRACTS_INSPECTED.json').write_text(json.dumps(lang['recordSchema'],ensure_ascii=False,indent=2)+'\n')
 # Actual blank form and canonical page widgets; no claims of universal viewer/accessibility compatibility.
 import fitz
 from pypdf import PdfReader
 pdfn=B+'output/pdf/Decennium_Descent_Character_Sheet_Playtest.pdf';pdfbytes=z.read(pdfn);pdf=PdfReader(io.BytesIO(pdfbytes));fields=pdf.get_fields();inventory=json.loads(z.read(B+'data/playtest/character_sheet_form_fields.json'))
 check('PDF','fivePages',len(pdf.pages),5);check('PDF','canonicalFields364',len(fields),364)
 pagefields={}
 for pi,page in enumerate(pdf.pages,1):
  for ref in page.get('/Annots',[]):
   ob=ref.get_object()
   if ob.get('/Subtype')=='/Widget':pagefields[str(ob['/T'])]=(pi,ob,ref.idnum)
 check('PDF','canonicalEqualsWidgets',set(fields)==set(pagefields));check('PDF','inventory364',len(inventory['fields']),364)
 for f in inventory['fields']:
  pi,ob,_=pagefields[f['name']];check('PDFfield',f['name'],[pi,[round(float(x),6) for x in ob['/Rect']],bool(int(ob.get('/Ff',0))&4096),str(ob.get('/V',''))],[f['page'],[round(float(x),6) for x in f['rect']],f['multiline'],f['initialValue']])
 fd=fitz.open(stream=pdfbytes,filetype='pdf');fieldtokens={};i=0
 for page in fd:
  for w in page.widgets():i+=1;v=f'T{i:03}';fieldtokens[w.field_name]=v;w.field_value=v;w.update()
 dest=out/'PDF_SYNTHETIC_FIELD_TEST_ONLY.pdf';fd.save(dest);fd.close();fd=fitz.open(dest)
 renders=out/'pdf_filled_renders';renders.mkdir(exist_ok=True)
 for i,page in enumerate(fd,1):
  for w in page.widgets():check('PDFroundTrip',w.field_name,w.field_value,fieldtokens[w.field_name])
  pix=page.get_pixmap(matrix=fitz.Matrix(1.5,1.5),annots=True);pix.save(renders/f'page-{i}.png')
  # Text appearance is extracted from a rendered/flattened copy, below.
 fd.close()
 blank=fitz.open(stream=pdfbytes,filetype='pdf');br=out/'pdf_blank_renders';br.mkdir(exist_ok=True)
 for i,page in enumerate(blank,1):page.get_pixmap(matrix=fitz.Matrix(1.5,1.5),annots=True).save(br/f'page-{i}.png')
 blank.close()
 # Exact currently authoritative references relevant to finite corrections.
 conf=json.loads(z.read(D+'CROSS_GUIDE_EFFICIENT_RECYCLING_CONFLICT.json'))
 check('recycling','lifecycleExplicitNoEnemy',conf['olderReviewedLifecycleRow'] in txt(B+'docs/mechanics/DEVICE_LIFECYCLE_PLAYTEST.md'))
 check('recycling','publicGuideHasNarrowing',conf['laterReviewedCraftingParagraph'] in txt(B+'docs/mechanics/ADVANCED_CRAFT_CANDIDATE_GUIDE.md'))
 adv=json.loads(z.read(B+'data/crafting/advanced_craft_recipe_candidate_public.json'));check('recycling','publicFullGuideParity',adv['operatingGuideText'],txt(B+'docs/mechanics/ADVANCED_CRAFT_CANDIDATE_GUIDE.md'))
 rows[-1]['actual']=h(adv['operatingGuideText'].encode());rows[-1]['expected']=h(txt(B+'docs/mechanics/ADVANCED_CRAFT_CANDIDATE_GUIDE.md').encode())
 nestedreads={}
 status=json.loads(z.read(B+'docs/mechanics/ADVANCED_CRAFT_REVIEW_STATUS.json'))
 for n in [B+'docs/director-only/ADVANCED_CRAFT_INTERNAL_OPERATIONAL_GUIDE.md',B+'data/director/advanced_craft_recipe_candidate_internal.json']:
  bb=nested.read(n);nestedreads[n]=dict(bytes=len(bb),sha256=h(bb),container=D+'DD_Low_Rank_136_Exact_Review_v1.zip');check('nestedCurrentAuthority',n,h(bb),status['artifactHashes'][n])
 internal=json.loads(nested.read(B+'data/director/advanced_craft_recipe_candidate_internal.json'))
 check('recycling','TD13InternalText',internal['procedureSections']['TD-13']['text'],conf['laterSourceVerdictTD13']);rows[-1]['actual']=h(rows[-1]['actual'].encode());rows[-1]['expected']=h(rows[-1]['expected'].encode())
 crimson=json.loads(z.read(B+'data/public/class_playtests/crimson-agent.json'));check('sourcePredicate','BG9Automatic','automatically reaches capacity 6 at class 9' in crimson['engine'][7])
 index=json.loads(z.read(B+'data/public/spell_playtests/authored_review_index.json'))
 (out/'AUTHORING_INDEX_SCOPE_INSPECTED.json').write_text(json.dumps({k:v for k,v in index.items() if k not in ['spells','records','entries']},ensure_ascii=False,indent=2)+'\n')
 report=dict(scope='Frozen source/manifest, full comparison-record membership, exact engine/guide parity, navigation and PDF form save/reopen only. Not gameplay/runtime or human trials.',archiveSha256=h(p.read_bytes()),manifestPayloads=len(m),repositoryPayloads=len(m)-1,zipEntryCount=len(z.namelist()),checks=len(rows),passed=sum(x['passed'] for x in rows),failed=[x for x in rows if not x['passed']],categoryCounts=dict(collections.Counter(x['category'] for x in rows)),notes=['147-input staging README is checked against its expressly archived pre-dispatch original.','Navigation inverse compares normalized manuscript line endings; submitted candidate uses CRLF while original uses LF. No lexical/number change is ignored.','PDF geometry is compared at 0.000001 point precision.','Direct source catalog fallback and internal advanced files come from the supplied nested immutable ZIP.'],nestedCurrentReads=nestedreads,rows=rows)
 (out/'CONTINUATION_READ_ONLY_AUDIT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(out/'INSPECTED_CLASS_MEMBERSHIP.json').write_text(json.dumps(snapshots,ensure_ascii=False,indent=2)+'\n');(out/'DIRECT_LINK_CHECKS.json').write_text(json.dumps(links,ensure_ascii=False,indent=2)+'\n');(out/'PDF_FIELD_TEST_TOKENS.json').write_text(json.dumps(fieldtokens,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k!='rows'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
