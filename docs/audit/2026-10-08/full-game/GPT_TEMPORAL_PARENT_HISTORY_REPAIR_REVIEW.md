# Actual GPT review of the 55-method parent history repair

ChatGPT said:

The four prior findings are materially repaired. The new authority binding, finite-state fingerprint, operation transition matrix/save-callback guard, and OUTSIDE_EVENT/OUTSIDE_CAST split all address the failures from the 38-method version. The 55-method suite is useful evidence, and the packet remains correctly limited to operation history rather than restoration. 
Pasted text

I still find two narrow, reproducible history-evidence defects before I would let the larger parent transaction trust this journal.

1. valid_form_deadline() can certify an expired form by accepting a backdated query time

Ordinary operations correctly enforce monotonic time, and initiative operations require the actual scheduler event/time. _begin() does that. 
Pasted text

But the evidence query does not:

Python
Run
def valid_form_deadline(self, owner, form_id, now):
    ...
    marker = ClockMarker(**endpoint)
    require(clock_marker(now) < marker, ...)
    return marker

It never requires the supplied now to equal the canonical scheduler time in initiative or even to be at least the journal's last_time. 
Pasted text

Concrete reproducer:

Plain text
1. Create F at t=0. Its real endpoint is 600.
2. Bind/enter initiative with scheduler.now = 601.
3. Call valid_form_deadline("a", "F", 599).
4. The method returns ClockMarker(600).

The evidence query has now said F's endpoint is still valid even though the canonical world is already at second 601.

That is dangerous specifically because this method is intended to feed the later restoration planner.

Repair: centralize a canonical query-time check. At minimum:

Plain text
marker = clock_marker(now)
require(marker >= self.last_time)

if mode == initiative:
    require(marker == scheduler.now)

For Time Loop use, I would go further and have the eventual planner call a no-argument/current-time form of the query so it takes scheduler.now internally rather than accepting an arbitrary timestamp.

Outside initiative, use the canonical world-clock provider once that adapter exists; until then at least reject a marker earlier than last_time.

2. The canonical-reference pin tables are not themselves integrity protected

You correctly pin Forms, Casts, Links, Bodies and concentration slots. The validation then uses whatever entries currently remain in _pins and _slot_pins. 
Pasted text
 
Pasted text

But unlike events, receipts, failures, and chain, there is no protected expected copy/manifest of those pin registries.

That means deleting a pin disables the corresponding identity check.

Concrete form reproducer:

Plain text
shift F through the journal

del journal._pins[("form", "a", "F")]

replacement = deepcopy(druid.current)
druid.instances["F"] = replacement
druid.current = replacement

journal.validate()

The replacement has the same data, so _state() == _expected. The instances dictionary object itself remains the canonical dictionary, satisfying _druid_bindings. And because the F entry was removed from _pins, the final object-identity loop has nothing left to compare.

The journal can therefore accept an equal-field replacement of an object it previously claimed to pin.

There is an even simpler historical concentration case:

Plain text
cast C
end C's concentration normally
journal._slot_pins.clear()
journal.validate()

Because no concentration slot is currently active, validation has no slot to look up. The strong historical reference that is supposed to prevent callback/slot identity reuse has silently disappeared.

This matters to the forthcoming parent restoration layer because the whole point of retaining those references is to prove the exact original source closure.

Repair: make both pin sets append-only, self-verifying journal state. For example, maintain protected manifests parallel to the audit shadows:

Plain text
_pin_manifest:
    key -> exact object reference

_slot_manifest:
    slot token -> exact slot reference + callback reference

At every validation require:

identical key sets;
each live _pins[key] is manifest[key];
each slot pin is the same retained tuple;
historical slot pins may not disappear merely because concentration ended.

Only _pin_objects() after a successfully admitted operation may extend those manifests. It must never replace/remove an existing entry.

Add regressions for both the form-pin deletion/equal replacement and historical concentration-pin deletion.

What I consider fixed

The previously reported source-authority problem is closed. Druid operations require the bound DruidStats, casts/repeat saves require the bound CastStats, and ordinary cast prices are freshly rederived from the real catalog, repertoire, current RP and current cadence before the supplied CastPrice is accepted. 
Pasted text
 
Pasted text

The finite Druid state is also now separately fingerprinted while cadence is intentionally excluded and remains current. 
Pasted text
 
Pasted text

The source-transition and save-callback repairs are substantial as well: unrelated form/cast/link/concentration transitions are no longer automatically laundered into receipts, and a save resolver cannot mutate parent/economy state and then have that mutation attributed to the enclosing cast. 
Pasted text

And the outside-origin distinction is now correct: generic events remain OUTSIDE_EVENT, while only an actual created cast gets an OUTSIDE_CAST receipt. 
Pasted text
 
Pasted text

Disposition

I would currently record this as:

PARENT OPERATION HISTORY CANDIDATE — all four prior review findings repaired; two narrow evidence-integrity blockers remain: canonical query time and append-only reference-pin integrity.

The reported 55 methods / 0 failures / 0 errors remain useful bounded validation, and the status correctly keeps parentRuntimeIntegrated: false and fullTimeLoopOperational: false. 
Pasted text

These two repairs require no new source ruling. Full parent restoration, replay-safe temporal wrappers, all seven broader integrations, full Time Loop, and the final whole-game flow/GitHub gate remain open.
