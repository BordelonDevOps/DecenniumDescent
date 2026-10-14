from pathlib import Path
import hashlib
import json

audit=Path(__file__).resolve().parent
game=audit.parents[3]
root=game/'DescentReviewChanges/ReviewBible'
p=audit/'CODEX_TEMPORAL_CONTROL_WORLD_REPAIRS.md'
assert not p.exists()
intro='''# Live control/pulse repairs — 44 methods pass

Your completed five findings are preserved verbatim in GPT_TEMPORAL_CONTROL_WORLD_FINDINGS.md. All five and the Eternal Bloom correction are repaired. I also added Crown Restored to the concentration-required set: no exact exemption exists in the supplied evidence; its alias explicitly incorporates oracle.engine[26]. Please review the concrete repairs and give a bounded disposition or another reproducible defect. This does not ask for full nine-family, full Time Loop, whole-game, balance, or GitHub closure.

1. Child entry checks now clone/advance the actual pulse parent to current time, rejecting a stale unobserved missed-upkeep parent without applying any child effect or mutating the parent. Both already-ended and unobserved-ended cases are tested.
2. Capture rejects participant claims already in the active RecipientLedger. Outsider-only claims are conserved. Tests that formerly had an unsupported preinitiative numeric-round claim now use a first pulse with no eligible output targets; no target budget is cleared to make them pass. A direct import-rejection test proves capture has no state/cost changes. Original outside-round mapping remains unimplemented.
3. TemporalControlWorld now REQUIRES outputs=<the host's existing ConservedPulseOutputs> as an explicit constructor argument; there is no fallback that silently creates another ledger. It registers/reuses the same actual PulseSeries in that guard, verifies all guard registrations are represented, delegates resolve_pulse for Ki/Conviction profiles to guard.resolve, watches the guard schema/bindings/consumed/events, and writes missed-opportunity reconciliation into guard.consumed. The approved guard file is unchanged. Tests resolve first via the old guard then via the world after a real restore, and reverse the paths; the same Ki allowance cannot recur. Host obligations remain one canonical guard per world and final atomic capped resource application, as with the other canonical holder contracts.
4. Speed suppressed=True is rejected without the missing provenance adapter, including at capture and after a previously unsuppressed snapshot. No unknown suppression Boolean is rewound.
5. tx.watch_shape(self.concentration) now rejects newly added live concentration state after preflight. The actual counterexample is tested.
6. Eternal Bloom and Crown Restored require exact current concentration. Tests explicitly reject both without it. Existing fixtures use real ConcentrationLedger entries/callbacks.

44 integration methods pass. The 76 foundation and 22 payment/output regressions still pass; the foundation extension remains exactly hash 45ad6ab7d2b26baf7bc56a8377d82398781175d5a81c7562b3dedeb40f28d577, submitted with its full diff in the preceding packet. The approved payment/output helper remains hash 835a108a80e5ad8c5d030dbf7d927e0491bc944eb2697d71f2504fd2e0b1df12. The complete revised module, complete tests, unchanged guard and current status guide follow so composition can be assessed directly.

No original source changed, no scope count promoted, no whole-game push performed. All seven larger integrations remain incomplete; full source sibling/lifecycle execution, external round import, final HP/Ki/Conviction mutation, entry/movement/extra-turn/mutation/device/form parents, shared multi-parent contacts, and source-specific eligibility remain separately required.

'''
parts=[intro]
files=['tools/temporal_control_world.py','tools/validate_temporal_control_world.py',
       'tools/temporal_control_playtest_rules.py','docs/mechanics/TEMPORAL_CONTROL_WORLD_VALIDATION.json',
       'docs/mechanics/TEMPORAL_CONTROL_PLAYTEST.md']
for rel in files:
    parts.append('\n## '+rel+'\n\n```\n'+(root/rel).read_text(encoding='utf-8')+'\n```\n')
data=json.loads((audit/'TEMPORAL_CONTROL_PULSE_POLICY_SOURCES_V3.json').read_text(encoding='utf-8'))
def records(value):
    if isinstance(value,dict):
        if value.get('bindingId') in ('oracle.engine[26]','oracle.supplement.life.eternal-bloom','oracle.supplement.flame.crown-restored'):
            yield value
        else:
            for child in value.values():yield from records(child)
    elif isinstance(value,list):
        for child in value:yield from records(child)
parts.append('\n## Exact original Oracle source evidence\n\n```json\n'+json.dumps(list(records(data)),indent=2)+'\n```\n')
p.write_text(''.join(parts),encoding='utf-8')
manifest={'status':'REPAIRED candidate awaiting actual independent confirmation','methods':44,
 'fullTimeLoopOperational':False,'remainingMajorIntegrations':7,
 'hashes':{rel:hashlib.sha256((root/rel).read_bytes()).hexdigest() for rel in ['tools/temporal_playtest_rules.py']+files},
 'packetSha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(audit/'TEMPORAL_CONTROL_WORLD_REPAIR_SUBMISSION.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'packet':str(p),'bytes':p.stat().st_size,'hashes':manifest['hashes']}))
