# Frozen source excerpts for LAX findings

Internal reviewer evidence, not a player distribution. Excerpts retain the submitted text; they are not replacement rules.

## DescentReviewChanges/ReviewBible/docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md, submitted lines 169–171

169: ## Class features and Paladin oaths
170: 
171: Use the full [class library](CLASS_PLAYTEST_INDEX.md) and [Paladin paths](PALADIN_OATHS_AND_OATHBREAKERS.md) for acquisition and actual cards. The language data gives an explicit interface for every selected card while retaining each card's status. These language completions never grant the card itself.

## DescentReviewChanges/ReviewBible/docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md, submitted lines 191–193

191: ## Scribing, runes and devices
192: 
193: The reviewed [advanced operating guide](ADVANCED_CRAFT_CANDIDATE_GUIDE.md), [Scribing cards](SCRIBING_CANDIDATE_RECIPE_CARDS.md) and [Tinkering cards](TINKERING_CANDIDATE_RECIPE_CARDS.md) retain their authority. Reading words does not establish a functional magical payload, caster eligibility or device control.

## DescentReviewChanges/ReviewBible/docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md, submitted lines 203–205

203: Runic knowledge does not confer Runecarver's-tools proficiency, glyph-function knowledge or arm/disarm permission. Use actual tools, hands, inspection/disarm procedures, DCs and triggers. A failed translation does not automatically activate a rune; reading does not recharge it. Ward attunement and charge/Reaction timing remain separate.
204: 
205: A crafted device requires an actual authorized capable controller with INT 6+, consent and ten active minutes using actual Tinker's tools and its legitimate accessible interface. No tool proficiency is granted or required merely to use a known functioning interface. An already bound machine requires actual release by its controller or a separately completed lawful control procedure; ownership does not hack unknown, locked or hostile equipment. Commands require the configured visible/audible channel within 60 ft, a Bonus Action on the controller's regular turn, and the shared one-command/one-offensive-output allowance per owner per numbered round across class and crafted systems. Execution follows the controller's whole turn in its attached phase. Failed execution still spends committed allowances; rebinding does not refund them. Fluency, overhearing, an interpreter or a telepathic ally does not supply control authority or undocumented hardware/protocol. Service, repair and controller transfer keep their real histories and costs. A language lesson does not reset them. Class device membership remains separate; TD-08 retains at most two CURRENT Dissonance into ONE own active qualifying device within 30 ft under its actual timing/frequency.

## Both candidate JSON envelopes: /recordSchema/definitions/provenance
```json
{
  "required": [
    "sourcePath",
    "sourceSha256",
    "recordId",
    "fieldPresence",
    "sourceSpelling",
    "authority"
  ],
  "fields": {
    "sourcePath": "string; original path",
    "sourceSha256": "64 lowercase hex characters",
    "recordId": "string; exact original ID",
    "fieldPresence": "absent|null|value; preserve distinction",
    "sourceSpelling": "original value only when present; no normalized replacement",
    "authority": "exact grant/decision that permits the derived effect"
  }
}
```

## Native completed advanced /procedureSections/TI-04
Source: `DescentReviewChanges/ReviewBible/data/director/advanced_craft_recipe_candidate_internal.json`
**NEW crafted control protocol:** a capable consenting user with INT6+ and actual access to the nonhostile unbound chassis may spend ten active minutes with Tinker's tools to register one controller and one simple task; no proficiency is granted or required merely to use a known functioning control interface. An already bound item requires its existing controller's actual release or a separately completed lawful control procedure. Ownership alone does not hack hostile/unknown/locked machinery. Transfer preserves service/HP/use histories and consumes the same ten minutes; no combat rebind for another action.

A controller may have **three active crafted automata** among the18 ordinary profiles, plus at most **one active686 coordinator** under its own exception. Additional owned machines must be deactivated, carried/stored with their real mass, or actually transferred to a capable different controller. They do not consume class Anacite/deployable slots and cannot become extra class-slot capacity. Class limits remain separately applicable, and **one shared command and one offensive companion/device allowance per owner per numbered round** applies across both systems. Deactivation/rebinding does not refund a round's spent allowance.

Command: Bonus Action on the controller's regular turn, target within60ft with actual visible/audible control communication and lawful access. Choose that machine's one eligible move plus one basic attack or one programmed task action. It executes after the controller's whole turn in the existing attached phase; no independent initiative turn, Reaction or recharge. Uncommanded active machines may move defensively and Dodge only; they do not obey a standing kill/harvest/attack order. Failed execution consumes the committed command/offense allowance; later controller incapacity alone does not cancel it, but source ending, suppression, exhausted power or an illegal target can prevent execution.

Outside initiative a programmed task must be a deterministic physically possible sequence using its actual appendages: carry one identified supported item along an already traversable specified route, operate one known ordinary lever, or sort a finite identified set by a visible physical property. No unseen search/identification, discretionary hostile targeting, professional task or indefinite resource production. Reprogramming takes ten real active minutes and does not refresh its service block. An hour of work pays TI-05's six blocks, not six free encounters. Loss of communication permits only its already legal finite noncombat sequence; no new target choice or attack. A controller may give one wholly noncombat task start with an Action; the same capacities and actual power limits apply.

## Native completed advanced /procedureSections/TI-05
Source: `DescentReviewChanges/ReviewBible/data/director/advanced_craft_recipe_candidate_internal.json`
For each18 ordinary automaton, `serviceRemaining` starts at its printed N. First actual operation in a genuine encounter spends one unit, covering only that encounter and at most **ten elapsed minutes**. If the encounter genuinely exceeds ten minutes, another unit funds the next block without declaring a new encounter or refreshing class uses. Leaving/reentering that same encounter inside its paid block does not spend or grant another unit; starting a distinct genuine encounter does spend another. No benefit from attacking allies, helpless captives or harmless animals to manufacture encounter boundaries.

Outside encounters, first operation opens one **ten-elapsed-minute** block and spends one unit. A pause/shutdown/suppression does not refund or extend that block. Entering a genuine encounter closes an earlier noncombat block and spends a new encounter unit. Ordinary idleness before a block starts spends nothing and grants no active behavior. At zero with no remaining paid block, the creature is inert and grants no movement/Dodge/task/attack until real service; a balance of zero during a paid block does not shorten that legitimately paid block. Blocks remain tied to physical identity across transfer, rest, damage, repair and initiative changes.

These are NEW finite accounting completions of the printed encounter service life, not independent charge attacks within the paid encounter. An attack still requires its own normal command/offense allowance every round. Short/long rest, dawn, Field Repair, Snap Rebuild and returning from meld restore no service unit.686 has its distinct winding profile; it does not inherit N from a similarly named automaton.

## Native completed advanced /procedureSections/TD-01
Source: `DescentReviewChanges/ReviewBible/data/director/advanced_craft_recipe_candidate_internal.json`
KEEP automatic Anacite ownership, its actual AC/HP/flight/bolt/Shock profile and its specific reconstruction/module routes. The 18 TI automata and686 are separate purchased/crafted Constructs; the other24 TI outputs are mechanical objects. None is an Anacite, class bomb, class turret, class Net Trap or class temporary deployable solely by a shared word. The complete 48-card eligibility register below identifies every card's reach. General device effects are expressly admitted only through the gates below; no Tinker level or selected card is awarded by ownership.

For general class-device effects, **NEW target binding** is a complete actual TI mechanical body or surviving recoverable original TI wreck, with the required current state. It does not automatically include EN weapons, Rune tablets, Scribing books, gathering implements or every magical item. Jury-rig's separate printed weapon target may admit an actual EN weapon on its own terms; that does not make it a Tinker device. Consumed process lenses, power cells and input Control mechanisms are not additional finished target devices.

## Native completed advanced /procedureSections/TD-08
Source: `DescentReviewChanges/ReviewBible/data/director/advanced_craft_recipe_candidate_internal.json`
KEEP once per short rest, Bonus Action, up to two **current** Dissonance, one of that Tinker's actual active devices within30ft. Explicitly admit TI devices only when currently genuinely active: an armed charged trap; a powered automaton/686 in its paid/wound operating interval; a utility actually participating in a live eligible task; or an aligned ram in its live legal cycle. Merely carrying a cheap unused tool is not an active device. This is an eligibility definition, not a new Dissonance/RP conversion rate.

Routing disables movement, attack, aura, trigger and other active use while its duration/service clock continues. No RP appears and Refrain does not reset. Clear that specific disable through actual Field Repair where qualified, or the engine's ten active minutes/1RP/Tinker's tools route, or **the routing Tinker's next completed genuine short rest**. A buyer's unrelated rest does not clear another user's routed state. Normal HP restoration may clear it only after that actual repair completes; paying a quote or renaming a device does not. None refills uses. Transfer retains disable origin, expiry, resource record and current body. One short-rest allowance remains one regardless of the number or price of owned machines.
