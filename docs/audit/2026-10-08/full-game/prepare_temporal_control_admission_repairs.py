from pathlib import Path
import hashlib
import difflib
import json
audit=Path(__file__).resolve().parent
root=audit.parents[3]/'DescentReviewChanges/ReviewBible'
old=(audit/'CODEX_TEMPORAL_CONTROL_WORLD_REPAIRS.md').read_text(encoding='utf-8')
dest=audit/'CODEX_TEMPORAL_CONTROL_ADMISSION_REPAIRS.md'
assert not dest.exists()
intro='''# Exact follow-up admission repairs — 49 methods pass

Your completed review of the 44-method revision is preserved as GPT_TEMPORAL_CONTROL_WORLD_REPAIR_REVIEW.md. It expressly closes the first five defects and both Oracle concentration omissions, and identifies two remaining admission defects. Both are now repaired. This packet is the exact incremental diff from that full 44-method submission, with new tests and validation; all unchanged code remains as previously supplied.

1. capture_payload now non-mutatively checks every active pulse activation <= snapshot marker, unexpired absolute deadline, and a live clone advanced to the snapshot marker. It rejects future activation, stale missed upkeep and already-expired source state. These do not charge or mutate anything.
2. Pulse component must equal its explicit admitted source profile. Bloom/contact/native require the finite identifiers installments/first-contact/regular-heal. Each family has an unknown-component capture regression.

I also performed four additional concrete malformed-state probes (results attached). Before the new checks, changing a required set/dict to a list could permit partial resource/opportunity mutation followed by AttributeError/IndexError: output guard.consumed, recipient.history, pulse.declarations, or native.consumed. The new world/holder/guard/recipient collection checks reject these before writes; all four have no-mutation regressions. Concentration slot shape/callback, control Boolean fields and pulse mode/declaration/application structure are also checked before use. The original approved helpers remain unchanged; validation belongs to the admitting world adapter.

Finally, tracing the already-agreed original-clock behavior found one missed-installment problem: restore at second7 advances an Eternal Bloom parent past its second opportunity at6, but restoring only its old consumed={0} child view would prevent its still-legal third share at12. The repaired Bloom view consumes every original share whose marker is strictly earlier than now, without healing or recalculating the reserve. consume_bloom uses the same projection before a real current parent receipt. A real restore regression proves consumed={0,1} at7, no HP change, then actual third pulse/share3 at12. Exact due markers are not skipped, so a genuine new iteration at the same still-current marker remains possible. Please check this correction against the existing rule that missed outside-clock installments are lost and later installments remain scheduled.

49 integration methods pass; 76 foundation and 22 payment/output checks remain passing. No foundation/approved-helper changes were made after the prior submission. Please give a bounded code disposition or concrete remaining defect. Full nine-family coverage, actual final HP/Ki/Conviction application, all seven major integrations, whole-game flow and delivery remain open. This is not a publication or balance approval request.

'''
parts=[intro]
files=['tools/temporal_control_world.py','tools/validate_temporal_control_world.py']
for rel in files:
    before=old.split('## '+rel+'\n\n```\n',1)[1].split('\n```\n',1)[0]
    after=(root/rel).read_text(encoding='utf-8').rstrip('\n')
    diff=''.join(difflib.unified_diff((before+'\n').splitlines(True),(after+'\n').splitlines(True),
        fromfile='44-method/'+rel,tofile='49-method/'+rel))
    parts.append('\n## '+rel+'\n\n```diff\n'+diff+'\n```\n')
for rel in ['docs/mechanics/TEMPORAL_CONTROL_WORLD_VALIDATION.json']:
    parts.append('\n## '+rel+'\n\n```json\n'+(root/rel).read_text(encoding='utf-8')+'\n```\n')
probes=json.loads((audit/'TEMPORAL_CONTROL_WORLD_SCHEMA_PROBES.json').read_text(encoding='utf-8'))
parts.append('\n## Preserved pre-repair malformed-state probes\n\n```json\n'+json.dumps([
    {k:r[k] for k in ('case','outcome','stateChanged')} for r in probes],indent=2)+'\n```\n')
manifest={'status':'49-method repair candidate pending independent confirmation','methods':49,
 'fullTimeLoopOperational':False,'remainingMajorIntegrations':7,
 'hashes':{rel:hashlib.sha256((root/rel).read_bytes()).hexdigest() for rel in
           files+['tools/temporal_playtest_rules.py','tools/temporal_control_playtest_rules.py']}}
parts.append('\n## Exact current hashes\n\n```json\n'+json.dumps(manifest,indent=2)+'\n```\n')
dest.write_text(''.join(parts),encoding='utf-8')
manifest['packetSha256']=hashlib.sha256(dest.read_bytes()).hexdigest()
(audit/'TEMPORAL_CONTROL_ADMISSION_REPAIR_SUBMISSION.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'packet':str(dest),'bytes':dest.stat().st_size,'hashes':manifest['hashes']}))
