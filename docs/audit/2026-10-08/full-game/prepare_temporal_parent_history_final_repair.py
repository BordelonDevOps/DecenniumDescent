"""Prepare the two narrow fixes as an exact diff from the submitted 55-method code."""
from pathlib import Path
import difflib,hashlib,json

audit=Path(__file__).resolve().parent;root=audit.parents[3]/'DescentReviewChanges/ReviewBible'
old=(audit/'CODEX_TEMPORAL_PARENT_HISTORY_REPAIR.md').read_text(encoding='utf-8')
out=audit/'CODEX_TEMPORAL_PARENT_HISTORY_TIME_PIN_REPAIR.md';assert not out.exists()
parts=['''# Parent history: canonical query time and retained-reference repair

Your actual 55-method review is preserved verbatim in GPT_TEMPORAL_PARENT_HISTORY_REPAIR_REVIEW.md. The original four findings are independently confirmed repaired; these are the two remaining implementation corrections. No new source rule is introduced.

The suite now has 59 passing methods. valid_form_deadline() defaults to the actual scheduler time in initiative, rejects a supplied time different from that clock, and always rejects times earlier than the last observed event. Outside initiative an explicit actual-world marker is still required; it is bounded by observed history until the broader calendar adapter exists.

Both reference-pin tables now have retained-reference manifests checked before every validation and before extending pins. Key deletion, entry replacement and lost historical concentration tuples reject. Existing manifest entries cannot be overwritten through _pin_objects(); retained tuple and callback references remain even after ordinary concentration ending. Failed native operations no longer extend pins. This uses the same accidental-corruption/shadow-evidence model as the existing audit copies; it is not a security sandbox against a caller deliberately rewriting every private validator root.

Four new methods cover expired/backdated initiative queries, no-argument current-time queries plus the outside-history lower bound, form-pin deletion with equal-field replacement, and deletion of ended concentration pins. All preceding native-operation, authority, finite-economy and transition checks still pass.

Below is the exact diff from your immutable 55-method submission plus current hashes/report. Please confirm this bounded source-history checkpoint if no reproducible issue remains. Parent restoration, full class casting hooks, replay-safe wrappers, all seven broader integrations, full Time Loop and the final whole-game/GitHub gate remain open.
''']
hashes={}
for name in ('tools/temporal_parent_history.py','tools/validate_temporal_parent_history.py'):
    p=root/name;hashes[name]=hashlib.sha256(p.read_bytes()).hexdigest()
    previous=old.split('## Exact '+name+'\n',1)[1].split('```\n',1)[1].split('\n```',1)[0]
    parts.append('\n## '+name+'\nCurrent SHA-256 `'+hashes[name]+'`\n\n```diff\n'+
        ''.join(difflib.unified_diff(previous.splitlines(True),p.read_text(encoding='utf-8').splitlines(True),fromfile='submitted-55/'+name,tofile='repair-59/'+name))+'\n```\n')
report=root/'docs/mechanics/TEMPORAL_PARENT_HISTORY_VALIDATION.json'
parts.append('\n## Exact validation report\n\n```json\n'+report.read_text()+'\n```\n')
hashes['docs/mechanics/TEMPORAL_PARENT_HISTORY_VALIDATION.json']=hashlib.sha256(report.read_bytes()).hexdigest()
out.write_text(''.join(parts),encoding='utf-8')
(audit/'TEMPORAL_PARENT_HISTORY_TIME_PIN_SUBMISSION.json').write_text(json.dumps({
 'status':'59-method two-finding repair awaiting actual notebook review','hashes':hashes,
 'packetSha256':hashlib.sha256(out.read_bytes()).hexdigest(),'parentRuntimeIntegrated':False,
 'fullTimeLoopOperational':False,'remainingMajorIntegrations':7},indent=2)+'\n')
print(out.stat().st_size,'bytes prepared')
