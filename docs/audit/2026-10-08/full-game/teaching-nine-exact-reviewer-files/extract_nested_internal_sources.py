"""Extract only two authentic included internal comparison files to a separate tree.
Does not synthesize missing helper modules or change the submission.
"""
from pathlib import Path
from hashlib import sha256
import argparse, json, zipfile
EXPECTED = {
 'DescentReviewChanges/ReviewBible/data/director/advanced_craft_recipe_candidate_internal.json':'e200829356160960cac6bebc033245272df34b16a01f334a722a629f84230e9e',
 'DescentReviewChanges/ReviewBible/docs/director-only/ADVANCED_CRAFT_INTERNAL_OPERATIONAL_GUIDE.md':'3a491ea8158423816446ddd8b93ff49bde973243f99b9e9baa46b798f695a2ed'
}
def main():
 p=argparse.ArgumentParser();p.add_argument('submission',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
 if a.output.resolve().is_relative_to(a.submission.resolve()):raise ValueError('Use an output outside the frozen submission.')
 zpath=a.submission/'docs/audit/2026-10-08/full-game/DD_Low_Rank_136_Exact_Review_v1.zip'
 if sha256(zpath.read_bytes()).hexdigest()!='a95210e8292f41f36df8656e71300a589790dce72c774d2b535e65be39ff1db0':raise ValueError('Nested frozen ZIP hash mismatch')
 receipts=[]
 with zipfile.ZipFile(zpath) as z:
  mf=json.loads(z.read('FILE_MANIFEST.json'))
  for rel,expected in EXPECTED.items():
   b=z.read(rel);actual=sha256(b).hexdigest()
   if actual!=expected or actual!=mf[rel]['sha256'] or len(b)!=mf[rel]['bytes']:raise ValueError('Nested original mismatch: '+rel)
   q=a.output/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b);receipts.append({'path':rel,'bytes':len(b),'sha256':actual})
 print(json.dumps({'actualNestedFiles':receipts},indent=2))
if __name__=='__main__':main()
