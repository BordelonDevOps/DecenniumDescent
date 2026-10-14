"""Reproduce the source audit, authoring exports and limited reference checks.
Usage:
  python reproduce_review.py --archive DD_Low_Rank_Spells_137_Source_Prepared_v3.zip --output ./lr-reproduced
Optional --source-root points to an already extracted, unmodified submitted tree.
No installation/network. Original files are only read. Reports go under --output.
"""
from pathlib import Path
import argparse,hashlib,os,shutil,stat,subprocess,sys,zipfile
EXPECTED='5acb3e4c6d9b3652b5731ffc111539a558874285c87dd0952a3398431b896640'
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--archive',type=Path,required=True)
 ap.add_argument('--output',type=Path,required=True)
 ap.add_argument('--source-root',type=Path)
 ns=ap.parse_args();archive=ns.archive.resolve();out=ns.output.resolve();here=Path(__file__).resolve().parent
 if not archive.is_file():ap.error('archive is not a file')
 if archive.stat().st_size!=29192630 or hashlib.sha256(archive.read_bytes()).hexdigest()!=EXPECTED:ap.error('archive bytes/SHA256 differ from the frozen submission')
 if out==here:ap.error('choose a separate output directory; do not overwrite the frozen reviewer package')
 out.mkdir(parents=True,exist_ok=True)
 if ns.source_root:
  root=ns.source_root.resolve()
  if not (root/'FILE_MANIFEST.json').is_file():ap.error('source root lacks FILE_MANIFEST.json')
 else:
  root=out/'submitted'
  if root.exists() and any(root.iterdir()):ap.error('submitted output directory is nonempty; use another output or --source-root')
  root.mkdir(parents=True,exist_ok=True)
  with zipfile.ZipFile(archive) as z:
   for info in z.infolist():
    target=(root/info.filename).resolve()
    if root not in target.parents and target!=root:ap.error('archive member escapes extraction root')
    if stat.S_ISLNK(info.external_attr>>16):ap.error('symlink archive member not admitted')
   z.extractall(root)
 evidence=out/'evidence';evidence.mkdir(exist_ok=True)
 for name in ['SELECTED_137_ORIGINAL_RECORDS.json','CLASS_COMPARISONS.json','COUNTERPARTS.json']:
  shutil.copyfile(here/'evidence'/name,evidence/name)
 env=os.environ.copy();env.update(DD_SOURCE_ROOT=str(root),DD_REVIEW_OUTPUT=str(out),DD_SUBMITTED_ARCHIVE=str(archive))
 for script in ['read_only_source_audit.py','export_verdict.py','validate_authoring_register.py']:
  subprocess.run([sys.executable,str(here/script)],env=env,check=True)
 print('Reproduction completed. These are source/static/reference checks, not gameplay runtime or promotion.')
if __name__=='__main__':main()
