"""Independent blank/form-tree/save-reopen checks. Never changes the submission."""
from pathlib import Path
import argparse,hashlib,json,collections,subprocess
from pypdf import PdfReader,PdfWriter
import fitz

def main():
 ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('--out',required=True,type=Path);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 r=a.root/'DescentReviewChanges/ReviewBible';p=r/'output/pdf/Decennium_Descent_Character_Sheet_Playtest.pdf';inv=json.loads((r/'data/playtest/character_sheet_form_fields.json').read_text());rd=PdfReader(p);fields=rd.get_fields();exp={f['name']:f for f in inv['fields']};checks=[]
 def ck(name,x,y=True):checks.append({'name':name,'passed':x==y,'actual':x,'expected':y})
 ck('five pages',len(rd.pages),5);ck('364 canonical fields',len(fields),364);ck('unique inventory names',len(exp),364);ck('inventory PDF hash',hashlib.sha256(p.read_bytes()).hexdigest(),inv['pdfSha256']);ck('not encrypted',rd.is_encrypted,False);ck('no document JavaScript',not('/JavaScript' in rd.trailer['/Root'].get('/Names',{})))
 widgets=[]
 for no,page in enumerate(rd.pages,1):
  ck('US Letter page '+str(no),list(map(float,page.mediabox)),[0.,0.,612.,792.]);names=[]
  for ref in page.get('/Annots',[]):
   w=ref.get_object()
   if w.get('/Subtype')!='/Widget':continue
   n=w.get('/T');widgets.append(n);names.append(n);f=exp[n];rect=list(map(float,w['/Rect']));ck(n+' page',f['page'],no);ck(n+' rectangle coordinates within 1e-6 pt (PDF decimal precision)',all(abs(x-y)<=1e-6 for x,y in zip(rect,f['rect'])));ck(n+' blank',str(w.get('/V','')),'');ck(n+' appearance',w.get('/AP',{}).get('/N') is not None);ck(n+' editable',int(w.get('/Ff',0))&1,0);ck(n+' inside printable bounds',rect[0]>=36 and rect[1]>=46 and rect[2]<=576 and rect[3]<=723)
 ck('widget names equal canonical/inventory',set(widgets)==set(fields)==set(exp));ck('no duplicate widgets',len(widgets),len(set(widgets)));ck('pages widget count',[sum(x['page']==i for x in exp.values()) for i in range(1,6)],[93,50,89,73,59])
 writer=PdfWriter();writer.clone_document_from_reader(rd);values={n:f'{i:03}' for i,n in enumerate(exp,1)}
 for page in writer.pages:writer.update_page_form_field_values(page,values,auto_regenerate=False)
 filled=a.out/'FORM_ROUNDTRIP_SYNTHETIC.pdf'
 with filled.open('wb') as f:writer.write(f)
 back=PdfReader(filled).get_fields();ck('reopened names',set(back)==set(exp))
 for n,v in values.items():ck(n+' saved value',str(back[n].get('/V','')),v)
 fd=fitz.open(filled);seen={w.field_name:w.field_value for page in fd for w in page.widgets()};ck('second parser names',set(seen)==set(exp))
 for n,v in values.items():ck(n+' MuPDF saved value',seen[n],v)
 # Poppler checks appearances independently of the original MuPDF review renders.
 render=[]
 for tag,src in [('blank',p),('filled',filled)]:
  prefix=a.out/('poppler-'+tag);res=subprocess.run(['pdftoppm','-r','110','-png',str(src),str(prefix)],capture_output=True,text=True,timeout=45);ck('Poppler '+tag+' rendered',res.returncode,0);render.append({'kind':tag,'returncode':res.returncode,'stderr':res.stderr,'files':[x.name for x in sorted(a.out.glob('poppler-'+tag+'-*.png'))]})
 out={'scope':'Five-page blank/form-tree/edit/save/reopen checks and Poppler rendering. Synthetic three-digit values are not player data; no calculation, game legality, accessibility/user trial or persistent viewer compatibility certified.','checks':len(checks),'failed':[c for c in checks if not c['passed']],'pdfSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'fields':364,'pages':5,'rendering':render,'results':checks}
 (a.out/'PDF_REVIEW_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'checks':len(checks),'failed':out['failed'],'fieldCount':364,'pages':5}))
 if out['failed']: raise SystemExit(1)
if __name__=='__main__':main()
