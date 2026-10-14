"""Check the submitted ZIP itself for candidate guide link targets; preserve original report."""
from pathlib import Path
from zipfile import ZipFile
from datetime import datetime, timezone
import hashlib
import json
import posixpath
import re

R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
archive=A/'DD_Language_Communication_Exact_Review_v1.zip'
out=A/'LANGUAGE_EXACT_V1_ARCHIVE_LINK_AUDIT.json'
assert not out.exists(), 'Preserve the original portable audit'
checks=[]
with ZipFile(archive) as z:
    members=set(z.namelist())
    for p in sorted(members):
        if not p.endswith(('LANGUAGE_COMMUNICATION_PLAYTEST.md','LANGUAGE_COMMUNICATION_WORKED_SEQUENCES.md','LANGUAGE_COMMUNICATION_INTERNAL_CANDIDATE.md')):continue
        for link in re.findall(r'\]\(([^)]+)\)',z.read(p).decode('utf-8')):
            if '://' in link:continue
            dest=posixpath.normpath(posixpath.join(posixpath.dirname(p),link.split('#')[0]))
            check={'guide':p,'link':link,'target':dest,'inSubmittedArchive':dest in members}
            if dest not in members:
                f=G/dest
                check.update({'workingTreeExists':f.exists(),'workingTreeBytes':f.stat().st_size,'workingTreeSha256':hashlib.sha256(f.read_bytes()).hexdigest()})
            checks.append(check)
report={'atUtc':datetime.now(timezone.utc).isoformat(),'archiveSha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
    'status':'Four supplied-guide link targets missing from archive; all exist in working tree',
    'scope':'Portable archive link validation, supplementing the original working-tree-only link check. Original496 report and submitted archive remain unchanged.',
    'checks':checks,'missing':[x for x in checks if not x['inSubmittedArchive']],
    'nextAction':'Supply these complete unchanged target files with the bounded exact-verdict fulfillment. Await final GPT verdict before preparing that response; do not interrupt or resend the active review.',
    'candidateRulesChanged':False,'newApproval':False,'pushPerformed':False}
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checked':len(checks),'missing':report['missing']},indent=2))
