"""Prepare an exact-source policy conference; preserve every prior packet."""
from pathlib import Path
import hashlib
import json

AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parents[3]/'DescentReviewChanges/ReviewBible'

def main():
    output = AUDIT/'CODEX_TEMPORAL_CONTROL_PULSE_CONFERENCE.md'
    assert not output.exists()
    evidence = json.loads((AUDIT/'TEMPORAL_CONTROL_PULSE_POLICY_SOURCES_V3.json').read_text(encoding='utf-8'))
    all_control = json.loads((ROOT/'data/playtest/control_state_bindings.json').read_text(encoding='utf-8'))['bindings']
    selected = {r['bindingId']:r for r in evidence['controlBindings']}
    # Include the exact parent cards for the generic rider and Cold profiles.
    names = ('balanced-scales','drake-mark','omen-reader','marked-for-death','target-scanner',
             'carrion-conductor','constellation','cold-focus','glacier','elemental-bolt',
             'elemental-surge','echoing-guard','brutal-strike','moment-s-pause',
             'slumber-glimpse','retribution')
    for row in all_control:
        if any(x in row['bindingId'] or x in ' '.join(row.get('componentIds',[])) for x in names):
            selected[row['bindingId']] = row
    keep = ('bindingId','sourceKind','sourcePath','sourceId','sourceSha256','componentIds',
            'sourceProcedure','operationalOverrides','modifiesComponents','referencesComponents')
    trimmed = [{k:r[k] for k in keep if k in r} for r in selected.values()]
    pulse = [{k:r[k] for k in keep if k in r and k!='operationalOverrides'} for r in evidence['pulseBindings']]
    title = '''# Time Loop: nine control/healing-pulse families — exact-source conference

Codex records your completed 76-test foundation approval, bound to helper SHA256 b821829ed352e69ce1ecf3c3d753f0206c8f8d2ec5a5d64bc89d5fd7d8a72151. The helper is unchanged. Full Time Loop remains unavailable; seven larger integrations and the whole-game/GitHub gate remain open. A repository scan finds no existing production consumer of consumed_reducer_ids outside the original healing commit method overridden by the temporal subclass; FeatWorld uses returned canonical IDs. Full FeatWorld synchronization is still missing.

Next is the control/pulse integration you requested. This is a policy conference, not a claim of implementation or request to approve unshown code. The attached exact sources and already-reviewed helper/guide text cover the nine named holder families. Historical unrelated discussion is omitted from these excerpts, but all originals and the complete V3 evidence remain preserved. Current reviewed operational guides control older first-proposal text in source rows.

Please resolve the following concrete boundaries, correcting these proposals where needed. We will implement the agreed policies against the real existing holders, test them and return the actual code for review. Unknown sources still block; do not infer policy from a helper class, component name or numeric six-second deadline.

1. Clock descriptors: propose storing exact source/component plus origin (in-initiative or outside), boundary kind, referenced actor, remaining regular starts/ends at snapshot, original absolute deadline if any, and parent lifetime/concentration. Explicit reviewed next/Nth regular markers restore remaining logical progress in the new iteration; actual world time and the Druid recharge clock remain conserved. Bare outside-initiative deadlines remain WORLD_ABSOLUTE. Current-actual-turn-end records should be restored only if the containing snapshot turn exists; our initiative-start snapshot has no active turn, so an in-progress actual-turn attachment is unavailable, not silently moved to a new turn. Confirm which listed source components use each policy, including fixed pulse schedules that normally preserve original virtual markers through initiative changes. A rewind must not create a free regular event at commit.

2. SpeedRecord: restore same-ID snapshot internal records/profiles and remaining logical endpoint where source-qualified; world-expired records do not return. Keep independently current external sources/suppression as overlays or reject when unimplemented. Reconciliation must not invoke refresh_speed_record, saves, application costs or entry hooks. Please identify any selected sources whose exact policy is still missing and keep them unsupported explicitly.

3. GuidingStarMark (actual source oracle.supplement.stars.guiding-bolt): restore snapshot attack/hit availability and active status with the same _identity; require _pending empty at capture and preflight; preserve monotonic _next_token and historical issued/resolved tokens so an old attack cannot replay. Wrathful Brand similarly restores its two independent snapshot entitlements, original parent/deadline and current external suppression. Neither is a new paid application.

4. Generic OneShotRider needs an exact parent source/component, canonical application ID, owner/target, reviewed endpoint and trigger kind. Propose an explicit finite source table, initially Scanner's attack, Drake Mark's hit, Marked for Death's hit damage rider, Vein Cutter/Crippling Lash weapon-hit rider, Balanced Scales positive-damage retaliation and Omen Reader's attack adjustment where the supplied source supports that holder. Reject any rider whose complete parent state is missing. Carrion Conductor corpse history is conserved and is not one of these effect-consumption views. Please correct mapping/trigger errors before code.

5. PerTurnReflection: preserve canonical historical used-turn evidence; fresh iteration-qualified ACTUAL turn IDs allow a genuinely new regular/extra target turn to trigger once. It is distinct from regular-only repeat saves/endpoints. No reflection at restore or replay of an old damage event. Extra-turn support may remain unavailable until the scheduler adapter is present; no fake regular-start substitution.

6. PulseSeries: same instance and fixed roster; restore snapshot states/declarations/window applications only for still-valid parent. Never replay cast pulse or an opportunity already consumed at the snapshot. A later opportunity that was pending at snapshot can occur once in the new iteration, paying its printed current RP/RC/action cost at the new logical due event. RP remains conserved; RC is the kernel's explicitly restored encounter resource (correct the V3 preparation's loose wording suggesting all RC is conserved). Do not restore a separate PulseWallet that could duplicate canonical resources. Use the real actor wallet via a checked adapter. Restored already-funded windows keep snapshot funding; later windows pay again when due. RecipientLedger domains keep historical iteration-qualified (domain,target,round) evidence. Shared named Circle of Harmony limits remain shared across owners. Please confirm finite sequence/maintenance/window/command policies separately, including outside-initiative absolute schedules and world-expired/concentration-ended effects.

7. Independent outputs: propose opportunity key (canonical effect instance, pulse index, recipient/component) CONSERVED for Transcendent Meditation's Ki, so restoring a pending second pulse can repeat its heal but cannot grant the same already received independent Ki twice. If that component was actually suppressed/missed previously, is its entitlement irrevocably lost or eligible in a newly rewound iteration? Please decide explicitly. No catch-up output at commit. Other finite BG/Ki/Conviction/material costs remain spent. Prepaid finite effect healing installments are effect state, not regenerated resource pools.

8. BloomReserve retains original missing-HP capture/shares; restores only snapshot installment-consumption view and same parent/roster. It never recomputes missing HP or grows capacity. Preserve historical installment evidence by iteration; once-per-ally floor is a separate survival record, not this reserve. FirstContactLedger restores snapshot per-instance recipient entitlements for Garden/Enhanced Garden/Seed with exact reviewed event types; no contact event on restoration, and no change to conserved real-rest family history. Please resolve whether a contact consumed after snapshot may qualify again in a genuinely new event under the same valid restored source.

9. NativeOccurrenceLedger: source-qualified genuinely new regular events only, no artificial three-pulse cap, current paid RP/current Mutation Recovery Reserve, exact current eligibility; keep old consumption history while allowing new iteration turn IDs. It must not receive a free tick at restoration. Existing ClockMarker-only keys are insufficient when logical clocks repeat; use a temporal wrapper/subclass tied to scheduler receipts. Additional unsupported live source state must block full snapshot admission.

Please give an explicit implementable source-policy disposition and any missing exact evidence. Do not reopen previously reviewed non-temporal rules absent a concrete contradiction. The goal is a coherent campaign-playtest candidate; reference code supports that goal, and this interface is not full-game closure.
'''
    sections = [title, '\n## Exact control sources\n\n```json\n'+json.dumps(trimmed,ensure_ascii=False,indent=2)+'\n```\n',
                '\n## Exact pulse source aliases\n\n```json\n'+json.dumps(evidence['pulseProfileMaps'],ensure_ascii=False,indent=2)+'\n```\n',
                '\n## Exact pulse source procedures\n\n```json\n'+json.dumps(pulse,ensure_ascii=False,indent=2)+'\n```\n',
                '\n## Direct supplemental source procedures\n\n```json\n'+json.dumps(evidence['supplementalExactSources'],ensure_ascii=False,indent=2)+'\n```\n']
    files = ['docs/mechanics/CONTROL_STATES_PLAYTEST.md','docs/mechanics/HEALING_PULSE_PLAYTEST.md',
             'tools/control_playtest_rules.py','tools/healing_pulse_playtest_rules.py']
    hashes = {}
    for name in files:
        raw = (ROOT/name).read_bytes()
        hashes[name] = hashlib.sha256(raw).hexdigest()
        sections.append('\n## '+name+'\n\n```'+('python' if name.endswith('.py') else 'markdown')+'\n'+raw.decode('utf-8')+'\n```\n')
    output.write_bytes('\n'.join(sections).encode('utf-8'))
    manifest = {'packetSha256':hashlib.sha256(output.read_bytes()).hexdigest(), 'bytes':output.stat().st_size,
                'controlRecords':len(trimmed),'pulseRecords':len(pulse),'directSupplementalRecords':len(evidence['supplementalExactSources']),
                'fileHashes':hashes,'status':'PREPARED; proposals require actual notebook conference; no implementation promotion'}
    (AUDIT/'TEMPORAL_CONTROL_PULSE_CONFERENCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest))

if __name__ == '__main__':main()
