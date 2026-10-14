from pathlib import Path
import difflib
import hashlib
import json

audit=Path(__file__).resolve().parent
game=audit.parents[3]
root=game/'DescentReviewChanges/ReviewBible'
baseline=audit/'temporal_playtest_rules_reviewed_foundation.py'
assert hashlib.sha256(baseline.read_bytes()).hexdigest()=='b821829ed352e69ce1ecf3c3d753f0206c8f8d2ec5a5d64bc89d5fd7d8a72151'
packet=audit/'CODEX_TEMPORAL_CONTROL_WORLD_REVIEW.md'
assert not packet.exists(), 'Preserve submitted review packets'
intro='''# Actual live control/pulse transaction candidate — 36 integration methods

This continues the nine-family conference and approved 22-method payment/output bridge. The original 76-method foundation is preserved byte-for-byte under its approved hash. The CURRENT foundation file has a small explicit extension below, so its old approval does not cover this current version. All 36 new + 76 foundation + 22 bridge checks pass.

Please inspect the actual code for consequential defects in this bounded integration. Give concrete counterexamples, then a bounded disposition. This is NOT a request to close full Time Loop, all control sources, complete cards, or the whole game. All seven major integrations remain counted as missing. No class/catalog status is promoted.

Implemented: canonical existing holders are joined to the original preflight/commit transaction, exact source registry, same-object restoration (frozen SpeedRecord is a value in its canonical BoundEffect), immutable source metadata, concentration alias/callback staleness, original outside-clock retirement without catch-up, current RP/RC/BA facade, iteration history, authentic regular-start windows, target-start Hemostasis, current parent pulse receipts for Bloom/contact, once-evaluated paid native starts.

Known remaining dependencies, not presented as complete: full source sibling effects (save/lifecycle/aura/floor/etc.), application-source legality/target predicates, original-clock construction, outside-initiative round-ledger import, actual final HP/Ki/Conviction application and caps, parent replacement/retirement/restoration, device/stasis/copy/physical/form parents, Omen Reader setup, extra turns, movement/entry receipts, mutation reserves, shared multi-parent FirstContactLedger. Missing supplied adapters reject explicitly where represented. A BoundEffect is the selected component's binding, not evidence that the whole source card has been executed. The host still owns action/source transactions.

All active timed sources captured at the initiative-start boundary must already exist and have outside-origin schedules. Later encounter-created sources can retire on rewind but cannot acquire snapshot membership. Native ability records are persistent preexisting capabilities; restore produces no native start.

Specific points to check: source/target start authority; candidate's recipient claimed view versus conserved iteration-round history; parent activity after missed upkeep; old event receipt reuse; preservation of original costs; stale-plan coverage; malformed source holder admission. One test fixture originally tried two Song pulses in the same numbered round; it now advances a genuine complete round before the later pulse rather than clearing the target budget. Original helper behavior was unchanged.

The real-source clock policies were settled in the preceding conference. If the implementation has a defect, identify it; if a source parent needs more actual data, distinguish that missing adapter from a new rule question. Please do not infer an approval of deferred pieces from passing checks.

'''
diff=''.join(difflib.unified_diff(baseline.read_text(encoding='utf-8').splitlines(True),
    (root/'tools/temporal_playtest_rules.py').read_text(encoding='utf-8').splitlines(True),
    fromfile='reviewed-foundation',tofile='current-extension'))
files=['tools/temporal_control_world.py','tools/validate_temporal_control_world.py',
       'docs/mechanics/TEMPORAL_CONTROL_WORLD_VALIDATION.json','docs/mechanics/TEMPORAL_CONTROL_PLAYTEST.md']
parts=[intro,'## Foundation extension diff\n\n```diff\n'+diff+'\n```\n']
for rel in files:
    parts.append('\n## '+rel+'\n\n```\n'+(root/rel).read_text(encoding='utf-8')+'\n```\n')
packet.write_text(''.join(parts),encoding='utf-8')
manifest={'status':'SUBMITTED-CANDIDATE pending actual GPT reply','fullTimeLoopOperational':False,
 'tests':{'integration':36,'foundation':76,'paymentOutput':22},
 'hashes':{rel:hashlib.sha256((root/rel).read_bytes()).hexdigest() for rel in
           ['tools/temporal_playtest_rules.py']+files},
 'packetSha256':hashlib.sha256(packet.read_bytes()).hexdigest()}
(audit/'TEMPORAL_CONTROL_WORLD_SUBMISSION.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'packet':str(packet),'bytes':packet.stat().st_size,'manifest':manifest}))
