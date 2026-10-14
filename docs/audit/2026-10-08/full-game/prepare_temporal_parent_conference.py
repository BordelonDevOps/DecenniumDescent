"""Exact parent-source evidence for the next notebook conference."""
from pathlib import Path
import hashlib
import json

audit=Path(__file__).resolve().parent
game=audit.parents[3]
root=game/'DescentReviewChanges/ReviewBible'
out=audit/'CODEX_TEMPORAL_PARENT_CONFERENCE.md'
assert not out.exists()
head='''# Time Loop parent conference: concentration, spell anatomy and Druid

The previous 50+76+22 bounded live-control checkpoint is recorded exactly as approved. Full Time Loop still has seven incomplete integration domains. Here is the actual current source code for the next parent integrations; it is evidence, not a claim they are implemented. No original source, catalog status, or global rule is being changed. The human already authorized GitHub push after our final whole-game flow agreement; that condition has not yet been met and does not need renewed human permission.

Please settle the following concrete cases together, using the twelve existing conservation decisions. Distinguish already-implied interpretations from any new provisional decision. Correct these proposed interpretations where necessary. Implementation review will follow separately.

1. **Participant concentration restoration.** A participant's snapshot Polymorph (absolute deadline still future) ended after initiative because of concentration failure. Proposed: restore that exact original cast/link and canonical end callback without a new cast/save/payment/start event, provided all dependent targets/gear/geometry are reconcilable. If that participant now concentrates on a different post-snapshot source, its entire source closure must retire without refund; unsupported or protected outsider consequences reject the rewind. Outsider casters' slots remain strictly current. Is that the intended full adapter beyond the exact-still-current restriction of the approved control bridge?

2. **Mixed-roster concentration.** Snapshot Mass Polymorph reaches one participant and one nonparticipant. Proposed: participant state may rewind while the nonparticipant's current link/state remains unchanged; only if a complete proposed shared cast/slot can maintain both. If reconstructing or retiring the parent's callback would end, revive, reapply or alter the outsider effect, reject. No synthetic half-cast and no replay of saves. Confirm or specify a simpler always-reject boundary for the first complete parent adapter.

3. **True Polymorph stabilization.** Snapshot link was shaping; the exact current link legitimately reached its original 60-second checkpoint and is permanent. Proposed: conserve permanent status and lack of concentration, restore compatible participant encounter state/geometry/gear, keep the same lineage/enrollment, and do not re-run checkpoint. What if that newly permanent link was then legitimately dispelled or replaced: can the old snapshot restore it as permanent, or must that historical world resolution make it unavailable? Please resolve the actual latter case rather than inferring from a current link.state label.

4. **Druid paid same-instance renewal.** Snapshot at t=599 has form F with deadline600. At t=600 the owner legally pays a shift and renews F to1200 (natural_endpoint updates the same instance). Rewind occurs at t=601 before round4. Proposed: conserve the actual paid renewal and F's current valid1200 endpoint, without refunding its shift; do not rebase to now+600 or reinstate expired600. A new form ID never inherits that extension. Confirm the exact endpoint when the same F subsequently ended before the rewind, and whether an explicit historical renewal receipt is required.

5. **Druid form-local and global expenditures.** A snapshot-unspent per-form special may regain its local permission, while current Form Surges, shifts, reserve, rest_uses, recharges and recharge-clock ticks stay spent/current. Snapshot-spent stays spent. A restored Broodmother never reopens its actual entry-only spawn window. Rest/attunement changes require exact current eligibility; absent a rest/progression adapter reject structural divergence. Confirm this separation, especially that a current exhausted global payment cannot be bypassed by restoring a local flag.

6. **Druid entry and dependent shields.** Restore exact original form and eligible snapshot entry-buffer grant/remaining amount without calling shift(), offering a new buffer or decrementing reserve again. Example: Bear entered with20, snapshot buffer12, spent8 more and reverted; valid F can restore12 and current reserve remains spent. Invalid/expired F cannot support its entry shield. Mooncursed Howl uses recipient LR rather than form dependency in current helper; it follows its original independent grant lifetime. Confirm both. All other active shield sources still require explicit policies.

7. **Recharge bridge and authentic markers.** Proposed: one existing OwnerRechargeClock per actual Druid, preserve all its fields and recharges. kernel.regular_start supplies its monotonic global_regular to DruidState.regular_start exactly once, only for that owner's genuine start. A first post-loop start at unchanged world seconds advances marker identity but does not manufacture a six-second tick. Restore calls no clock method. A prepared plan watches every clock/finite field and rejects if a real tick/rest occurs before commit. Initiative entry/exit still use the same ordinary clock. Confirm.

8. **Shapechange and hostile repeat windows.** Current TransformationWorld uses numeric regular_index and round_number. Proposed source wrapper uses authenticated iteration-qualified turn/round windows for once/later-regular-turn switches and damage repeat saves, preserving historical event IDs. Absolute deadline remains unchanged; no save at restore. Clarify 'later than original casting turn' for an outside-origin snapshot Shapechange in new iteration round1, and a restored hostile link whose first HP-damage save was consumed only after snapshot.

9. **Druid cadence.** shift() clears refrain and rememberedSpell only on actual entry. Temporal restoration must not call it. Are the participant's snapshot refrain/rememberedSpell/dissonance independently rewindable encounter state, or conserved finite class economy? The current Druid adapter shares a canonical cadence dict; the complete class-cadence adapter is not present. Proposed initial parent implementation rejects any scene requiring changes to that cadence until its source-specific policy exists, rather than inventing a reset. Please identify the policy or required source evidence.

10. **Expired forms and current external effects.** If snapshot Druid/temporary spell form has expired at current world time without a valid same-instance extension, proposal is to reject when restoring that snapshot's anatomy requires replaying the expired endpoint; do not silently grant a fresh form or drop the form while restoring dependent movement/gear/shields. Existing external suppression is preserved only through exact canonical records and simultaneous legal geometry. Is any supported normalization to base anatomy already authorized, or should these cases remain unavailable pending a specific reconciliation?

Source limitations to preserve: current DruidState does not own gear or a body HP copy. TransformationWorld.Body.life must alias Core life; its buffers/concentration must be the same objects as other adapters. The first full implementation must not invent a separate form world, calendar, concentration pool, HP pool or persistent slot map. Complete creature/physical/device dependencies still require their adapters; empty registries do not prove scene completeness.

'''
parts=[head]
names=['tools/form_temphp_playtest_rules.py','tools/transformation_spell_playtest_rules.py']
hashes={}
for name in names:
    raw=(root/name).read_bytes();hashes[name]=hashlib.sha256(raw).hexdigest()
    parts.append(f'\n## Exact current file: {name}\nSHA-256: `{hashes[name]}`\n\n```python\n{raw.decode("utf-8")}\n```\n')
forms=json.loads((root/'data/playtest/druid_form_profiles.json').read_text(encoding='utf-8'))['profiles']
selected={k:{f:p[f] for f in ('sourceId','sourceSha256','sourceProcedure','minimumLevel','circle','archAttunement','entryBuffer','specials')} for k,p in forms.items()}
parts.append('\n## All26 actual Druid source profiles: costs, entry buffers and specials\n\n```json\n'+json.dumps(selected,ensure_ascii=False,indent=2)+'\n```\n')
parts.append('\n## Existing twelve decisions (actual notebook reply)\n\n'+(audit/'GPT_TEMPORAL_WORLD_BOUNDARIES.md').read_text(encoding='utf-8'))
out.write_text(''.join(parts),encoding='utf-8')
(audit/'TEMPORAL_PARENT_CONFERENCE_SUBMISSION.json').write_text(json.dumps({'status':'policy conference prepared; actual response pending','hashes':hashes,'packetSha256':hashlib.sha256(out.read_bytes()).hexdigest(),'fullTimeLoopOperational':False},indent=2)+'\n',encoding='utf-8')
print(f'{out}: {out.stat().st_size} bytes')
