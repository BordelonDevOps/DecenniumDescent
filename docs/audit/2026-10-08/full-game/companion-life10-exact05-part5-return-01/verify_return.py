"""Verify the extracted Companion review return, without modifying sources."""
import argparse, hashlib, json, pathlib, zipfile, sys
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--root',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent)
p.add_argument('--companion',type=pathlib.Path)
a=p.parse_args();root=a.root
h=lambda b:hashlib.sha256(b).hexdigest()
manifest=json.loads((root/'MANIFEST.json').read_text());bad=[]
for entry in manifest['files']:
 path=root/entry['path']
 if not path.is_file():bad.append('Missing '+entry['path']);continue
 data=path.read_bytes()
 if len(data)!=entry['bytes'] or h(data)!=entry['sha256']:bad.append('Manifest mismatch '+entry['path'])
acc=json.loads((root/'ACCEPTANCE.json').read_text())
for entry in acc['exactAcceptedArtifacts']:
 data=(root/'accepted/current'/entry['filename']).read_bytes()
 if len(data)!=entry['bytes'] or h(data)!=entry['sha256']:bad.append('Accepted artifact mismatch '+entry['filename'])
 if a.companion:
  with zipfile.ZipFile(a.companion) as z:
   if data!=z.read(entry['archivePath']):bad.append('Original ZIP mismatch '+entry['filename'])
print(json.dumps({'manifestMembers':len(manifest['files']),'exactArtifacts':len(acc['exactAcceptedArtifacts']),'failures':bad,'gameRuntimeTests':0},indent=2))
sys.exit(bool(bad))
