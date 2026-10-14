from pathlib import Path
import re
import difflib
import hashlib
import json
audit=Path(__file__).resolve().parent
root=audit.parents[3]/'DescentReviewChanges/ReviewBible'
packet44=(audit/'CODEX_TEMPORAL_CONTROL_WORLD_REPAIRS.md').read_text(encoding='utf-8')
packet49=(audit/'CODEX_TEMPORAL_CONTROL_ADMISSION_REPAIRS.md').read_text(encoding='utf-8')
manifest49=json.loads((audit/'TEMPORAL_CONTROL_ADMISSION_REPAIR_SUBMISSION.json').read_text(encoding='utf-8'))

def replay(before,diff):
    source=before.splitlines(True);lines=diff.splitlines(True);out=[];cursor=0;i=0
    while i<len(lines):
        match=re.match(r'@@ -(\d+)(?:,\d+)? \+\d+(?:,\d+)? @@',lines[i])
        if not match:i+=1;continue
        start=int(match[1])-1;out.extend(source[cursor:start]);cursor=start;i+=1
        while i<len(lines) and not lines[i].startswith('@@ '):
            line=lines[i]
            if line[:1] in (' ','-'):
                assert source[cursor]==line[1:]
                if line.startswith(' '):out.append(line[1:])
                cursor+=1
            elif line.startswith('+'):out.append(line[1:])
            elif line.strip():raise AssertionError(line)
            i+=1
    return ''.join(out+source[cursor:])

dest=audit/'CODEX_TEMPORAL_CONTROL_BINDING_REPAIR.md'
assert not dest.exists()
intro='''# Final concentration identity repair — 50 integration methods pass

Your completed 49-method review is preserved as GPT_TEMPORAL_CONTROL_ADMISSION_REVIEW.md. It confirms the two admission repairs, four malformed-collection cases and Bloom lost-installment reconciliation. I repaired its one remaining same-ID/different-callback blocker. Here is the exact diff from that 49-method revision, reconstructed from the prior submitted full code plus patch and verified against its exact hashes.

Each active concentration-dependent snapshot record now carries owner, concentration ID, actual slot-identity token and callback-identity token. Preflight requires the same actual slot and callback. Source registration retains strong references to actual concentration slots, so those object-identity tokens cannot be recycled after detachment. Pins are classified, validated and watched; their callbacks are never copied into a second world or invoked at restore. Register the actual concentration parent before registering its dependent component.

The added regression tests three variants before preflight: same textual ID with a different callback; same callback repackaged as a new slot; and a replacement callback subsequently pinned by another newly registered component. All reject without state/resource mutation. The last case proves a newly recognized slot cannot substitute for the immutable snapshot's binding. The existing post-preflight replacement test and later real concentration-end callback test still pass.

50 integration methods pass. Foundation remains hash45ad6ab7d2b26baf7bc56a8377d82398781175d5a81c7562b3dedeb40f28d577 and approved output bridge remains hash835a108a80e5ad8c5d030dbf7d927e0491bc944eb2697d71f2504fd2e0b1df12; their 76+22 checks remain unchanged/passing. Please confirm the admitted transaction checkpoint or give a concrete remaining defect. All broader parent/source integrations, complete nine-family coverage, actual final HP/Ki/Conviction mutation, full Time Loop and the final whole-game flow/GitHub delivery remain unfinished. No original source or catalog count changed.

'''
parts=[intro]
files=['tools/temporal_control_world.py','tools/validate_temporal_control_world.py']
for rel in files:
    before44=packet44.split('## '+rel+'\n\n```\n',1)[1].split('\n```\n',1)[0]+'\n'
    diff49=packet49.split('## '+rel+'\n\n```diff\n',1)[1].split('\n```\n',1)[0]
    before49=replay(before44,diff49)
    assert hashlib.sha256(before49.encode()).hexdigest()==manifest49['hashes'][rel]
    current=(root/rel).read_text(encoding='utf-8')
    diff=''.join(difflib.unified_diff(before49.splitlines(True),current.splitlines(True),fromfile='49-method/'+rel,tofile='50-method/'+rel))
    parts.append('\n## '+rel+'\n\n```diff\n'+diff+'\n```\n')
report=(root/'docs/mechanics/TEMPORAL_CONTROL_WORLD_VALIDATION.json').read_text(encoding='utf-8')
parts.append('\n## Current validation\n\n```json\n'+report+'\n```\n')
manifest={'status':'50-method callback-binding repair pending independent confirmation','methods':50,
 'fullTimeLoopOperational':False,'remainingMajorIntegrations':7,
 'hashes':{rel:hashlib.sha256((root/rel).read_bytes()).hexdigest() for rel in
           files+['tools/temporal_playtest_rules.py','tools/temporal_control_playtest_rules.py']}}
parts.append('\n## Exact current hashes\n\n```json\n'+json.dumps(manifest,indent=2)+'\n```\n')
dest.write_text(''.join(parts),encoding='utf-8');manifest['packetSha256']=hashlib.sha256(dest.read_bytes()).hexdigest()
(audit/'TEMPORAL_CONTROL_BINDING_REPAIR_SUBMISSION.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'packet':str(dest),'bytes':dest.stat().st_size,'hashes':manifest['hashes']}))
