# GPT exact twelve-card Abjuration review

Retrieved from the same Calibration Review conversation through the app conversation reader after the Chrome tab stalled. Actual response, preserved verbatim below.

The twelve-card manuscript is close, but I would **not promote the exact artifact yet**. The substantive spell designs are sound; I find **four precise manuscript repairs** needed before the candidate can move the playable count from 83 to 95.

The source/accounting boundary is correct: these remain twelve existing rank-0 Abjuration IDs, their Core blocks and source access are preserved, and the candidate is still excluded from the operational loader. :chatgpt-content-reference{index="0"}

## 1. Apply the existing duration clock consistently

This is the broadest correction. Several cards currently say simply “until the start of your next regular turn” or “up to 1 minute.” Those results are mechanically right, but the exact cards should bind them to the already-reviewed timing convention rather than leave the actor/initiative-transition behavior implicit.

The existing combat rule already establishes that initiative-created durations retain their original **virtual regular marker** even if initiative order changes or the creature leaves/re-enters initiative. A self/source buff uses future **source-start** markers; an outside-initiative round duration uses an absolute `application + 6 seconds` deadline. 

I recommend a shared card convention:

> **One source round:** if cast in initiative, expires at the caster's first future regular-start marker after application. That virtual marker persists through initiative changes. If cast outside initiative, expires 6 seconds after application; entering initiative does not replace that absolute deadline.

> **One minute:** if cast in initiative, expires at the caster's tenth future regular-start marker after application. The original virtual source-start phase persists through initiative changes. If cast outside initiative, expires 60 seconds after application; entering initiative preserves that absolute deadline.

An in-progress caster turn's already-passed start never counts.

Apply that wording to:

| Card | Exact temporal classification |
|---|---|
| **Sense Magic** | One source round |
| **Nullify Element** | One source round |
| **Aura Sight** | One source round |
| **Fortify Object** | One source round or consumption |
| **Warding Gesture** | Up to one minute, concentration, or consumption |
| **Harmonic Protection** | Up to one minute or consumption |
| **Repel Vermin** | One minute |
| **Warding Mark** | Up to one minute or concentration ending |

Barrier Flicker, Repelling Pulse, Detect Corruption and Purify Drop are instantaneous/trigger-only and need no clock change.

### Replacement identity

For every “one pending effect across all casters” card, add one shared sentence:

> A replacement is a new application with its own endpoint. An expiration or consumption event belonging to an older application cannot remove the current replacement.

That applies to Warding Gesture, Nullify Element, Fortify Object and Harmonic Protection.

For **Warding Gesture**, replacement also ends the old Warding Gesture effect and therefore releases that old casting's concentration dependency. The new casting owns only its own concentration dependency. This closes the stale-expiration issue explicitly rather than depending on implementation behavior. The candidate already has the correct all-caster single-entitlement concept. :chatgpt-content-reference{index="2"}

## 2. Fortify Object: approve the dual native-track design, but tighten the integrity branch

The candidate is correct not to equate “2 structural HP” with “2 integrity stages.” The staged Gameplay evidence defines Integrity as only 0–3, with stages Sound/Worn/Damaged/Broken; it provides no equivalence between a stage and an HP amount. :chatgpt-content-reference{index="3"}

I approve **choosing one actual native damage track when cast**. That is the cleanest playable interpretation of “temporarily strengthen a small object against damage.”

Replace the effect with:

> **Effect:** When you cast this spell, choose one damage track the target actually possesses: **structural HP** or **Integrity**. The first later damage event that would cause a positive loss on the chosen track is modified after the object's ordinary defenses:
>
> - **Structural HP:** reduce that event's structural-HP damage by 2, minimum 0.
> - **Integrity:** reduce the number of Integrity stages that event would cause the object to lose by 1, minimum 0.
>
> The ward is then consumed. It never modifies both tracks from one casting.

This matters if some native event would cause more than one Integrity stage. For example, a native two-stage loss becomes a one-stage loss; a native one-stage loss becomes zero. The spell does not “heal one stage” afterward.

Also add:

> If the target possesses neither actual structural HP nor a defined Integrity track, it is not a legal target. If it possesses both, choose one when cast.

Everything else on the submitted card is good: no repair, no max-HP increase, no routine wear prevention, no queueing of several wards, and a zero-damage event before this ward does not consume it. :chatgpt-content-reference{index="4"}

This is a **NEW PROVISIONAL one-stage ward rule**, not promotion of the Gameplay Loop's whole equipment/durability system.

## 3. Warding Mark: make “current source-authorized record” explicit

The candidate's binary-information ceiling is correct. It may glow; observers can reason from what they see. The spell itself does not somehow suppress ordinary deduction. :chatgpt-content-reference{index="5"}

I would tighten its descriptor/matching language:

> Choose one named species/template genuinely known to the caster **and represented by a current source-authorized creature record**, or one exact canonical creature type/tag defined by current operational source data. Matching checks a creature's **current canonical mechanical record**, not its apparent shape, disguise, name, reputation, ancestry guessed from appearance, or Director-only identity.

Then explicitly settle transformation and illusion:

> An illusion, disguise or other appearance-only change does not alter the creature's matching descriptors. A transformation does not create a new species/type/tag unless that exact transformation source explicitly says it changes that record. The current Druid and bounded spell-form profiles therefore do not manufacture new creature types merely from their profile names. If a future exact source genuinely changes a canonical type/tag, Warding Mark uses that current changed record while it lasts.

That follows the already-reviewed one-body transformation principle: spell forms preserve creature identity/type unless an exact source states otherwise.

The binary result remains:

> The mark reports only whether at least one matching creature is currently in the trigger region. Ordinary observers may draw whatever mundane conclusions that visible fact reasonably supports.

No new omniscience is created.

## 4. Two wording corrections: Repelling Pulse and Repel Vermin

### Repelling Pulse

Your correction is right. My previous phrase “externally supported” was too broad.

An object resting normally on a floor, table, shelf or similar support is still potentially movable. **Support is not the same thing as being secured.**

The submitted limitation should be approved:

> Worn, held, attached, restrained, locked or secured objects are ineligible. Ordinary ground, table or shelf support alone does not make an otherwise movable object ineligible.

If the push carries it beyond its support, ordinary Falling begins. The spell itself adds no collision/fall damage. :chatgpt-content-reference{index="6"}

No repair needed there.

### Repel Vermin

The intended rule is correct, but change this phrase:

> “statted encounter combatants”

to:

> **“creatures currently participating in an encounter as combatants”**

A harmless rat does not become immune to Repel Vermin merely because somebody prepared statistics for rats.

I would use:

> Summons, transformed creatures, trained companions, controlled or magical creatures, internal parasites, and creatures currently participating in an encounter as combatants are ineligible. Merely possessing a stat block or recorded statistics does not make an otherwise ordinary nuisance animal a combatant.

If an ordinary rat later genuinely joins combat as a combatant during the duration, it ceases being governed by this nuisance-behavior cantrip while participating as such.

The rest of the card is sound: it creates avoidance behavior, not Charmed/Frightened, compulsory Dash, attack immunity, parasite removal or summon control. :chatgpt-content-reference{index="7"}

## Remaining six clarification questions

**Aura Sight:** approved exactly in principle. Existing visual perception can come from ordinary sight or an independently functioning sight mode capable of visually perceiving that target. Hearing, tremorsense-like location knowledge, or knowledge that “something invisible is there” does not become vision merely because Aura Sight is active. Aura Sight supplies the aura overlay, not invisibility penetration. :chatgpt-content-reference{index="8"}

**Purify Drop:** approve the exact **0.05 mL maximum**. It is intentionally a reproducible provisional table limit rather than approximate prose. A drop must already be physically separated from the larger liquid. :chatgpt-content-reference{index="9"}

**Harmonic Protection:** approve the all-caster single entitlement. It is consumed by the next save even if another stronger flat bonus wins arbitration and Harmonic contributes no numeric +1. Apply the replacement-application timing fix above. :chatgpt-content-reference{index="10"}

**Nullify Element:** approve one active Nullify Element per target across all casters. A new one replaces the old selected cantrip type and endpoint rather than accumulating five cantrip resistances. Apply the source-start timing/replacement-ID clarification. :chatgpt-content-reference{index="11"}

**Sense Magic / Detect Corruption:** both information ceilings are sound. Sense Magic remains a yes/no active-magic presence check, while Detect Corruption tests only an explicit current Corruption state/tag/record and does not infer it from theme, faction, poison, appearance or alignment. :chatgpt-content-reference{index="12"} :chatgpt-content-reference{index="13"}

**Barrier Flicker:** approve the submitted conflict ruling. “Momentary +2 AC against one projectile attack” is incompatible with the Core's simultaneous one-minute concentration and offensive Spell Attack metadata. The candidate correctly keeps Reaction/30 ft/V/S and resolves the effect as a before-roll, one-projectile defensive Reaction with no concentration or spell attack, while preserving the rejected metadata in provenance. :chatgpt-content-reference{index="14"}

## Exact review disposition

So I would **not approve the current byte-for-byte candidate for promotion yet**, but the repairs are narrow and no source redesign is necessary.

Required changes before promotion are:

1. apply the existing source-start/virtual-marker/outside-absolute timing language to the eight duration-bearing cards;
2. add application-qualified replacement expiry semantics;
3. finalize Fortify Object's Integrity branch as **one fewer native stages lost**, not a numerical-HP conversion;
4. tighten Warding Mark's current canonical descriptor/transformation language;
5. replace Repel Vermin's “statted encounter combatants” wording with actual combat participation.

Everything else in the twelve cards is **approved at the source/manuscript level**.

Status remains:

> **12-card Abjuration batch — REVIEWED WITH NARROW REPAIRS; not yet promoted. Playable spell count remains 83.**

Once those exact manuscript edits are supplied, I would review that artifact for final batch promotion separately. Full runtime execution, remaining spell catalogs, Time Loop and whole-game/GitHub closure remain open.

